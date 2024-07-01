"""
@package docstring:
This package is responsible with calculating the kpi needed for the reports.

TODO: update documentation
"""

import pandas as pd
from . import file_ops
from . import consolidate


def get_women_combo(df, cval):
    return df.loc[
        (df["department"] == cval) & (df["gender"] == "Female"), "employee_id"
    ].count()


def get_total_employees_combo(df, cval):
    return df.loc[df["department"] == cval, "employee_id"].count()


def get_percentage(total, margin):
    if total == 0:
        return float(0)
    return round((margin / total) * 100, 2)


def calculate_gap_percentage(val1, val2):
    return 100 * (abs(val1 - val2) / ((val1 + val2) / 2))


def calculate_gap_value(val1, val2):
    return abs(val1 - val2)


def form_df(df, cval):
    d = {
        "Total Employees": [get_total_employees_combo(df, cval)],
        "From which Women": [get_women_combo(df, cval)],
        "Ambition": ["45%"],
        "Gap %": [
            calculate_gap_percentage(
                get_percentage(
                    get_total_employees_combo(df, cval), get_women_combo(df, cval)
                ),
                45,
            )
        ],
        "Gap #": [
            calculate_gap_value(
                get_women_combo(df, cval), get_total_employees_combo(df, cval)
            )
        ],
    }
    return pd.DataFrame(data=d)
