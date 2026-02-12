from datetime import datetime
import random
import string


def format_menu_for_ai(menu_items: list) -> str:
    """
    Formatea el menú como JSON estructurado para la IA.
    El JSON es más fácil de parsear para el modelo.
    """
    import json

    if not menu_items:
        return "[]"

    # Agrupar por producto
    products = {}
    for item in menu_items:
        product_name = item.get("producto", "Sin nombre")

        if product_name not in products:
            products[product_name] = {
                "name": product_name,
                "ingredients": item.get("description", ""),
                "category": item.get("food_type", "Otros"),
                "sizes": []
            }

        products[product_name]["sizes"].append({
            "size": item.get("size", "Única"),
            "price": item.get("price", 0),
            "id": item.get("id", "")
        })

    # Ordenar tamaños por precio
    for product in products.values():
        product["sizes"].sort(key=lambda x: x["price"])

    # Convertir a lista
    menu_list = list(products.values())

    return json.dumps(menu_list, ensure_ascii=False, indent=2)



def format_barrios_for_ai(barrios: list) -> str:
    """Formatea la lista de barrios como JSON para la IA."""
    import json
    if not barrios:
        return "[]"
    return json.dumps(barrios, ensure_ascii=False, indent=2)


def generate_ticket_id() -> str:
    """
    Genera ID único tipo "TDP-20250119-001"
    """
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = "".join(random.choices(string.digits, k=3))
    return f"TDP-{date_part}-{random_part}"
