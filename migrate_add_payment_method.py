"""
Script de migración para agregar la columna payment_method a la tabla orders.
Este script usa la API REST de Supabase para modificar la estructura de la tabla.
"""
import requests
import os
from app.config import settings

def add_payment_method_column():
    """
    Agrega la columna payment_method a la tabla orders usando SQL directo.
    """
    # URL del proyecto de Supabase
    project_url = settings.SUPABASE_URL
    api_key = settings.SUPABASE_KEY

    # Extraer el project_ref de la URL
    project_ref = project_url.split('//')[1].split('.')[0]

    print(f"🔄 Intentando agregar columna payment_method a la tabla orders...")
    print(f"📍 Project: {project_ref}")

    # SQL para agregar la columna
    sql = """
    DO $$
    BEGIN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name = 'orders' AND column_name = 'payment_method'
        ) THEN
            ALTER TABLE orders
            ADD COLUMN payment_method TEXT DEFAULT 'efectivo';

            ALTER TABLE orders
            ADD CONSTRAINT orders_payment_method_check
            CHECK (payment_method IN ('efectivo', 'transferencia'));

            RAISE NOTICE 'Columna payment_method agregada exitosamente';
        ELSE
            RAISE NOTICE 'La columna payment_method ya existe';
        END IF;
    END $$;
    """

    print(f"\n📝 SQL a ejecutar:")
    print(sql)

    print(f"\n⚠️  NOTA: Este script requiere permisos administrativos en Supabase.")
    print(f"Si falla, por favor ejecuta el siguiente SQL manualmente en:")
    print(f"https://supabase.com/dashboard/project/{project_ref}/sql")
    print(f"\n{sql}\n")

    # Intentar crear una orden de prueba con payment_method para verificar si ya existe
    try:
        from app.database import get_supabase_client
        supabase = get_supabase_client()

        # Intentar leer una orden existente para verificar las columnas
        result = supabase.table("orders").select("*").limit(1).execute()

        if result.data and 'payment_method' in result.data[0]:
            print("✅ La columna payment_method YA EXISTE en la tabla orders!")
            return True
        else:
            print("❌ La columna payment_method NO existe aún.")
            print("\n📋 Por favor, ejecuta este SQL en el editor SQL de Supabase:")
            print("=" * 80)
            print("""
ALTER TABLE orders
ADD COLUMN payment_method TEXT DEFAULT 'efectivo';

ALTER TABLE orders
ADD CONSTRAINT orders_payment_method_check
CHECK (payment_method IN ('efectivo', 'transferencia'));
            """)
            print("=" * 80)
            return False

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    add_payment_method_column()
