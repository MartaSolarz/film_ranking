"""Load and basic processing of the data."""
from typing import Tuple

import numpy as np
import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """
    Load the data from the CSV or TSV file.

    :param file_path: str: Path to the CSV  or TSV file with the data

    :return pd.DataFrame: Data from the file
    """
    if file_path.endswith('.tsv'):
        sep = '\t'
    elif file_path.endswith('.csv'):
        sep = ','
    else:
        raise ValueError("Invalid file format. Only CSV and TSV files are supported.")

    data = pd.read_csv(file_path, low_memory=False, na_values=[np.NAN, '\\N', '..'], sep=sep)

    return data


def process_data_and_merge(
        basics_df: pd.DataFrame,
        ratings_df: pd.DataFrame,
        akas_df: pd.DataFrame,
        countries_df: pd.DataFrame,
        population_df: pd.DataFrame,
        gdp_df: pd.DataFrame,
        start: int,
        end: int,
) -> pd.DataFrame:
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
    :param population_df: pd.DataFrame:
        Data with the population of the countries
    :param gdp_df: pd.DataFrame:
        Data with the GDP of the countries
    :param start: int: Start year for the filter
    :param end: int: End year for the filter

    :return: pd.DataFrame: Filtered and merged data
    """
    basics_df = basics_df[['tconst', 'titleType', 'primaryTitle', 'startYear']]
    ratings_df = ratings_df[['tconst', 'averageRating', 'numVotes']]
    akas_df = akas_df[['titleId', 'region']]
    akas_df = akas_df.dropna(subset=['region'])
    countries_df = countries_df[['alpha-2', 'alpha-3', 'name']]

    population_df = process_world_bank_data(population_df, 'Population')
    gdp_df = process_world_bank_data(gdp_df, 'GDP')

    basics_df, population_df, gdp_df = filter_years(basics_df, population_df, gdp_df, start, end)

    merged_df = merge_data(
        basics_df, ratings_df, akas_df, countries_df, population_df, gdp_df,
    )
    merged_df = clean(merged_df)

    return merged_df


def process_world_bank_data(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    """
    Process the World Bank data.

    :param df: pd.DataFrame: Dataframe with the World Bank data
    :param value_name: str: Name of the value column

    :return: pd.DataFrame: Processed data
    """
    df.drop(columns=['Series Name', 'Series Code', 'Country Name'], inplace=True)
    df = df.melt(id_vars=['Country Code'], var_name='Year', value_name=value_name)
    df['Year'] = df['Year'].map(lambda x: int(x[:5]))
    df.dropna(subset=['Country Code', value_name], inplace=True)

    return df


def filter_years(
        basics_df: pd.DataFrame,
        population_df: pd.DataFrame,
        gdp_df: pd.DataFrame,
        start_year: int,
        end_year: int,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Filter the data based on the start and end years.

    :param basics_df: pd.DataFrame: Data to filter
    :param population_df: pd.DataFrame: Data with the population of the countries
    :param gdp_df: pd.DataFrame: Data with the GDP of the countries
    :param start_year: int: Start year for the filter
    :param end_year: int: End year for the filter

    :return: Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]: Filtered data
    """
    basics_years = set(basics_df['startYear'].dropna().unique().astype(int))
    population_years = set(population_df['Year'].dropna().unique().astype(int))
    gdp_years = set(gdp_df['Year'].dropna().unique().astype(int))

    common_years = basics_years & population_years & gdp_years

    if start_year and end_year:
        common_years = common_years.intersection(range(start_year, end_year + 1))

    if not common_years:
        raise ValueError("No common years found between the datasets.")

    basics_filtered = basics_df[basics_df['startYear'].isin(common_years)]
    population_filtered = population_df[population_df['Year'].isin(common_years)]
    gdp_filtered = gdp_df[gdp_df['Year'].isin(common_years)]

    return basics_filtered, population_filtered, gdp_filtered


def merge_data(
        basics_df: pd.DataFrame,
        ratings_df: pd.DataFrame,
        akas_df: pd.DataFrame,
        countries_df: pd.DataFrame,
        population_df: pd.DataFrame,
        gdp_df: pd.DataFrame,
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
    :param population_df: pd.DataFrame:
        Data with the population of the countries
    :param gdp_df: pd.DataFrame:
        Data with the GDP of the countries

    :return: pd.DataFrame: Merged data from the dataframes
    """
    merged_df = akas_df.merge(basics_df, left_on='titleId', right_on='tconst')
    merged_df = merged_df.merge(ratings_df, on='tconst')
    merged_df = merged_df.merge(countries_df, left_on='region', right_on='alpha-2')
    merged_df = merged_df.merge(population_df, left_on=['alpha-3', 'startYear'],
                                right_on=['Country Code', 'Year'])
    merged_df = merged_df.merge(gdp_df, left_on=['alpha-3', 'startYear'],
                                right_on=['Country Code', 'Year'])

    return merged_df


def clean(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the merged data.

    :param merged_df: pd.DataFrame: Merged data

    :return: pd.DataFrame: Cleaned data
    """
    merged_df = merged_df[merged_df['titleType'] == 'movie']
    merged_df = merged_df.drop(
        columns=['tconst', 'titleType', 'startYear', 'alpha-2', 'alpha-3',
                 'Country Code_x', 'Country Code_y', 'Year_y'],
    )
    merged_df.columns = ['titleId', 'region', 'title', 'averageRating', 'numVotes',
                         'countryName', 'year', 'population', 'gdp']
    merged_df = merged_df.drop_duplicates(
        subset=['region', 'titleId', 'year', 'averageRating', 'numVotes', 'population', 'gdp'],
        keep='first',
    )
    merged_df.set_index('titleId', inplace=True)

    return merged_df
