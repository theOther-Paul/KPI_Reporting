import json
import pycountry as pc
import pycountry_convert as pconv
import pandas as pd
import os
from . import file_ops as fo


def country_to_continent(country_name):
    """
    The function `country_to_continent` converts a country name to its corresponding continent name.
    
    :param country_name: The function `country_to_continent` takes a `country_name` as input and
    attempts to convert it to a continent name. It uses the `pconv` module to perform the conversion. If
    the country name is not found or an error occurs during the conversion process, it returns "Unknown"
    :return: The function `country_to_continent` is returning the continent name for a given country
    name. If the country name is valid and can be converted to a continent name, it will return the
    continent name. If the country name is not found or cannot be converted, it will return "Unknown".
    """
    try:
        country_alpha2 = pconv.country_name_to_country_alpha2(country_name)
        country_continent_code = pconv.country_alpha2_to_continent_code(country_alpha2)
        return pconv.convert_continent_code_to_continent_name(country_continent_code)
    except LookupError:
        return "Unknown"


def make_map(df: pd.DataFrame):
    """
    The function `make_map` creates a dictionary mapping countries to their corresponding continents
    based on a DataFrame input.
    
    :param df: A pandas DataFrame containing a column named "country" which stores the names of
    countries
    :type df: pd.DataFrame
    :return: The function `make_map` takes a pandas DataFrame as input, extracts unique country names
    from the "country" column of the DataFrame, and then creates a list of lists where each sublist
    contains a country name and its corresponding continent (retrieved using the `country_to_continent`
    function). If the continent for a country cannot be found (KeyError), it assigns "Unknown" as the
    continent
    """
    clist = df["country"].unique().tolist()
    cont_list = []

    for i in clist:
        try:
            cont_list.append([i, country_to_continent(i)])
        except KeyError:
            cont_list.append([i, "Unknown"])
    return dict(cont_list)


def memo_map(map_file="mapping\\markets.json"):
    """
    The function `memo_map` writes a JSON file containing a map generated from data prepared by
    `FilePrep` class, handling exceptions by writing to a different file if necessary.
    
    :param map_file: The `map_file` parameter is a file path that specifies the location where the
    mapping data will be stored or retrieved from. In this case, the default value for `map_file` is set
    to "mapping\markets.json", defaults to mapping\markets.json (optional)
    """
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
        """
        The function `find_column_position` returns the position of a specified column in a DataFrame if it
        exists.
        
        :param df: A pandas DataFrame containing the data
        :param column_name: The `column_name` parameter is the name of the column in a pandas DataFrame for
        which you want to find the position or index
        :return: The function `find_column_position` returns the position (index) of the specified
        `column_name` in the DataFrame `df` if the column exists in the DataFrame. If the column does not
        exist in the DataFrame, it returns `None`.
        """
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
