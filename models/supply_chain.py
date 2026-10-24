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

# Section 2: Logic for reordering (when and how much to order)
# Just a note: Order quantity is calculated based on sales rates each week, EOQ used only for min order size.
ORDERING_COST = 50
HOLDING_COST_RATE = 0.25        # 25% of value per year
REVIEW_PERIOD_DAYS = 7
Z_95 = 1.65                     # z-score for 95% service

def safety_stock(demand_std_dev, lead_time_days):
    """Extra stock held in case demand is higher than average.

        SS = z x standard deviation of daily demand x square root of lead time

    z = 1.65 gives a 95% assurance that we won't run out while waiting for delivery.
    """
    return Z_95 * demand_std_dev * math.sqrt(lead_time_days)

def reorder_point(daily_demand, lead_time_days, safety_stock_units):
    """The stock level when a new order must be made.

        ROP = daily demand x lead time + safety stock
    """
    return daily_demand * lead_time_days + safety_stock_units

def needs_reorder(in_stock, on_order, reorder_point_units):
    """Need to reorder if total stock (including what is on order) has fallen to the ROP."""
    return in_stock + on_order <= reorder_point_units