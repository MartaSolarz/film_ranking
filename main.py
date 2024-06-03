"""Main file to start the data analysis app."""
import argparse
import logging

from app import app

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
        app.run(parser.parse_args())
    except Exception as e:
        logging.critical("An unexpected error occurred: %s", str(e))
