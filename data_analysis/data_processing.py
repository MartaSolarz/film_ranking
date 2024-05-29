"""Load and process the data from the CSV file."""
import pandas as pd


def load_and_process_data(file_path: str) -> pd.DataFrame:
    """
    Load and process the data from the CSV file.

    :param file_path: str: Path to the CSV file with the data

    :return: pd.DataFrame: Processed data
    """
    data = pd.read_csv(file_path, sep='\t', low_memory=False)

    clean_data(data)

    return data


def clean_data(data: pd.DataFrame) -> None:
    """
    Clean the data.

    :param data: pd.DataFrame: Data to process

    :return: None
    """

    # TODO: Implement the processing of the data
    data.dropna(inplace=True)


def merge_data(basics: pd.DataFrame, ratings: pd.DataFrame, crew: pd.DataFrame) -> pd.DataFrame:
    """
    Merge the data from the basics, ratings, and crew DataFrames.

    :param basics: pd.DataFrame: Data with basic information about the movies
    :param ratings: pd.DataFrame: Data with ratings of the movies
    :param crew: pd.DataFrame: Data with information about the crew of the movies

    :return: pd.DataFrame: Merged data from the basics, ratings, and crew DataFrames
    """
    merged_data = pd.merge(basics, ratings, on='tconst', how='inner')
    merged_data = pd.merge(merged_data, crew[['tconst', 'directors']], on='tconst', how='left')

    return merged_data
