"""
@package docstring

This package is responsible with calculating the kpi needed for the reports

"""

import pandas as pd
from .. import file_ops
from .. import consolidate
from . import calculus


class EmployeeAnalytics:
    def __init__(self, df, cval):
        self.df = df
        self.cval = cval

    def get_women_combo(self):
        """
        The function `get_women_combo` returns the count of female employees in a specific department.
        :return: The `get_women_combo` method is returning the count of female employees in the DataFrame
        `df` where the department matches the value stored in `self.cval`.
        """
        return self.df.loc[
            (self.df["department"] == self.cval) & (self.df["gender"] == "Female"),
            "employee_id",
        ].count()

    def get_woman_lm(self):
        """
        The function `get_woman_lm` returns the count of female employees with pay grades G34, G35, or G36
        in a specific department.
        :return: The `get_woman_lm` method is returning the count of female employees with pay grades G34,
        G35, or G36 in the specified department (`self.cval`).
        """
        return self.df.loc[
            (self.df["pay_grade"].isin(["G34", "G35", "G36"]))
            & (self.df["department"] == self.cval)
            & (self.df["gender"] == "Female"),
            "employee_id",
        ].count()

    def get_woman_um(self):
        """
        This Python function returns the count of female employees in a specific department with pay
        grades G37 to G41.
        :return: The `get_woman_um` method is returning the count of female employees in the DataFrame
        `self.df` where the pay grade is in the specified list ["G37", "G38", "G39", "G40", "G41"], the
        department matches the value stored in `self.cval`, and the gender is "Female".
        """
        return self.df.loc[
            (self.df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
            & (self.df["department"] == self.cval)
            & (self.df["gender"] == "Female"),
            "employee_id",
        ].count()

    def get_total_employees_combo(self):
        """
        This function returns the total number of employees in a specific department based on the provided
        department value.
        :return: The `get_total_employees_combo` method is returning the total count of employees in the
        DataFrame `df` where the department column matches the value stored in `cval`.
        """
        return self.df.loc[self.df["department"] == self.cval, "employee_id"].count()

    def get_total_employees_lm(self):
        """
        The function `get_total_employees_lm` returns the count of employees with pay grades G34, G35, or
        G36 in a specific department.
        :return: The `get_total_employees_lm` method is returning the count of employees whose pay grade is
        in ["G34", "G35", "G36"] and who belong to the department specified by `self.cval`.
        """
        return self.df.loc[
            (self.df["pay_grade"].isin(["G34", "G35", "G36"]))
            & (self.df["department"] == self.cval),
            "employee_id",
        ].count()

    def get_total_employees_um(self):
        """
        The function `get_total_employees_um` returns the count of employees with specific pay grades in a
        particular department.
        :return: The `get_total_employees_um` method is returning the count of employees who belong to pay
        grades G37, G38, G39, G40, or G41 and are in the department specified by `self.cval`.
        """
        return self.df.loc[
            (self.df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
            & (self.df["department"] == self.cval),
            "employee_id",
        ].count()

    def form_df(self):
        """
        The `form_df` function calculates gender pay gap percentages and values for different management
        types.
        """
        management_types = ["LM", "UM"]
        total_employees = [
            self.get_total_employees_lm(),
            self.get_total_employees_um(),
        ]
        women_employees = [self.get_woman_lm(), self.get_woman_um()]
        ambition = "45%"

        gap_percentages = [
            calculus.calculate_gap_percentage(
                calculus.get_percentage(total_employees[0], women_employees[0]), 45
            ),
            calculus.calculate_gap_percentage(
                calculus.get_percentage(total_employees[1], women_employees[1]), 45
            ),
        ]

        gap_numbers = [
            calculus.calculate_gap_value(women_employees[0], total_employees[0]),
            calculus.calculate_gap_value(women_employees[1], total_employees[1]),
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
