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


# ---------------------------------------------------------------------
# Alerts and forecasts
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Recommendations and purchase orders
# ---------------------------------------------------------------------