#Python supply chain model calculations

import math

# Section 1: Sample data ----------------------------------------------------

PRODUCTS = [
    {"sku": "DT-1001", "name": "Light Blue Oversized Denim Jacket", "units_last_7_days": 380,
     "units_previous_7_days": 330, "in_stock": 270, "on_order": 0,
     "lead_time_days": 18, "demand_std_dev": 12, "price": 899},
    {"sku": "DT-1002", "name": "Black Cotton Logo T-Shirt", "units_last_7_days": 392,
     "units_previous_7_days": 385, "in_stock": 840, "on_order": 600,
     "lead_time_days": 10, "demand_std_dev": 10, "price": 249},
    {"sku": "DT-1003", "name": "Olive Green Relaxed-Fit Cargo Pants", "units_last_7_days": 248,
     "units_previous_7_days": 196, "in_stock": 710, "on_order": 500,
     "lead_time_days": 35, "demand_std_dev": 9, "price": 599},
    {"sku": "DT-1004", "name": "Cream Long-Sleeve Ribbed Knit Top", "units_last_7_days": 168,
     "units_previous_7_days": 208, "in_stock": 1490, "on_order": 0,
     "lead_time_days": 14, "demand_std_dev": 6, "price": 329},
    {"sku": "DT-1005", "name": "Charcoal Pullover Hoodie", "units_last_7_days": 266,
     "units_previous_7_days": 280, "in_stock": 1140, "on_order": 300,
     "lead_time_days": 10, "demand_std_dev": 8, "price": 549},
    {"sku": "DT-1006", "name": "Dark Blue High-Waisted Wide-Leg Jeans", "units_last_7_days": 245,
     "units_previous_7_days": 231, "in_stock": 840, "on_order": 400,
     "lead_time_days": 18, "demand_std_dev": 8, "price": 699},
    {"sku": "DT-1007", "name": "Black Quilted Puffer Vest", "units_last_7_days": 126,
     "units_previous_7_days": 156, "in_stock": 1440, "on_order": 0,
     "lead_time_days": 35, "demand_std_dev": 5, "price": 649},
    {"sku": "DT-1008", "name": "White Cotton Cropped T-Shirt", "units_last_7_days": 357,
     "units_previous_7_days": 340, "in_stock": 460, "on_order": 0,
     "lead_time_days": 10, "demand_std_dev": 11, "price": 179},
]

# Denim Jacket units sold per week
DENIM_WEEKLY_SALES = [210, 225, 245, 282, 330, 380]

# Section 2: Logic for reordering (when and how much to order)
# NB: Order quantity -> Based on sales rates each week; EOQ -> min order size.
ORDERING_COST = 50
HOLDING_COST_RATE = 0.25        
REVIEW_PERIOD_DAYS = 7
Z_95 = 1.65                     # z-score -> 95% service

def safety_stock(demand_std_dev, lead_time_days):
    """Extra stock for high demand.
    z = 1.65 -> 95% service rate
    """
    return Z_95 * demand_std_dev * math.sqrt(lead_time_days)

def reorder_point(daily_demand, lead_time_days, safety_stock_units):
    """New order must be made at this point.
       ROP = daily demand x lead time + SS
    """
    return daily_demand * lead_time_days + safety_stock_units

def needs_reorder(in_stock, on_order, reorder_point_units):
    """Total stock (including what is on order) less than ROP."""
    return in_stock + on_order <= reorder_point_units

def calculate_eoq(demand, order_cost, hold_cost):
    """Order size with the lowest total cost.
       EOQ = square root(2 x D x S / H)
    """
    return math.sqrt((2 * demand * order_cost) / hold_cost)


def total_annual_cost(demand, order_cost, hold_cost, order_qty):
    """Ordering cost + holding cost for the year
       Total = (D / Q) x S + (Q / 2) x H
    """
    ordering = (demand / order_qty) * order_cost
    holding = (order_qty / 2) * hold_cost
    return ordering + holding


def recommended_order_quantity(daily_demand, lead_time_days, safety_stock_units,
                               in_stock, on_order, eoq):
    """Number of units to order, rounded up to a multiple of 10.
   target covers demand until the NEXT weekly order would arrive.
    Returns 0 if there is already enough stock.
    """
    target = daily_demand * (lead_time_days + REVIEW_PERIOD_DAYS) + safety_stock_units
    shortfall = target - (in_stock + on_order)
    if shortfall <= 0:
        return 0
    quantity = max(shortfall, eoq)
    return math.ceil(quantity / 10) * 10


# Section 3: Stock alerts 

EXCESS_WEEKS = 6        
HIGH_EXCESS_WEEKS = 9    


def average_daily_demand(units_last_7_days):
    """Average units sold per day over the last week.

        daily demand = units sold in 7 days / 7

    Example: 357 units / 7 = 51 units per day
    """
    return units_last_7_days / 7


def days_of_cover(in_stock, on_order, daily_demand):
    """How many days the stock will last at the current sales rate.

        days of cover = (in stock + on order) / daily demand

    Stock on order is counted because it will arrive.
    Example: (840 + 600) / 56 = 25.7 days
    If nothing is selling we can't divide by zero, so return 999
    (meaning: the stock lasts a very long time).
    """
    if daily_demand <= 0:
        return 999
    return (in_stock + on_order) / daily_demand


def weeks_of_cover(cover_days):
    """Convert days of cover to weeks. Example: 80 days / 7 = 11.4 weeks"""
    return cover_days / 7


def alert_status(cover_days, lead_time_days):
    """Classify a product as "Stockout risk", "Excess stock" or "Healthy"."""
    if cover_days < lead_time_days:
        return "Stockout risk"
    elif weeks_of_cover(cover_days) > EXCESS_WEEKS:
        return "Excess stock"
    else:
        return "Healthy"


def alert_severity(status, cover_days, lead_time_days):
    """How urgent an alert is: "High", "Medium", or "" for healthy products.

    Stockout risk is High if the stock lasts less than HALF the lead time.
    Excess stock is High if there are more than 9 weeks of cover.
    """
    if status == "Stockout risk":
        if cover_days < lead_time_days / 2:
            return "High"
        else:
            return "Medium"
    elif status == "Excess stock":
        if weeks_of_cover(cover_days) > HIGH_EXCESS_WEEKS:
            return "High"
        else:
            return "Medium"
    else:
        return ""

    
# Section 4: Forecasting

TREND_THRESHOLD = 10  # Percentage change threshold for trend labels


def percent_change(current, previous):
    """Percentage change between two weeks of unit sales.
    If the previous week had 0 sales, then return 0.
    """
    if previous == 0:
        return 0
    return (current - previous) / previous * 100


def trend_forecast(this_week, last_week):
    """Forecast next week's sales in units and forecasts cannot be negative.
    """
    forecast = this_week + (this_week - last_week)
    if forecast < 0:
        return 0
    return forecast


def trend_label(forecast, this_week):
    """Determine if the forecast is rising by 10% or more, falling by 10% or more, or stable compared to this week's sales.
    """
    change = percent_change(forecast, this_week)
    if change >= TREND_THRESHOLD:
        return "Rising"
    elif change <= -TREND_THRESHOLD:
        return "Falling"
    else:
        return "Stable"


def forecast_error_percent(forecast, actual):
    """Calculate if the forecast was above or below actual sales, as a percentage.
    If the actual is 0 then return 0.
    """
    if actual == 0:
        return 0
    return (forecast - actual) / actual * 100


def mape(forecasts, actuals):
    """Average absolute percentage error for matching lists of sales units.
    This would assume equal list lengths and an empty list returns 0.
    """
    if len(forecasts) == 0:
        return 0
    total = 0
    for i in range(len(forecasts)):
        total = total + abs(forecast_error_percent(forecasts[i], actuals[i]))
    return total / len(forecasts)


