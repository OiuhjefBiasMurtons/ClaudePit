"""
Script para verificar la estructura de la tabla orders.
"""
from app.database import get_supabase_client
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_orders_table():
    """
    Verifica la estructura de la tabla orders.
    """
    try:
        supabase = get_supabase_client()

        # Intentar obtener un pedido para ver las columnas disponibles
        result = supabase.table("orders").select("*").limit(1).execute()

        if result.data:
            logger.info("✅ Estructura de la tabla orders:")
            logger.info(f"Columnas disponibles: {list(result.data[0].keys())}")

            if 'payment_method' in result.data[0]:
                logger.info("✅ La columna 'payment_method' YA EXISTE en la tabla orders")
            else:
                logger.info("❌ La columna 'payment_method' NO existe en la tabla orders")
                logger.info("\nPor favor, ejecuta este SQL en Supabase SQL Editor (https://supabase.com/dashboard/project/vdpongjfmldvjxokhiov/sql):")
                logger.info("""
ALTER TABLE orders
ADD COLUMN payment_method TEXT DEFAULT 'efectivo'
CHECK (payment_method IN ('efectivo', 'transferencia'));
                """)
        else:
            logger.info("⚠️  No hay pedidos en la tabla para verificar")

    except Exception as e:
        logger.error(f"❌ Error al verificar tabla: {str(e)}")

if __name__ == "__main__":
    check_orders_table()
