# Main file to run the app
import argparse
import cProfile
import pstats

from data_analysis.data_processing import load_and_process_data, merge_data


def save_profile(profiler: cProfile.Profile, output_file='profile_results.txt'):
    """
    Save the profile results to a file.

    :param profiler: cProfile.Profile: Profiler object
    :param output_file: str: Path to the output file

    :return: None
    """
    with open(output_file, 'w') as f:
        stats = pstats.Stats(profiler, stream=f)
        stats.sort_stats('cumulative')
        stats.print_stats()


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    parser = argparse.ArgumentParser('App to analyze cinematic impact')
    parser.add_argument('film_data', help='Path to the film data in CSV file')
    parser.add_argument('ranking_film_data', help='Path to the ranking film data in CSV file')
    parser.add_argument('crew_data', help='Path to the crew data in CSV file')
    parser.add_argument('-start', type=int, default=1960, help='Start year for analysis')
    parser.add_argument('-end', type=int, default=2024, help='End year for analysis')

    args = parser.parse_args()

    films_df = load_and_process_data(args.film_data)
    ranking_films_df = load_and_process_data(args.ranking_film_data)
    crew_df = load_and_process_data(args.crew_data)

    merged_data = merge_data(films_df, ranking_films_df, crew_df)

    profiler.disable()

    print(merged_data.sample(2))


if __name__ == '__main__':
    main()
