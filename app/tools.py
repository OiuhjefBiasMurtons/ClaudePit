from app.database import get_supabase_client
from app.utils import generate_ticket_id
import logging

logger = logging.getLogger(__name__)


def validate_variant_ids(supabase, items: list) -> tuple[list, list]:
    """
    Valida que los variant_ids existan en la base de datos.
    Retorna (items_validos, items_invalidos).
    """
    if not items:
        return [], []

    variant_ids = [item["variant_id"] for item in items]
    result = supabase.table("product_variants").select("id").in_("id", variant_ids).execute()
    valid_ids = {row["id"] for row in result.data}

    valid_items = []
    invalid_items = []

    for item in items:
        if item["variant_id"] in valid_ids:
            valid_items.append(item)
        else:
            invalid_items.append(item)

    return valid_items, invalid_items


def calculate_order_preview(items: list) -> dict:
    """
    Calcula el total del pedido en el backend.
    Lanza ValueError si hay IDs inválidos o cantidades incorrectas.
    """
    if not items:
        raise ValueError("No hay items para calcular")

    supabase = get_supabase_client()
    variant_ids = [item["variant_id"] for item in items]
    
    result = supabase.table("product_variants").select(
        "id, nombre_variante, price, products(name)"
    ).in_("id", variant_ids).execute()

    variants_map = {v["id"]: v for v in result.data}
    
    # Validar que TODOS los IDs existan
    invalid_ids = [vid for vid in variant_ids if vid not in variants_map]
    if invalid_ids:
        raise ValueError(f"Variant IDs no encontrados: {invalid_ids}")

    items_con_precio = []
    total = 0

    for item in items:
        variant_id = item["variant_id"]
        quantity = max(1, int(item.get("quantity", 1)))  # Mínimo 1

        variant = variants_map[variant_id]
        price = variant["price"]
        subtotal = price * quantity
        total += subtotal

        items_con_precio.append({
            "variant_id": variant_id,
            "product_name": variant.get("products", {}).get("name", "Producto"),
            "variant_name": variant["nombre_variante"],
            "quantity": quantity,
            "unit_price": price,
            "subtotal": subtotal
        })

    return {
        "items": items_con_precio,
        "total": total
    }


def create_new_order(client_id: str, items: list, delivery_address: str, payment_method: str = "efectivo") -> dict:
    """
    Crea un nuevo pedido.

    items: lista de dicts con {variant_id, quantity, note}
    payment_method: método de pago ("efectivo" o "transferencia")
    """
    logger.info(f"create_new_order llamado con {len(items)} items: {items}, payment_method: {payment_method}")
    supabase = get_supabase_client()

    # Validar que los variant_ids existan
    valid_items, invalid_items = validate_variant_ids(supabase, items)

    if invalid_items:
        logger.warning(f"Items inválidos detectados: {invalid_items}")
    logger.info(f"Items válidos: {len(valid_items)}, Items inválidos: {len(invalid_items)}")

    if invalid_items:
        invalid_ids = [item["variant_id"] for item in invalid_items]
        return {
            "error": f"Los siguientes IDs de variante no existen: {invalid_ids}. Verifica el menú y usa solo IDs válidos.",
            "invalid_ids": invalid_ids
        }

    if not valid_items:
        return {"error": "No hay items válidos para crear el pedido."}

    # Crear orden (sin ticket_id ni total_order, la BD los genera automáticamente)
    order_data = {
        "client_id": client_id,
        "address_delivery": delivery_address,
        "payment_method": payment_method.lower(),
        "state": "PREPARANDO"
    }
    order_result = supabase.table("orders").insert(order_data).execute()
    order = order_result.data[0]
    order_id = order["id"]

    # Insertar items validados
    for item in valid_items:
        detail_data = {
            "order_id": order_id,
            "variant_id": item["variant_id"],
            "quantity": item.get("quantity", 1),
            "note": item.get("note", "")
        }
        supabase.table("order_details").insert(detail_data).execute()

    # Actualizar dirección del cliente para futuros pedidos
    supabase.table("clients").update({"address": delivery_address}).eq("id", client_id).execute()

    # Leer order actualizado para obtener total calculado por trigger
    updated_order = supabase.table("orders").select("*").eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "ticket_id": updated_order.data[0].get("ticket_id"),
        "total": updated_order.data[0].get("total_order", 0),
        "address": delivery_address,
        "payment_method": payment_method
    }


def get_active_order(client_id: str) -> dict | None:
    """
    Busca pedido activo del cliente.
    Un pedido está activo si NO está ENTREGADO ni CANCELADO.
    Estados activos: PREPARANDO, EN_CAMINO
    Retorna order con sus order_details incluyendo nombres de productos.
    """
    supabase = get_supabase_client()

    # Buscar orden activa (no entregada ni cancelada)
    result = supabase.table("orders").select("*").eq("client_id", client_id).not_.in_("state", ["ENTREGADO", "CANCELADO"]).order("created_at", desc=True).limit(1).execute()

    if not result.data:
        return None

    order = result.data[0]

    # Obtener detalles del pedido con nombres de productos
    details_result = supabase.table("order_details") \
        .select("*, product_variants(*, products(*))") \
        .eq("order_id", order["id"]) \
        .execute()

    # Formatear items con información completa (filtrar quantity <= 0)
    items_list = []
    for detail in details_result.data:
        quantity = detail.get("quantity", 1)

        # Ignorar items con cantidad <= 0 (borrados o cantidades negativas erróneas)
        if quantity <= 0:
            continue

        variant = detail.get("product_variants", {})
        product = variant.get("products", {})
        items_list.append({
            "quantity": quantity,
            "product_name": product.get("name", "producto"),
            "variant_name": variant.get("nombre_variante", ""),
            "price": variant.get("price", 0),
            "note": detail.get("note", ""),
            "variant_id": detail.get("variant_id", "")
        })

    order["items"] = items_list

    return order


def _validate_order_belongs_to_client(supabase, order_id: str, client_id: str) -> dict | None:
    """
    Valida que el pedido pertenece al cliente.
    Retorna None si pertenece, o un dict con error si no.
    """
    order_result = supabase.table("orders").select("client_id").eq("id", order_id).execute()

    if not order_result.data:
        return {"error": f"No se encontró el pedido {order_id}"}

    order_client_id = order_result.data[0].get("client_id")

    if order_client_id != client_id:
        return {"error": "No tienes permiso para modificar este pedido."}

    return None


def _validate_order_is_editable(supabase, order_id: str) -> dict | None:
    """
    Valida que el pedido esté en estado PREPARANDO (editable).
    Retorna None si es editable, o un dict con error si no lo es.
    """
    order_result = supabase.table("orders").select("state").eq("id", order_id).execute()

    if not order_result.data:
        return {"error": f"No se encontró el pedido {order_id}"}

    state = order_result.data[0].get("state")

    if state != "PREPARANDO":
        if state == "EN_CAMINO":
            return {"error": "Tu pedido ya va en camino con el repartidor 🛵. No se pueden hacer cambios."}
        elif state == "ENTREGADO":
            return {"error": "Ese pedido ya fue entregado. No se pueden hacer cambios."}
        elif state == "CANCELADO":
            return {"error": "Ese pedido fue cancelado. No se pueden hacer cambios."}
        else:
            return {"error": f"No se puede modificar el pedido en estado {state}."}

    return None


def add_items_to_order(order_id: str, items: list, client_id: str) -> dict:
    """
    Agrega items a un pedido existente.
    Solo permite modificar pedidos en estado PREPARANDO y que pertenezcan al cliente.

    items: lista de dicts con {variant_id, quantity, note}
    client_id: ID del cliente (para validación de seguridad)
    """
    supabase = get_supabase_client()

    # Validar que el pedido pertenece al cliente
    ownership_error = _validate_order_belongs_to_client(supabase, order_id, client_id)
    if ownership_error:
        return ownership_error

    # Validar que el pedido sea editable
    validation_error = _validate_order_is_editable(supabase, order_id)
    if validation_error:
        return validation_error

    # Validar que los variant_ids existan
    valid_items, invalid_items = validate_variant_ids(supabase, items)

    if invalid_items:
        invalid_ids = [item["variant_id"] for item in invalid_items]
        return {
            "error": f"Los siguientes IDs de variante no existen: {invalid_ids}. Verifica el menú y usa solo IDs válidos.",
            "invalid_ids": invalid_ids
        }

    if not valid_items:
        return {"error": "No hay items válidos para agregar."}

    # Validar que todas las cantidades sean positivas
    for item in valid_items:
        quantity = item.get("quantity", 1)
        if quantity <= 0:
            return {"error": f"La cantidad debe ser positiva (mayor a 0), recibido: {quantity}"}

    for item in valid_items:
        detail_data = {
            "order_id": order_id,
            "variant_id": item["variant_id"],
            "quantity": item.get("quantity", 1),
            "note": item.get("note", "")
        }
        supabase.table("order_details").insert(detail_data).execute()

    # Leer order actualizado para obtener total calculado por trigger
    updated_order = supabase.table("orders").select("*").eq("id", order_id).execute()

    # Obtener todos los items del pedido actualizado con detalles de producto
    details_result = supabase.table("order_details") \
        .select("*, product_variants(*, products(*))") \
        .eq("order_id", order_id) \
        .execute()

    # Formatear items para el bot (filtrar quantity <= 0)
    items_list = []
    for detail in details_result.data:
        quantity = detail.get("quantity", 1)

        # Ignorar items con cantidad <= 0
        if quantity <= 0:
            continue

        variant = detail.get("product_variants", {})
        product = variant.get("products", {})
        items_list.append({
            "quantity": quantity,
            "product_name": product.get("name", "producto"),
            "variant_name": variant.get("nombre_variante", ""),
            "price": variant.get("price", 0),
            "note": detail.get("note", "")
        })

    return {
        "order_id": order_id,
        "total": updated_order.data[0].get("total_order", 0),
        "items": items_list,
        "address": updated_order.data[0].get("address_delivery", ""),
        "message": "Items agregados correctamente"
    }


def replace_item_in_order(order_id: str, old_variant_id: str, new_variant_id: str, client_id: str, quantity: int = 1) -> dict:
    """
    Reemplaza un item por otro en un pedido existente.
    Solo permite modificar pedidos en estado PREPARANDO y que pertenezcan al cliente.

    Args:
        order_id: ID del pedido
        old_variant_id: ID de la variante a reemplazar
        new_variant_id: ID de la nueva variante
        client_id: ID del cliente (para validación de seguridad)
        quantity: Cantidad a reemplazar (default 1)

    Ejemplo: Cambiar 1 Pizza Hawaiana Familiar por 1 Pizza De la Casa Familiar
    """
    supabase = get_supabase_client()

    # Validar que el pedido pertenece al cliente
    ownership_error = _validate_order_belongs_to_client(supabase, order_id, client_id)
    if ownership_error:
        return ownership_error

    # Validar que el pedido sea editable
    validation_error = _validate_order_is_editable(supabase, order_id)
    if validation_error:
        return validation_error

    # Validar que el new_variant_id existe
    valid_items, invalid_items = validate_variant_ids(supabase, [{"variant_id": new_variant_id}])
    if invalid_items:
        return {"error": f"El variant_id '{new_variant_id}' no existe en el menú."}

    # Buscar el item actual en order_details
    current_items = supabase.table("order_details") \
        .select("*") \
        .eq("order_id", order_id) \
        .eq("variant_id", old_variant_id) \
        .execute()

    if not current_items.data:
        return {"error": f"No se encontró el item con variant_id '{old_variant_id}' en el pedido."}

    current_item = current_items.data[0]
    current_quantity = current_item["quantity"]

    if current_quantity < quantity:
        return {"error": f"Solo hay {current_quantity} unidades de este item, no se pueden reemplazar {quantity}."}

    # Reducir cantidad del item actual
    new_quantity = current_quantity - quantity

    if new_quantity <= 0:
        # Eliminar el registro
        supabase.table("order_details").delete().eq("id", current_item["id"]).execute()
    else:
        # Actualizar cantidad
        supabase.table("order_details").update({"quantity": new_quantity}).eq("id", current_item["id"]).execute()

    # Agregar el nuevo item
    new_detail = {
        "order_id": order_id,
        "variant_id": new_variant_id,
        "quantity": quantity,
        "note": current_item.get("note", "")
    }
    supabase.table("order_details").insert(new_detail).execute()

    # Obtener pedido actualizado para retornar
    updated_order = supabase.table("orders").select("*").eq("id", order_id).execute()

    # Obtener todos los items del pedido actualizado
    details_result = supabase.table("order_details") \
        .select("*, product_variants(*, products(*))") \
        .eq("order_id", order_id) \
        .execute()

    # Formatear items (filtrar quantity <= 0)
    items_list = []
    for detail in details_result.data:
        qty = detail.get("quantity", 1)
        if qty <= 0:
            continue

        variant = detail.get("product_variants", {})
        product = variant.get("products", {})
        items_list.append({
            "quantity": qty,
            "product_name": product.get("name", "producto"),
            "variant_name": variant.get("nombre_variante", ""),
            "price": variant.get("price", 0),
            "note": detail.get("note", "")
        })

    return {
        "order_id": order_id,
        "total": updated_order.data[0].get("total_order", 0),
        "items": items_list,
        "address": updated_order.data[0].get("address_delivery", ""),
        "message": f"Item reemplazado correctamente"
    }


def update_order_address(order_id: str, new_address: str, client_id: str) -> dict:
    """
    Actualiza la dirección de entrega de un pedido.
    Solo permite modificar pedidos en estado PREPARANDO y que pertenezcan al cliente.
    """
    supabase = get_supabase_client()

    # Validar que el pedido pertenece al cliente
    ownership_error = _validate_order_belongs_to_client(supabase, order_id, client_id)
    if ownership_error:
        return ownership_error

    # Validar que el pedido sea editable
    validation_error = _validate_order_is_editable(supabase, order_id)
    if validation_error:
        return validation_error

    supabase.table("orders").update({"address_delivery": new_address}).eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "new_address": new_address,
        "message": "Dirección actualizada correctamente"
    }


def confirm_order(order_id: str, client_id: str) -> dict:
    """
    Confirma un pedido cambiando su estado a 'EN_CAMINO'.
    Solo permite confirmar pedidos que pertenezcan al cliente.
    """
    supabase = get_supabase_client()

    # Validar que el pedido pertenece al cliente
    ownership_error = _validate_order_belongs_to_client(supabase, order_id, client_id)
    if ownership_error:
        return ownership_error

    supabase.table("orders").update({"state": "EN_CAMINO"}).eq("id", order_id).execute()

    # Obtener datos actualizados
    order = supabase.table("orders").select("*").eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "ticket_id": order.data[0].get("ticket_id"),
        "total": order.data[0].get("total_order", 0),
        "state": "EN_CAMINO",
        "message": "Pedido confirmado correctamente"
    }


def cancel_order(order_id: str, client_id: str) -> dict:
    """
    Cancela un pedido cambiando su estado a 'CANCELADO'.
    Solo permite cancelar pedidos que pertenezcan al cliente.
    """
    supabase = get_supabase_client()

    # Validar que el pedido pertenece al cliente
    ownership_error = _validate_order_belongs_to_client(supabase, order_id, client_id)
    if ownership_error:
        return ownership_error

    supabase.table("orders").update({"state": "CANCELADO"}).eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "state": "CANCELADO",
        "message": "Pedido cancelado correctamente"
    }


def get_client_orders(client_id: str, include_completed: bool = False, limit: int = 5) -> dict:
    """
    Obtiene los pedidos del cliente directamente desde la base de datos.

    Esta función es la FUENTE DE VERDAD para consultar pedidos.
    Evita que el bot invente información del historial de conversación.

    Args:
        client_id: ID del cliente
        include_completed: Si True, incluye pedidos ENTREGADOS y CANCELADOS.
                          Si False (default), solo muestra PREPARANDO y EN_CAMINO
        limit: Máximo número de pedidos a retornar (default: 5, más recientes primero)

    Returns:
        dict con:
        - orders: lista de pedidos con toda su información
        - count: número de pedidos encontrados

    Ejemplo de uso:
        Bot: Cuando el cliente pregunta "¿Qué pedidos tengo?", llama esta función.
    """
    supabase = get_supabase_client()

    try:
        # Query base
        query = supabase.table("orders").select("*").eq("client_id", client_id)

        # Filtrar por estado si no se incluyen completados
        if not include_completed:
            query = query.in_("state", ["PREPARANDO", "EN_CAMINO"])

        # Ordenar por más reciente y limitar
        result = query.order("created_at", desc=True).limit(limit).execute()

        if not result.data:
            return {
                "orders": [],
                "count": 0,
                "message": "No tienes pedidos activos en este momento."
            }

        # Formatear cada pedido con sus items
        orders_list = []
        for order in result.data:
            # Obtener items del pedido
            details_result = supabase.table("order_details") \
                .select("*, product_variants(*, products(*))") \
                .eq("order_id", order["id"]) \
                .execute()

            # Formatear items (filtrar quantity <= 0)
            items_list = []
            for detail in details_result.data:
                quantity = detail.get("quantity", 1)

                # Ignorar items corruptos
                if quantity <= 0:
                    continue

                variant = detail.get("product_variants", {})
                product = variant.get("products", {})
                items_list.append({
                    "quantity": quantity,
                    "product_name": product.get("name", "producto"),
                    "variant_name": variant.get("nombre_variante", ""),
                    "price": variant.get("price", 0)
                })

            # Agregar pedido formateado
            orders_list.append({
                "order_id": order["id"],
                "ticket_id": order.get("ticket_id", ""),
                "state": order.get("state", ""),
                "items": items_list,
                "total": order.get("total_order", 0),
                "address": order.get("address_delivery", ""),
                "payment_method": order.get("payment_method", ""),
                "created_at": order.get("created_at", "")
            })

        return {
            "orders": orders_list,
            "count": len(orders_list),
            "message": f"Se encontraron {len(orders_list)} pedido(s)."
        }

    except Exception as e:
        logger.error(f"Error en get_client_orders: {str(e)}")
        return {
            "error": "No pude consultar tus pedidos en este momento. Por favor intenta de nuevo.",
            "orders": [],
            "count": 0
        }
