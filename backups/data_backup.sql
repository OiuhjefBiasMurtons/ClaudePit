-- ============================================
-- BACKUP DE DATOS - PitzBias
-- Proyecto: vdpongjfmldvjxokhiov
-- Fecha: 2026-01-29 23:22:52
-- ============================================

-- ============================================
-- 1. DATOS DE CLIENTES
-- ============================================

INSERT INTO
    public.clients (
        id,
        created_at,
        name,
        cel,
        address
    )
VALUES (
        'd81a9d4d-ef43-45ad-9551-489b615a434a',
        '2026-01-29 03:55:58.45493+00',
        'AC',
        '3137479005',
        'calle azul roja'
    );

-- ============================================
-- 2. DATOS DE PRODUCTOS
-- ============================================

INSERT INTO
    public.products (
        id,
        name,
        description,
        food_type,
        activo
    )
VALUES (
        '93b0166a-cd94-4495-8eac-2781f9e63739',
        'Pizza Hawaiana',
        'Jamon, Pina y Queso',
        'PIZZA',
        true
    ),
    (
        '9128899e-c165-48fe-b2ec-999718a937b6',
        'Limonada de Coco',
        'Limon, Coco',
        'BEBIDA',
        true
    ),
    (
        '21b20dda-6beb-42b5-ad40-ec3de88fa678',
        'Pizza De la Casa',
        'Jamon, Cabano, Champinon, Cebolla',
        'PIZZA',
        true
    ),
    (
        '80d91853-ab60-412f-acda-50de2fb4a9a2',
        'Coca cola',
        'Coca Cola',
        'BEBIDA',
        true
    ),
    (
        '772366e8-0219-4255-a89c-004605185e82',
        'Coca cola zero',
        'Sin Azucar',
        'BEBIDA',
        true
    );

-- ============================================
-- 3. DATOS DE VARIANTES DE PRODUCTOS
-- ============================================

INSERT INTO
    public.product_variants (
        id,
        product_id,
        nombre_variante,
        price
    )
VALUES (
        'a7800efb-397c-42da-a020-2563c73feaa7',
        '93b0166a-cd94-4495-8eac-2781f9e63739',
        'Mediana',
        37000
    ),
    (
        'e3cf0154-b762-47f8-91f3-2b851cdc7089',
        '9128899e-c165-48fe-b2ec-999718a937b6',
        'Vaso',
        12000
    ),
    (
        'a2e991e0-79fa-4026-8fb2-28e586e65e33',
        '21b20dda-6beb-42b5-ad40-ec3de88fa678',
        'Grande',
        45000
    ),
    (
        'a5cda3b1-b462-4089-8211-557044d8e217',
        '21b20dda-6beb-42b5-ad40-ec3de88fa678',
        'Mediana',
        37000
    ),
    (
        '39efb19e-27e9-45b6-be0b-3c1447ef0a17',
        '80d91853-ab60-412f-acda-50de2fb4a9a2',
        'Personal',
        4000
    ),
    (
        '065b751d-ce9b-4004-adff-0601563ffcb0',
        '80d91853-ab60-412f-acda-50de2fb4a9a2',
        '1/2 Litro',
        5500
    ),
    (
        '608414ee-ae08-4ead-8381-19cf0cc45e1f',
        '80d91853-ab60-412f-acda-50de2fb4a9a2',
        '2 Litros',
        8000
    ),
    (
        '1f119a4d-bc90-4348-829d-2b5463d15891',
        '772366e8-0219-4255-a89c-004605185e82',
        'Personal',
        3350
    );

-- ============================================
-- 4. DATOS DE ÓRDENES
-- ============================================

INSERT INTO
    public.orders (
        id,
        created_at,
        client_id,
        state,
        address_delivery,
        total_order,
        ticket_id
    )
VALUES (
        '2a2eaab4-3588-4a9b-b8d4-dc715dc216c4',
        '2026-01-29 04:05:49.004169+00',
        'd81a9d4d-ef43-45ad-9551-489b615a434a',
        'EN_CAMINO',
        'Cra siempre víva 23',
        49000,
        13
    ),
    (
        'b5dab4ed-758f-47a0-945f-ee115b0e02f2',
        '2026-01-29 23:47:52.233636+00',
        'd81a9d4d-ef43-45ad-9551-489b615a434a',
        'PREPARANDO',
        'calle azul roja',
        45000,
        14
    );

-- ============================================
-- 5. DATOS DE DETALLES DE ORDEN
-- ============================================

INSERT INTO
    public.order_details (
        id,
        order_id,
        variant_id,
        quantity,
        precio_unitario_congelado,
        nombre_producto_snapshot,
        note
    )
VALUES (
        '09e601a9-cb8c-4448-9364-ed66b3c847a6',
        '2a2eaab4-3588-4a9b-b8d4-dc715dc216c4',
        'a2e991e0-79fa-4026-8fb2-28e586e65e33',
        1,
        45000,
        'Pizza De la Casa - Grande',
        ''
    ),
    (
        '70c790a0-f07a-4584-b03a-7cd0405abaea',
        '2a2eaab4-3588-4a9b-b8d4-dc715dc216c4',
        '39efb19e-27e9-45b6-be0b-3c1447ef0a17',
        1,
        4000,
        'Coca cola - Personal',
        ''
    ),
    (
        '24786eb0-964a-4ca4-8dfe-b920a5b54e38',
        'b5dab4ed-758f-47a0-945f-ee115b0e02f2',
        'a7800efb-397c-42da-a020-2563c73feaa7',
        1,
        37000,
        'Pizza Hawaiana - Mediana',
        ''
    ),
    (
        '9abf76b6-ddd9-4c25-ad1a-97777d979966',
        'b5dab4ed-758f-47a0-945f-ee115b0e02f2',
        '608414ee-ae08-4ead-8381-19cf0cc45e1f',
        1,
        8000,
        'Coca cola - 2 Litros',
        ''
    );

-- ============================================
-- FIN DEL BACKUP DE DATOS
-- ============================================