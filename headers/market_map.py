import json
import pycountry as pc
import pycountry_convert as pconv
import pandas as pd
import os
from . import file_ops as fo


def country_to_continent(country_name):
    country_alpha2 = pconv.country_name_to_country_alpha2(country_name)
    country_continent_code = pconv.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pconv.convert_continent_code_to_continent_name(
        country_continent_code
    )
    return country_continent_name


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
        if len(p2f) != 0:
            with open(p2f, "r") as f:
                self.country_to_continent = json.load(f)
        else:
            memo_map()
            return self.__init__()

    def find_column_position(self, df, column_name):
        """
        Find the position (index) of a column in the DataFrame.

        Parameters:
        - df: The DataFrame to search.
        - column_name: The name of the column to find.

        Returns:
        - The index of the column, or None if the column does not exist.
        """
        if column_name in df.columns:
            return df.columns.get_loc(column_name)
        return None

    def assign_continent(self, df, left_col_name, new_col_name):
        if left_col_name not in df.columns:
            raise KeyError(f"Column '{left_col_name}' does not exist in the DataFrame.")

        df[new_col_name] = df[left_col_name].apply(self.country_name_to_continent)

        position = self.find_column_position(df, left_col_name) + 1

        df = pd.concat(
            [df.iloc[:, :position], df[[new_col_name]], df.iloc[:, position + 1 :]],
            axis=1,
        )

        return df
