"""Perform analysis on the merged data."""
import pandas as pd


def perform_task_1(merged_df: pd.DataFrame, numbers=(10, 20, 50, 100, 200)) -> None:
    """
    Perform the task 1 analysis.

    :param merged_df: pd.DataFrame: Merged dataframe with the movie data
    :param numbers: tuple: Tuple with the numbers of top movies to consider
    :return: None
    """
    for n in numbers:
        top_n_ratings_df = get_top_n_movies_per_country(merged_df, n)
        top_n_ratings_df = top_n_ratings_df.sort_values(by='avg_rating', ascending=False)
        print('-' * 50)
        print(f"Top 10 countries based on top {n} films: ")
        print(top_n_ratings_df.head(10))


def get_top_n_movies_per_country(movies_df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Get the average rating of the top n movies per country.
    In case of same rating, the number of votes is used as a tiebreaker.
    The process takes into account only countries with at least n movies
    (in order to have comparable and fair rankings)

    :param movies_df: pd.DataFrame: Dataframe with the movies data
    :param n: int: Number of top movies to choose per country

    :return: pd.DataFrame: Dataframe with the average rating of the top n movies per country
    """
    country_movie_counts = movies_df['region'].value_counts()
    countries_with_at_least_n_films = country_movie_counts[country_movie_counts >= n].index
    valid_df = movies_df[movies_df['region'].isin(countries_with_at_least_n_films)]
    valid_df = valid_df.sort_values(
        by=['countryName', 'region', 'averageRating', 'numVotes'],
        ascending=[True, True, False, False],
    )

    top_n_movies_df = valid_df.groupby('region').head(n)
    top_n_ratings_df = top_n_movies_df.groupby(['countryName', 'region']).agg({
        'averageRating': 'mean',
        'numVotes': 'sum',
        'title': 'count'
    }).reset_index()

    top_n_ratings_df.columns = [
        'country_name', 'country_code', 'avg_rating', 'total_votes', 'film_count',
    ]
    return top_n_ratings_df
