from __future__ import annotations
import contextlib
from tkinter import messagebox
from headers import helper, visuals, fixture, movements, utils
import pandas as pd
import networkx as nx

# decorators
from headers.utils import measure_execution_time


@measure_execution_time
def profile():
    for lt in helper.generate_combo():
        with contextlib.suppress(Exception):
            print("=" * 247)
            print(f"Preparing {lt} file")
            fixture.fix_generate_file(lt)


# history_df = fixture.correct_q_data()[1]
# actual_df = helper.RawDataCleanPrep().split_by_snap()[1]
# combo = "Marketing"
# mov = movements.CalculateMovements(history_df, actual_df, combo)


@measure_execution_time
def measure_function():
    fixture.fix_generate_file("USA")


some_df = movements.CompareG34().unite_outer_inner()
some_df.to_csv("out.csv", index=False)
