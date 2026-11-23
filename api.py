"""JSON routes, all starting with /api."""
from flask import Blueprint, jsonify, request

import models

api = Blueprint("api", __name__, url_prefix="/api")

# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------
@api.route("/kpis")
def kpis():
    stats = models.dashboard_stats()
    stats.pop("products")
    return jsonify(stats)

# ---------------------------------------------------------------------
# Products and sales
# ---------------------------------------------------------------------


@api.route("/products")
def products():
    """Return a page of products, optionally filtered by name."""
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    size = request.args.get("size", 10, type=int)
    if page < 1 or size < 1 or size > 100:
        return jsonify(
            error="Bad Request",
            message="Could not list products: page must be at least 1 and size must be between 1 and 100."
        ), 400
    return jsonify(page=page, size=size, items=models.list_products(search, page, size))


@api.route("/products/<int:product_id>")
def product(product_id):
    """Return the requested product or a clear message if it is missing."""
    product_details = models.get_product(product_id)
    if product_details is None:
        return jsonify(
            error="Not Found",
            message="Could not find the requested product."
        ), 404
    return jsonify(product_details)


@api.route("/products", methods=["POST"])
def product_create():
    """Create a product from JSON and return the result with its status code."""
    success, message = models.create_product(request.get_json(silent=True) or {})
    if not success:
        return jsonify(error="Bad Request", message=message), 400
    return jsonify(message=message), 201


@api.route("/sales", methods=["POST"])
def sale_create():
    """Read sale details from JSON and return the result of recording the sale."""
    sale_data = request.get_json(silent=True) or {}
    try:
        product_id = int(sale_data.get("product_id", ""))
        quantity = int(sale_data.get("quantity", ""))
    except (ValueError, TypeError):
        return jsonify(
            error="Bad Request",
            message="Could not record sale: product_id and quantity must be whole numbers."
        ), 400

    success, message = models.record_sale(
        product_id, quantity, sale_data.get("channel", "")
    )
    if not success:
        return jsonify(error="Bad Request", message=message), 400
    return jsonify(message=message), 201


# ---------------------------------------------------------------------
# Alerts and forecasts

@api.route("/alerts")
def alerts():
    return jsonify(stockout=models.list_alerts("Stockout risk"),
                   excess=models.list_alerts("Excess stock"))

@api.route("/forecasts")
def forecasts():
    return jsonify(models.next_week_forecasts())


# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Recommendations and purchase orders
# ---------------------------------------------------------------------


@api.route("/recommendations")
def recommendations():
    """This returns the products the model says to reorder, with the recommended quantities (as JSON)."""
    return jsonify(models.recommendations())


@api.route("/purchase-orders")
def purchase_orders():
    """This returns the purchase orders as JSON, adding '?status=' to only get orders with that status."""
    status = request.args.get("status", "").strip()
    return jsonify(models.list_purchase_orders(status))