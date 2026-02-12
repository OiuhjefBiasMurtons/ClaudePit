"""
Script para agregar la columna payment_method directamente a través de Supabase.
"""
import requests
from app.config import settings

def execute_sql_on_supabase(sql_query: str) -> dict:
    """
    Ejecuta una consulta SQL en Supabase usando la API REST.
    """
    # Extraer el project_ref de la URL
    project_ref = settings.SUPABASE_URL.split('//')[1].split('.')[0]

    # URL de la API REST de Supabase para ejecutar SQL
    # Intentamos usar diferentes endpoints que podrían funcionar

    print(f"🔄 Intentando agregar columna payment_method...")
    print(f"📍 Project: {project_ref}")
    print(f"🔗 URL: {settings.SUPABASE_URL}")

    # Método 1: Intentar usando postgrest directamente
    headers = {
        'apikey': settings.SUPABASE_KEY,
        'Authorization': f'Bearer {settings.SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

    # Primero, intentemos verificar si podemos acceder a la metadata
    try:
        # Verificar columnas actuales
        columns_url = f"{settings.SUPABASE_URL}/rest/v1/rpc/exec_sql"

        print("\n📋 Intentando ejecutar SQL directo...")

        # Preparar el SQL
        sql_commands = [
            "ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo';",
            "ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_payment_method_check;",
            "ALTER TABLE orders ADD CONSTRAINT orders_payment_method_check CHECK (payment_method IN ('efectivo', 'transferencia'));"
        ]

        for sql in sql_commands:
            print(f"\n⚙️  Ejecutando: {sql[:50]}...")

            payload = {'sql': sql}
            response = requests.post(columns_url, json=payload, headers=headers)

            print(f"📊 Status: {response.status_code}")
            if response.status_code != 200:
                print(f"❌ Error: {response.text}")
            else:
                print(f"✅ Éxito!")

        return {"success": True}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"success": False, "error": str(e)}

def add_column_via_python():
    """
    Intenta agregar la columna usando Python directamente.
    """
    try:
        import psycopg2
        from urllib.parse import urlparse

        print("🔄 Intentando conexión directa con PostgreSQL...")

        # Construir la URL de conexión de PostgreSQL
        # Nota: Esto requiere las credenciales de conexión directa de Supabase
        print("⚠️  Este método requiere acceso directo a PostgreSQL")
        print("    Las credenciales REST API no son suficientes")

        return False

    except ImportError:
        print("⚠️  psycopg2 no está instalado")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 SCRIPT PARA AGREGAR COLUMNA payment_method")
    print("=" * 80)

    result = execute_sql_on_supabase("")

    if not result.get("success"):
        print("\n" + "=" * 80)
        print("❌ No se pudo agregar la columna automáticamente")
        print("=" * 80)
        print("\n📋 Por favor, ejecuta este SQL manualmente en:")
        print(f"https://supabase.com/dashboard/project/vdpongjfmldvjxokhiov/sql")
        print("\n" + "=" * 80)
        print("""
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo';

ALTER TABLE orders
DROP CONSTRAINT IF EXISTS orders_payment_method_check;

ALTER TABLE orders
ADD CONSTRAINT orders_payment_method_check
CHECK (payment_method IN ('efectivo', 'transferencia'));
        """)
        print("=" * 80)
