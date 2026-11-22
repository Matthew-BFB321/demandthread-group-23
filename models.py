"""SQL + business rules app.py and api.py call functions"""

import pymysql
from werkzeug.security import check_password_hash

import supply_chain as sc
from db import execute, get_db, query_all, query_one

# =====================================================================
# Dashboard
# =====================================================================
BADGES = {"Stockout risk": "danger", "Excess stock": "warning", "Healthy": "success"}

def units_sold(d_from, d_to):
    """Units sold per product between d_from and d_to days ago as {product_id: units}."""
    rs = query_all("""
        SELECT product_id, SUM(quantity) AS units
        FROM sales
        WHERE sold_at >  DATE_SUB(NOW(), INTERVAL %s DAY)
          AND sold_at <= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY product_id
    """, (d_from, d_to))
    return {r["product_id"]: int(r["units"]) for r in rs}


def stock_on_order():
    """Units on open purchase orders per product, as {product_id: units}."""
    rs = query_all("""
        SELECT product_id, SUM(quantity) AS units
        FROM purchase_orders
        WHERE status <> 'Delivered'
        GROUP BY product_id
    """)
    return {r["product_id"]: int(r["units"]) for r in rs}

def product_metrics():
    """Every product with its sales and the supply_chain.py numbers."""
    prods = query_all("""
        SELECT p.id, p.sku, p.name, p.price, p.stock, p.lead_time_days,
               p.demand_std_dev, p.supplier_id, s.name AS supplier
        FROM products p
        JOIN suppliers s ON s.id = p.supplier_id
        ORDER BY p.sku
    """)
    wk_now = units_sold(7, 0)
    wk_prev = units_sold(14, 7)
    po_qty = stock_on_order()
    for p in prods:
        p["price"] = float(p["price"])
        p["sold_7"] = wk_now.get(p["id"], 0)
        p["sold_prev_7"] = wk_prev.get(p["id"], 0)
        p["on_order"] = po_qty.get(p["id"], 0)
        p["change"] = sc.percent_change(p["sold_7"], p["sold_prev_7"])
        p["daily_demand"] = sc.average_daily_demand(p["sold_7"])
        p["cover_days"] = sc.days_of_cover(p["stock"], p["on_order"], p["daily_demand"])
        p["status"] = sc.alert_status(p["cover_days"], p["lead_time_days"])
        p["severity"] = sc.alert_severity(p["status"], p["cover_days"], p["lead_time_days"])
        p["badge"] = BADGES[p["status"]]
        p["safety_stock"] = sc.safety_stock(float(p["demand_std_dev"]), p["lead_time_days"])
        p["reorder_point"] = sc.reorder_point(p["daily_demand"], p["lead_time_days"], p["safety_stock"])
        p["needs_reorder"] = sc.needs_reorder(p["stock"], p["on_order"], p["reorder_point"])
    return prods

def dashboard_stats():
    products = product_metrics()
    sold = sum(p["sold_7"] for p in products)
    sold_prev = sum(p["sold_prev_7"] for p in products)
    revenue = sum(p["sold_7"] * p["price"] for p in products)
    revenue_prev = sum(p["sold_prev_7"] * p["price"] for p in products)
    return dict(sold=sold, sold_change=sc.percent_change(sold, sold_prev),
                revenue=revenue, revenue_change=sc.percent_change(revenue, revenue_prev),
                stockout=len([p for p in products if p["status"] == "Stockout risk"]),
                excess=len([p for p in products if p["status"] == "Excess stock"]),
                reorders=len([p for p in products if p["needs_reorder"]]),
                products=products)

# =====================================================================
# Products and sales
# =====================================================================


def record_sale(product_id, quantity, channel):
    """Save a sale and reduce stock together, rolling back if a write fails."""
    if quantity <= 0:
        return False, "Enter a quantity of at least 1."
    if channel not in ("Store", "Online"):
        return False, "Choose Store or Online as the sales channel."

    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name, stock, price FROM products "
                           "WHERE id = %s FOR UPDATE", (product_id,))
            product = cursor.fetchone()
            if product is None:
                connection.rollback()
                return False, "Could not find that product."
            if quantity > product["stock"]:
                connection.rollback()
                return False, (f"Could not record sale: only {product['stock']} x "
                               f"{product['name']} available.")

            cursor.execute("INSERT INTO sales (product_id, quantity, unit_price, channel) "
                           "VALUES (%s, %s, %s, %s)",
                           (product_id, quantity, product["price"], channel))
            cursor.execute("UPDATE products SET stock = stock - %s WHERE id = %s",
                           (quantity, product_id))
        connection.commit()
        return True, f"Saved sale: {quantity} x {product['name']} ({channel})."
    except Exception:
        connection.rollback()
        raise


def list_products(search, page, size):
    """Find products by name and return the requested page."""
    query = "SELECT id, sku, name, supplier_id, price, stock, lead_time_days FROM products WHERE 1=1"
    parameters = []
    if search:
        query += " AND name LIKE %s"
        parameters.append(f"%{search}%")
    query += " ORDER BY sku LIMIT %s OFFSET %s"
    parameters += [size, (page - 1) * size]
    return query_all(query, parameters)


def get_product(product_id):
    """Find one product by its ID, returning None if it is missing."""
    return query_one("SELECT id, sku, name, supplier_id, price, stock, lead_time_days, "
                     "demand_std_dev FROM products WHERE id = %s", (product_id,))


# =====================================================================
# Alerts, forecasts and sign-in
def check_login(email, password):
    """The user if the email and password match, otherwise None."""
    user = query_one("""
        SELECT u.id, u.password_hash, u.role, u.supplier_id, s.name AS supplier
        FROM users u
        LEFT JOIN suppliers s ON s.id = u.supplier_id
        WHERE u.email = %s
    """, (email,))
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None

def list_alerts(status):
    """Products with this alert status, High severity first."""
    products = [p for p in product_metrics() if p["status"] == status]
    return sorted(products, key=lambda p: p["severity"] != "High")


# =====================================================================


# =====================================================================
# Recommendations and purchase orders
# =====================================================================


def recommendations():
    """This will return the products the model says to reorder with the recommended quantity."""
    to_order = []
    for prod in product_metrics():
        if prod["needs_reorder"]:
            # EOQ using annual demand and single unit annual holding cost
            eoq = sc.calculate_eoq(prod["daily_demand"] * 365, sc.ORDERING_COST,
                                   prod["price"] * sc.HOLDING_COST_RATE)
            prod["quantity"] = sc.recommended_order_quantity(
                prod["daily_demand"], prod["lead_time_days"], prod["safety_stock"],
                prod["stock"], prod["on_order"], eoq)
            to_order.append(prod)
    return to_order


def create_purchase_order(product_id, quantity, notes):
    """This will save an approved recommendation as a new purchase order with default status 'Placed'."""
    if quantity <= 0:
        return False, "The order quantity must be at least 1."
    try:
        # 'execute()' returns the new row's id, also used as the PO number
        po_id = execute("INSERT INTO purchase_orders (product_id, quantity, notes) "
                        "VALUES (%s, %s, %s)", (product_id, quantity, notes or None))
        return True, f"Purchase order {po_id} has been created and sent to the supplier."
    except pymysql.err.IntegrityError:
        get_db().rollback()
        return False, "The selected product does not exist."