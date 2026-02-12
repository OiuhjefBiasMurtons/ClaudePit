#!/usr/bin/env python3
"""Script para diagnosticar el menú y el sistema prompt del bot"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

from app.database import get_menu, get_or_create_client, get_supabase_client
from app.utils import format_menu_for_ai
from app.tools import get_active_order
from app.ai_service import build_system_prompt


def main():
    print("\n" + "="*80)
    print("DIAGNÓSTICO DEL BOT - MENÚ Y PROMPT")
    print("="*80 + "\n")

    # 1. Verificar productos en la base de datos
    print("1. PRODUCTOS EN BASE DE DATOS:")
    print("-" * 80)
    try:
        supabase = get_supabase_client()

        # Contar productos por tipo
        products_result = supabase.table("products").select("id, name, food_type, activo").execute()
        products = products_result.data

        print(f"Total de productos: {len(products)}")

        by_type = {}
        for p in products:
            food_type = p.get("food_type", "SIN_TIPO")
            if food_type not in by_type:
                by_type[food_type] = []
            by_type[food_type].append(p)

        for food_type, items in sorted(by_type.items()):
            active_count = sum(1 for item in items if item.get("activo", False))
            print(f"  {food_type}: {len(items)} productos ({active_count} activos)")

        # Contar variantes
        variants_result = supabase.table("product_variants").select("id, activo").execute()
        variants = variants_result.data
        active_variants = sum(1 for v in variants if v.get("activo", False))
        print(f"\nTotal de variantes: {len(variants)} ({active_variants} activas)")

    except Exception as e:
        print(f"ERROR al consultar BD: {e}")

    # 2. Obtener menú formateado
    print("\n2. MENÚ FORMATEADO PARA IA:")
    print("-" * 80)
    try:
        menu_items = get_menu()
        print(f"Items obtenidos de get_menu(): {len(menu_items)}")

        if not menu_items:
            print("⚠️  WARNING: El menú está VACÍO. El bot no tiene productos para ofrecer.")
            print("   Esto explica por qué el bot inventa productos.")
        else:
            menu_formateado = format_menu_for_ai(menu_items)
            print(f"\nLongitud del menú formateado: {len(menu_formateado)} caracteres")
            print("\nPrimeros 500 caracteres del menú:")
            print(menu_formateado[:500])
            print("...\n")

            # Buscar bebidas en el menú
            if "BEBIDA" in menu_formateado:
                print("✓ El menú contiene BEBIDAS")
            else:
                print("✗ El menú NO contiene BEBIDAS (el bot las está inventando)")

    except Exception as e:
        print(f"ERROR al obtener menú: {e}")

    # 3. Ver ejemplo de system prompt
    print("\n3. SYSTEM PROMPT DE EJEMPLO:")
    print("-" * 80)
    try:
        # Crear cliente de prueba
        test_cliente = {
            "id": "test-id",
            "name": "Test User",
            "address": "Calle 123"
        }

        menu_items = get_menu()
        menu_formateado = format_menu_for_ai(menu_items)

        system_prompt = build_system_prompt(test_cliente, menu_formateado, None)

        print(f"Longitud del system prompt: {len(system_prompt)} caracteres\n")
        print("Primeros 1000 caracteres:")
        print(system_prompt[:1000])
        print("...")

    except Exception as e:
        print(f"ERROR al generar system prompt: {e}")

    print("\n" + "="*80)
    print("FIN DEL DIAGNÓSTICO")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
