import numpy as np
import subprocess
import pandas as pd
from functools import wraps
import time
import logging
import os
import random


# The `GrabLogs` class is a singleton design pattern implementation in Python that initializes a
# logging configuration and logs messages with different severity levels based on the input level
# parameter, and also provides a function to clear the contents of a log file.
class GrabLogs:
    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        This is a singleton design pattern implementation in Python.

        :param cls: The cls parameter refers to the class that the method is being called on. In this case,
        it is the class "GrabLogs"
        :return: The method `__new__` is returning an instance of the `GrabLogs` class. If the class has not
        been instantiated before, it creates a new instance and sets the `__instance` attribute to that
        instance. If the class has already been instantiated, it returns the existing instance.
        """
        if cls.__instance is None:
            cls.__instance = super(GrabLogs, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def configure_logger(self) -> None:
        """
        This function initializes a logging configuration with a specified file path, logging level, format,
        and file mode.
        :return: If the `__initialized` attribute is already `True`, the `__init__` method will return
        without doing anything. If `__initialized` is `False`, the method will initialize the logger with
        the specified configuration. No value is explicitly returned from the `__init__` method.
        """
        if self.__initialized:
            return
        self.__initialized = True
        try:
            logging.basicConfig(
                filename=f"{os.getcwd()}\\logs\\log.txt",
                level=logging.DEBUG,
                format="%(asctime)s %(message)s",
                filemode="a",
            )
        except Exception:
            logging.basicConfig(
                filename="C:/Users/10020624/BAT/D&I at BAT - General/07. Stakeholder management/Management Board reporting/DnI_automation/logs/log.txt",
                level=logging.DEBUG,
                format="%(asctime)s %(message)s",
                filemode="a",
            )

    def form_log(self, message, level):
        """
        The function logs messages with different severity levels based on the input level parameter.

        :param message: The message to be logged
        :param level: The severity level of the log message, represented as an integer. The levels are
        typically defined as follows:
        """
        logging.getLogger("matplotlib.font_manager").disabled = True
        if 0 <= level <= 20:
            logging.info(message)
        elif 20 < level <= 30:
            logging.warning(message)
        elif 30 < level <= 40:
            logging.error(message)
        elif 40 < level < 50:
            logging.critical(message)

    def clear_logs(self):
        """
        This function clears the contents of a log file located at a specific file path.
        """
        try:
            filename = "C:/Users/85163144/BAT/D&I at BAT - General/07. Stakeholder management/Management Board reporting/DnI_automation/logs/log.txt"
            open(filename, "w").close()
        except Exception:
            filename = "C:/Users/10020624/BAT/D&I at BAT - General/07. Stakeholder management/Management Board reporting/DnI_automation/logs/log.txt"
            open(filename, "w").close()


def get_level(keyword: str = "Info"):
    if keyword.lower() in "Information".lower():
        return random.randint(0, 20)

    elif keyword.lower() in "Warning".lower():
        return random.randint(21, 30)

    elif keyword.lower() in "Error".lower():
        return random.randint(31, 40)

    elif keyword.lower() in "Critical".lower():
        return random.randint(41, 49)


def unique_elem_list(ls: list) -> np.array:
    x = np.array(ls)
    return np.unique(x)


def close_one_drive():
    """
    Shell script that closes OneDrive if it's active, in order to preserve the integrity
    of the file generation process
    :param: None
    :return: Shell script to stop OneDrive
    """
    return subprocess.call("taskkill /f /im onedrive.exe", shell=True)


def start_one_drive():  # sourcery skip: remove-unreachable-code
    """
    Shell script that starts OneDrive application.
    This function can be used to start the
    OneDrive application if it's not already running. Starting OneDrive might be useful to ensure
    that files are synchronized with the cloud before performing certain operations.

    :param: None
    :return: Shell script to start OneDrive
    """
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Use subprocess.Popen to open OneDrive silently in the background
    subprocess.Popen(
        ["C:\\Program Files\\Microsoft OneDrive\\OneDrive.exe"], startupinfo=startupinfo
    )


def onedrive_operations_decorator(func):
    """
    Decorator that starts OneDrive before a set of operations and stops it afterward.

    This decorator can be applied to functions that require ensuring that OneDrive is active
    before performing certain operations. It starts OneDrive before calling the decorated function
    and stops OneDrive after the function has completed.

    :param func: The function to be decorated
    :return: Decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        close_one_drive()

        result = func(*args, **kwargs)

        start_one_drive()

        return result

    return wrapper


def seconds_to_hours_minutes(seconds):
    hours = seconds / 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds / 60
    return f"{minutes:.4f} minutes" if hours <= 1 else f"{hours:.4f} hours"


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        formatted_time = seconds_to_hours_minutes(execution_time)
        print(f"{func.__name__} took {formatted_time} to execute.")
        return result

    return wrapper


def left_join(df1: pd.DataFrame, df2: pd.DataFrame, on_column: str) -> pd.DataFrame:
    """Makes an outer left join between 2 similar dataframes, that have the same common column

    Args:
        df1 (pd.DataFrame): the dataframe you want to see the differences from
        df2 (pd.DataFrame): the dataframe you want to compare the first dataframe with
        on_column (str): the common column's name

    Returns:
        pd.DataFrame: a dataframe with all the entries from df1 that can't be found in df2
    """
    merged_df = pd.merge(df1, df2, on=on_column, how="left", indicator=True)
    left_only_df = merged_df[merged_df["_merge"] == "left_only"]

    return left_only_df.drop(columns=["_merge"]).copy()
