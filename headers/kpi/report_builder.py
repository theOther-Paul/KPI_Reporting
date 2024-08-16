from operator import index
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
from . import excel_styles as es


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

        rep_title = f"Q{last_q[1]} vs Q{actual_q[1]} {self.dpt}"

        rep_loc = os.path.join(os.getcwd(), "QvQ Files", rep_title)

        with xw.App() as rb:
            self._build_report(rb, rep_loc)

    def _build_report(self, rb, rep_loc):

        last_df = self.split_by_snap()[0]
        actual_df = self.split_by_snap()[1]

        wb = rb.books.add()
        rb.display_alerts = False
        # =======================================================================================

        ws1 = wb.sheets.add(name="Gender Split per market")

        ws1["B2"].value = "Market Lists with gender %"
        ws1.range("B2:D2").merge()
        es.header_text_look(ws1, "A2:E2")

        um_gen_df = kdep.EmployeeAnalytics(actual_df, self.dpt).get_market_UM_by_dpt()

        ws1["B4"].options(pd.DataFrame, header=1, index=False, expand="table").value = (
            um_gen_df
        )

        es.write_dataframe_with_borders(ws1, "B4", um_gen_df)

        ws1["B17"].value = "Upper Management members"
        ws1.range("B17:D17").merge()
        es.header2_text_look(ws1, "A17:E17")

        um_members = kdep.EmployeeAnalytics(actual_df, self.dpt).get_um_members_w_data()
        ws1["B19"].options(
            pd.DataFrame, header=1, index=False, expand="table"
        ).value = um_members

        es.write_dataframe_with_borders(ws1, "B19", um_members)

        um_qvq_data = [
            self.get_gender_split_um(last_df),
            self.get_gender_split_um(actual_df),
        ]

        qvq_columns = ["Previous Q", "Actual Q", "Progress"]

        um_qvq_df = pd.DataFrame(um_qvq_data, columns=qvq_columns)

        ws1["F3"].options(pd.DataFrame, header=1, index=False, expand="table").value = (
            um_qvq_df
        )
        es.write_dataframe_with_borders(ws1, "F3", um_qvq_df)

        lm_qvq_data = [
            self.get_gender_split_lm(last_df),
            self.get_gender_split_lm(actual_df),
        ]

        lm_qvq_df = pd.DataFrame(lm_qvq_data, columns=qvq_columns)

        ws1["F9"].options(pd.DataFrame, header=1, index=False, expand="table").value = (
            um_qvq_df
        )
        es.write_dataframe_with_borders(ws1, "F9", lm_qvq_df)

        # =======================================================================================

        ws2 = wb.sheets.add(name="Gender Split in Education")

        # =======================================================================================

        ws4 = wb.sheets.add(name="Movements")

        # =======================================================================================
        ws5 = wb.sheets.add(name="Actual Population")

        ws5["C2"].value = "Actual population for the current quarter"

        ws5.range("B2:D2").merge()
        es.header2_text_look(ws5, "B2:D2")

        current_population = kdep.EmployeeAnalytics(
            actual_df, self.dpt
        ).get_actual_population()

        ws5["B4"].options(pd.DataFrame, header=1, index=False, expand="table").value = (
            current_population
        )

        es.write_dataframe_with_borders(ws5, "B4", current_population)

        # =======================================================================================
        ws6 = wb.sheets.add(name="Comments")

        ws6["B2"].value = "Please write you comments below, based on the table formula"
        ws6.range("B2:G2").merge()
        es.header_text_look(ws6, "B2:G2")

        ws6["B4"].value = "employee_id"
        ws6["E4"].value = "first_name"
        ws6["F4"].value = "last_name"
        ws6["G4"].value = "Comments"

        # TODO: Fix this border
        es.header3_text_look(ws6, "B4:G4")
        ws6.range("B4:G4").api.Borders.LineStyle = 1
        ws6.range("B4:G4").api.Borders.Weight = 2

        ws6["A5"].value = "Example"
        ws6["B5"].value = "2002"
        ws6["E5"].value = "Smith"
        ws6["F5"].value = "Jane"
        ws6["G5"].value = "Moved to Sales before May-2024"

        if "Sheet1" in [sheet.name for sheet in wb.sheets]:
            wb.sheets["Sheet1"].delete()

        ws1.activate()

        wb.save(f"{rep_loc}.xlsx")
        wb.close()
