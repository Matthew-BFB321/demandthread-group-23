--DemandThread sample data
INSERT INTO suppliers (name, email) VALUES
    ('Kingsgate Clothing', 'sales@kingsgate-demo.co.za'),
    ('Ninian & Lester', 'orders@ninianlester-demo.co.za'),
    ('Danmore Clothing Manufacturers', 'sales@danmore-demo.co.za');

INSERT INTO products (sku, name, supplier_id, price, stock, lead_time_days, demand_std_dev) VALUES
    ('DT-1001', 'Light Blue Oversized Denim Jacket', 1, 899, 270, 18, 12),
    ('DT-1002', 'Black Cotton Logo T-Shirt', 2, 249, 840, 10, 10),
    ('DT-1003', 'Olive Green Relaxed-Fit Cargo Pants', 3, 599, 710, 35, 9),
    ('DT-1004', 'Cream Long-Sleeve Ribbed Knit Top', 2, 329, 1490, 14, 6),
    ('DT-1005', 'Charcoal Pullover Hoodie', 1, 549, 1140, 10, 8),
    ('DT-1006', 'Dark Blue High-Waisted Wide-Leg Jeans', 1, 699, 840, 18, 8),
    ('DT-1007', 'Black Quilted Puffer Vest', 3, 649, 1440, 35, 5),
    ('DT-1008', 'White Cotton Cropped T-Shirt', 2, 179, 460, 10, 11);

INSERT INTO purchase_orders (id, product_id, quantity, status, expected_delivery, created_at) VALUES
    (389, 7, 600, 'Delivered', DATE_SUB(CURDATE(), INTERVAL 60 DAY), DATE_SUB(NOW(), INTERVAL 95 DAY)),
    (410, 8, 700, 'Delivered', DATE_SUB(CURDATE(), INTERVAL 30 DAY), DATE_SUB(NOW(), INTERVAL 40 DAY)),
    (421, 3, 500, 'Confirmed', DATE_ADD(CURDATE(), INTERVAL 15 DAY), DATE_SUB(NOW(), INTERVAL 20 DAY)),
    (430, 2, 600, 'Shipped', DATE_ADD(CURDATE(), INTERVAL 2 DAY), DATE_SUB(NOW(), INTERVAL 8 DAY)),
    (433, 5, 300, 'In production', DATE_ADD(CURDATE(), INTERVAL 4 DAY), DATE_SUB(NOW(), INTERVAL 6 DAY)),
    (436, 6, 400, 'Placed', NULL, DATE_SUB(NOW(), INTERVAL 2 DAY));

--Demo sign-ins (stored as password hashes):
--buyer@demandthread.co.za      Buyer@2026      buyer
--kingsgate@demandthread.co.za  Supplier@2026   supplier for Kingsgate Clothing
INSERT INTO users (email, password_hash, role, supplier_id) VALUES
    ('buyer@demandthread.co.za', 'scrypt:32768:8:1$HJRaJIJO046wnWQT$354804b0967e6e833d92f695ec1ded7aa8311e3792b9f12a85f5321d6755903265eb2d286fe55b125c97cd68a2ecbb7cc2a1bad5b9b3c72c7ab018cd527f0942', 'buyer', NULL),
    ('kingsgate@demandthread.co.za', 'scrypt:32768:8:1$GQkvmuZi63dP25Ku$eda8490da6ac8c5150c9b61699d3a56919ed6c646f64c69084d51f3f38e6334922d3482e3f68a1dde0f088049b839ee96418940e581dc8980e0f470cd96d31ec', 'supplier', 1);


INSERT INTO sales (product_id, quantity, unit_price, channel, sold_at) VALUES
    (1, 126, 899, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (1, 84, 899, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (1, 135, 899, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (1, 90, 899, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (1, 147, 899, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (1, 98, 899, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (1, 169, 899, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (1, 113, 899, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (1, 198, 899, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (1, 132, 899, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (1, 228, 899, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (1, 152, 899, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (2, 223, 249, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (2, 149, 249, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (2, 228, 249, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (2, 152, 249, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (2, 226, 249, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (2, 150, 249, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (2, 233, 249, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (2, 155, 249, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (2, 231, 249, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (2, 154, 249, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (2, 235, 249, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (2, 157, 249, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (3, 84, 599, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (3, 56, 599, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (3, 91, 599, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (3, 61, 599, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (3, 99, 599, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (3, 66, 599, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (3, 107, 599, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (3, 71, 599, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (3, 118, 599, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (3, 78, 599, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (3, 149, 599, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (3, 99, 599, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (4, 157, 329, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (4, 105, 329, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (4, 150, 329, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (4, 100, 329, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (4, 142, 329, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (4, 94, 329, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (4, 133, 329, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (4, 88, 329, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (4, 125, 329, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (4, 83, 329, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (4, 101, 329, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (4, 67, 329, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (5, 181, 549, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (5, 120, 549, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (5, 177, 549, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (5, 118, 549, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (5, 174, 549, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (5, 116, 549, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (5, 170, 549, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (5, 114, 549, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (5, 168, 549, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (5, 112, 549, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (5, 160, 549, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (5, 106, 549, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (6, 127, 699, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (6, 85, 699, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (6, 132, 699, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (6, 88, 699, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (6, 131, 699, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (6, 87, 699, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (6, 136, 699, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (6, 90, 699, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (6, 139, 699, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (6, 92, 699, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (6, 147, 699, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (6, 98, 699, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (7, 128, 649, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (7, 86, 649, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (7, 120, 649, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (7, 80, 649, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (7, 113, 649, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (7, 75, 649, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (7, 102, 649, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (7, 68, 649, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (7, 94, 649, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (7, 62, 649, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (7, 76, 649, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (7, 50, 649, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (8, 180, 179, 'Store', DATE_SUB(NOW(), INTERVAL 38 DAY)), (8, 120, 179, 'Online', DATE_SUB(NOW(), INTERVAL 38 DAY)),
    (8, 187, 179, 'Store', DATE_SUB(NOW(), INTERVAL 31 DAY)), (8, 125, 179, 'Online', DATE_SUB(NOW(), INTERVAL 31 DAY)),
    (8, 193, 179, 'Store', DATE_SUB(NOW(), INTERVAL 24 DAY)), (8, 128, 179, 'Online', DATE_SUB(NOW(), INTERVAL 24 DAY)),
    (8, 200, 179, 'Store', DATE_SUB(NOW(), INTERVAL 17 DAY)), (8, 133, 179, 'Online', DATE_SUB(NOW(), INTERVAL 17 DAY)),
    (8, 204, 179, 'Store', DATE_SUB(NOW(), INTERVAL 10 DAY)), (8, 136, 179, 'Online', DATE_SUB(NOW(), INTERVAL 10 DAY)),
    (8, 214, 179, 'Store', DATE_SUB(NOW(), INTERVAL 3 DAY)), (8, 143, 179, 'Online', DATE_SUB(NOW(), INTERVAL 3 DAY));