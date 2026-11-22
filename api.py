"""JSON routes, all starting with /api."""
from flask import Blueprint, jsonify, request

import models

api = Blueprint("api", __name__, url_prefix="/api")

# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Products and sales
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Alerts and forecasts

@api.route("/alerts")
def alerts():
    return jsonify(stockout=models.list_alerts("Stockout risk"),
                   excess=models.list_alerts("Excess stock"))

# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Recommendations and purchase orders
# ---------------------------------------------------------------------