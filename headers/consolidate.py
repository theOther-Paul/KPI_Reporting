import pandas as pd
from . import file_ops
import flet as ft


# The `GatherData` class initializes with a DataFrame and provides methods to retrieve unique values
# from specific columns.
class GatherData:
    def __init__(self) -> None:
        self.df = file_ops.FilePrep().update_df()

    def form_combo(self, col_name: str):
        return self.df[col_name].unique()

    def get_uniq_val(self, head_name):
        return self.df[head_name].unique()


def rows(df: pd.DataFrame) -> list:
    return [
        ft.DataRow(cells=[ft.DataCell(ft.Text(row[header])) for header in df.columns])
        for _, row in df.iterrows()
    ]


def headers(df: pd.DataFrame) -> list:
    """
    The function `headers` takes a pandas DataFrame as input and returns a list of DataColumn objects
    with Text headers.
    
    :param df: A pandas DataFrame containing the data for which you want to create headers
    :type df: pd.DataFrame
    :return: A list of DataColumn objects, each containing a Text object representing a column header
    from the input DataFrame.
    """
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]
