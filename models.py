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


# =====================================================================
# Products and sales
# =====================================================================


# =====================================================================
# Alerts, forecasts and sign-in
# =====================================================================


# =====================================================================
# Recommendations and purchase orders
# =====================================================================