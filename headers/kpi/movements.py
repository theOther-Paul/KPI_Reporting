import pandas as pd


class EmployeeMovements:
    def __init__(
        self,
        last_q_df,
        actual_q_df,
        department,
        department_col="department",
        employee_id_col="employee_id",
    ):
        self.last_q_df = last_q_df[last_q_df[department_col] == department]
        self.actual_q_df = actual_q_df[actual_q_df[department_col] == department]
        self.department = department
        self.department_col = department_col
        self.employee_id_col = employee_id_col

        self.last_q_ids = set(self.last_q_df[self.employee_id_col])
        self.actual_q_ids = set(self.actual_q_df[self.employee_id_col])

    def _merge_dataframes(self, df1, df2, on_cols, how="outer"):
        return pd.merge(df1, df2, on=on_cols, how=how, suffixes=("_last", "_current"))

    def _calculate_population(self, df):
        total_population = len(df)
        female_population = df[df["gender"] == "Female"].shape[0]
        return total_population, female_population

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

    def get_lateral_movements_in(self):
        lateral_in_df = self.actual_q_df[
            (self.actual_q_df[self.department_col] == self.department)
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
        merged_df = merged_df[
            merged_df[self.department_col + "_last"] != self.department
        ]
        merged_df["reason"] = (
            "Lateral Movement In from " + merged_df[self.department_col + "_last"]
        )

        return merged_df.drop_duplicates(self.employee_id_col)

    def get_lateral_movements_out(self):
        lateral_out_df = self.last_q_df[
            (self.last_q_df[self.department_col] == self.department)
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
        merged_df = merged_df[
            merged_df[self.department_col + "_current"] != self.department
        ]
        merged_df["reason"] = (
            "Lateral Movement Out to " + merged_df[self.department_col + "_current"]
        )

        return merged_df.drop_duplicates(self.employee_id_col)

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

    def get_lateral_with_promotion_or_demotion(self):
        lateral_in = self.get_lateral_movements_in()
        lateral_out = self.get_lateral_movements_out()

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

        # Lateral Out with Promotion or Demotion
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

    def get_all_movements(self):
        terminations = self.get_terminations()
        hires = self.get_hires()
        lateral_in = self.get_lateral_movements_in()
        lateral_out = self.get_lateral_movements_out()
        promotions = self.get_promotions()
        demotions = self.get_demotions()
        lateral_with_promotion_or_demotion = (
            self.get_lateral_with_promotion_or_demotion()
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

        # Adjust the required_columns list to correctly reference the merged columns
        required_columns = [
            self.employee_id_col,
            "first_name",
            "last_name",
            "gender",
            "pay_grade",
            "department",
            "market",
            "reason",
        ]

        # Select the columns that are common after merging
        available_columns = [
            col for col in required_columns if col in all_movements.columns
        ]
        all_movements = all_movements[available_columns]

        # Drop duplicates
        return all_movements.drop_duplicates(
            subset=["employee_id", "reason"], keep="first"
        )

    def calculate_inflow(self):
        hires = self.get_hires()
        lateral_in = self.get_lateral_movements_in()
        lateral_with_promotion_or_demotion = (
            self.get_lateral_with_promotion_or_demotion()
        )

        inflow_population_df = pd.concat(
            [hires, lateral_in, lateral_with_promotion_or_demotion], ignore_index=True
        )
        inflow_total, inflow_female = self._calculate_population(inflow_population_df)

        return inflow_total, inflow_female

    def calculate_outflow(self):
        terminations = self.get_terminations()
        lateral_out = self.get_lateral_movements_out()
        outflow_population_df = pd.concat(
            [terminations, lateral_out], ignore_index=True
        )

        outflow_total, outflow_female = self._calculate_population(
            outflow_population_df
        )

        return outflow_total, outflow_female

    def get_population_summary(self):
        last_q_total, last_q_female = self._calculate_population(self.last_q_df)
        inflow_total, inflow_female = self.calculate_inflow()
        outflow_total, outflow_female = self.calculate_outflow()
        actual_q_total, actual_q_female = self._calculate_population(self.actual_q_df)

        # Validate the population calculations to ensure the rule is respected
        calculated_actual_q_total = last_q_total - outflow_total + inflow_total
        calculated_actual_q_female = last_q_female - outflow_female + inflow_female

        warnings = []

        if (
            calculated_actual_q_total != actual_q_total
            or calculated_actual_q_female != actual_q_female
        ):
            warnings.extend(
                (
                    "Warning: Population calculation mismatch. Check your inflow/outflow logic.",
                    f"Expected total: {calculated_actual_q_total}, Actual total: {actual_q_total}",
                    f"Expected female: {calculated_actual_q_female}, Actual female: {actual_q_female}",
                )
            )
        summary_data = {
            " ": ["Total Population", "Female #"],
            "Last_q population": [last_q_total, last_q_female],
            "Outflow": [-outflow_total, -outflow_female],
            "Inflow": [inflow_total, inflow_female],
            "Actual_q population": [actual_q_total, actual_q_female],
        }

        summary_df = pd.DataFrame(summary_data, index=["Population", "Females"])

        if warnings:
            warnings_df = pd.DataFrame({"Warnings": warnings})
            return summary_df, warnings_df

        return summary_df, None
