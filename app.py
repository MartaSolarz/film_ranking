"""Main script to run the data analysis app."""
import argparse
import cProfile
import pstats
import logging

import data_analysis.data_processing as dp
from data_analysis.analysis import perform_task_1, perform_task_2, perform_task_3


def save_profile(profiler: cProfile.Profile, output_file='profile_results.txt'):
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


def main(args: argparse.Namespace) -> None:
    """
    Main function to run the film data analysis app.

    :param args: argparse.Namespace: Arguments from the command line
    :return: None
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')
    logging.info("Starting the data analysis app with profiler...")

    profiler = cProfile.Profile()
    profiler.enable()

    try:
        logging.info("Loading data...")
        basics = dp.load_data(args.basics_title_data)
        ratings = dp.load_data(args.rating_title_data)
        akas = dp.load_data(args.akas_title_data)
        crew = dp.load_data(args.crew_title_data)
        name = dp.load_data(args.name_people_data)
        countries = dp.load_data(args.countries_name_data)
        population = dp.load_data(args.population_data)
        gdp = dp.load_data(args.gdp_data)
    except FileNotFoundError as file_err:
        logging.error("File not found: %s", str(file_err))
        return
    except ValueError as val_err:
        logging.error("Invalid file format: %s", str(val_err))
        return
    except Exception as exc_err:
        logging.error("An error occurred during data loading: %s", str(exc_err))
        return

    try:
        logging.info("Processing data...")
        merged_data = dp.process_data_and_merge(
            basics, ratings, akas, crew, name,
            countries, population, gdp, args.start, args.end,
        )
    except Exception as exc_err:
        logging.error("An error occurred during data processing: %s", str(exc_err))
        return

    try:
        logging.info("Performing analysis...")
        perform_task_1(merged_data)
        perform_task_2(merged_data)
        perform_task_3(merged_data)
    except KeyError as key_err:
        logging.error("Key error: %s", str(key_err))
        return
    except Exception as exc_err:
        logging.error("An error occurred during data analysis: %s", str(exc_err))
        return

    profiler.disable()

    logging.info("Saving profile results...")
    save_profile(profiler)

    logging.info("Successfully finished the data analysis app!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Film data analysis app')
    parser.add_argument('basics_title_data',
                        help='Path to the basics title data in CSV or TSV file')
    parser.add_argument('rating_title_data',
                        help='Path to the ranking title data in CSV or TSV file')
    parser.add_argument('akas_title_data',
                        help='Path to the title akas data in CSV or TSV file')
    parser.add_argument('crew_title_data',
                        help='Path to the crew title data in CSV or TSV file')
    parser.add_argument('name_people_data',
                        help='Path to the name people data in CSV or TSV file')
    parser.add_argument('countries_name_data',
                        help='Path to the countries name data in CSV or TSV file')
    parser.add_argument('population_data',
                        help='Path to the population data in CSV or TSV file')
    parser.add_argument('gdp_data',
                        help='Path to the GDP data in CSV or TSV file')
    parser.add_argument('-start', type=int, default=None, help='Start year for analysis')
    parser.add_argument('-end', type=int, default=None, help='End year for analysis')

    try:
        main(parser.parse_args())
    except Exception as e:
        logging.critical("An unexpected error occurred: %s", str(e))
