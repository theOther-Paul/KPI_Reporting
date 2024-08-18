import pandas as pd


class EmployeeMovements:
    def __init__(
        self,
        last_q_df,
        actual_q_df,
        department_col="department",
        employee_id_col="employee_id",
    ):
        self.last_q_df = last_q_df
        self.actual_q_df = actual_q_df
        self.department_col = department_col
        self.employee_id_col = employee_id_col

        # Create sets of employee IDs for faster lookup
        self.last_q_ids = set(self.last_q_df[self.employee_id_col])
        self.actual_q_ids = set(self.actual_q_df[self.employee_id_col])

    def _merge_dataframes(self, df1, df2, on_cols, how="outer"):
        return pd.merge(df1, df2, on=on_cols, how=how, suffixes=("_last", "_current"))

    def get_terminations(self):
        terminated_ids = self.last_q_ids - self.actual_q_ids
        terminations = self.last_q_df[
            self.last_q_df[self.employee_id_col].isin(terminated_ids)
        ]
        terminations["reason"] = "Termination"
        return terminations

    def get_hires(self):
        hired_ids = self.actual_q_ids - self.last_q_ids
        hires = self.actual_q_df[self.actual_q_df[self.employee_id_col].isin(hired_ids)]
        hires["reason"] = "Hire"
        return hires

    def get_lateral_movements_in(self, department):
        lateral_in_df = self.actual_q_df[
            (self.actual_q_df[self.department_col] == department)
            & (self.actual_q_df[self.employee_id_col].isin(self.last_q_ids))
        ]
        last_q_lateral_in_df = self.last_q_df[
            self.last_q_df[self.employee_id_col].isin(
                lateral_in_df[self.employee_id_col]
            )
        ]

        merged_df = self._merge_dataframes(
            last_q_lateral_in_df,
            lateral_in_df,
            on_cols=[self.employee_id_col],
            how="inner",
        )
        merged_df = merged_df[merged_df[self.department_col + "_last"] != department]
        merged_df["reason"] = (
            "Lateral Movement In from " + merged_df[self.department_col + "_last"]
        )

        return merged_df

    def get_lateral_movements_out(self, department):
        lateral_out_df = self.last_q_df[
            (self.last_q_df[self.department_col] == department)
            & (self.last_q_df[self.employee_id_col].isin(self.actual_q_ids))
        ]
        actual_q_lateral_out_df = self.actual_q_df[
            self.actual_q_df[self.employee_id_col].isin(
                lateral_out_df[self.employee_id_col]
            )
        ]

        merged_df = self._merge_dataframes(
            lateral_out_df,
            actual_q_lateral_out_df,
            on_cols=[self.employee_id_col],
            how="inner",
        )
        merged_df = merged_df[merged_df[self.department_col + "_current"] != department]
        merged_df["reason"] = (
            "Lateral Movement Out to " + merged_df[self.department_col + "_current"]
        )

        return merged_df

    def get_promotions(self):
        merged_df = self._merge_dataframes(
            self.last_q_df,
            self.actual_q_df,
            on_cols=[self.employee_id_col],
            how="inner",
        )
        promotions = merged_df[
            merged_df["pay_grade_last"] < merged_df["pay_grade_current"]
        ]
        promotions["reason"] = "Promotion"

        return promotions

    def get_demotions(self):
        merged_df = self._merge_dataframes(
            self.last_q_df,
            self.actual_q_df,
            on_cols=[self.employee_id_col],
            how="inner",
        )
        demotions = merged_df[
            merged_df["pay_grade_last"] > merged_df["pay_grade_current"]
        ]
        demotions["reason"] = "Demotion"

        return demotions

    def get_lateral_with_promotion_or_demotion(self, department):
        lateral_in = self.get_lateral_movements_in(department)
        lateral_out = self.get_lateral_movements_out(department)

        lateral_with_promotion = lateral_in[
            lateral_in["pay_grade_last"] < lateral_in["pay_grade_current"]
        ]
        lateral_with_promotion["reason"] = (
            "Lateral In with Promotion from "
            + lateral_with_promotion[self.department_col + "_last"]
        )

        lateral_with_demotion = lateral_in[
            lateral_in["pay_grade_last"] > lateral_in["pay_grade_current"]
        ]
        lateral_with_demotion["reason"] = (
            "Lateral In with Demotion from "
            + lateral_with_demotion[self.department_col + "_last"]
        )

        lateral_out_with_promotion = lateral_out[
            lateral_out["pay_grade_last"] < lateral_out["pay_grade_current"]
        ]
        lateral_out_with_promotion["reason"] = (
            "Lateral Out with Promotion to "
            + lateral_out_with_promotion[self.department_col + "_current"]
        )

        lateral_out_with_demotion = lateral_out[
            lateral_out["pay_grade_last"] > lateral_out["pay_grade_current"]
        ]
        lateral_out_with_demotion["reason"] = (
            "Lateral Out with Demotion to "
            + lateral_out_with_demotion[self.department_col + "_current"]
        )

        return pd.concat(
            [
                lateral_with_promotion,
                lateral_with_demotion,
                lateral_out_with_promotion,
                lateral_out_with_demotion,
            ],
            ignore_index=True,
        )

    def get_all_movements(self, department):
        terminations = self.get_terminations()
        hires = self.get_hires()
        lateral_in = self.get_lateral_movements_in(department)
        lateral_out = self.get_lateral_movements_out(department)
        promotions = self.get_promotions()
        demotions = self.get_demotions()
        lateral_with_promotion_or_demotion = (
            self.get_lateral_with_promotion_or_demotion(department)
        )

        all_movements = pd.concat(
            [
                terminations,
                hires,
                lateral_in,
                lateral_out,
                promotions,
                demotions,
                lateral_with_promotion_or_demotion,
            ],
            ignore_index=True,
        )

        # Ensure that the required columns are in the final DataFrame
        required_columns = [
            "employee_id",
            "first_name_current",
            "last_name_current",
            "gender_current",
            "pay_grade_current",
            "department_current",
            "market_current",
            "reason",
        ]
        all_movements = all_movements[required_columns]

        return all_movements.drop_duplicates(subset=["employee_id"], keep="first")
