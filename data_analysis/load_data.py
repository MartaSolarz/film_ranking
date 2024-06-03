"""Load the data from the files."""
import argparse
import logging
from typing import Dict

import pandas as pd
import numpy as np


def load_all_data(args: argparse.Namespace) -> Dict[str, pd.DataFrame]:
    """
    Load all the data from the files.

    :param args: argparse.Namespace: Arguments from the command line

    :return: Dict[str, pd.DataFrame]: Dictionary with the dataframes
    """
    dataframes = {}
    errors = []

    def load_data_wrapper(data_name: str, file_path: str) -> None:
        """
        Wrapper function to load the data and handle the exceptions.

        :param data_name: str: Name of the data
        :param file_path: str: Path to the file with the data

        :return: None
        """
        try:
            logging.info("Loading data for %s...", data_name)
            dataframes[data_name] = load_data(file_path)
        except FileNotFoundError as file_err:
            logging.error("File not found for %s: %s", data_name, str(file_err))
            errors.append(f"File not found for {data_name}: {str(file_err)}")
        except ValueError as val_err:
            logging.error("Invalid file format for %s: %s", data_name, str(val_err))
            errors.append(f"Invalid file format for {data_name}: {str(val_err)}")
        except Exception as exc_err:
            logging.error(
                "An error occurred during data loading for %s: %s",
                data_name, str(exc_err))
            errors.append(f"Error loading {data_name}: {str(exc_err)}")

    load_data_wrapper('basics', args.basics_title_data)
    load_data_wrapper('ratings', args.rating_title_data)
    load_data_wrapper('akas', args.akas_title_data)
    load_data_wrapper('crew', args.crew_title_data)
    load_data_wrapper('name', args.name_people_data)
    load_data_wrapper('countries', args.countries_name_data)
    load_data_wrapper('population', args.population_data)
    load_data_wrapper('gdp', args.gdp_data)

    if errors:
        logging.info("Data loading completed with errors:")
        for error in errors:
            logging.info(error)
    else:
        logging.info("All data loaded successfully.")

    return dataframes


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

    try:
        data = pd.read_csv(file_path, low_memory=False, na_values=[np.NAN, '\\N', '..'], sep=sep)
    except Exception as e:
        logging.error("Error loading data from %s: %s", file_path, str(e))
        raise

    if data.empty:
        logging.warning("The file %s is empty.", file_path)
        raise ValueError("The file is empty.")

    return data
