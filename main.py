"""Main script to run the data analysis app."""
import argparse
import cProfile
import pstats
import logging

import data_analysis.data_processing as dp
from data_analysis.analysis import perform_task_1


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

    logging.info("Loading data...")
    basics = dp.load_data(args.basics_title_data)
    ratings = dp.load_data(args.rating_title_data)
    akas = dp.load_data(args.akas_title_data)
    countries = dp.load_data(args.countries_name_data)
    population = dp.load_data(args.population_data)
    gdp = dp.load_data(args.gdp_data)

    logging.info("Processing data...")
    merged_data = dp.process_data_and_merge(
        basics, ratings, akas, countries, population, gdp,
        args.start, args.end,
    )

    logging.info("Performing analysis...")
    perform_task_1(merged_data)

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
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except KeyError as e:
        print(f"Column not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
