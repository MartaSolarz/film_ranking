"""Perform analysis on the merged data."""
import pandas as pd

PATH_TO_SAVE_RESULTS = "./results"
MARGIN = 100
NUM_OF_FILMS_TO_PROCESS = (10, 20, 50, 100, 200)


def perform_task_1(merged_df: pd.DataFrame) -> None:
    """
    Perform the task 1 analysis.

    :param merged_df: pd.DataFrame: Merged dataframe with the movie data

    :return: None
    """
    start_year = merged_df['year'].min()
    end_year = merged_df['year'].max()

    print('----- Results for Task 1: -----')
    for n in NUM_OF_FILMS_TO_PROCESS:
        top_n_ratings_df = get_top_n_movies_per_country(merged_df, n)
        top_n_ratings_df = top_n_ratings_df.sort_values(by='avg_rating', ascending=False)
        top_n_ratings_df.to_csv(
            f'{PATH_TO_SAVE_RESULTS}/1_top_{n}_ratings_{start_year}_{end_year}.csv',
            index=False)
        print('-' * MARGIN)
        print(f"Top 10 countries based on top {n} films: ")
        print(top_n_ratings_df.head(10))

    print('\nThe full results are saved in the results folder.')


def get_top_n_movies_per_country(movies_df: pd.DataFrame, n: int) -> pd.DataFrame:
    """
    Get the average rating of the top n movies per country.
    In the case of the same rating, the number of votes is used as a tiebreaker.
    The process takes into account only countries with at least n movies
    (to have comparable and fair rankings)

    :param movies_df: Pd.DataFrame: Dataframe with the movies data
    :param n: int: Number of top movies to choose per country

    :return: Pd.DataFrame: Dataframe with the average rating of the top n movies per country
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
        f'{PATH_TO_SAVE_RESULTS}/2_hegemony_pop_result_{start_year}_{end_year}.csv',
        index=False)

    # Compute hegemony for GDP
    hegemony_gdp_df = compute_hegemony(rank_df, 'gdp', 'gdp_rank')
    hegemony_gdp_df.to_csv(
        f'{PATH_TO_SAVE_RESULTS}/2_hegemony_gdp_result_{start_year}_{end_year}.csv',
        index=False)

    # Compute hegemony for GDP per population
    hegemony_gdp_per_pop_df = compute_hegemony(
        rank_df, 'gdp_per_population', 'gdp_per_population_rank',
    )
    hegemony_gdp_per_pop_df.to_csv(
        f'{PATH_TO_SAVE_RESULTS}/2_hegemony_gdp_per_pop_result_{start_year}_{end_year}.csv',
        index=False)

    hegemony_pop_weak_df = (hegemony_pop_df[['Country Name', 'Weak Hegemony Indicator',
                                             'Country Population Rank', 'Weak Impact Rank']].
                            sort_values(by='Weak Hegemony Indicator', ascending=False))
    hegemony_pop_strong_df = (hegemony_pop_df[['Country Name', 'Strong Hegemony Indicator',
                                               'Country Population Rank', 'Strong Impact Rank']].
                              sort_values(by='Strong Hegemony Indicator', ascending=False))

    hegemony_gdp_weak_df = (hegemony_gdp_df[['Country Name', 'Weak Hegemony Indicator',
                                             'Country Gdp Rank', 'Weak Impact Rank']].
                            sort_values(by='Weak Hegemony Indicator', ascending=False))
    hegemony_gdp_strong_df = (hegemony_gdp_df[['Country Name', 'Strong Hegemony Indicator',
                                               'Country Gdp Rank', 'Strong Impact Rank']].
                              sort_values(by='Strong Hegemony Indicator', ascending=False))

    hegemony_gdp_per_pop_weak_df = (hegemony_gdp_per_pop_df[
                                        ['Country Name', 'Weak Hegemony Indicator',
                                         'Country GdpPerPopulation Rank', 'Weak Impact Rank']].
                                    sort_values(by='Weak Hegemony Indicator', ascending=False))
    hegemony_gdp_per_pop_strong_df = (hegemony_gdp_per_pop_df[
                                          ['Country Name', 'Strong Hegemony Indicator',
                                           'Country GdpPerPopulation Rank',
                                           'Strong Impact Rank']].
                                      sort_values(by='Strong Hegemony Indicator', ascending=False))

    print('----- Results for Task 2: -----')
    print('-' * MARGIN)
    print('Top 10 countries with the highest weak population hegemony:')
    print(hegemony_pop_weak_df.head(10))
    print('-' * MARGIN)
    print('Top 10 countries with the highest strong population hegemony:')
    print(hegemony_pop_strong_df.head(10))
    print('-' * MARGIN)
    print('Top 10 countries with the highest weak GDP hegemony:')
    print(hegemony_gdp_weak_df.head(10))
    print('-' * MARGIN)
    print('Top 10 countries with the highest strong GDP hegemony:')
    print(hegemony_gdp_strong_df.head(10))
    print('-' * MARGIN)
    print('Top 10 countries with the highest weak GDP per population hegemony:')
    print(hegemony_gdp_per_pop_weak_df.head(10))
    print('-' * MARGIN)
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

    df.columns = ['Country Name',
                  f'Country {"".join(x.capitalize() for x in rank_type.split("_"))} Rank',
                  'Weak Impact Rank', 'Strong Impact Rank',
                  'Weak Hegemony Indicator', 'Strong Hegemony Indicator']

    return df


def perform_task_3(merged_df: pd.DataFrame) -> None:
    """
    Perform the task 3 analysis.

    :param merged_df: pd.DataFrame: Merged dataframe with the movie data

    :return: None
    """
    merged_df.dropna(subset=['director_name', 'director_id'], inplace=True)

    film_counts = merged_df['director_id'].value_counts()

    start_year = merged_df['year'].min()
    end_year = merged_df['year'].max()

    print('----- Results for Task 3: -----')
    for n in NUM_OF_FILMS_TO_PROCESS:
        eligible_directors = film_counts[film_counts >= n].index
        if not eligible_directors.any():
            print(f"No directors with at least {n} films found in specified time range.")
            continue

        career_progression = calculate_career_progression(merged_df, n, eligible_directors)

        res_rating = career_progression[
            ['directors', 'first_avg_rating', 'last_avg_rating', 'rating_diff']
        ].sort_values(
            by='rating_diff', ascending=False)
        res_rating.columns = ['Director', 'First Average Rating',
                              'Last Average Rating', 'Career Progression Rating']
        res_rating.to_csv(
            f'{PATH_TO_SAVE_RESULTS}/3_rating_diff_{n}_{start_year}_{end_year}.csv', index=False,
        )

        res_votes = career_progression[
            ['directors', 'first_num_of_votes', 'last_num_of_votes', 'votes_diff']
        ].sort_values(
            by='votes_diff', ascending=False)
        res_votes.columns = ['Director', 'First Number of Votes',
                             'Last Number of Votes', 'Career Progression Number of Votes']
        res_votes.to_csv(
            f'{PATH_TO_SAVE_RESULTS}/3_votes_diff_{n}_{start_year}_{end_year}.csv', index=False,
        )

        print('-' * MARGIN)
        print(f"Top 10 directors based on rating difference for {n} film adaptations: ")
        print(res_rating.head(10))

        print(f"Top 10 directors based on votes difference for {n} film adaptations: ")
        print(res_votes.head(10))

    print('\nThe full results are saved in the results folder.')


def calculate_career_progression(
        merged_df: pd.DataFrame, n: int, eligible_directors: pd.Series,
) -> pd.DataFrame:
    """
    Calculate the career progression of the directors
    based on the average rating and the number of votes.

    :param merged_df: pd.DataFrame: Merged data
    :param n: int: Number of films to consider
    :param eligible_directors: pd.Series: Series with the eligible directors

    :return: pd.DataFrame: Dataframe with the career progression of the directors
    """
    director_films = merged_df[merged_df['director_id'].isin(eligible_directors)]
    director_films = director_films.sort_values(by=['director_id', 'year'])

    first_films = director_films.groupby('director_id').head(n / 2)
    last_films = director_films.groupby('director_id').tail(n / 2)

    first_stats = first_films.groupby('director_name').agg({
        'average_rating': 'mean',
        'num_of_votes': 'sum'
    }).reset_index()
    first_stats.columns = ['directors', 'first_avg_rating', 'first_num_of_votes']

    last_stats = last_films.groupby('director_name').agg({
        'average_rating': 'mean',
        'num_of_votes': 'sum'
    }).reset_index()
    last_stats.columns = ['directors', 'last_avg_rating', 'last_num_of_votes']

    progression = first_stats.merge(last_stats, on='directors')
    progression['rating_diff'] = progression['last_avg_rating'] - progression['first_avg_rating']
    progression['votes_diff'] = progression['last_num_of_votes'] - progression['first_num_of_votes']

    return progression
