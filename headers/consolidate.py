import pandas as pd
from . import file_ops
import flet as ft


class GatherData:
    def __init__(self) -> None:
        self.df = file_ops.FilePrep().update_df()

    def form_combo(self):
        """
        The function `form_combo` returns the unique values in the "department" column of a DataFrame.
        :return: The `form_combo` method is returning the unique values in the "department" column of the
        DataFrame `self.df`.
        """
        return self.df["department"].unique()

    def get_uniq_val(self, head_name):
        """
        The function `get_uniq_val` returns unique values from a specified column in a DataFrame.

        :param head_name: The `get_uniq_val` method takes a parameter `head_name`, which is the name of the
        column in the DataFrame (`self.df`) for which you want to retrieve the unique values. The method
        returns an array of unique values present in that column
        :return: The `get_uniq_val` method returns an array of unique values from the specified column
        `head_name` in the DataFrame `self.df`.
        """
        return self.df[head_name].unique()


def create_flet_table(df):
    data_rows = []
    for row in df.itertuples(index=False):
        data_cells = [ft.DataCell(ft.Text(str(cell))) for cell in row]
        data_rows.append(ft.DataRow(cells=data_cells))

    return df.columns, data_rows
