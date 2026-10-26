"""
Individual tests for models/supply_chain.py.

We worked out each answer by hand first, which we show in the comment above it, and then check that it is working correctly.

This is run from the folder:   python -m pytest
"""

import models.supply_chain as sc

# Testing Section 2

def test_safety_stock():
    # 1.65 x 12 x square root of 18 = 1.65 x 12 x 4.2426 = 84.0
    assert round(sc.safety_stock(12, 18), 1) == 84.0


def test_reorder_point():
    # 50 x 10 + 30 = 530
    assert sc.reorder_point(50, 10, 30) == 530


def test_needs_reorder():
    # 270 + 0 = 270 -> below 1061 -> reorder
    assert sc.needs_reorder(270, 0, 1061) == True
    # 840 + 600 = 1440 -> above 600 -> no reorder
    assert sc.needs_reorder(840, 600, 600) == False

def test_eoq_tutorial_example():
    # From the EOQ tut: square root of (2 x 12000 x 50 / 2) = 774.6
    assert round(sc.calculate_eoq(12000, 50, 2), 1) == 774.6


def test_total_annual_cost_tutorial_example():
    # From the tut: (12000 / 774.6) x 50 + (774.6 / 2) x 2 = 1549.19
    eoq = sc.calculate_eoq(12000, 50, 2)
    assert round(sc.total_annual_cost(12000, 50, 2, eoq), 2) == 1549.19


def test_recommended_order_quantity():
    # target = 50 x (10 + 7) + 30 = 880 ; shortfall = 880 - 100 = 780 -> 780
    assert sc.recommended_order_quantity(50, 10, 30, 100, 0, 0) == 780
    # same, but EOQ is 900, which is bigger than 780 -> 900
    assert sc.recommended_order_quantity(50, 10, 30, 100, 0, 900) == 900
    # shortfall = 880 - 105 = 775 -> rounded up to 780
    assert sc.recommended_order_quantity(50, 10, 30, 105, 0, 0) == 780
    # 1000 in stock is above the target of 880 -> order nothing
    assert sc.recommended_order_quantity(50, 10, 30, 1000, 0, 0) == 0    


    # Section 3 tests: Stock alerts
def test_average_daily_demand():
    assert sc.average_daily_demand(357) == 51


def test_days_of_cover():
    assert round(sc.days_of_cover(840, 600, 56), 2) == 25.71
    assert sc.days_of_cover(100, 0, 0) == 999


def test_alert_status():
    assert sc.alert_status(5, 18) == "Stockout risk"
    assert sc.alert_status(80, 35) == "Excess stock"
    assert sc.alert_status(26, 10) == "Healthy"


def test_alert_severity():
    assert sc.alert_severity("Stockout risk", 5, 18) == "High"
    assert sc.alert_severity("Stockout risk", 9, 10) == "Medium"
    assert sc.alert_severity("Excess stock", 80, 35) == "High"
    assert sc.alert_severity("Excess stock", 62, 14) == "Medium"
