from app.database import get_supabase_client
from app.utils import generate_ticket_id


def create_new_order(client_id: str, items: list, delivery_address: str) -> dict:
    """
    Crea un nuevo pedido.

    items: lista de dicts con {variant_id, quantity, note}
    """
    supabase = get_supabase_client()
    ticket_id = generate_ticket_id()

    # Crear orden (sin total_order, el trigger lo calcula)
    order_data = {
        "client_id": client_id,
        "ticket_id": ticket_id,
        "address_delivery": delivery_address,
        "state": "PREPARANDO"
    }
    order_result = supabase.table("orders").insert(order_data).execute()
    order = order_result.data[0]
    order_id = order["id"]

    # Insertar items (solo variant_id, quantity, note)
    for item in items:
        detail_data = {
            "order_id": order_id,
            "variant_id": item["variant_id"],
            "quantity": item.get("quantity", 1),
            "note": item.get("note", "")
        }
        supabase.table("order_details").insert(detail_data).execute()

    # Leer order actualizado para obtener total calculado por trigger
    updated_order = supabase.table("orders").select("*").eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "ticket_id": ticket_id,
        "total": updated_order.data[0].get("total_order", 0)
    }


def get_active_order(client_id: str) -> dict | None:
    """
    Busca pedido activo (state='PREPARANDO') del cliente.
    Retorna order con sus order_details o None.
    """
    supabase = get_supabase_client()

    # Buscar orden en preparación
    result = supabase.table("orders").select("*").eq("client_id", client_id).eq("state", "PREPARANDO").execute()

    if not result.data:
        return None

    order = result.data[0]

    # Obtener detalles del pedido
    details_result = supabase.table("order_details").select("*").eq("order_id", order["id"]).execute()
    order["items"] = details_result.data

    return order


def add_items_to_order(order_id: str, items: list) -> dict:
    """
    Agrega items a un pedido existente.

    items: lista de dicts con {variant_id, quantity, note}
    """
    supabase = get_supabase_client()

    for item in items:
        detail_data = {
            "order_id": order_id,
            "variant_id": item["variant_id"],
            "quantity": item.get("quantity", 1),
            "note": item.get("note", "")
        }
        supabase.table("order_details").insert(detail_data).execute()

    # Leer order actualizado para obtener total calculado por trigger
    updated_order = supabase.table("orders").select("*").eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "total": updated_order.data[0].get("total_order", 0),
        "message": "Items agregados correctamente"
    }


def update_order_address(order_id: str, new_address: str) -> dict:
    """
    Actualiza la dirección de entrega de un pedido.
    """
    supabase = get_supabase_client()

    supabase.table("orders").update({"address_delivery": new_address}).eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "new_address": new_address,
        "message": "Dirección actualizada correctamente"
    }


def confirm_order(order_id: str) -> dict:
    """
    Confirma un pedido cambiando su estado a 'EN_CAMINO'.
    """
    supabase = get_supabase_client()

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


def cancel_order(order_id: str) -> dict:
    """
    Cancela un pedido cambiando su estado a 'CANCELADO'.
    """
    supabase = get_supabase_client()

    supabase.table("orders").update({"state": "CANCELADO"}).eq("id", order_id).execute()

    return {
        "order_id": order_id,
        "state": "CANCELADO",
        "message": "Pedido cancelado correctamente"
    }
