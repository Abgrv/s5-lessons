-- Удалите внешний ключ из sales
ALTER TABLE sales DROP CONSTRAINT sales_products_product_id_fk;

-- Удалите первичный ключ из products
ALTER TABLE products DROP CONSTRAINT products_pk;

-- Добавьте новое поле id для суррогантного ключа в products. Сделайте данное поле первичным ключом
ALTER TABLE products ADD COLUMN id SERIAL PRIMARY KEY;

-- Добавьте дату начала действия записи в products
ALTER TABLE products
ADD COLUMN valid_from timestamptz;

-- Добавьте дату окончания действия записи в products
ALTER TABLE products
ADD COLUMN valid_to timestamptz;

-- Добавьте новый внешний ключ sales_products_id_fk в sales
ALTER TABLE sales
ADD CONSTRAINT sales_products_id_fk
FOREIGN KEY (product_id)
REFERENCES products(id);