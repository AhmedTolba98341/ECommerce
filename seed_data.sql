-- ============================================================
-- seed_data.sql  –  Sample data for ECommerceDB
-- Run this in SSMS against ECommerceDB after creating tables
-- ============================================================

-- Payment Methods
INSERT INTO PAYMENT_METHOD (MethodName) VALUES
    ('Credit Card'), ('Cash on Delivery'), ('Bank Transfer');

-- Categories
INSERT INTO CATEGORY (CategoryName, Description) VALUES
    ('Electronics',  'Phones, laptops, gadgets'),
    ('Clothing',     'Apparel for men and women'),
    ('Books',        'Fiction and non-fiction'),
    ('Home & Garden','Furniture, decor, tools'),
    ('Sports',       'Equipment and apparel');

-- Brands
INSERT INTO BRAND (BrandName, Country) VALUES
    ('Apple',   'USA'),
    ('Samsung', 'South Korea'),
    ('Nike',    'USA'),
    ('Adidas',  'Germany'),
    ('Sony',    'Japan');

-- Products
INSERT INTO PRODUCT (ProductName, Description, Price, Stock, CategoryID, BrandID, IsActive) VALUES
    ('iPhone 15',          'Latest Apple smartphone',            999.99, 50, 1, 1, 1),
    ('Samsung Galaxy S24', 'Flagship Android phone',             849.99, 40, 1, 2, 1),
    ('Sony WH-1000XM5',    'Noise-cancelling headphones',        349.99, 30, 1, 5, 1),
    ('Nike Air Max 270',   'Comfortable running shoes',          129.99, 60, 5, 3, 1),
    ('Adidas Ultraboost',  'Performance running shoe',           159.99, 45, 5, 4, 1),
    ('Clean Code',         'Book by Robert C. Martin',            34.99, 20, 3, 1, 1),
    ('Nike Dri-FIT Tee',   'Lightweight training shirt',          29.99, 80, 2, 3, 1),
    ('Samsung 4K Monitor', '27-inch UHD display',                399.99, 15, 1, 2, 1);

-- Admin user  (password: admin123)
-- bcrypt hash for 'admin123' – replace with actual hash from Python if needed
INSERT INTO [USER] (Username, Email, Password, Role, IsActive) VALUES
    ('admin', 'admin@shopease.com',
     '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW',
     'Admin', 1);

INSERT INTO ADMIN (UserID, FullName)
    SELECT UserID, 'System Administrator' FROM [USER] WHERE Username = 'admin';

-- Discount example
INSERT INTO DISCOUNT (DiscountName, DiscountPercent, IsActive) VALUES
    ('Summer Sale', 10.00, 1),
    ('Flash Deal',  20.00, 1);
