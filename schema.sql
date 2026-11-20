-- Weekly sales, stock on order, alerts, forecasts and reorder amounts are
-- not stored: supply_chain.py calculates them with these tables.

CREATE TABLE IF NOT EXISTS suppliers (
    id     INT AUTO_INCREMENT PRIMARY KEY,
    name   VARCHAR(120) NOT NULL UNIQUE,
    email  VARCHAR(160) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS products (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    sku             VARCHAR(20)   NOT NULL UNIQUE,
    name            VARCHAR(120)  NOT NULL,
    supplier_id     INT           NOT NULL,
    price           DECIMAL(10,2) NOT NULL,
    stock           INT           NOT NULL DEFAULT 0,
    lead_time_days  INT           NOT NULL,
    demand_std_dev  DECIMAL(6,2)  NOT NULL DEFAULT 0,
    created_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
    CONSTRAINT chk_products_price CHECK (price >= 0),
    CONSTRAINT chk_products_stock CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS sales (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    product_id  INT           NOT NULL,
    quantity    INT           NOT NULL,
    unit_price  DECIMAL(10,2) NOT NULL,
    channel     VARCHAR(10)   NOT NULL,
    sold_at     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sales_product FOREIGN KEY (product_id) REFERENCES products (id),
    CONSTRAINT chk_sales_quantity CHECK (quantity > 0),
    CONSTRAINT chk_sales_channel CHECK (channel IN ('Store', 'Online')),
    INDEX idx_sales_product_date (product_id, sold_at)
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    product_id         INT          NOT NULL,
    quantity           INT          NOT NULL,
    status             VARCHAR(20)  NOT NULL DEFAULT 'Placed',
    expected_delivery  DATE         NULL,
    notes              VARCHAR(255) NULL,
    created_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_po_product FOREIGN KEY (product_id) REFERENCES products (id),
    CONSTRAINT chk_po_quantity CHECK (quantity > 0),
    CONSTRAINT chk_po_status CHECK (status IN ('Placed', 'Confirmed', 'In production', 'Shipped', 'Delivered'))
);


CREATE TABLE IF NOT EXISTS users (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    email          VARCHAR(160) NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    role           VARCHAR(10)  NOT NULL,
    supplier_id    INT          NULL,
    CONSTRAINT fk_users_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers (id),
    CONSTRAINT chk_users_role CHECK (role IN ('buyer', 'supplier'))
);