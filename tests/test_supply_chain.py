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