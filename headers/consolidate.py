import pandas as pd
from . import file_ops
import flet as ft


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
    return [ft.DataColumn(ft.Text(header)) for header in df.columns]
