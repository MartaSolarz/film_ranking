"""Perform analysis on the merged data."""
import pandas as pd

PATH_TO_SAVE_RESULTS = "./results"


def perform_task_1(merged_df: pd.DataFrame, numbers=(10, 20, 50, 100, 200)) -> None:
    """
    Perform the task 1 analysis.

    :param merged_df: pd.DataFrame: Merged dataframe with the movie data
    :param numbers: tuple: Tuple with the numbers of top movies to consider
    :return: None
    """
    start_year = merged_df['year'].min()
    end_year = merged_df['year'].max()

    print('----- Results for Task 1: -----')
    for n in numbers:
        top_n_ratings_df = get_top_n_movies_per_country(merged_df, n)
        top_n_ratings_df = top_n_ratings_df.sort_values(by='avg_rating', ascending=False)
        top_n_ratings_df.to_csv(
            f'{PATH_TO_SAVE_RESULTS}/top_{n}_ratings_{start_year}_{end_year}.csv',
            index=False)
        print('-' * 50)
        print(f"Top 10 countries based on top {n} films: ")
        print(top_n_ratings_df.head(10))

    print('\nThe full results are saved in the results folder.')


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
    country_movie_counts = movies_df['country_code'].value_counts()
    countries_with_at_least_n_films = country_movie_counts[country_movie_counts >= n].index
    valid_df = movies_df[movies_df['country_code'].isin(countries_with_at_least_n_films)]
    valid_df = valid_df.sort_values(
        by=['country_name', 'country_code', 'average_rating', 'num_of_votes'],
        ascending=[True, True, False, False],
    )

    top_n_movies_df = valid_df.groupby('country_code').head(n)
    top_n_ratings_df = top_n_movies_df.groupby(['country_name', 'country_code']).agg({
        'average_rating': 'mean',
        'num_of_votes': 'sum',
        'title': 'count'
    }).reset_index()

    top_n_ratings_df.columns = [
        'country_name', 'country_code', 'avg_rating', 'total_votes', 'film_count',
    ]
    return top_n_ratings_df


def perform_task_2(merged_df: pd.DataFrame) -> None:
    """
    Perform the task 2 analysis.

    :param merged_df: pd.DataFrame: Merged dataframe with the movie data
    :return: None
    """
    impact_df = calculate_impact_metrics(merged_df)
    rank_df = create_rank_dataframe(impact_df, merged_df)

    start_year = merged_df['year'].min()
    end_year = merged_df['year'].max()

    # Compute hegemony for population
    hegemony_pop_df = compute_hegemony(rank_df, 'population', 'pop_rank')
    hegemony_pop_df.to_csv(
        f'{PATH_TO_SAVE_RESULTS}/hegemony_pop_result_{start_year}_{end_year}.csv',
        index=False)

    # Compute hegemony for GDP
    hegemony_gdp_df = compute_hegemony(rank_df, 'gdp', 'gdp_rank')
    hegemony_gdp_df.to_csv(
        f'{PATH_TO_SAVE_RESULTS}/hegemony_gdp_result_{start_year}_{end_year}.csv',
        index=False)

    # Compute hegemony for GDP per population
    hegemony_gdp_per_pop_df = compute_hegemony(
        rank_df, 'gdp_per_population', 'gdp_per_population_rank',
    )
    hegemony_gdp_per_pop_df.to_csv(
        f'{PATH_TO_SAVE_RESULTS}/hegemony_gdp_per_pop_result_{start_year}_{end_year}.csv',
        index=False)

    hegemony_pop_weak_df = (hegemony_pop_df[['Country Name', 'Weak Hegemony Indicator',
                                             'Country Population Rank', 'Weak Impact Rank']].
                            sort_values(by='Weak Hegemony Indicator', ascending=False))
    hegemony_pop_strong_df = (hegemony_pop_df[['Country Name', 'Strong Hegemony Indicator',
                                               'Country Population Rank', 'Strong Impact Rank']].
                              sort_values(by='Strong Hegemony Indicator', ascending=False))

    hegemony_gdp_weak_df = (hegemony_gdp_df[['Country Name', 'Weak Hegemony Indicator',
                                             'Country GDP Rank', 'Weak Impact Rank']].
                            sort_values(by='Weak Hegemony Indicator', ascending=False))
    hegemony_gdp_strong_df = (hegemony_gdp_df[['Country Name', 'Strong Hegemony Indicator',
                                               'Country GDP Rank', 'Strong Impact Rank']].
                              sort_values(by='Strong Hegemony Indicator', ascending=False))

    hegemony_gdp_per_pop_weak_df = (hegemony_gdp_per_pop_df[
                                        ['Country Name', 'Weak Hegemony Indicator',
                                         'Country GDP per Population Rank', 'Weak Impact Rank']].
                                    sort_values(by='Weak Hegemony Indicator', ascending=False))
    hegemony_gdp_per_pop_strong_df = (hegemony_gdp_per_pop_df[
                                          ['Country Name', 'Strong Hegemony Indicator',
                                           'Country GDP per Population Rank',
                                           'Strong Impact Rank']].
                                      sort_values(by='Strong Hegemony Indicator', ascending=False))

    print('----- Results for Task 2: -----')
    print('-' * 50)
    print('Top 10 countries with the highest weak population hegemony:')
    print(hegemony_pop_weak_df.head(10))
    print('-' * 50)
    print('Top 10 countries with the highest strong population hegemony:')
    print(hegemony_pop_strong_df.head(10))
    print('-' * 50)
    print('Top 10 countries with the highest weak GDP hegemony:')
    print(hegemony_gdp_weak_df.head(10))
    print('-' * 50)
    print('Top 10 countries with the highest strong GDP hegemony:')
    print(hegemony_gdp_strong_df.head(10))
    print('-' * 50)
    print('Top 10 countries with the highest weak GDP per population hegemony:')
    print(hegemony_gdp_per_pop_weak_df.head(10))
    print('-' * 50)
    print('Top 10 countries with the highest strong GDP per population hegemony:')
    print(hegemony_gdp_per_pop_strong_df.head(10))

    print('\nThe full results are saved in the results folder.')


def calculate_impact_metrics(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weak impact and strong impact metrics.

    :param merged_df: pd.DataFrame: Merged data
    :return: pd.DataFrame: Data with impact metrics
    """
    impact_df = merged_df.groupby(['country_name', 'country_code']).agg(
        weak_impact=('num_of_votes', 'sum'),
        strong_impact=('average_rating', 'mean')
    ).reset_index()

    return impact_df


def create_rank_dataframe(impact_df: pd.DataFrame, merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a dataframe with the ranks of the impact metrics.

    :param impact_df: pd.DataFrame: Data with impact metrics
    :param merged_df: pd.DataFrame: Merged data

    :return: pd.DataFrame: Data with adjusted impact metrics
    """
    population_gdp_df = (merged_df[['country_code', 'population', 'gdp', 'gdp_per_population']].
                         drop_duplicates('country_code'))

    # Merge once with population and GDP data
    impact_df = impact_df.merge(population_gdp_df, on='country_code', how='left')

    impact_df['weak_impact_rank'] = impact_df['weak_impact'].rank(ascending=False).astype(int)
    impact_df['strong_impact_rank'] = impact_df['strong_impact'].rank(ascending=False).astype(int)
    impact_df['gdp_rank'] = impact_df['gdp'].rank(ascending=False).astype(int)
    impact_df['pop_rank'] = impact_df['population'].rank(ascending=False).astype(int)
    impact_df['gdp_per_population_rank'] = (impact_df['gdp_per_population'].
                                            rank(ascending=False).astype(int))

    return impact_df[['country_name', 'country_code', 'weak_impact_rank', 'strong_impact_rank',
                      'gdp_rank', 'pop_rank', 'gdp_per_population_rank']]


def compute_hegemony(rank_df: pd.DataFrame, rank_type: str, rank_column: str) -> pd.DataFrame:
    """
    Compute the hegemony metrics for the specified rank type.

    :param rank_df: pd.DataFrame: Data with the ranks of the impact metrics
    :param rank_type: str:
        Type of the rank ('population', 'gdp', 'gdp_per_population')
    :param rank_column: str:
        Name of the column for the rank ('pop_rank', 'gdp_rank', 'gdp_per_population_rank')

    :return: pd.DataFrame: Dataframe with the hegemony metrics for the specified rank type
    """
    df = rank_df[['country_name', rank_column, 'weak_impact_rank', 'strong_impact_rank']].copy()
    df[f'weak_{rank_type}_hegemony'] = df[rank_column] - df['weak_impact_rank']
    df[f'strong_{rank_type}_hegemony'] = df[rank_column] - df['strong_impact_rank']

    df.columns = ['Country Name', f'Country {rank_type.capitalize()} Rank',
                  'Weak Impact Rank', 'Strong Impact Rank',
                  f'Weak {rank_type.capitalize()} Hegemony Indicator',
                  f'Strong {rank_type.capitalize()} Hegemony Indicator']

    return df
