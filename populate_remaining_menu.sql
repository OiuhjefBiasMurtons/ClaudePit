

-- Pizza: Peperoni
INSERT INTO products (name, description, food_type, activo)
VALUES ('Peperoni', 'Peperoni', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Peperoni'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Peperoni'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Peperoni'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Peperoni'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Peperoni'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Bolognesa
INSERT INTO products (name, description, food_type, activo)
VALUES ('Bolognesa', 'Jamon, maicitos, tomate, carne bolognesa, pimenton, cebolla', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Mexicana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Mexicana', 'Jamon, carne bolognesa, maicitos, pimenton, jalapeños, cebolla, tomate', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Mexicana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Mexicana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Mexicana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Mexicana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Mexicana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Zamba
INSERT INTO products (name, description, food_type, activo)
VALUES ('Zamba', 'Maduro, tocineta, maicitos', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Zamba'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Zamba'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Zamba'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Zamba'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Zamba'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Madurito
INSERT INTO products (name, description, food_type, activo)
VALUES ('Madurito', 'Maduro, cabano, maicitos', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Madurito'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Madurito'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Madurito'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Madurito'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Madurito'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;





-- Pizza: Hawaiana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Hawaiana', 'Jamon, piña', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Hawaiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Hawaiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Hawaiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Hawaiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Hawaiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Piña
INSERT INTO products (name, description, food_type, activo)
VALUES ('Piña', 'Piña, carne bolognesa', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Tropical
INSERT INTO products (name, description, food_type, activo)
VALUES ('Tropical', 'Pollo, piña, tocineta', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Parmesana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Parmesana', 'Queso parmesano, maduro, tocineta', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Parmesana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Parmesana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Parmesana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Parmesana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Parmesana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Del Campo
INSERT INTO products (name, description, food_type, activo)
VALUES ('Del Campo', 'Jamon, maicitos, tocineta, tomate', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Del Campo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Del Campo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Del Campo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Del Campo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Del Campo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;





-- Pizza: Topo
INSERT INTO products (name, description, food_type, activo)
VALUES ('Topo', 'Pollo, tomate, tocineta', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Topo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Topo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Topo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Topo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Topo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Toposa
INSERT INTO products (name, description, food_type, activo)
VALUES ('Toposa', 'Tocineta, pollo, salami', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Toposa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Toposa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Toposa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Toposa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Toposa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Margarita
INSERT INTO products (name, description, food_type, activo)
VALUES ('Margarita', 'Tomate, albahaca, aceite de oliva', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Margarita'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Margarita'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Margarita'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Margarita'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Margarita'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Vegetariana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Vegetariana', 'Cebolla, ajo, champinones, tomate, pimenton', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Margarita Especial
INSERT INTO products (name, description, food_type, activo)
VALUES ('Margarita Especial', 'Tomate, albahaca, tocineta, aceite de oliva', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Margarita Especial'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Margarita Especial'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Margarita Especial'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Margarita Especial'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Margarita Especial'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;





-- Pizza: Italiana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Italiana', 'Jamon, champinones, tomate, maicitos', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Italiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Italiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Italiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Italiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Italiana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Primavera
INSERT INTO products (name, description, food_type, activo)
VALUES ('Primavera', 'Pollo, tomate, maicitos', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Primavera'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Primavera'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Primavera'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Primavera'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Primavera'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Americana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Americana', 'Jamon, salchicha, maicitos', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Americana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Americana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Americana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Americana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Americana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Julieta
INSERT INTO products (name, description, food_type, activo)
VALUES ('Julieta', 'Jamon, salami, maicitos', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Julieta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Julieta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Julieta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Julieta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Julieta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Pollo con Champiñones
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pollo con Champiñones', 'Pollo, champinones', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Pollo con Champiñones'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Pollo con Champiñones'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Pollo con Champiñones'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Pollo con Champiñones'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Pollo con Champiñones'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;





-- Pizza: Pollo con Bolognesa y Piña
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pollo con Bolognesa y Piña', 'Pollo, carne bolognesa, piña', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Pollo con Bolognesa y Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Pollo con Bolognesa y Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Pollo con Bolognesa y Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Pollo con Bolognesa y Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Pollo con Bolognesa y Piña'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Pollo con Tocineta y Maiz
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pollo con Tocineta y Maiz', 'Pollo, tocineta, maiz', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Pollo con Tocineta y Maiz'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Pollo con Tocineta y Maiz'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Pollo con Tocineta y Maiz'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Pollo con Tocineta y Maiz'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Pollo con Tocineta y Maiz'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Pollo y Jamon
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pollo y Jamon', 'Pollo, jamon', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Pollo y Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Pollo y Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Pollo y Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Pollo y Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Pollo y Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Española
INSERT INTO products (name, description, food_type, activo)
VALUES ('Española', 'Salami, cabano, aceitunas', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Española'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Española'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Española'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Española'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Española'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;




-- Pizza: Picante
INSERT INTO products (name, description, food_type, activo)
VALUES ('Picante', 'Jamon, pollo, carne bolognesa, pimienta negra', 'PIZZA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Junior', 21000, true
FROM products
WHERE name = 'Picante'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Personal', 29000, true
FROM products
WHERE name = 'Picante'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 37000, true
FROM products
WHERE name = 'Picante'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Mediana', 44000, true
FROM products
WHERE name = 'Picante'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 55000, true
FROM products
WHERE name = 'Picante'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Bolognesa
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Bolognesa', 'Carne bolognesa', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 14000, true
FROM products
WHERE name = 'Lasagna Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 20000, true
FROM products
WHERE name = 'Lasagna Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Bolognesa'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;



-- Lasagna: Lasagna Bolognesa + Jamon
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Bolognesa + Jamon', 'Carne bolognesa, jamon', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 14000, true
FROM products
WHERE name = 'Lasagna Bolognesa + Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 20000, true
FROM products
WHERE name = 'Lasagna Bolognesa + Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Bolognesa + Jamon'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Pollo + Maicitos
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Pollo + Maicitos', 'Pollo, maicitos', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 14000, true
FROM products
WHERE name = 'Lasagna Pollo + Maicitos'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 20000, true
FROM products
WHERE name = 'Lasagna Pollo + Maicitos'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Pollo + Maicitos'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Pollo
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Pollo', 'Pollo', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 16000, true
FROM products
WHERE name = 'Lasagna Pollo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 23000, true
FROM products
WHERE name = 'Lasagna Pollo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Pollo'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Pocha
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Pocha', 'Pollo, champinon', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 16000, true
FROM products
WHERE name = 'Lasagna Pocha'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 23000, true
FROM products
WHERE name = 'Lasagna Pocha'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Pocha'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Mixta
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Mixta', 'Pollo, carne bolognesa', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 16000, true
FROM products
WHERE name = 'Lasagna Mixta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 23000, true
FROM products
WHERE name = 'Lasagna Mixta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Mixta'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Tropical
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Tropical', 'Pollo, carne bolognesa, piña', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 16000, true
FROM products
WHERE name = 'Lasagna Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 23000, true
FROM products
WHERE name = 'Lasagna Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Tropical'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Lasagna: Lasagna Vegetariana
INSERT INTO products (name, description, food_type, activo)
VALUES ('Lasagna Vegetariana', 'Champinones, cebolla, ajo, tomate', 'LASAGNA', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Pequeña', 14000, true
FROM products
WHERE name = 'Lasagna Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Grande', 20000, true
FROM products
WHERE name = 'Lasagna Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Extra', 27000, true
FROM products
WHERE name = 'Lasagna Vegetariana'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;

-- Entrada: Pancito con Queso Crema y Parmesano
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pancito con Queso Crema y Parmesano', 'Pancito', 'PAN', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Única', 10000, true
FROM products
WHERE name = 'Pancito con Queso Crema y Parmesano'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Entrada: Pancito con Tomate y Queso Crema
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pancito con Tomate y Queso Crema', 'Pancito', 'PAN', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Única', 10000, true
FROM products
WHERE name = 'Pancito con Tomate y Queso Crema'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;


-- Entrada: Pancito con Queso Mozzarella y Queso Crema
INSERT INTO products (name, description, food_type, activo)
VALUES ('Pancito con Queso Mozzarella y Queso Crema', 'Pancito', 'PAN', true)
ON CONFLICT (name)
DO UPDATE SET description = EXCLUDED.description;


INSERT INTO product_variants (product_id, nombre_variante, price, activo)
SELECT id, 'Única', 10000, true
FROM products
WHERE name = 'Pancito con Queso Mozzarella y Queso Crema'
ON CONFLICT (product_id, nombre_variante)
DO UPDATE SET price = EXCLUDED.price;

