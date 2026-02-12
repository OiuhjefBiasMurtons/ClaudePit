-- ============================================
-- BACKUP COMPLETO DE SUPABASE - PitzBias
-- Proyecto: vdpongjfmldvjxokhiov
-- Fecha: 2026-01-29 23:22:52
-- ============================================

-- ============================================
-- 1. TIPOS PERSONALIZADOS (ENUMS)
-- ============================================

-- Tipo para categorías de comida
CREATE TYPE type_food AS ENUM ('PIZZA', 'LASAGNA', 'BEBIDA', 'ADICION', 'PAN');

-- Tipo para estados de orden
CREATE TYPE type_order_state AS ENUM ('PREPARANDO', 'EN_CAMINO', 'ENTREGADO', 'CANCELADO');

-- ============================================
-- 2. TABLAS
-- ============================================

-- Tabla de clientes
CREATE TABLE IF NOT EXISTS public.clients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    created_at TIMESTAMP
    WITH
        TIME ZONE DEFAULT now(),
        name TEXT NOT NULL,
        cel TEXT NOT NULL UNIQUE,
        address TEXT
);

-- Tabla de productos
CREATE TABLE IF NOT EXISTS public.products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    name TEXT NOT NULL,
    description TEXT,
    food_type type_food NOT NULL,
    activo BOOLEAN DEFAULT true
);

-- Tabla de variantes de productos
CREATE TABLE IF NOT EXISTS public.product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    product_id UUID NOT NULL REFERENCES public.products (id),
    nombre_variante TEXT NOT NULL,
    price INTEGER NOT NULL
);

-- Tabla de órdenes
CREATE TABLE IF NOT EXISTS public.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    client_id UUID NOT NULL REFERENCES public.clients(id),
    state type_order_state DEFAULT 'PREPARANDO'::type_order_state,
    address_delivery TEXT NOT NULL,
    total_order INTEGER DEFAULT 0,
    ticket_id BIGINT GENERATED ALWAYS AS IDENTITY
);

-- Tabla de detalles de orden
CREATE TABLE IF NOT EXISTS public.order_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid (),
    order_id UUID NOT NULL REFERENCES public.orders (id),
    variant_id UUID NOT NULL REFERENCES public.product_variants (id),
    quantity INTEGER DEFAULT 1,
    precio_unitario_congelado INTEGER NOT NULL,
    nombre_producto_snapshot TEXT,
    note TEXT
);

COMMENT ON COLUMN public.order_details.note IS 'Additional info, like quitar un ingrediente o indicaciones del domicilio';

-- ============================================
-- 3. HABILITAR ROW LEVEL SECURITY (RLS)
-- ============================================

ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.product_variants ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.order_details ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 4. ÍNDICES (Opcional - para optimización)
-- ============================================

-- Índice en cel de clients para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_clients_cel ON public.clients (cel);

-- Índice en client_id de orders
CREATE INDEX IF NOT EXISTS idx_orders_client_id ON public.orders (client_id);

-- Índice en order_id de order_details
CREATE INDEX IF NOT EXISTS idx_order_details_order_id ON public.order_details (order_id);

-- Índice en product_id de product_variants
CREATE INDEX IF NOT EXISTS idx_product_variants_product_id ON public.product_variants (product_id);

-- ============================================
-- FIN DEL BACKUP DE ESQUEMA
-- ============================================