import json
import pycountry as pc
import pycountry_convert as pconv
import pandas as pd
import os
from . import file_ops as fo


def country_to_continent(country_name):
    try:
        country_alpha2 = pconv.country_name_to_country_alpha2(country_name)
        country_continent_code = pconv.country_alpha2_to_continent_code(country_alpha2)
        return pconv.convert_continent_code_to_continent_name(country_continent_code)
    except LookupError:
        return "Unknown"


def make_map(df: pd.DataFrame):
    clist = df["country"].unique().tolist()
    cont_list = []

    for i in clist:
        try:
            cont_list.append([i, country_to_continent(i)])
        except KeyError:
            cont_list.append([i, "Unknown"])
    return dict(cont_list)


def memo_map(map_file="mapping\\markets.json"):
    try:
        with open(map_file, "w") as mf:
            json.dump(make_map(fo.FilePrep().update_df()), mf)
    except Exception as e:
        p2f = os.getcwd() + "\\headers\\" + map_file
        with open(p2f, "w") as mf:
            json.dump(make_map(fo.FilePrep().update_df()), mf)


class CountryMapper:
    def __init__(self, json_file="mapping\\markets.json"):
        p2f = os.getcwd() + "\\headers\\" + json_file
        if os.path.exists(p2f) and os.path.getsize(p2f) > 0:
            with open(p2f, "r") as f:
                self.country_to_continent = json.load(f)
        else:
            memo_map()
            return self.__init__()

    def find_column_position(self, df, column_name):
        return df.columns.get_loc(column_name) if column_name in df.columns else None

    def assign_continent(self, df, left_col_name: str, new_col_name: str):
        """
        Assigns continent names to country names in a DataFrame based on a mapping.

        Args:
            df: pandas.DataFrame
            left_col_name: str - The name of the column containing country names.
            new_col_name: str - The name of the new column to store continent names.

        Returns:
            pandas.DataFrame - DataFrame with the new column added containing continent names.

        Raises:
            KeyError: If left_col_name does not exist in the DataFrame.
            ValueError: If the column specified by left_col_name does not contain string values representing country names.
        """
        if left_col_name not in df.columns:
            raise KeyError(f"Column '{left_col_name}' does not exist in the DataFrame.")

        if df[left_col_name].dtype != object:
            raise ValueError(
                f"Column '{left_col_name}' must contain string values representing country names."
            )

        df[new_col_name] = (
            df[left_col_name].map(self.country_to_continent).fillna("Unknown")
        )

        position = self.find_column_position(df, left_col_name) + 1
        df.insert(position, new_col_name, df.pop(new_col_name))

        return df
