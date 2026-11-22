import logging
import os

from datetime import date

from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)

import db
import models
from api import api
from config import CONFIGS

app = Flask(__name__)
app.config.from_object(CONFIGS[os.getenv("APP_ENV", "development")])
db.init_app(app)
app.register_blueprint(api)

#Warnings and errors are written to app.log with their time
logging.basicConfig(filename="app.log", level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

#One handler for 400, 404 and 500 errors, and it answers with JSON.
@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_error(error):
    app.logger.warning("%s on %s", error.code, request.path)
    return jsonify(error=error.name, message=error.description), error.code


# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------
@app.route("/")
def dashboard():
    return render_template("dashboard.html", stats=models.dashboard_stats())

# ---------------------------------------------------------------------
# Sales and inventory
# ---------------------------------------------------------------------


@app.route("/sales", methods=["GET", "POST"])
def sales_inventory():
    """Show current inventory and handle sales submitted through the form."""
    if request.method == "POST":
        try:
            product_id = int(request.form.get("product_id", ""))
            quantity = int(request.form.get("quantity", ""))
        except ValueError:
            flash("Could not save sale: select a product and enter the quantity as a whole number.", "error")
            return redirect(url_for("sales_inventory"))
        success, message = models.record_sale(
            product_id, quantity, request.form.get("channel", "")
        )
        flash(message, "success" if success else "error")
        return redirect(url_for("sales_inventory"))

    return render_template(
        "sales_inventory.html", products=models.product_metrics()
    )


# ---------------------------------------------------------------------
# Sign in, alerts and forecasts
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = models.check_login(request.form.get("email", "").strip().lower(),
                                  request.form.get("password", ""))
        if user is None:
            flash("Wrong email address or password.", "error")
            return redirect(url_for("login"))
        session["role"] = user["role"]
        session["supplier_id"] = user["supplier_id"]
        session["name"] = user["supplier"] or "Buyer"
        flash(f"Signed in as {session['name']}.", "success")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))

@app.route("/alerts")
def alerts():
    return render_template("alerts.html",
    stockout=models.list_alerts("Stockout risk"),
    excess=models.list_alerts("Excess stock"))

@app.route("/forecasts")
def forecasts():
    return render_template("forecasts.html", forecasts=models.next_week_forecasts(),
                           weeks=models.forecast_vs_actual(1))


# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Orders and supplier portal
# ---------------------------------------------------------------------


@app.route("/orders", methods=["GET", "POST"])
def orders():
    """This shows the reorder recommendations, and creates a purchase order when one is approved."""
    if request.method == "POST":
        try:
            # if the field is empty or not a whole number, int() would give an error so we deal with it with 'except'
            product_id = int(request.form.get("product_id", ""))
            quantity = int(request.form.get("quantity", ""))
        except ValueError:
            flash("Please select a product and enter a whole-number quantity.", "error")
            return redirect(url_for("orders"))
        ok, message = models.create_purchase_order(product_id, quantity,
                                                   request.form.get("reason", "").strip())
        flash(message, "success" if ok else "error")
        return redirect(url_for("orders"))
    return render_template("orders.html", recommendations=models.recommendations())


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])