import pandas as pd
import os
from logs import logger_class
import flet as ft
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

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
