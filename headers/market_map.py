import json
import pycountry as pc
import pandas as pd
import os


class CountryMapper:
    def __init__(self, json_file="mapping\\markets.json"):
        # Load the country to continent mapping from the JSON file
        try:
            with open(json_file, "r") as f:
                self.country_to_continent = json.load(f)
        except Exception as e:
            p2f = os.getcwd() + "\\headers\\" + json_file
            with open(p2f, "r") as f:
                self.country_to_continent = json.load(f)

    def country_name_to_alpha2(self, country_name):
        """Convert country name to its alpha-2 code."""
        try:
            country = pc.countries.lookup(country_name)
            return country.alpha_2
        except LookupError:
            return None

    def country_name_to_continent(self, country_name):
        """Map country name to continent using alpha-2 code."""
        alpha2 = self.country_name_to_alpha2(country_name)
        if alpha2:
            return self.country_to_continent.get(alpha2, "Unknown")
        return "Unknown"

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
