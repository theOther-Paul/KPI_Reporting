from . import kpi_department as kdep
from . import kpi_market as kmkt
import pandas as pd
import numpy as np
import os
import calculus
from .. import file_ops as fo
import xlwings as xw
import threading


class BuildReport(fo.FilePrep):
    def __init__(self, dpt: str) -> None:
        super().__init__()
        self.dpt = dpt

    def get_um_list(self):
        pass

    def get_lm_list(self):
        pass

    def get_gender_split(self):
        pass

    def get_movements(self):
        pass

    def build_report(self):
        pass
