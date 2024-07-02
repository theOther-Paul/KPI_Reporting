"""
@package docstring

This package is responsible with calculating the kpi needed for the reports

"""

import pandas as pd
from . import file_ops
from . import consolidate


def get_percentage(total, margin):
    if total == 0:
        return float(0)
    return round((margin / total) * 100, 2)


def calculate_gap_percentage(val1, val2):
    return round(100 * (abs(val1 - val2) / ((val1 + val2) / 2)), 2)


def calculate_gap_value(val1, val2):
    return abs(val1 - val2)


class EmployeeAnalytics:
    def __init__(self, df, cval):
        self.df = df
        self.cval = cval

    def get_women_combo(self):
        return self.df.loc[
            (self.df["department"] == self.cval) & (self.df["gender"] == "Female"),
            "employee_id",
        ].count()

    def get_woman_lm(self):
        return self.df.loc[
            (self.df["pay_grade"].isin(["G34", "G35", "G36"]))
            & (self.df["department"] == self.cval)
            & (self.df["gender"] == "Female"),
            "employee_id",
        ].count()

    def get_woman_um(
        self,
    ):
        return self.df.loc[
            (self.df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
            & (self.df["department"] == self.cval)
            & (self.df["gender"] == "Female"),
            "employee_id",
        ].count()

    def get_total_employees_combo(self):
        return self.df.loc[self.df["department"] == self.cval, "employee_id"].count()

    def get_total_employees_lm(self):
        return self.df.loc[
            (self.df["pay_grade"].isin(["G34", "G35", "G36"]))
            & (self.df["department"] == self.cval),
            "employee_id",
        ].count()

    def get_total_employees_um(self):
        return self.df.loc[
            (self.df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
            & (self.df["department"] == self.cval),
            "employee_id",
        ].count()

    def form_df(self):
        management_types = ["LM", "UM"]
        total_employees = [
            self.get_total_employees_lm(),
            self.get_total_employees_um(),
        ]
        women_employees = [self.get_woman_lm(), self.get_woman_um()]
        ambition = "45%"

        gap_percentages = [
            calculate_gap_percentage(
                get_percentage(total_employees[0], women_employees[0]), 45
            ),
            calculate_gap_percentage(
                get_percentage(total_employees[1], women_employees[1]), 45
            ),
        ]

        gap_numbers = [
            calculate_gap_value(women_employees[0], total_employees[0]),
            calculate_gap_value(women_employees[1], total_employees[1]),
        ]

        data = {
            "Management": management_types,
            "Total Employees": total_employees,
            "From which Women": women_employees,
            "Ambition": [ambition, ambition],
            "Gap %": gap_percentages,
            "Gap #": gap_numbers,
        }

        return pd.DataFrame(data=data)
