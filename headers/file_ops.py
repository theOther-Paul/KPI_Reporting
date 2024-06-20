import subprocess
import pandas as pd
import os
import json
import functools
from logs import logger_class

"""
@package docstring

This file serves as a helper module for both the primary and secondary interfaces.
Its primary purpose is to manage the source file, raw_data, by handling tasks such as uploading, updating, and cleansing the extracted files.

"""


class FilePrep:
    def __init__(self) -> None:
        self.file_name = "\\raw_data\\personnel3.xlsx"
        self.grab_logs = logger_class.GrabLogs()

    def open_raw_data(self):
        print(f"{self.file_name} will open shortly")
        path2file = os.getcwd() + self.file_name
        return os.system(path2file)
