import pandas as pd
import tkinter as tk
from tkinter import filedialog

try:
    import helper, visuals, fixture, utils
except ImportError:
    from . import helper, visuals, fixture, utils


class CalculateMovements:
    def __init__(self, history_df, actual_df, comb_val):
        self.df = fixture.fix_mb2_moves_per_quarters(history_df, actual_df, comb_val)

    def get_last_2_columns(self):
        last_two_columns = self.df.iloc[:, -2:]
        return self.df[["Name", "Gender"] + last_two_columns.columns.tolist()]

    def get_removed(self):
        new_df = self.get_last_2_columns()
        columns_list = [
            "Removed",
            "Gender",
        ]
        removed_list = [
            [col[0], col[1]] for idx, col in new_df.iterrows() if col[2] > col[3]
        ]

        removed_df = pd.DataFrame(removed_list, columns=columns_list)

        removed_df["CrossIndustry"] = None
        removed_df["Observations"] = None

        return removed_df

    def get_added(self):
        new_df = self.get_last_2_columns()
        columns_list = [
            "Added",
            "Gender",
        ]
        removed_list = [
            [col[0], col[1]] for idx, col in new_df.iterrows() if col[2] < col[3]
        ]

        added_df = pd.DataFrame(removed_list, columns=columns_list)

        added_df["CrossIndustry"] = None
        added_df["Observations"] = None

        return added_df

    def __fill_ci(self, target_df):
        """
        Fills the "CrossIndustry" column in the target DataFrame based on matching values in the "FullName" column
        with the "Experience" column from another DataFrame.

        Parameters:
        - target_df (pandas.DataFrame): The target DataFrame where the "CrossIndustry" column will be filled.

        Returns:
        - pandas.DataFrame: The target DataFrame with the "CrossIndustry" column filled.
        """
        base_df = helper.CalculateLT().assign_lt()

        merged_df = target_df.merge(
            base_df, left_on=target_df.iloc[:, 0], right_on="FullName", how="inner"
        )

        target_df["CrossIndustry"] = merged_df["Experience"]

        return target_df

    def fill_in_ci(self):
        """
        Fills the "CrossIndustry" column for added and removed DataFrames.

        This method internally calls the __fill_ci method to fill the "CrossIndustry" column
        for both the added and removed DataFrames obtained using get_added() and get_removed().

        Returns:
        - Tuple[pandas.DataFrame, pandas.DataFrame]: A tuple containing the target DataFrames with the
          "CrossIndustry" column filled for added and removed entries, respectively.
        """
        filled_added = self.__fill_ci(self.get_added())
        filled_removed = self.__fill_ci(self.get_removed())

        return filled_added, filled_removed


class CompareG34:
    def __init__(self):
        root = tk.Tk()
        root.withdraw()
        file = filedialog.askopenfilename(
            title="Choose base data", filetypes=[("Excel files", ".csv")]
        )

        self.df = pd.read_csv(file)

    def trim_df(self):
        return self.df.loc[
            (self.df["MBFinalInclude2"] == "Include"),
            [
                "FullName",
                "Gender",
                "MBSecondView2",
                "MBLevel2",
                "Region",
                "Area",
                "Market",
                "HomeFunction",
                "Experience",
                "PayGradeCode",
                "PersonIDExternal",
                "DateLabel",
            ],
        ]

    def merge_trimmed_inner(self):
        new_df = helper.split_by_snap_custom(self.trim_df(), "DateLabel")
        return new_df[0].merge(new_df[1], on="PersonIDExternal")

    def merge_trimmed_outer_hires(self):
        new_df = helper.split_by_snap_custom(self.trim_df(), "DateLabel")
        return new_df[0].merge(new_df[1], on="PersonIDExternal", how="outer")

    def merge_trimmed_outer_terminations(self):
        new_df = helper.split_by_snap_custom(self.trim_df(), "DateLabel")
        return new_df[1].merge(new_df[0], on="PersonIDExternal", how="outer")

    def unite_outer_inner(self):
        intermed_df = pd.concat(
            [self.merge_trimmed_inner(), self.merge_trimmed_outer_hires()],
            ignore_index=True,
        )
        return pd.concat(
            [intermed_df, self.merge_trimmed_outer_terminations()], ignore_index=True
        )
