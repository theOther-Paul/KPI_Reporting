"""
@package docstring

This package is responsible with every function tahat calculates chunks of data or manipulates numbers in a complex way

"""

import numpy as np
import pandas as pd


def get_percentage(total, margin):
    return float(0) if total == 0 else round((margin / total) * 100, 2)


def calculate_gap_percentage(val1, val2):
    return round(100 * (abs(val1 - val2) / ((val1 + val2) / 2)), 2)


def calculate_gap_value(val1, val2):
    return abs(val1 - val2)
