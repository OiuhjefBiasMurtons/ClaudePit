"""
Script para agregar la columna payment_method a la tabla orders en Supabase.
Este script ejecuta un comando SQL usando las credenciales de Supabase del proyecto.
"""
from app.database import get_supabase_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_payment_method_column():
    """
    Agrega la columna payment_method a la tabla orders.
    """
    try:
        supabase = get_supabase_client()

        # Ejecutar el comando SQL para agregar la columna
        sql_query = """
        ALTER TABLE orders
        ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo'
        CHECK (payment_method IN ('efectivo', 'transferencia'));
        """

        logger.info("Ejecutando comando SQL para agregar columna payment_method...")

        # Usar RPC para ejecutar SQL directo
        result = supabase.rpc('exec_sql', {'sql': sql_query}).execute()

        logger.info("✅ Columna payment_method agregada exitosamente!")
        return True

    except Exception as e:
        logger.error(f"❌ Error al agregar columna: {str(e)}")
        logger.info("\nPor favor, ejecuta este SQL manualmente en Supabase SQL Editor:")
        logger.info("""
        ALTER TABLE orders
        ADD COLUMN IF NOT EXISTS payment_method TEXT DEFAULT 'efectivo'
        CHECK (payment_method IN ('efectivo', 'transferencia'));
        """)
        return False

if __name__ == "__main__":
    add_payment_method_column()
