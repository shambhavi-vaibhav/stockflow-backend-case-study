-- Companies Table (Multi-tenant support)
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Product Types for thresholds
CREATE TABLE product_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    low_stock_threshold INT DEFAULT 10
);

-- Main Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    product_type_id INT REFERENCES product_types(id),
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    price NUMERIC(12, 2) NOT NULL,
    is_bundle BOOLEAN DEFAULT FALSE
);

-- Bundle Logic
CREATE TABLE bundle_items (
    bundle_id INT REFERENCES products(id),
    component_id INT REFERENCES products(id),
    quantity INT CHECK (quantity > 0)
);

-- Inventory Table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    warehouse_id INT NOT NULL,
    quantity INT DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE(product_id, warehouse_id)
);

-- Audit log for Sales Velocity
CREATE TABLE inventory_changes (
    id SERIAL PRIMARY KEY,
    inventory_id INT REFERENCES inventory(id),
    change_type VARCHAR(50), -- 'sale', 'restock'
    quantity_diff INT,
    created_at TIMESTAMP DEFAULT NOW()
);
