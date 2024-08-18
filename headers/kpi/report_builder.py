from email import header
from . import kpi_department as kdep
from . import kpi_market as kmkt
from . import movements as mv
import pandas as pd
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
        self.last_q = self.map_q()[0]
        self.actual_q = self.map_q()[1]
        self.last_df = self.split_by_snap()[0]
        self.actual_df = self.split_by_snap()[1]

    def _check_department_validity(self):
        if self.dpt not in self.dpt_list:
            raise ValueError(f"{self.dpt} not in {self.dpt_list}")

    def get_um_df(self, df):
        self._check_department_validity()
        return df.loc[
            (df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
            & (df["department"] == self.dpt),
            ["first_name", "last_name", "gender", "pay_grade"],
        ]

    def get_um_fem_df(self, df):
        self._check_department_validity()
        return df.loc[
            (df["pay_grade"].isin(["G37", "G38", "G39", "G40", "G41"]))
            & (df["department"] == self.dpt)
            & (df["gender"] == "Female"),
            ["first_name", "last_name", "gender", "pay_grade"],
        ]

    def get_um_fem_list(self, df):
        return self.get_um_fem_df(df).values.tolist()

    def get_um_list(self, df):
        return self.get_um_df(df).values.tolist()

    def get_lm_df(self, df):
        self._check_department_validity()
        return df.loc[
            (df["pay_grade"].isin(["G34", "G35", "G36"]))
            & (df["department"] == self.dpt),
            ["first_name", "last_name", "gender", "pay_grade"],
        ]

    def get_lm_list(self, df):
        return self.get_lm_df(df).values.tolist()

    def get_gender_split_um(self, df):
        analytics = kdep.EmployeeAnalytics(df, self.dpt)
        total = analytics.get_total_employees_um()
        fem = analytics.get_woman_um()
        proc = calculus.get_percentage(total, fem)

        return [int(total), int(fem), float(proc)]

    def get_gender_split_lm(self, df):
        analytics = kdep.EmployeeAnalytics(df, self.dpt)
        total = analytics.get_total_employees_lm()
        fem = analytics.get_woman_lm()
        proc = calculus.get_percentage(total, fem)

        return [int(total), int(fem), float(proc)]

    def build_report(self):
        rep_title = f"{self.last_q[0]} {self.last_q[1]} vs {self.actual_q[0]} {self.actual_q[1]} {self.dpt}.xlsx"
        rep_loc = os.path.join(os.getcwd(), "QvQ Files", rep_title)

        with xw.App() as rb:
            self._build_report(rb, rep_loc)

    def _build_report(self, rb, rep_loc):
        wb = rb.books.add()
        rb.display_alerts = False

        ws1 = wb.sheets.add(name="Gender Split per market")
        ws1["B2"].value = "Market Lists with gender %"
        ws1.range("B2:D2").merge()
        es.header_text_look(ws1, "A2:E2")

        threads = []
        results = {}

        def thread_function(key, method, *args):
            results[key] = method(*args)

        threads.append(
            threading.Thread(
                target=thread_function,
                args=(
                    "um_gen_df",
                    kdep.EmployeeAnalytics(
                        self.actual_df, self.dpt
                    ).get_market_UM_by_dpt,
                ),
            )
        )
        threads.append(
            threading.Thread(
                target=thread_function,
                args=(
                    "um_members",
                    kdep.EmployeeAnalytics(
                        self.actual_df, self.dpt
                    ).get_um_members_w_data,
                ),
            )
        )

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        es.write_dataframe_with_borders(ws1, "B4", results["um_gen_df"])

        ws1["B17"].value = "Upper Management members"
        ws1.range("B17:D17").merge()
        es.header2_text_look(ws1, "A17:E17")

        es.write_dataframe_with_borders(ws1, "B19", results["um_members"])

        # Precompute gender splits
        last_um_split = self.get_gender_split_um(self.last_df)
        actual_um_split = self.get_gender_split_um(self.actual_df)
        last_lm_split = self.get_gender_split_lm(self.last_df)
        actual_lm_split = self.get_gender_split_lm(self.actual_df)

        um_qvq_df = pd.DataFrame(
            {
                " ": [
                    f"{self.last_q[0]} {self.last_q[1]}",
                    f"{self.actual_q[0]} {self.actual_q[1]}",
                    "Progress",
                ],
                "Total": [
                    last_um_split[0],
                    actual_um_split[0],
                    calculus.compare_progress(last_um_split[0], actual_um_split[0]),
                ],
                "Women #": [
                    last_um_split[1],
                    actual_um_split[1],
                    calculus.compare_progress(last_um_split[1], actual_um_split[1]),
                ],
                "Women %": [
                    last_um_split[2],
                    actual_um_split[2],
                    calculus.get_percentage(last_um_split[2], actual_um_split[2]),
                ],
            }
        )

        es.write_dataframe_with_borders(ws1, "F4", um_qvq_df)

        lm_qvq_df = pd.DataFrame(
            {
                " ": [
                    f"{self.last_q[0]} {self.last_q[1]}",
                    f"{self.actual_q[0]} {self.actual_q[1]}",
                    "Progress",
                ],
                "Total": [
                    last_lm_split[0],
                    actual_lm_split[0],
                    calculus.compare_progress(last_lm_split[0], actual_lm_split[0]),
                ],
                "Women #": [
                    last_lm_split[1],
                    actual_lm_split[1],
                    calculus.compare_progress(last_lm_split[1], actual_lm_split[1]),
                ],
                "Women %": [
                    last_lm_split[2],
                    actual_lm_split[2],
                    calculus.get_percentage(last_lm_split[2], actual_lm_split[2]),
                ],
            }
        )

        es.write_dataframe_with_borders(ws1, "F9", lm_qvq_df)

        ws4 = wb.sheets.add(name="Movements")
        ws4["B2"].value = "Movement List"
        ws4.range("B2:D2").merge()
        es.header_text_look(ws4, "A2:E2")

        q_move = mv.EmployeeMovements(
            self.last_df, self.actual_df, self.dpt
        ).get_all_movements()
        ws4["B4"].options(pd.DataFrame, header=1, index=False, expand="Table").value = (
            q_move
        )
        es.write_dataframe_with_borders(ws4, "B4", q_move)

        summary_df = mv.EmployeeMovements(
            self.last_df, self.actual_df, self.dpt
        ).get_population_summary()

        es.write_dataframe_with_borders(ws4, "B20", summary_df)

        ws5 = wb.sheets.add(name="Active Population")
        ws5["C2"].value = "Active population for the current quarter"
        ws5.range("B2:E2").merge()
        es.header2_text_look(ws5, "B2:E2")

        current_population = kdep.EmployeeAnalytics(
            self.actual_df, self.dpt
        ).get_actual_population()

        es.write_dataframe_with_borders(ws5, "B4", current_population)

        ws6 = wb.sheets.add(name="Comments")
        ws6["B2"].value = "Please write your comments below, based on the table formula"
        ws6.range("B2:G2").merge()
        es.header_text_look(ws6, "B2:G2")

        com_df = pd.DataFrame(
            {
                " ": ["Example"],
                "employee_id": [2002],
                "employee_first_name": ["Smith"],
                "employee_last_name": ["Jane"],
                "Comments": ["Moved to Sales before May-2024"],
            }
        )

        es.write_dataframe_with_borders(ws6, "A4", com_df)

        if "Sheet1" in [sheet.name for sheet in wb.sheets]:
            wb.sheets["Sheet1"].delete()

        ws1.activate()

        wb.save(rep_loc)
        rb.display_alerts = True
        wb.close()
