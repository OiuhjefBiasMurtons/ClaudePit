#!/usr/bin/env python3
"""
Script para crear backups automáticos de Supabase
Uso: python create_backup.py
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Configuración
PROJECT_ID = "vdpongjfmldvjxokhiov"
BACKUP_DIR = Path(__file__).parent / "backups"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Nota: Este script requiere que tengas configurado el MCP de Supabase
# o que uses la API de Supabase directamente

def create_backup_directory():
    """Crea el directorio de backup si no existe"""
    backup_path = BACKUP_DIR / TIMESTAMP
    backup_path.mkdir(parents=True, exist_ok=True)
    return backup_path

def generate_schema_backup():
    """Genera el SQL del esquema"""
    schema_sql = """-- ============================================
-- BACKUP AUTOMÁTICO DE SUPABASE - PitzBias
-- Proyecto: {project_id}
-- Fecha: {timestamp}
-- ============================================

-- TIPOS PERSONALIZADOS
CREATE TYPE type_food AS ENUM ('PIZZA', 'LASAGNA', 'BEBIDA', 'ADICION', 'PAN');
CREATE TYPE type_order_state AS ENUM ('PREPARANDO', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO');

-- TABLAS
CREATE TABLE IF NOT EXISTS public.clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    name TEXT NOT NULL,
    cel TEXT NOT NULL UNIQUE,
    address TEXT
);

CREATE TABLE IF NOT EXISTS public.products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    description TEXT,
    food_type type_food NOT NULL,
    activo BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS public.product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES public.products(id),
    nombre_variante TEXT NOT NULL,
    price INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS public.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    client_id UUID NOT NULL REFERENCES public.clients(id),
    state type_order_state DEFAULT 'PREPARANDO'::type_order_state,
    address_delivery TEXT NOT NULL,
    total_order INTEGER DEFAULT 0,
    ticket_id BIGINT GENERATED ALWAYS AS IDENTITY
);

CREATE TABLE IF NOT EXISTS public.order_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES public.orders(id),
    variant_id UUID NOT NULL REFERENCES public.product_variants(id),
    quantity INTEGER DEFAULT 1,
    precio_unitario_congelado INTEGER NOT NULL,
    nombre_producto_snapshot TEXT,
    note TEXT
);

-- RLS
ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.product_variants ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.order_details ENABLE ROW LEVEL SECURITY;

-- ÍNDICES
CREATE INDEX IF NOT EXISTS idx_clients_cel ON public.clients(cel);
CREATE INDEX IF NOT EXISTS idx_orders_client_id ON public.orders(client_id);
CREATE INDEX IF NOT EXISTS idx_order_details_order_id ON public.order_details(order_id);
CREATE INDEX IF NOT EXISTS idx_product_variants_product_id ON public.product_variants(product_id);
""".format(project_id=PROJECT_ID, timestamp=TIMESTAMP)
    
    return schema_sql

def backup_with_supabase_client():
    """
    Backup usando el cliente de Supabase directamente
    Requiere: pip install supabase
    """
    try:
        from supabase import create_client
        from dotenv import load_dotenv
        
        load_dotenv()
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            print("❌ Error: SUPABASE_URL y SUPABASE_KEY deben estar en .env")
            return False
        
        supabase = create_client(url, key)
        backup_path = create_backup_directory()
        
        # Tablas a respaldar
        tables = ['clients', 'products', 'product_variants', 'orders', 'order_details']
        
        print(f"📦 Creando backup en: {backup_path}")
        
        # Backup de datos
        data_backup = {
            "metadata": {
                "project_id": PROJECT_ID,
                "timestamp": TIMESTAMP,
                "date": datetime.now().isoformat()
            },
            "data": {}
        }
        
        for table in tables:
            print(f"  📋 Respaldando tabla: {table}")
            response = supabase.table(table).select("*").execute()
            data_backup["data"][table] = response.data
            print(f"     ✅ {len(response.data)} registros")
        
        # Guardar JSON
        json_path = backup_path / "data_backup.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_backup, f, indent=2, ensure_ascii=False, default=str)
        
        # Guardar SQL del esquema
        schema_path = backup_path / "schema_backup.sql"
        with open(schema_path, 'w', encoding='utf-8') as f:
            f.write(generate_schema_backup())
        
        # Generar SQL de datos
        sql_path = backup_path / "data_backup.sql"
        with open(sql_path, 'w', encoding='utf-8') as f:
            f.write(f"-- Backup de datos - {TIMESTAMP}\n\n")
            
            for table, records in data_backup["data"].items():
                if records:
                    f.write(f"-- Tabla: {table}\n")
                    for record in records:
                        columns = ', '.join(record.keys())
                        values = ', '.join([
                            f"'{v}'" if isinstance(v, str) else str(v) if v is not None else 'NULL'
                            for v in record.values()
                        ])
                        f.write(f"INSERT INTO public.{table} ({columns}) VALUES ({values});\n")
                    f.write("\n")
        
        # Crear README
        readme_path = backup_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"""# Backup - {TIMESTAMP}

**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Proyecto:** {PROJECT_ID}

## Contenido

- `schema_backup.sql` - Estructura de la base de datos
- `data_backup.sql` - Datos en formato SQL
- `data_backup.json` - Datos en formato JSON

## Estadísticas

""")
            for table, records in data_backup["data"].items():
                f.write(f"- **{table}:** {len(records)} registros\n")
        
        print(f"\n✅ Backup completado exitosamente!")
        print(f"📁 Ubicación: {backup_path}")
        print(f"\nArchivos creados:")
        print(f"  - schema_backup.sql")
        print(f"  - data_backup.sql")
        print(f"  - data_backup.json")
        print(f"  - README.md")
        
        return True
        
    except ImportError:
        print("❌ Error: Instala el cliente de Supabase con: pip install supabase")
        return False
    except Exception as e:
        print(f"❌ Error durante el backup: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Iniciando backup de Supabase...")
    print(f"📅 Timestamp: {TIMESTAMP}\n")
    
    success = backup_with_supabase_client()
    
    if success:
        print("\n💡 Tip: Guarda estos backups en un lugar seguro (Git, Cloud Storage, etc.)")
    else:
        print("\n❌ El backup falló. Revisa los errores anteriores.")
        exit(1)

if __name__ == "__main__":
    main()
