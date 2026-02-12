-- Script para agregar columna payment_method a la tabla orders
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
