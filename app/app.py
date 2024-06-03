"""App module to run the film data analysis app."""
import argparse
import cProfile
import pstats
import logging

import pandas as pd

import data_analysis.data_processing as dp
from data_analysis.analysis import perform_task_1, perform_task_2, perform_task_3
from data_analysis.load_data import load_all_data


def save_profile(profiler: cProfile.Profile, output_file='./profile/profile_results.txt'):
    """
    Save the profile results to a file.

    :param profiler: cProfile.Profile: Profiler object
    :param output_file: str: Path to the output file

    :return: None
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.sort_stats('cumulative')
        stats.print_stats()


def run(args: argparse.Namespace) -> None:
    """
    Main function to run the film data analysis app.

    :param args: argparse.Namespace: Arguments from the command line
    :return: None
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    logging.info("Starting the data analysis app with profiler...")

    profiler = cProfile.Profile()
    profiler.enable()

    logging.info("Loading all data...")
    dataframes = load_all_data(args)

    empty_df = pd.DataFrame()
    basics = dataframes.get('basics', empty_df)
    ratings = dataframes.get('ratings', empty_df)
    akas = dataframes.get('akas', empty_df)
    crew = dataframes.get('crew', empty_df)
    name = dataframes.get('name', empty_df)
    countries = dataframes.get('countries', empty_df)
    population = dataframes.get('population', empty_df)
    gdp = dataframes.get('gdp', empty_df)

    try:
        logging.info("Processing data...")
        merged_data = dp.process_data_and_merge(
            basics, ratings, akas, crew, name,
            countries, population, gdp, args.start, args.end,
        )
    except Exception as exc_err:
        logging.error("An error occurred during data processing: %s", str(exc_err))
        merged_data = pd.DataFrame()

    try:
        logging.info("Performing analysis...")
        perform_task_1(merged_data)
        perform_task_2(merged_data)
        perform_task_3(merged_data)
    except KeyError as key_err:
        logging.error("Key error: %s", str(key_err))
    except Exception as exc_err:
        logging.error("An error occurred during data analysis: %s", str(exc_err))

    profiler.disable()

    logging.info("Saving profile results...")
    save_profile(profiler)

    logging.info("Successfully finished the data analysis app!")
