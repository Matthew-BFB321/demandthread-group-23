"""SQL and business rules. app.py and api.py call these functions; they never contain SQL themselves."""
from datetime import date
from decimal import Decimal, InvalidOperation

import pymysql
from werkzeug.security import check_password_hash

import supply_chain as sc
from db import execute, get_db, query_all, query_one

# =====================================================================
# Dashboard
# =====================================================================
BADGES = {"Stockout risk": "danger", "Excess stock": "info", "Healthy": "success"}

def units_sold(days_from, days_to):
    """Units sold per product between days_from and days_to days ago, as {product_id: units}."""
    rows = query_all("""
        SELECT product_id, SUM(quantity) AS units
        FROM sales
        WHERE sold_at >  DATE_SUB(NOW(), INTERVAL %s DAY)
          AND sold_at <= DATE_SUB(NOW(), INTERVAL %s DAY)
        GROUP BY product_id
    """, (days_from, days_to))
    return {r["product_id"]: int(r["units"]) for r in rows}


def stock_on_order():
    """Units on open purchase orders per product, as {product_id: units}."""
    rows = query_all("""
        SELECT product_id, SUM(quantity) AS units
        FROM purchase_orders
        WHERE status <> 'Delivered'
        GROUP BY product_id
    """)
    return {r["product_id"]: int(r["units"]) for r in rows}


def product_metrics():
    """Every product with its sales and the supply_chain.py numbers."""
    products = query_all("""
        SELECT p.id, p.sku, p.name, p.price, p.stock, p.lead_time_days,
               p.demand_std_dev, p.supplier_id, s.name AS supplier
        FROM products p
        JOIN suppliers s ON s.id = p.supplier_id
        ORDER BY p.sku
    """)
    this_week = units_sold(7, 0)
    last_week = units_sold(14, 7)
    on_order = stock_on_order()
    for p in products:
        p["price"] = float(p["price"])
        p["sold_7"] = this_week.get(p["id"], 0)
        p["sold_prev_7"] = last_week.get(p["id"], 0)
        p["on_order"] = on_order.get(p["id"], 0)
        p["change"] = sc.percent_change(p["sold_7"], p["sold_prev_7"])
        p["daily_demand"] = sc.average_daily_demand(p["sold_7"])
        p["cover_days"] = sc.days_of_cover(p["stock"], p["on_order"], p["daily_demand"])
        p["status"] = sc.alert_status(p["cover_days"], p["lead_time_days"])
        p["severity"] = sc.alert_severity(p["status"], p["cover_days"], p["lead_time_days"])
        p["badge"] = BADGES[p["status"]]
        p["safety_stock"] = sc.safety_stock(float(p["demand_std_dev"]), p["lead_time_days"])
        p["reorder_point"] = sc.reorder_point(p["daily_demand"], p["lead_time_days"], p["safety_stock"])
        p["needs_reorder"] = sc.needs_reorder(p["stock"], p["on_order"], p["reorder_point"])
    return products

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