import subprocess
from tkinter.filedialog import askopenfilename
import pandas as pd
import os
from tkinter import messagebox
from datetime import date, datetime
import json
import networkx as nx
import functools

from . import utils

"""
@package docstring

This file serves as a helper module for both the primary and secondary interfaces.
Its primary purpose is to manage the source file, raw_data, by handling tasks such as uploading, updating, and cleansing the extracted files.

"""


class CalculateLT:
    def __init__(self) -> None:
        self.df = RawDataCleanPrep().update_df()

    def summarize_population_list_raw(self):
        """
        Given a snapshot of the whole raw data, this function will summarize the file with
        all the relevant data neede for future operations

        :return: a dataframe with only relevant data
        """
        return self.df[
            [
                "FullName",
                "PositionCode",
                "ParentPositionCode",
                "Gender",
                "Nationality2",
                "MBLevel2",
                "JobTitle",
                "MBSecondView2",  # Ops in regions
                "MBSharedResponsibility2",  # old: MB Functional Responsibility
                "MBFinalFullName",
                "Region",
                "Area",
                "Market",
                "Experience",  # the old Cross Industry
                "HomeFunction",
                "PayGradeCode",
                "PersonIDExternal",
                "UserID",
                "LineManagerPersonIDExternal",
                "LineManagerUserID",
                "LineManagerFullName",
                "LineManagerPositionCode",
                "DateLabel",  # The old Shapshot Date
                "MBFinalInclude2",
            ]
        ].fillna("No level")

    def add_parents_column(self):
        G = nx.DiGraph()
        for _, row in self.df.iterrows():
            G.add_edge(row["ParentPositionCode"], row["PositionCode"])

        parents_dict = {}
        for position_code in G.nodes:
            parents = list(nx.ancestors(G, position_code))
            parents_dict[position_code] = parents

        self.df["Parents"] = self.df["PositionCode"].map(parents_dict)

        return self.df

    def match_lt(self, walked_df: pd.DataFrame, mb_list: pd.DataFrame) -> pd.DataFrame:
        mb_positions_dict = pair_mb_positions(mb_list)
        chain_id = pair_mb_positions(
            walked_df, key_col="PositionCode", val_col="Parents"
        )
        lt_var = []

        for key, val in chain_id.items():
            reversed_list = val[::-1]
            lt_var.extend(
                [
                    [key, val, mb_positions_dict[item]]
                    for item in reversed_list
                    if item in mb_positions_dict
                ]
            )
        return pd.DataFrame(lt_var, columns=["PositionCode", "Parents", "LT"])

    def assign_lt_secondview(self):
        df = self.summarize_population_list_raw()

        new = self.match_lt(self.add_parents_column(), get_mblt_func())

        new = new[["PositionCode", "LT"]]
        columns_to_keep = [
            "FullName",
            "PositionCode",
            "ParentPositionCode",
            "Gender",
            "Nationality2",
            "MBLevel2",
            "JobTitle",
            "MBSecondView2",
            "MBSharedResponsibility2",
            "MBFinalFullName",
            "Region",
            "Area",
            "Market",
            "Experience",
            "HomeFunction",
            "PayGradeCode",
            "PersonIDExternal",
            "UserID",
            "LineManagerPersonIDExternal",
            "LineManagerUserID",
            "LineManagerFullName",
            "LineManagerPositionCode",
            "DateLabel",
            "MBFinalInclude2",
            "LT",
        ]

        final_df = df.merge(new, on="PositionCode", how="left")[columns_to_keep]
        final_df.drop_duplicates()

        return final_df

    def assign_lt_sec(self):
        summ_df = self.assign_lt_secondview()
        mb = get_mblt_sec()

        summ_df["LT_Functional"] = ""
        for i, val in summ_df.iterrows():
            for idx, mbval in mb.iterrows():
                if val["HomeFunction"] == mbval["Function"]:
                    if val["HomeFunction"] in [
                        "Exec & Corp Services",
                        "Facilities",
                    ]:
                        summ_df.at[i, "LT_Functional"] = val["LT"]
                    else:
                        summ_df.at[i, "LT_Functional"] = mbval["LT_Functional"]
        return summ_df

    def mod_lt(self):
        incomplete_df = self.assign_lt_sec()
        mb = get_mblt_func()

        for idx, val in incomplete_df.iterrows():
            for _, mbname in mb.iterrows():
                if (
                    val["MBSecondView2"] == mbname["MBSharedResponsibility2"]
                    and val["LT"] != mbname["LT"]
                ):
                    incomplete_df.at[idx, "LT"] = mbname["LT"]
                if val["HomeFunction"] in [
                    "Exec & Corp Services",
                    "Facilities",
                ]:
                    incomplete_df.at[idx, "LT_Functional"] = val["LT"]
        return incomplete_df

    @functools.lru_cache(maxsize=None)
    def assign_lt(self):
        df = self.mod_lt()

        df.rename(
            columns={
                "LT": "LT_SecondView2",
                "LT_Functional": "LT_SharedResponsibility2",
            },
            inplace=True,
        )
        return df


def download_file(val, df):
    """
    This function returns an excel file containing a sliced verion of the current general file

     :params: val - the LT we want to slice the base file with
     :return: an Excel file
    """
    df = df.loc[(df["LT_SecondView2"] == val) | (df["LT_SharedResponsibility2"] == val)]
    df.to_excel(f"downloads/Downloaded {val} data.xlsx", index=False)
    if prompt := messagebox.askokcancel(
        title=f"Data Ready for {val}",
        message=f"Sliced data ready for {val} is complete. \n Would you like to open this file?",
    ):
        return subprocess.call(
            [f"downloads/Downloaded {val} data.xlsx"],
            shell=True,
        )


def get_mblt_func(file="mapping/mblt_map.xlsx"):
    return pd.read_excel(file, index_col=None, sheet_name="Functional Line")


def get_mblt_sec(file="mapping/mblt_map.xlsx"):
    return pd.read_excel(file, index_col=None, sheet_name="Reporting Line")


def pair_mb_positions(pos_df, key_col="PositionCode", val_col="LT"):
    return dict(zip(pos_df[key_col], pos_df[val_col]))


class RawDataCleanPrep:
    def __init__(self) -> None:
        self.file_name = "raw_data_files/raw_gen.csv"
        self.grab_log = utils.GrabLogs()

    def _clean_df(self, df):
        """
        The function removes the last three rows from a given dataframe and returns the modified dataframe.

        :param df: The input dataframe that needs to be cleaned
        :return: The function `clean_df` takes a DataFrame `df` as input, removes the last three rows of the
        DataFrame using slicing, and returns the modified DataFrame.
        """
        df = df[:-3]
        return df

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
        messagebox.showinfo(
            title="Contents cleared",
            message=f"{self.file_name} contents have been cleared!",
        )
        self.grab_log.form_log(
            "Data Cleared on behalf of app admin", utils.get_level("warn")
        )

    def add_columns(self, values=None, position=0, columnname="Comments"):
        """
        This function adds a new column with specified values to a pandas dataframe at a specified position.

        :param df: The pandas DataFrame to which the new column(s) will be added
        :param values: A list of values to be added as a new column in the dataframe
        :param position: The position parameter specifies the index position at which the new column(s)
        should be inserted. If position is set to 0, the new column(s) will be added at the beginning of the
        DataFrame. If position is set to -1, the new column(s) will be added at the end, defaults to 0
        (optional)
        :param columnname: The name of the new column that will be added to the DataFrame, defaults to
        Comments (optional)
        """
        if values is None:
            values = []
        df = self.update_df()
        # by default, values will be NAN (the default pandas values for nothing)
        if position == 0:
            position = len(df.columns)
            values = (
                pd.Series(values)
                if bool(values)
                else pd.Series(list(range(len(df.index))))
            )
        df.insert(position, columnname, values, allow_duplicates=True)
        self.__dump2df()
        self.grab_log.form_log(
            f"Column {columnname} added on position {position}",
        )

    def __dump2df(self, df):
        """
        dumps all the dataframe into the file, when doing operations with the whole database.
        It is reccomended to use this only when working with the whole set of data as this
        will overwrite everything in the table.
            * Input:
                a dataframe
            * Output:
                dataframe will be added to the raw csv file
                and a messagebox announcing the operation is complete
        """
        try:
            with open("raw_data_files/raw_gen.csv", "w+", encoding="utf-8") as ftd:
                df.to_csv(ftd, index=False, index_label=True, lineterminator="\r")
            self.grab_log.form_log("Dump complete", utils.get_level())
        except Exception:
            self.grab_log.form_log(
                f"Dump insuccessful because of {Exception}", utils.get_level("crit")
            )

    def _raw_data_oap(self, first_file, filename="raw_gen.csv", w_col=True):
        """
        This function appends a pandas dataframe to a CSV file and displays a message box indicating a
        successful upload.

        :param first_file: The first_file parameter is a pandas DataFrame containing the raw data that needs
        to be uploaded to a CSV file
        :param filename: The name of the file to which the data will be appended. If no filename is
        provided, the default name "raw_gen.csv" will be used, defaults to raw_gen.csv (optional)
        """
        if w_col:
            try:
                with open(f"raw_data_files/{filename}", "a+", encoding="utf-8") as rd:
                    first_file.to_csv(
                        rd, index=False, index_label=True, lineterminator="\r"
                    )
            except Exception:
                with open(f"raw_data_files/{filename}", "a+", encoding="latin-1") as rd:
                    first_file.to_csv(
                        rd, index=False, index_label=True, lineterminator="\r"
                    )

        else:
            try:
                with open(f"raw_data_files/{filename}", "a+", encoding="utf-8") as rd:
                    first_file.to_csv(
                        rd,
                        index=False,
                        index_label=True,
                        header=False,
                        lineterminator="\r",
                    )
            except Exception:
                with open(f"raw_data_files/{filename}", "a+", encoding="latin-1") as rd:
                    first_file.to_csv(
                        rd,
                        index=False,
                        index_label=True,
                        header=False,
                        lineterminator="\r",
                    )
        messagebox.showinfo(title="Upload file", message="Upload successful!")
        self.grab_log.form_log("Upload successful", utils.get_level())

    def _upload_file(self, file):
        df = self.update_df()
        if all(item in df.columns for item in file.columns):
            self._raw_data_oap(file, w_col=False)
        else:
            self._raw_data_oap(file)

    def update_df(self):
        """
        This function updates a pandas dataframe from a CSV file and checks if the file is empty before
        proceeding.

        :param filename_loc: The file path and name of the CSV file to be read. If no value is provided, the
        default file path and name "raw_data_files/raw_gen.csv" will be used, defaults to
        raw_data_files/raw_gen.csv (optional)
        :return: either a pandas DataFrame containing the contents of the CSV file specified by the
        `filename_loc` parameter, or `None` if the file is empty or cannot be read.
        """
        try:
            content = pd.read_csv(self.file_name, encoding="utf-8", low_memory=False)
        except Exception:
            content = pd.read_csv(self.file_name, encoding="latin-1", low_memory=False)
            self.grab_log.form_log(
                f"Content converted to latin-1, because of {Exception}",
                utils.get_level("Warn"),
            )
        if content.empty:
            return None
        self.grab_log.form_log("Update complete", utils.get_level())
        return content

    def undo_upload(self):
        """
        This function allows the user to undo an uploaded file by removing its content from a dataframe and
        saving the updated dataframe to a CSV file.
        """
        file = askopenfilename(
            filetypes=[
                ("Excel Files", "*.xlsx"),
            ],
        )
        file_content = pd.read_excel(file)
        raw = self.update_df()
        raw.drop(file_content.index, axis=0, inplace=True)
        with open("raw_data_files/raw_gen.csv", "w", encoding="utf-8") as rd:
            raw.to_csv(rd, index=False, index_label=True)
        messagebox.showinfo(title="Undo action", message="Undo complete")
        self.grab_log.form_log("Undo complete", utils.get_level())

    def mod_file(self):
        """
        This function performs modifications on a specified Excel or CSV file.

        It first prompts the user to select an Excel or CSV file using a file dialog.
        If a file is selected, it performs modifications on the selected file using the `core_mod` function.

        If the resulting modified data is empty (contains 3 or fewer bytes), it will save the data as "raw_data_files/raw_gen.csv"
        using the `__dump2df` function. Otherwise, it will upload the modified data using the `upload_file` function.

        This function does not return any values.

        Parameters:
            None

        Returns:
            None
        """
        base_file = None
        base_file = askopenfilename(
            filetypes=[
                ("Excel Files", "*.csv"),
                ("Excel Files", "*.xlsx"),
            ],
        )
        if base_file is not None:
            content = self.__core_mod(base_file)
        filename_loc = "raw_data_files/raw_gen.csv"
        if filename_loc is not None and os.stat(filename_loc).st_size <= 3:
            self.__dump2df(content)
        else:
            self._upload_file(content)

    def __core_mod(self, content):
        """Modify and clean data from an Excel or CSV file.

        This function reads data from a specified Excel or CSV file, performs data cleaning operations,
        and returns the modified DataFrame.

        Parameters:
            file_content (str or file-like object): The path to the Excel or CSV file or a file-like object containing data.

        Returns:
            pandas.DataFrame: A cleaned and modified DataFrame with specified data cleaning operations applied.

        Raises:
            pandas.errors.ParserError: If the provided file_content is not a valid Excel or CSV file.

        Example:
            >>> file_path = "data.xlsx"
            >>> modified_data = core_mod(file_path)
        """
        try:
            result = pd.read_excel(content, engine=None)
        except Exception:
            try:
                result = pd.read_csv(content, encoding="utf-8")
            except UnicodeDecodeError:
                result = pd.read_csv(content, encoding="latin-1")

        result = self._clean_df(result)
        snap_date = result["DateLabel"].tolist()
        for i in range(len(snap_date)):
            if "Today" in snap_date[i]:
                snap_date[i] = repl_date()
        result["DateLabel"] = snap_date
        result = result[~result["Market"].isin(["Russia", "Belarus"])]
        result = result[
            result["PayGradeCode"].isin(
                ["GR34", "GR35", "GR36", "GR37", "GR38", "GR40", "GR41", "GRMB", "GRMT"]
            )
        ]
        result.columns = result.columns.str.strip()
        return result

    def __snap_list(self):
        base_file = self.update_df()
        try:
            snap_list = list(base_file["DateLabel"].unique())
        except Exception:
            snap_list = list(base_file["DateLabel"].unique())
        return snap_list

    def map_quarters(self):
        snap = last_quarters(self.__snap_list())
        month = []
        year = []
        for val in snap:
            month.append(val[:3])
            year.append(val[-2:])
        q_list = get_quarter_month_list()
        res = []
        key_list = []
        for key, values in q_list.items():
            if key not in ["Q1 20", "Q2 20", "Q3 20", "Q4 20"]:
                break
            res.extend(n[:3] for n in values)
        for key, values in q_list.items():
            if key[3:] in year[0] or key[3:] == year[0]:
                for vv in values:
                    for valm in month:
                        if valm in vv or valm == vv:
                            key_list.extend(
                                key for l_res in res if l_res in valm or l_res == valm
                            )
                # if key_list[0] == key_list[1]:
                #     raise Exception("Same Quarter")
                # else:
        return key_list[1], key_list[0]  # actual quarter and previous quarter

    def map_q(self):
        """
        0- previous quarter. 1- actual quarter
        """
        snap = last_quarters(self.__snap_list())
        return [get_quarter_for_snap(x) for x in snap]

    @utils.measure_execution_time
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
        df = CalculateLT().assign_lt()
        dfprev = df[df["DateLabel"] == snap[0]]
        dfact = df[df["DateLabel"] == snap[1]]
        return (
            dfprev,
            dfact,
        )


def generate_combo():
    return get_mblt_func()["LT"].drop_duplicates()


def repl_date():
    """
    The function `repl_date()` returns the current month and year in a specific format.
    :return: The function `repl_date()` returns a string representing the current month and year in the
    format "Month Year".
    """
    tod = date.today()
    return tod.strftime("%B %y")


def get_quarter_month_list(q_map="mapping/snapshot_mapping.json"):
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
