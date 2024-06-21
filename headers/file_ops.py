import subprocess
import pandas as pd
import os
import json
import functools
from logs import logger_class
import flet as ft
from openpyxl import load_workbook

"""
@package docstring

This file serves as a helper module for both the primary and secondary interfaces.
Its primary purpose is to manage the source file, raw_data, by handling tasks such as uploading, updating, and cleansing the extracted files.

"""


class FilePrep:
    def __init__(self) -> None:
        self.file_name = "raw_data\\personnel3.xlsx"
        self.grab_logs = logger_class.GrabLogs()

    def open_raw_data(self):
        print(f"{self.file_name} will open shortly")
        path2file = os.getcwd() + "\\" + self.file_name
        return os.system(path2file)

    def update_df(self):
        """
        This function updates a pandas DataFrame from a CSV or Excel file.

        It first attempts to read the CSV file with UTF-8 encoding. If that fails,
        it tries with Latin-1 encoding. If both attempts fail, it tries to read an Excel file.
        Logs are recorded at each step, indicating success or failure.

        :return: A pandas DataFrame containing the contents of the file specified by
        `self.file_name`, or `None` if the file is empty or cannot be read.
        """
        try:
            content = pd.read_csv(self.file_name, encoding="utf-8", low_memory=False)
        except Exception:
            try:
                content = pd.read_csv(
                    self.file_name, encoding="latin-1", low_memory=False
                )
                self.grab_logs.form_log(
                    f"Content converted to Latin-1 due to encoding issues",
                    self.grab_logs.get_level("warn"),
                )
            except Exception:
                try:
                    content = pd.read_excel(self.file_name)
                    self.grab_logs.form_log(
                        "Updated successfully",
                        self.grab_logs.get_level("info"),
                    )
                except Exception as e:
                    self.grab_logs.form_log(
                        f"Update unsuccessful due to {e}",
                        self.grab_logs.get_level("error"),
                    )
                    return None

        if content.empty:
            return None

        self.grab_logs.form_log("Update complete", self.grab_logs.get_level("info"))
        return content

    def _append_to_df(self, file_to_upload) -> pd.DataFrame:
        base_df = self.update_df()
        new_df = pd.concat([base_df, file_to_upload], ignore_index=True)
        return self.__append_to_excel(new_df)

    def __append_to_excel(self, df_to_append):
        try:
            with pd.ExcelWriter(self.file_name, engine="openpyxl", mode="a") as writer:
                writer.book = load_workbook(self.file_name)
                writer.sheets = {ws.title: ws for ws in writer.book.worksheets}

                start_row = writer.sheets["Sheet1"].max_row + 1

                df_to_append.to_excel(
                    writer,
                    index=False,
                    header=False,
                    sheet_name="Sheet1",
                    startrow=start_row,
                )
        except Exception as e:
            print(f"Error appending to Excel: {e}")
