#Python supply chain model calculations

import math

# Section 1: Sample data ----------------------------------------------------
#Variables:
# units_last_7_days
# units_previous_7_days
# in_stock
# on_order
# lead_time_days
# demand_std_dev
# price

PRODUCTS = [
    {"sku": "DT-1001", "name": "Denim Jacket", "units_last_7_days": 380,
     "units_previous_7_days": 330, "in_stock": 270, "on_order": 0,
     "lead_time_days": 18, "demand_std_dev": 12, "price": 899},
    {"sku": "DT-1002", "name": "Graphic Tee", "units_last_7_days": 392,
     "units_previous_7_days": 385, "in_stock": 840, "on_order": 600,
     "lead_time_days": 10, "demand_std_dev": 10, "price": 249},
    {"sku": "DT-1003", "name": "Cargo Pants", "units_last_7_days": 248,
     "units_previous_7_days": 196, "in_stock": 710, "on_order": 500,
     "lead_time_days": 35, "demand_std_dev": 9, "price": 599},
    {"sku": "DT-1004", "name": "Ribbed Knit Top", "units_last_7_days": 168,
     "units_previous_7_days": 208, "in_stock": 1490, "on_order": 0,
     "lead_time_days": 14, "demand_std_dev": 6, "price": 329},
    {"sku": "DT-1005", "name": "Oversized Hoodie", "units_last_7_days": 266,
     "units_previous_7_days": 280, "in_stock": 1140, "on_order": 300,
     "lead_time_days": 10, "demand_std_dev": 8, "price": 549},
    {"sku": "DT-1006", "name": "Wide-Leg Jeans", "units_last_7_days": 245,
     "units_previous_7_days": 231, "in_stock": 840, "on_order": 400,
     "lead_time_days": 18, "demand_std_dev": 8, "price": 699},
    {"sku": "DT-1007", "name": "Puffer Vest", "units_last_7_days": 126,
     "units_previous_7_days": 156, "in_stock": 1440, "on_order": 0,
     "lead_time_days": 35, "demand_std_dev": 5, "price": 649},
    {"sku": "DT-1008", "name": "Basic Crop Top", "units_last_7_days": 357,
     "units_previous_7_days": 340, "in_stock": 460, "on_order": 0,
     "lead_time_days": 10, "demand_std_dev": 11, "price": 179},
]

# Denim Jacket units sold per week
# weeks starting 17 Aug, 24 Aug, 31 Aug, 7 Sep, 14 Sep, 21 Sep
DENIM_WEEKLY_SALES = [210, 225, 245, 282, 330, 380]
