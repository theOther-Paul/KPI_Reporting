import pandas as pd
import os
from logs import logger_class
import flet as ft
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import json
from datetime import date, datetime
import functools
from . import market_map as mm

"""
@package docstring

This file serves as a helper module for both the primary and secondary interfaces.
Its primary purpose is to manage the source file, raw_data, by handling tasks such as uploading, updating, and cleansing the extracted files.

"""


# The `FilePrep` class in Python contains methods for opening, updating, appending, clearing, and
# manipulating data in Excel files, with logging and error handling functionalities.
class FilePrep:
    def __init__(self) -> None:
        self.file_name = "raw_data\\personnel3.xlsx"
        self.grab_logs = logger_class.GrabLogs()
        self.c_map = mm.CountryMapper()

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
                    "Content converted to Latin-1 due to encoding issues",
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
        int_df = pd.concat([base_df, file_to_upload], ignore_index=True)
        new_df = self.asign_market(int_df)
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
        """
        The function `__undo_upload` is a placeholder method that prints a message indicating it is to be
        developed.
        """
        print("undo method to be developed")

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

    def __snap_list(self):
        """
        The function `__snap_list` retrieves unique snapshot dates from a DataFrame.
        :return: The `snap_list` variable is being returned, which is a list of unique values from the
        "snapshot_date" column in the `base_file` DataFrame.
        """
        base_file = self.update_df()
        try:
            snap_list = list(base_file["snapshot_date"].unique())
        except Exception:
            snap_list = list(base_file["snapshot_date"].unique())
        return snap_list

    def map_quarters(self):
        """
        The `map_quarters` function extracts quarter information based on month and year from a given list.
        :return: The `map_quarters` method is returning the second and first elements of the `key_list` in
        that order.
        """
        snap = last_quarters(self.__snap_list())
        month = [val[:3] for val in snap]
        year = [val[-2:] for val in snap]
        q_list = get_quarter_month_list()
        res = [
            n[:3]
            for key, values in q_list.items()
            if key in ["Q1 20", "Q2 20", "Q3 20", "Q4 20"]
            for n in values
        ]
        key_list = [
            key
            for key, values in q_list.items()
            if key[3:] in year[0]
            for vv in values
            for valm in month
            if valm in vv
        ]
        return key_list[1], key_list[0]

    def map_q(self):
        """
        The `map_q` function returns a list of quarters based on the previous quarters in a snapshot list.
        :return: The `map_q` method returns a list of quarter values corresponding to the previous quarters
        of the snapshots obtained from the `last_quarters` function.

        0- previous quarter. 1- actual quarter
        """
        snap = last_quarters(self.__snap_list())
        return [get_quarter_for_snap(x) for x in snap]

    @functools.lru_cache(maxsize=None)
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

    def __dump_to_df(self, df_to_dump: pd.DataFrame):
        """
        This function dumps a pandas DataFrame to an Excel file and logs the outcome.
        
        :param df_to_dump: The `df_to_dump` parameter is a pandas DataFrame that contains the data to be
        dumped into an Excel file. The method `__dump_to_df` attempts to write this DataFrame to an Excel
        file specified by `self.file_name`. If successful, a log message is created indicating that the new
        DataFrame
        :type df_to_dump: pd.DataFrame
        """
        try:
            df_to_dump.to_excel(self.file_name, index=False)
            self.grab_logs.form_log(
                "New dataframe was dumped into the raw data file. Please consult backup file for additional checks",
                self.grab_logs.get_level("warn"),
            )
        except Exception as e:
            self.grab_logs.form_log(
                f"New dataframe was not dumped into the raw data file due to the Exception {e}",
                self.grab_logs.get_level("crit"),
            )

    def asign_market(self, df: pd.DataFrame):
        """
        The function `asign_market` assigns continents to countries in a DataFrame and returns the updated
        DataFrame.
        
        :param df: The `df` parameter in the `asign_market` method is a Pandas DataFrame that is being
        passed as input to the method. The method seems to be assigning a continent to each country in the
        DataFrame and then returning a new DataFrame with the continent information added as a new column
        named "market
        :type df: pd.DataFrame
        :return: The `asign_market` method is returning a DataFrame that is the result of assigning
        continents to countries in the input DataFrame `df` based on the mapping provided by `c_map` and
        then dumping the result into a new DataFrame using the `__dump_to_df` method.
        """
        new_df = self.c_map.assign_continent(df, "country", "market")
        return self.__dump_to_df(new_df)


def repl_date():
    """
    The function `repl_date()` returns the current month and year in a specific format.
    :return: The function `repl_date()` returns a string representing the current month and year in the
    format "Month Year".

    Currently unused
    """
    tod = date.today()
    return tod.strftime("%B %y")


def get_quarter_month_list(q_map="headers/mapping/quarters.json"):
    """
    The function `get_quarter_month_list` reads a JSON file containing quarter-month mappings and
    returns the content as a nested dictionary.

    :param q_map: The `q_map` parameter is the file path to a JSON file that contains a mapping of
    quarters to months for different years. The function `get_quarter_month_list` reads this JSON file
    and returns the content as a dictionary where each year is mapped to its quarters, and each quarter
    is mapped, defaults to headers/mapping/quarters.json (optional)
    :return: A dictionary containing the mapping of quarters to months for each year, as read from the
    specified JSON file.
    """
    json_content = {}
    with open(q_map, "r") as q_map_file:
        content = json.load(q_map_file)
        for year, quarters in content.items():
            json_content[year] = dict(quarters.items())
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
    """
    This Python function retrieves the current quarter based on the current year and month.
    :return: The code is returning the current quarter based on the current year and month.
    """
    c_year = datetime.now().year
    date = datetime.now()
    c_month = date.strftime("%b")
    base = get_quarter_month_list()
    for key, val in base.items():
        if key in str(c_year):
            for idx, x in val.items():
                for mth in x:
                    if c_month in mth:
                        return idx


def get_quarter_for_snap(month_snap):
    """
    The function `get_quarter_for_snap` determines the quarter of the year based on a given month
    abbreviation.

    :param month_snap: The function `get_quarter_for_snap` takes a parameter `month_snap`, which is a
    string representing a month in the format "MMM-YY" (e.g., "Jan-22")
    :return: the quarter corresponding to the given month_snap.
    """
    q_list = get_quarter_month_list()
    for key, val in q_list.items():
        if key in month_snap:
            for q, mth in val.items():
                for m in mth:
                    if month_snap[:3] in m:
                        return q, key


def add_quarter_for_snap2list(list_of_lists):
    """
    The function `add_quarter_for_snap2list` iterates through a list of lists and updates the second
    element of each inner list with the quarter value obtained from a function `get_quarter_for_snap`.

    :param list_of_lists: It seems like the code snippet you provided is incomplete.
    :return: The function `add_quarter_for_snap2list` is returning the `list_of_lists` after modifying
    the second element of each sublist to contain the quarter obtained from the `get_quarter_for_snap`
    function.
    """
    for val in list_of_lists:
        for j, jval in enumerate(val):
            if j == 1:
                val[j] = get_quarter_for_snap(jval)
    return list_of_lists


def get_snap_list(choosen_df: pd.DataFrame, snap_column: str) -> list:
    """
    This function returns a list of unique values from a specified column in a pandas DataFrame.

    :param choosen_df: The `choosen_df` parameter is a pandas DataFrame that contains the data from
    which you want to extract unique values from a specific column
    :type choosen_df: pd.DataFrame
    :param snap_column: The `snap_column` parameter is the name of the column in the DataFrame
    `choosen_df` from which you want to extract unique values to create a list
    :type snap_column: str
    :return: The function `get_snap_list` returns a list of unique values from the specified column
    `snap_column` in the DataFrame `choosen_df`.
    """
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


def convert_date_string(date_str: str) -> str:
    """
    The function `convert_date_string` takes a date string in the format "dd/mm/yyyy" and converts it to
    a string in the format "MMM-yyyy".
    
    :param date_str: Thank you for providing the code snippet. It looks like you are trying to convert a
    date string in the format "dd/mm/yyyy" to a different format "MMM-YYYY"
    :type date_str: str
    :return: The `convert_date_string` function takes a date string in the format "dd/mm/yyyy", converts
    it to a datetime object, and then returns a formatted date string in the format "MMM-YYYY" (e.g.,
    "Jan-2022"). If the input date string is not in the correct format, it will return an error message
    indicating the ValueError that occurred.
    """
    try:
        date_obj = datetime.strptime(date_str, "%d/%m/%Y")
        return date_obj.strftime("%b-%Y")
    except ValueError as e:
        return f"Error: {e}"
