from supabase import create_client, Client
from app.config import settings


def get_supabase_client() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_or_create_client(telefono: str, nombre: str) -> dict:
    """
    Busca un cliente por teléfono o lo crea si no existe.
    Valida que los datos no estén vacíos antes de crear.
    """
    # Validar datos de entrada
    if not telefono or not telefono.strip():
        raise ValueError("El teléfono no puede estar vacío")
    if not nombre or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío")

    telefono = telefono.strip()
    nombre = nombre.strip()

    supabase = get_supabase_client()

    # Buscar cliente existente
    result = supabase.table("clients").select("*").eq("cel", telefono).execute()

    if result.data:
        return result.data[0]

    # Crear nuevo cliente (solo si no existe)
    new_client = {"cel": telefono, "name": nombre}
    result = supabase.table("clients").insert(new_client).execute()

    if not result.data:
        raise Exception("Error al crear cliente en la base de datos")

    return result.data[0]


def update_client_address(telefono: str, nueva_direccion: str) -> None:
    """Actualiza la dirección guardada del cliente cuando entrega una nueva."""
    supabase = get_supabase_client()
    supabase.table("clients") \
        .update({"address": nueva_direccion}) \
        .eq("cel", telefono) \
        .execute()


def update_client_barrio(telefono: str, barrio: str) -> None:
    """Guarda el barrio confirmado del cliente para no volver a preguntarlo."""
    supabase = get_supabase_client()
    supabase.table("clients") \
        .update({"barrio": barrio}) \
        .eq("cel", telefono) \
        .execute()


def get_barrios() -> list:
    """Obtiene los barrios activos con cobertura de delivery."""
    supabase = get_supabase_client()
    result = supabase.table("barrios") \
        .select("id, nombre, precio_domicilio") \
        .eq("activo", True) \
        .order("nombre") \
        .execute()
    return result.data


def get_menu() -> list:
    supabase = get_supabase_client()
    # JOIN entre products y product_variants usando la sintaxis correcta de Supabase
    result = supabase.table("product_variants").select(
        "id, nombre_variante, price, product_id, products!inner(name, description, food_type)"
    ).eq("activo", True).execute()
    
    # Formatear los datos para que coincidan con el formato esperado
    formatted_menu = []
    for item in result.data:
        product_info = item.get("products", {})
        formatted_item = {
            "id": item["id"],  # ID de la variante
            "product_id": item["product_id"],
            "producto": product_info.get("name", ""),
            "description": product_info.get("description", ""),
            "size": item["nombre_variante"],  # La variante es el tamaño
            "price": item["price"],
            "food_type": product_info.get("food_type", "")
        }
        formatted_menu.append(formatted_item)
    
    return formatted_menu
