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


def compare_progress(q_last, q_act):
    """
    The function `compare_progress` compares two quantities and returns the difference between them with
    appropriate signs.
    
    :param q_last: The `q_last` parameter represents the last recorded progress value
    :param q_act: The `q_act` parameter represents the actual progress made in a certain task or goal
    :return: The function `compare_progress` compares two quantities `q_last` and `q_act` and returns
    the difference between them. If `q_act` is greater than `q_last`, it returns the positive difference
    as a string with a plus sign (e.g., "+5"). If `q_last` is greater than `q_act`, it returns the
    negative difference. If they are equal, it
    """
    if q_last < q_act:
        return f"+{q_act-q_last}"
    elif q_act < q_last:
        return q_act - q_last
    else:
        return "0"


def std_mt_df():
    return pd.DataFrame(columns=["This Table", "has", "no data"])
