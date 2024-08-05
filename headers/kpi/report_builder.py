from . import kpi_department as kdep
from . import kpi_market as kmkt
import pandas as pd
import numpy as np
import os
from . import calculus
from .. import file_ops as fo
import xlwings as xw
import threading
from .. import consolidate as CS


class BuildReport(fo.FilePrep):
    def __init__(self, dpt: str) -> None:
        super().__init__()
        self.dpt = dpt
        self.dpt_list = CS.GatherData().form_combo("department")

    def get_um_df(self, df):
        if self.dpt not in self.dpt_list:
            raise ValueError(f"{self.dpt} not in {self.dpt_list}")
        else:
            return df.loc[
                (df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
                & (df["department"] == self.dpt),
                ["first_name", "last_name", "gender", "pay_grade"],
            ]

    def get_um_fem_df(self, df):
        if self.dpt not in self.dpt_list:
            raise ValueError(f"{self.dpt} not in {self.dpt_list}")
        else:
            return df.loc[
                (
                    (df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
                    & (df["department"] == self.dpt)
                    & (df["gender"] == "Female")
                ),
                ["first_name", "last_name", "gender", "pay_grade"],
            ]

    def get_um_fem_list(self, df):
        return self.get_um_fem_df(df).values.tolist()

    def get_um_list(self, df):
        return self.get_um_df(df).values.tolist()

    def get_lm_df(self, df):
        if self.dpt not in self.dpt_list:
            raise ValueError(f"{self.dpt} not in {self.dpt_list}")
        else:
            return df.loc[
                (df["pay_grade"].isin(["G34", "G35", "G36"]))
                & (df["department"] == self.dpt),
                ["first_name", "last_name", "gender", "pay_grade"],
            ]

    def get_lm_list(self, df) -> list:
        return self.get_lm_df(df).values.tolist()

    def get_gender_split_um(self, df):
        total = kdep.EmployeeAnalytics(df, self.dpt).get_total_employees_um()
        fem = kdep.EmployeeAnalytics(df, self.dpt).get_woman_um()
        proc = calculus.get_percentage(total, fem)

        return [int(total), int(fem), float(proc)]

    def get_gender_split_lm(self, df):
        total = kdep.EmployeeAnalytics(df, self.dpt).get_total_employees_lm()
        fem = kdep.EmployeeAnalytics(df, self.dpt).get_woman_lm()
        proc = calculus.get_percentage(total, fem)

        return [int(total), int(fem), float(proc)]

    def build_report(self):
        last_q = self.map_q()[0]
        actual_q = self.map_q()[1]

        rep_title = f"Quarterly Reports {last_q[0]} {last_q[1]} vs. {actual_q[0]} {actual_q[1]} for {self.dpt}"

        rep_loc = f"{os.getcwd()}\\QvQ Files\\{rep_title}.xlsx"

        with xw.App() as rb:
            wb = rb.books(rep_loc)

            ws1 = wb.sheets("Gender Split in Management per market")

            ws2 = wb.sheets("Gender Split in Education")

            ws3 = wb.sheets("Ethnic Distribution per Markets")

            ws4 = wb.sheets("Movements")

            ws5 = wb.sheets("Population")

            ws6 = wb.sheets("Comments")
