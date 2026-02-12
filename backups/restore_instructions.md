# 🔄 Instrucciones de Restauración - Backup Supabase

## Métodos de Restauración

### Método 1: Usando la Interfaz Web de Supabase (Recomendado para principiantes)

1. **Accede al Dashboard de Supabase**
   - Ve a https://app.supabase.com
   - Selecciona tu proyecto o crea uno nuevo

2. **Abre el SQL Editor**
   - En el menú lateral, haz clic en "SQL Editor"

3. **Restaurar el Esquema**
   - Crea una nueva query
   - Copia y pega el contenido de `schema_backup.sql`
   - Haz clic en "Run" o presiona `Ctrl+Enter`

4. **Restaurar los Datos**
   - Crea otra nueva query
   - Copia y pega el contenido de `data_backup.sql`
   - **IMPORTANTE:** Modifica los INSERTs de `orders` para manejar `ticket_id`:
   
   ```sql
   -- Opción A: Eliminar ticket_id del INSERT
   INSERT INTO public.orders (id, created_at, client_id, state, address_delivery, total_order) VALUES
   ('2a2eaab4-3588-4a9b-b8d4-dc715dc216c4', '2026-01-29 04:05:49.004169+00', 'd81a9d4d-ef43-45ad-9551-489b615a434a', 'EN_CAMINO', 'Cra siempre víva 23', 49000);
   
   -- Opción B: Usar OVERRIDING SYSTEM VALUE
   INSERT INTO public.orders (id, created_at, client_id, state, address_delivery, total_order, ticket_id) 
   OVERRIDING SYSTEM VALUE VALUES
   ('2a2eaab4-3588-4a9b-b8d4-dc715dc216c4', '2026-01-29 04:05:49.004169+00', 'd81a9d4d-ef43-45ad-9551-489b615a434a', 'EN_CAMINO', 'Cra siempre víva 23', 49000, 13);
   ```
   
   - Haz clic en "Run"

---

### Método 2: Usando el MCP de Supabase (Desde este proyecto)

#### Restaurar Esquema

```python
# Desde Python o usando las herramientas MCP
from mcp import supabase_mcp_server

# Leer el archivo de esquema
with open('backups/schema_backup.sql', 'r') as f:
    schema_sql = f.read()

# Aplicar como migración
supabase_mcp_server.apply_migration(
    project_id='vdpongjfmldvjxokhiov',
    name='restore_schema_backup',
    query=schema_sql
)
```

#### Restaurar Datos

```python
# Leer el archivo de datos
with open('backups/data_backup.sql', 'r') as f:
    data_sql = f.read()

# Ejecutar SQL
supabase_mcp_server.execute_sql(
    project_id='vdpongjfmldvjxokhiov',
    query=data_sql
)
```

---

### Método 3: Usando psql (Para usuarios avanzados)

1. **Obtén las credenciales de conexión**
   ```bash
   # Desde el dashboard de Supabase:
   # Settings > Database > Connection string
   ```

2. **Conecta a la base de datos**
   ```bash
   psql "postgresql://postgres:[PASSWORD]@db.vdpongjfmldvjxokhiov.supabase.co:5432/postgres"
   ```

3. **Ejecuta los archivos SQL**
   ```sql
   -- Restaurar esquema
   \i /ruta/a/backups/schema_backup.sql
   
   -- Restaurar datos
   \i /ruta/a/backups/data_backup.sql
   ```

---

### Método 4: Usando Supabase CLI

1. **Instala Supabase CLI**
   ```bash
   # Ver instrucciones en el mensaje anterior
   brew install supabase/tap/supabase
   ```

2. **Inicia sesión**
   ```bash
   supabase login
   ```

3. **Vincula tu proyecto**
   ```bash
   supabase link --project-ref vdpongjfmldvjxokhiov
   ```

4. **Ejecuta las migraciones**
   ```bash
   # Copia los archivos a la carpeta de migraciones
   cp backups/schema_backup.sql supabase/migrations/20260129_schema_restore.sql
   
   # Aplica la migración
   supabase db push
   ```

---

## 🚨 Consideraciones Importantes

### 1. Manejo de `ticket_id`
El campo `ticket_id` en la tabla `orders` es autogenerado. Al restaurar:
- **Si es una base nueva:** Usa `OVERRIDING SYSTEM VALUE` para mantener los IDs originales
- **Si agregas a datos existentes:** Omite `ticket_id` del INSERT para que se genere automáticamente

### 2. Conflictos de UUIDs
Si restauras en una base que ya tiene datos:
```sql
-- Opción 1: Eliminar datos existentes
TRUNCATE TABLE order_details, orders, product_variants, products, clients CASCADE;

-- Opción 2: Usar ON CONFLICT
INSERT INTO public.clients (id, created_at, name, cel, address) VALUES
('d81a9d4d-ef43-45ad-9551-489b615a434a', '2026-01-29 03:55:58.45493+00', 'AC', '3137479005', 'calle azul roja')
ON CONFLICT (id) DO NOTHING;
```

### 3. Row Level Security (RLS)
Después de restaurar, configura las políticas de RLS:
```sql
-- Ejemplo: Permitir todas las operaciones (solo para desarrollo)
CREATE POLICY "Allow all" ON public.clients FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.products FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.product_variants FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.orders FOR ALL USING (true);
CREATE POLICY "Allow all" ON public.order_details FOR ALL USING (true);
```

### 4. Verificación Post-Restauración
```sql
-- Verificar conteo de registros
SELECT 'clients' as tabla, COUNT(*) FROM clients
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'product_variants', COUNT(*) FROM product_variants
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_details', COUNT(*) FROM order_details;

-- Resultado esperado:
-- clients: 1
-- products: 5
-- product_variants: 8
-- orders: 2
-- order_details: 4
```

---

## 📅 Backups Programados (Recomendación)

Para automatizar backups futuros, crea un script:

```python
# backup_scheduler.py
import schedule
import time
from datetime import datetime
from mcp import supabase_mcp_server

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Obtener datos
    tables = ['clients', 'products', 'product_variants', 'orders', 'order_details']
    
    for table in tables:
        result = supabase_mcp_server.execute_sql(
            project_id='vdpongjfmldvjxokhiov',
            query=f'SELECT * FROM {table}'
        )
        
        # Guardar en archivo
        with open(f'backups/{timestamp}_{table}.json', 'w') as f:
            f.write(result)
    
    print(f"Backup creado: {timestamp}")

# Ejecutar backup diario a las 2 AM
schedule.every().day.at("02:00").do(create_backup)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🆘 Soporte

Si encuentras problemas durante la restauración:
1. Verifica que los tipos ENUM existan antes de crear las tablas
2. Revisa los logs de error en Supabase Dashboard > Logs
3. Asegúrate de tener permisos suficientes en el proyecto

---

**Última actualización:** 2026-01-29
