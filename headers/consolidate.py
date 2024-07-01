import pandas as pd
from . import file_ops


class GatherData:
    def __init__(self) -> None:
        self.df = file_ops.FilePrep().update_df()

    def form_combo(self):
        return self.df["department"].unique()

    def get_combo_table(self, cval):
        pass