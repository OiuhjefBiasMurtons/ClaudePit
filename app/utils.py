from datetime import datetime
import random
import string


def format_menu_for_ai(menu_items: list) -> str:
    """
    Agrupa productos por nombre y formatea para la IA.

    Input: lista de dicts de products_with_variants
    Output: string formateado
    """
    if not menu_items:
        return "No hay productos disponibles."

    # Agrupar por producto
    products = {}
    for item in menu_items:
        product_name = item.get("producto", "Sin nombre")
        if product_name not in products:
            products[product_name] = {
                "description": item.get("description", ""),
                "food_type": item.get("food_type", ""),
                "variants": []
            }
        products[product_name]["variants"].append({
            "size": item.get("size", ""),
            "price": item.get("price", 0),
            "variant_id": item.get("id", "")
        })

    # Formatear salida
    lines = []
    for product_name, data in products.items():
        lines.append(f"{product_name} ({data['food_type']})")
        if data["description"]:
            lines.append(f"  {data['description']}")
        for variant in data["variants"]:
            price = f"${variant['price']:,}" if variant['price'] else "N/A"
            lines.append(f"  • {variant['size']}: {price} [ID: {variant['variant_id']}]")
        lines.append("")  # Línea vacía entre productos

    return "\n".join(lines).strip()


def generate_ticket_id() -> str:
    """
    Genera ID único tipo "TDP-20250119-001"
    """
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = "".join(random.choices(string.digits, k=3))
    return f"TDP-{date_part}-{random_part}"
