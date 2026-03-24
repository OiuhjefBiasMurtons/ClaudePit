-- ============================================
-- MIGRACIÓN: Agregar cliente_nombre, cliente_cel y barrio
-- a la vista dashboard_pedidos
-- Fecha: 2026-03-19
-- Columnas existentes confirmadas vía REST API:
--   ticket_id, precio_total, resumen_pedido, direccion,
--   estado, fecha, precio_domicilio
-- Columnas nuevas: cliente_nombre, cliente_cel, barrio
-- ============================================

-- Paso 1: eliminar la vista existente
DROP VIEW IF EXISTS public.dashboard_pedidos;

-- Paso 2: recrear con columnas originales + las 3 nuevas al final
CREATE VIEW public.dashboard_pedidos AS
SELECT
    o.ticket_id,
    (o.total_order + COALESCE(b.precio_domicilio, 0))            AS precio_total,
    (
        SELECT STRING_AGG(
            p.name || ' - ' || pv.nombre_variante
            || ': ' || od.quantity::TEXT,
            ' | '
            ORDER BY od.id
        )
        FROM public.order_details od
        JOIN public.product_variants pv ON pv.id = od.variant_id
        JOIN public.products p ON p.id = pv.product_id
        WHERE od.order_id = o.id
          AND od.quantity > 0
    )                                                            AS resumen_pedido,
    o.address_delivery                                           AS direccion,
    o.state                                                      AS estado,
    o.created_at                                                 AS fecha,
    b.precio_domicilio,
    -- Columnas nuevas
    c.name                                                       AS cliente_nombre,
    c.cel                                                        AS cliente_cel,
    b.nombre                                                     AS barrio
FROM public.orders o
JOIN public.clients c ON c.id = o.client_id
LEFT JOIN public.barrios b ON b.id = o.barrio_id
ORDER BY o.created_at DESC;
