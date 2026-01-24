# Esquema de Base de Datos - Supabase (PitzBias)

## Tabla: `clients`
Almacena información de los clientes.

**Columnas:**
- `id` (uuid, PK, auto-generado) - `gen_random_uuid()`
- `created_at` (timestamptz, auto-generado) - `now()`
- `name` (text, required) - Nombre del cliente
- `cel` (text, required, unique) - Número de teléfono/celular del cliente
- `address` (text, nullable) - Dirección del cliente

**RLS:** Habilitado
**Relaciones:** Referenciado por `orders.client_id`

---

## Tabla: `products`
Almacena los productos base (pizzas, bebidas, etc).

**Columnas:**
- `id` (uuid, PK, auto-generado) - `gen_random_uuid()`
- `name` (text, required) - Nombre del producto
- `description` (text, nullable) - Descripción del producto
- `food_type` (enum type_food, required) - Tipo de comida
  - Valores: `PIZZA`, `LASAGNA`, `BEBIDA`, `ADICION`, `PAN`
- `activo` (boolean, default: true) - Si el producto está activo

**RLS:** Habilitado
**Relaciones:** Referenciado por `product_variants.product_id`

---

## Tabla: `product_variants`
Almacena las variantes de productos (tamaños, sabores, etc).

**Columnas:**
- `id` (uuid, PK, auto-generado) - `gen_random_uuid()`
- `product_id` (uuid, FK -> products.id, required) - ID del producto base
- `nombre_variante` (text, required) - Nombre de la variante (ej: "Mediana", "Grande")
- `price` (integer, required) - Precio en centavos o unidad mínima

**RLS:** Habilitado
**Relaciones:** 
- Referencia a `products.id`
- Referenciado por `order_details.variant_id`

---

## Tabla: `orders`
Almacena las órdenes de los clientes.

**Columnas:**
- `id` (uuid, PK, auto-generado) - `gen_random_uuid()`
- `created_at` (timestamptz, auto-generado) - `now()`
- `client_id` (uuid, FK -> clients.id, required) - ID del cliente
- `ticket_id` (text, required) - Identificador único del ticket
- `address_delivery` (text, required) - Dirección de entrega
- `state` (enum type_order_state, default: 'PREPARANDO') - Estado del pedido
  - Valores: `PREPARANDO`, `EN_CAMINO`, `ENTREGADO`, `CANCELADO`
- `total_order` (integer, nullable, default: 0) - Total del pedido (calculado por trigger)

**RLS:** Habilitado
**Relaciones:** 
- Referencia a `clients.id`
- Referenciado por `order_details.order_id`

---

## Tabla: `order_details`
Almacena los items de cada orden.

**Columnas:**
- `id` (uuid, PK, auto-generado) - `gen_random_uuid()`
- `order_id` (uuid, FK -> orders.id, required) - ID de la orden
- `variant_id` (uuid, FK -> product_variants.id, required) - ID de la variante del producto
- `quantity` (integer, default: 1) - Cantidad del producto
- `precio_unitario_congelado` (integer, required) - Precio unitario congelado al momento de la orden
- `nombre_producto_snapshot` (text, nullable) - Snapshot del nombre del producto
- `note` (text, nullable) - Nota especial para el item (ej: "sin cebolla", "extra queso")

**RLS:** Habilitado
**Relaciones:** 
- Referencia a `orders.id`
- Referencia a `product_variants.id`

---

## Enums definidos:

### `type_food`
Valores: `PIZZA`, `LASAGNA`, `BEBIDA`, `ADICION`, `PAN`

### `type_order_state`
Valores: `PREPARANDO`, `EN_CAMINO`, `ENTREGADO`, `CANCELADO`

---

## Notas importantes:

1. **Columna de teléfono**: En la tabla `clients`, el campo se llama `cel`, NO `phone`.
2. **Columna de dirección**: En la tabla `orders`, el campo se llama `address_delivery`, NO `delivery_address`.
3. **Estados de orden**: Los valores válidos son `PREPARANDO`, `EN_CAMINO`, `ENTREGADO`, `CANCELADO` (en mayúsculas).
4. **No existe vista `products_with_variants`**: Debes hacer JOIN entre `products` y `product_variants`.
5. **Triggers**: La tabla `orders` tiene un trigger que calcula automáticamente el `total_order`.
6. **RLS habilitado**: Todas las tablas tienen Row-Level Security habilitado. Usa la service_role key para operaciones del backend.

---

## Mapeo correcto en el código:

### Estados de orden:
```python
# ✅ CORRECTO
"PREPARANDO"  # Estado inicial
"EN_CAMINO"   # Pedido confirmado
"ENTREGADO"   # Pedido completado
"CANCELADO"   # Pedido cancelado

# ❌ INCORRECTO
"pending", "confirmed", "cancelled"
```

### Columnas:
```python
# ✅ CORRECTO
{"cel": telefono, "name": nombre}
{"address_delivery": direccion}

# ❌ INCORRECTO
{"phone": telefono}
{"delivery_address": direccion}
```
