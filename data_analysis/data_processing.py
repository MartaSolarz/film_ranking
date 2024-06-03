"""Basic processing of the data."""
from typing import Tuple
import logging

import pandas as pd


def process_data_and_merge(
        basics_df: pd.DataFrame,
        ratings_df: pd.DataFrame,
        akas_df: pd.DataFrame,
        crew_df: pd.DataFrame,
        name_df: pd.DataFrame,
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
    :param crew_df: pd.DataFrame:
        Data with information about the crew of the movies
    :param name_df: pd.DataFrame:
        Data with information about the names of the people
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
    try:
        basics_df = basics_df[['tconst', 'titleType', 'primaryTitle', 'startYear']]
    except KeyError as e:
        logging.error("Error selecting columns from basics_df: %s", str(e))
    try:
        ratings_df = ratings_df[['tconst', 'averageRating', 'numVotes']]
    except KeyError as e:
        logging.error("Error selecting columns from ratings_df: %s", str(e))
    try:
        akas_df = akas_df[['titleId', 'region']]
        akas_df = akas_df.dropna(subset=['region'])
    except KeyError as e:
        logging.error("Error selecting columns from akas_df: %s", str(e))
    try:
        crew_df = crew_df.drop(columns=['writers'])
    except KeyError as e:
        logging.error("Error dropping columns from crew_df: %s", str(e))
    try:
        name_df = name_df[['nconst', 'primaryName']]
    except KeyError as e:
        logging.error("Error selecting columns from name_df: %s", str(e))
    try:
        countries_df = countries_df[['alpha-2', 'alpha-3', 'name']]
    except KeyError as e:
        logging.error("Error selecting columns from countries_df: %s", str(e))

    try:
        population_df = process_world_bank_data(population_df, 'Population')
    except Exception as e:
        logging.error("Error processing population_df: %s", str(e))
    try:
        gdp_df = process_world_bank_data(gdp_df, 'GDP')
    except Exception as e:
        logging.error("Error processing gdp_df: %s", str(e))

    try:
        basics_df, population_df, gdp_df = filter_years(
            basics_df, population_df, gdp_df, start, end,
        )
    except ValueError as e:
        logging.error("Error filtering the dataframes: %s", str(e))

    try:
        merged_df = merge_data(
            basics_df, ratings_df, akas_df, crew_df,
            name_df, countries_df, population_df, gdp_df,
        )
    except Exception as e:
        logging.error("Error merging the dataframes: %s", str(e))
        merged_df = pd.DataFrame()

    try:
        merged_df = clean(merged_df)
    except Exception as e:
        logging.error("Error cleaning the data: %s", str(e))

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
        crew_df: pd.DataFrame,
        name_df: pd.DataFrame,
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
    :param crew_df: pd.DataFrame:
        Data with information about the crew of the movies
    :param name_df: pd.DataFrame:
        Data with information about the names of the people
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
    merged_df = merged_df.merge(crew_df, on='tconst')
    merged_df = merged_df.merge(name_df, left_on='directors', right_on='nconst')
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
                 'Country Code_x', 'Country Code_y', 'Year_y', 'nconst'],
    )
    merged_df.rename(columns={'titleId': 'title_id', 'region': 'country_code',
                              'Year_x': 'year', 'primaryTitle': 'title', 'name': 'country_name',
                              'averageRating': 'average_rating', 'numVotes': 'num_of_votes',
                              'primaryName': 'director_name', 'directors': 'director_id',
                              'Population': 'population', 'GDP': 'gdp'}, inplace=True)
    merged_df = merged_df.drop_duplicates(
        subset=['country_code', 'title_id', 'year', 'average_rating', 'num_of_votes',
                'director_id', 'director_name', 'population', 'gdp'],
        keep='first',
    )
    merged_df['gdp_per_population'] = merged_df['gdp'] / merged_df['population']
    merged_df.set_index('title_id', inplace=True)

    return merged_df
