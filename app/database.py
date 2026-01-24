from supabase import create_client, Client
from app.config import settings


def get_supabase_client() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def get_or_create_client(telefono: str, nombre: str) -> dict:
    supabase = get_supabase_client()

    # Buscar cliente existente
    result = supabase.table("clients").select("*").eq("cel", telefono).execute()

    if result.data:
        return result.data[0]

    # Crear nuevo cliente
    new_client = {"cel": telefono, "name": nombre}
    result = supabase.table("clients").insert(new_client).execute()
    return result.data[0]


def get_menu() -> list:
    supabase = get_supabase_client()
    # JOIN entre products y product_variants usando la sintaxis correcta de Supabase
    result = supabase.table("product_variants").select(
        "id, nombre_variante, price, product_id, products!inner(name, description, food_type)"
    ).execute()
    
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
