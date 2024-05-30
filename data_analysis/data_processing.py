"""Load and basic processing of the data."""
import sys
from typing import Tuple

import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the data from the CSV file.

    :param file_path: str: Path to the CSV file with the data

    :return pd.DataFrame: Data from the CSV file
    """
    if file_path.endswith('.tsv'):
        sep = '\t'
    elif file_path.endswith('.csv'):
        sep = ','
    else:
        raise ValueError("Invalid file format. Only CSV and TSV files are supported.")

    data = pd.read_csv(file_path, low_memory=False, na_values='\\N', sep=sep)

    return data


def filter_years(data: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """
    Filter the data based on the start and end years.

    :param data: pd.DataFrame: Data to filter
    :param start_year: int: Start year for the filter
    :param end_year: int: End year for the filter

    :return: pd.DataFrame: Filtered data
    """
    common_years = set(data['startYear'].dropna().unique().astype(int))

    if start_year and end_year:
        common_years = common_years.intersection(range(start_year, end_year + 1))

    if not common_years:
        raise ValueError("No common years found between the datasets.")

    processed_data = data[data['startYear'].isin(common_years)]

    return processed_data


def keep_interesting_columns(
        basics_df: pd.DataFrame,
        ratings_df: pd.DataFrame,
        akas_df: pd.DataFrame,
        countries_df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Filter the dataframes to keep only the interesting columns.

    :param basics_df: pd.DataFrame:
        Data with basic information about the movies
    :param ratings_df: pd.DataFrame:
        Data with ratings of the movies
    :param akas_df: pd.DataFrame:
        Data with information about the different regions where the movies were presented
    :param countries_df: pd.DataFrame:
        Data with information about the names of the countries based on the region codes

    :return: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]: Filtered dataframes
    """
    basics_df = basics_df[['tconst', 'titleType', 'primaryTitle', 'startYear']]
    ratings_df = ratings_df[['tconst', 'averageRating', 'numVotes']]
    akas_df = akas_df[['titleId', 'region']]
    countries_df = countries_df[['alpha-2', 'name']]

    return basics_df, ratings_df, akas_df, countries_df


def merge_and_clean_data(
        basics_df: pd.DataFrame,
        ratings_df: pd.DataFrame,
        akas_df: pd.DataFrame,
        countries_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Merge the data from the dataframes.

    :param basics_df: pd.DataFrame:
        Data with basic information about the movies
    :param ratings_df: pd.DataFrame:
        Data with ratings of the movies
    :param akas_df: pd.DataFrame:
        Data with information about the different regions where the movies were presented
    :param countries_df: pd.DataFrame:
        Data with information about the names of the countries based on the region codes

    :return: pd.DataFrame: Merged data from the dataframes
    """
    merged_df = akas_df.merge(basics_df, left_on='titleId', right_on='tconst')
    merged_df = merged_df.merge(ratings_df, on='tconst')
    merged_df = merged_df.merge(countries_df, left_on='region', right_on='alpha-2')

    return clean(merged_df)


def clean(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the merged data.

    :param merged_df: pd.DataFrame: Merged data

    :return: pd.DataFrame: Cleaned data
    """
    merged_df = merged_df[merged_df['titleType'] == 'movie']
    merged_df = merged_df.dropna(subset=['region'])
    merged_df = merged_df.drop_duplicates(
        subset=['region', 'tconst', 'startYear', 'averageRating', 'numVotes'],
        keep='first',
    )

    return merged_df
