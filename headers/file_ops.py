import pandas as pd
import os
from logs import logger_class
import flet as ft
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import json
from datetime import date, datetime

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
        """
        This function returns an os process that opens the raw data file to the users for viewing.
        :param: self.file_name
        :return: os subprocess
        """
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
        """
        The function appends a new DataFrame to an existing DataFrame and then appends the combined
        DataFrame to an Excel file.

        :param file_to_upload: The `file_to_upload` parameter is expected to be a pandas DataFrame that you
        want to append to an existing DataFrame. The function `_append_to_df` takes this DataFrame,
        concatenates it with an existing DataFrame (`base_df`), and then appends the combined DataFrame to
        an Excel file using the
        :return: The method `_append_to_df` is returning the result of calling the private method
        `__append_to_excel` with the new DataFrame `new_df` as an argument.
        """
        base_df = self.update_df()
        new_df = pd.concat([base_df, file_to_upload], ignore_index=True)
        return self.__append_to_excel(new_df)

    def __append_to_excel(self, df_to_append: pd.DataFrame):
        """
        The function appends a pandas DataFrame to an existing Excel file.

        :param df_to_append: The `df_to_append` parameter is a pandas DataFrame that contains the data you
        want to append to an existing Excel file. The function loads the existing Excel file, selects the
        "data" sheet, appends the rows from the DataFrame to the sheet, and then saves and closes the
        workbook
        :type df_to_append: pd.DataFrame
        """
        if os.path.isfile(self.file_name):
            workbook = load_workbook(self.file_name)
            sheet = workbook["data"]

            for row in dataframe_to_rows(df_to_append, header=False, index=False):
                sheet.append(row)

            workbook.save(self.file_name)
            workbook.close()

    def __undo_upload(self):
        print("undo method to be developed")
        pass

    def __clear_df(self):
        """This function clears the contents of the support file (dataframe) and logs it in the logger
        How to call: due to name mangling, and the fact that this is a private method, it will need to be
        called like the following example:

        Example:
        ```
        class Foo:
            def __private_method(*args):
                #does things
                return *args

        Foo()._Foo__private_method(*args)
        ```
        """
        with open(self.file_name, "w") as file:
            pass
        print("Data cleared on behalf of admin")
        self.grab_log.form_log(
            "Data Cleared on behalf of app admin", self.grab_logs.get_level("warn")
        )

    def split_by_snap(self) -> tuple:
        """
        Splits the data into two DataFrames based on the most recent and previous quarters.

        Returns:
            tuple: A tuple containing two DataFrames.

            - The first DataFrame (index 0) represents data for the previous quarter.
            - The second DataFrame (index 1) represents data for the actual (most recent) quarter.
        """
        snap = last_quarters(self.__snap_list())  # will only contain 2 values
        df = self.update_df()
        dfprev = df[df["snapshot_date"] == snap[0]]
        dfact = df[df["snapshot_date"] == snap[1]]
        return (
            dfprev,
            dfact,
        )


# todo: Testing of all the below functions
def repl_date():
    """
    The function `repl_date()` returns the current month and year in a specific format.
    :return: The function `repl_date()` returns a string representing the current month and year in the
    format "Month Year".
    """
    tod = date.today()
    return tod.strftime("%B %y")


def get_quarter_month_list(q_map="mapping/quarters.json"):
    json_content = {}
    with open(q_map, "r") as q_map:
        content = json.loads(q_map.read())
        for iterator in content:
            for i in content[iterator]:
                json_content.update(i)
    return json_content


def last_quarters(quarter_list):
    """
    The function "last_quarters" returns the last two quarters from a given list of quarters.

    :param quarter_list: A list of quarters, where each quarter is represented as a string in the format
    "QX YYYY", where X is the quarter number (1-4) and YYYY is the year (e.g. "Q3 2021")
    :return: The function `last_quarters` takes a list of quarters as input and returns the last two
    quarters in the list.
    """
    return quarter_list[-2:]


def get_actual_q():
    c_year = datetime.now().year
    date = datetime.now()
    c_month = date.strftime("%b")
    base = get_quarter_month_list()
    for key, val in base.items():
        if key[3:] in str(c_year):
            for x in range(len(val)):
                if c_month in val[x]:
                    return key


def get_quarter_for_snap(month_snap):
    q_list = get_quarter_month_list()
    for key, val in q_list.items():
        if key[3:] in str(month_snap[-2:]):
            for x in range(len(val)):
                if month_snap[:3] in val[x][:3]:
                    return key


def add_quarter_for_snap2list(list_of_lists):
    for val in list_of_lists:
        for j, jval in enumerate(val):
            if j == 1:
                val[j] = get_quarter_for_snap(jval)
    return list_of_lists


def get_snap_list(choosen_df: pd.DataFrame, snap_column: str) -> list:
    return list(choosen_df[snap_column].unique())


def split_by_snap_custom(choosen_df, column_for_snap):
    """
    Given a raw data like dataframe, this funtion will split it into 2 quarters as follows:
    0 - previous q
    1 - actual q
    :returns: a dataframe tuple
    """
    snap = last_quarters(get_snap_list(choosen_df, column_for_snap))
    dfprev = choosen_df[choosen_df[column_for_snap] == snap[0]]
    dfact = choosen_df[choosen_df[column_for_snap] == snap[1]]
    return (
        dfprev,
        dfact,
    )
