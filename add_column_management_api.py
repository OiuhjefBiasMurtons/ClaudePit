"""
Script para agregar columna usando Supabase Management API o conexión directa.
"""
import os
import sys

def try_connection_string():
    """
    Intenta usar la connection string de Supabase si está disponible.
    """
    print("🔍 Buscando métodos de conexión alternativos...")

    # Verificar si hay variables de entorno adicionales
    env_vars = [
        'SUPABASE_DB_URL',
        'DATABASE_URL',
        'SUPABASE_CONNECTION_STRING',
        'POSTGRES_URL'
    ]

    print("\n📋 Variables de entorno disponibles:")
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"  ✅ {var}: {value[:30]}...")
            return var, value
        else:
            print(f"  ❌ {var}: No encontrada")

    return None, None

def create_sql_file():
    """
    Crea un archivo SQL que puede ser ejecutado manualmente.
    """
    sql_content = """-- Script para agregar columna payment_method a la tabla orders
-- Proyecto: vdpongjfmldvjxokhiov

-- 1. Agregar la columna payment_method
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo';

-- 2. Eliminar constraint anterior si existe (para evitar errores)
ALTER TABLE orders
DROP CONSTRAINT IF EXISTS orders_payment_method_check;

-- 3. Agregar constraint para validar valores
ALTER TABLE orders
ADD CONSTRAINT orders_payment_method_check
CHECK (payment_method IN ('efectivo', 'transferencia'));

-- 4. Verificar que la columna se creó correctamente
SELECT column_name, data_type, column_default, is_nullable
FROM information_schema.columns
WHERE table_name = 'orders' AND column_name = 'payment_method';

-- 5. Ver todas las columnas de la tabla orders
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'orders'
ORDER BY ordinal_position;
"""

    file_path = "migration_add_payment_method.sql"
    with open(file_path, 'w') as f:
        f.write(sql_content)

    print(f"\n✅ Archivo SQL creado: {file_path}")
    return file_path

if __name__ == "__main__":
    print("=" * 80)
    print("🔧 INTENTO DE CONEXIÓN DIRECTA A SUPABASE")
    print("=" * 80)

    # Intentar encontrar métodos alternativos
    var_name, connection_string = try_connection_string()

    if connection_string and 'postgres' in connection_string.lower():
        print(f"\n✅ Se encontró connection string en {var_name}")
        print("⚙️  Intentando conexión directa...")

        try:
            import psycopg2

            conn = psycopg2.connect(connection_string)
            cursor = conn.cursor()

            # Ejecutar los comandos SQL
            commands = [
                "ALTER TABLE orders ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo';",
                "ALTER TABLE orders DROP CONSTRAINT IF EXISTS orders_payment_method_check;",
                "ALTER TABLE orders ADD CONSTRAINT orders_payment_method_check CHECK (payment_method IN ('efectivo', 'transferencia'));"
            ]

            for cmd in commands:
                print(f"\n⚙️  Ejecutando: {cmd[:60]}...")
                cursor.execute(cmd)

            conn.commit()
            cursor.close()
            conn.close()

            print("\n✅ ¡Columna payment_method agregada exitosamente!")
            sys.exit(0)

        except ImportError:
            print("\n⚠️  psycopg2 no está instalado")
            print("    Instalar con: pip install psycopg2-binary")

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

    # Si no se pudo, crear archivo SQL
    print("\n" + "=" * 80)
    print("📋 CREANDO ARCHIVO SQL PARA EJECUCIÓN MANUAL")
    print("=" * 80)

    sql_file = create_sql_file()

    print("\n" + "=" * 80)
    print("📝 INSTRUCCIONES:")
    print("=" * 80)
    print(f"""
1. Ve a: https://supabase.com/dashboard/project/vdpongjfmldvjxokhiov/sql

2. Copia y pega el contenido del archivo: {sql_file}
   O ejecuta directamente este SQL:

   ALTER TABLE orders
   ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo';

   ALTER TABLE orders
   ADD CONSTRAINT orders_payment_method_check
   CHECK (payment_method IN ('efectivo', 'transferencia'));

3. Haz clic en "Run" (Ctrl+Enter)

4. Verifica con: python check_orders_table.py
    """)
    print("=" * 80)
