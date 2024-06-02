"""Tests for the analysis module."""
import pytest
import pandas as pd
import data_analysis.analysis as a


# Test the get_top_n_movies_per_country function

@pytest.fixture
def movies_data():
    """Create a DataFrame with basic data about movies."""
    data = {
        'title': ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5', 'Movie6', 'Movie7'],
        'country_code': ['US', 'US', 'US', 'FR', 'FR', 'FR', 'DE'],
        'country_name': ['United States', 'United States', 'United States',
                         'France', 'France', 'France', 'Germany'],
        'average_rating': [9.0, 8.5, 9.5, 8.0, 7.5, 9.0, 8.0],
        'num_of_votes': [100, 150, 200, 120, 80, 110, 90]
    }
    return pd.DataFrame(data)


def test_get_top_n_movies_per_country_basic(movies_data):
    """Test the function with basic data."""
    n = 2
    result = a.get_top_n_movies_per_country(movies_data, n)
    expected_data = {
        'country_name': ['France', 'United States'],
        'country_code': ['FR', 'US'],
        'avg_rating': [8.5, 9.25],
        'total_votes': [230, 300],
        'film_count': [2, 2]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_top_n_movies_per_country_single_country(movies_data):
    """Test the function with data for a single country."""
    n = 3
    result = a.get_top_n_movies_per_country(movies_data, n)
    expected_data = {
        'country_name': ['France', 'United States'],
        'country_code': ['FR', 'US'],
        'avg_rating': [8.166666666666666, 9.0],
        'total_votes': [310, 450],
        'film_count': [3, 3]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_top_n_movies_per_country_not_enough_movies(movies_data):
    """Test the function with not enough movies."""
    n = 4
    result = a.get_top_n_movies_per_country(movies_data, n)
    expected_data = {
        'country_name': [],
        'country_code': [],
        'avg_rating': [],
        'total_votes': [],
        'film_count': []
    }

    expected_df = pd.DataFrame(expected_data)
    expected_df.country_code = expected_df.country_code.astype('object')
    expected_df.country_name = expected_df.country_name.astype('object')
    expected_df.avg_rating = expected_df.avg_rating.astype('float64')
    expected_df.total_votes = expected_df.total_votes.astype('int64')
    expected_df.film_count = expected_df.film_count.astype('int64')

    pd.testing.assert_frame_equal(result, expected_df)


def test_get_top_n_movies_per_country_tiebreaker(movies_data):
    """Test the function with a tiebreaker."""
    n = 1
    additional_data = {
        'title': ['Movie8'],
        'country_code': ['US'],
        'country_name': ['United States'],
        'average_rating': [9.5],
        'num_of_votes': [250]
    }
    updated_movies_data = pd.concat([movies_data, pd.DataFrame(additional_data)], ignore_index=True)
    result = a.get_top_n_movies_per_country(updated_movies_data, n)
    expected_data = {
        'country_name': ['France', 'Germany', 'United States'],
        'country_code': ['FR', 'DE', 'US'],
        'avg_rating': [9.0, 8.0, 9.5],
        'total_votes': [110, 90, 250],
        'film_count': [1, 1, 1]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_get_top_n_movies_per_country_no_valid_country(movies_data):
    """Test the function with no valid country."""
    n = 5
    result = a.get_top_n_movies_per_country(movies_data, n)
    expected_data = {
        'country_name': [],
        'country_code': [],
        'avg_rating': [],
        'total_votes': [],
        'film_count': []
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.country_code = expected_df.country_code.astype('object')
    expected_df.country_name = expected_df.country_name.astype('object')
    expected_df.avg_rating = expected_df.avg_rating.astype('float64')
    expected_df.total_votes = expected_df.total_votes.astype('int64')
    expected_df.film_count = expected_df.film_count.astype('int64')
    pd.testing.assert_frame_equal(result, expected_df)


# Test the calculate_impact_metrics function

@pytest.fixture
def merged_data():
    """Create a DataFrame with merged data."""
    data_merged = {
        'title': ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5', 'Movie6', 'Movie7'],
        'country_code': ['US', 'US', 'US', 'FR', 'FR', 'FR', 'DE'],
        'country_name': ['United States', 'United States', 'United States',
                         'France', 'France', 'France', 'Germany'],
        'average_rating': [9.0, 8.5, 9.5, 8.0, 7.5, 9.0, 8.0],
        'num_of_votes': [100, 150, 200, 120, 80, 110, 90]
    }
    return pd.DataFrame(data_merged)


def test_calculate_impact_metrics_basic(merged_data):
    """Test the function with basic data."""
    result = a.calculate_impact_metrics(merged_data)
    expected_data = {
        'country_name': ['France', 'Germany', 'United States'],
        'country_code': ['FR', 'DE', 'US'],
        'weak_impact': [310, 90, 450],
        'strong_impact': [8.166666666666666, 8.0, 9.0]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_impact_metrics_single_country(merged_data):
    """Test the function with data for a single country."""
    single_country_data = merged_data[merged_data['country_code'] == 'US']
    result = a.calculate_impact_metrics(single_country_data)
    expected_data = {
        'country_name': ['United States'],
        'country_code': ['US'],
        'weak_impact': [450],
        'strong_impact': [9.0]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_impact_metrics_empty_df():
    """Test the function with an empty DataFrame."""
    empty_df = pd.DataFrame(
        columns=['title', 'country_code', 'country_name', 'average_rating', 'num_of_votes'])
    result = a.calculate_impact_metrics(empty_df)
    expected_data = {
        'country_name': [],
        'country_code': [],
        'weak_impact': [],
        'strong_impact': []
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.country_code = expected_df.country_code.astype('object')
    expected_df.country_name = expected_df.country_name.astype('object')
    expected_df.weak_impact = expected_df.weak_impact.astype('object')
    expected_df.strong_impact = expected_df.strong_impact.astype('object')

    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_impact_metrics_missing_values():
    """Test the function with missing values."""
    data_with_missing_values = {
        'title': ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5'],
        'country_code': ['US', 'US', 'FR', 'FR', 'DE'],
        'country_name': ['United States', 'United States', 'France', 'France', 'Germany'],
        'average_rating': [9.0, None, 8.0, 7.5, None],
        'num_of_votes': [100, 150, 120, None, 90]
    }
    df_with_missing_values = pd.DataFrame(data_with_missing_values)
    result = a.calculate_impact_metrics(df_with_missing_values)
    expected_data = {
        'country_name': ['France', 'Germany', 'United States'],
        'country_code': ['FR', 'DE', 'US'],
        'weak_impact': [120.0, 90.0, 250.0],
        'strong_impact': [7.75, float('nan'), 9.0]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_impact_metrics_multiple_countries_same_name():
    """Test the function with multiple countries with the same name."""
    data_with_same_country_names = {
        'title': ['Movie1', 'Movie2', 'Movie3', 'Movie4', 'Movie5'],
        'country_code': ['US', 'US', 'USA', 'FR', 'FR'],
        'country_name': ['United States', 'United States', 'United States', 'France', 'France'],
        'average_rating': [9.0, 8.5, 9.0, 8.0, 7.5],
        'num_of_votes': [100, 150, 100, 120, 80]
    }
    df_with_same_country_names = pd.DataFrame(data_with_same_country_names)
    result = a.calculate_impact_metrics(df_with_same_country_names)
    expected_data = {
        'country_name': ['France', 'United States', 'United States'],
        'country_code': ['FR', 'US', 'USA'],
        'weak_impact': [200, 250, 100],
        'strong_impact': [7.75, 8.75, 9.0]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


# Test the create_rank_dataframe function

@pytest.fixture
def impact_data():
    """Create a DataFrame with impact data."""
    data = {
        'country_name': ['United States', 'France', 'Germany'],
        'country_code': ['US', 'FR', 'DE'],
        'weak_impact': [450, 310, 90],
        'strong_impact': [9.0, 8.166666666666666, 8.0]
    }
    return pd.DataFrame(data)


@pytest.fixture
def merged_data2():
    """Create a DataFrame with merged data."""
    data = {
        'country_code': ['US', 'FR', 'DE'],
        'country_name': ['United States', 'France', 'Germany'],
        'population': [331000000, 67000000, 83000000],
        'gdp': [21000000000000, 2600000000000, 3800000000000],
        'gdp_per_population': [63531, 38805, 45783]
    }
    return pd.DataFrame(data)


def test_create_rank_dataframe_basic(impact_data, merged_data2):
    """Test the function with basic data."""
    result = a.create_rank_dataframe(impact_data, merged_data2)
    expected_data = {
        'country_name': ['United States', 'France', 'Germany'],
        'country_code': ['US', 'FR', 'DE'],
        'weak_impact_rank': [1, 2, 3],
        'strong_impact_rank': [1, 2, 3],
        'gdp_rank': [1, 3, 2],
        'pop_rank': [1, 3, 2],
        'gdp_per_population_rank': [1, 3, 2]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_create_rank_dataframe_single_country(impact_data, merged_data2):
    """Test the function with data for a single country."""
    single_country_impact = impact_data[impact_data['country_code'] == 'US']
    single_country_merged = merged_data2[merged_data2['country_code'] == 'US']
    result = a.create_rank_dataframe(single_country_impact, single_country_merged)
    expected_data = {
        'country_name': ['United States'],
        'country_code': ['US'],
        'weak_impact_rank': [1],
        'strong_impact_rank': [1],
        'gdp_rank': [1],
        'pop_rank': [1],
        'gdp_per_population_rank': [1]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_create_rank_dataframe_empty_df():
    """Test the function with an empty DataFrame."""
    empty_impact_df = pd.DataFrame(
        columns=['country_name', 'country_code', 'weak_impact', 'strong_impact'])
    empty_merged_df = pd.DataFrame(
        columns=['country_code', 'country_name', 'population', 'gdp', 'gdp_per_population'])
    result = a.create_rank_dataframe(empty_impact_df, empty_merged_df)
    expected_data = {
        'country_name': [],
        'country_code': [],
        'weak_impact_rank': [],
        'strong_impact_rank': [],
        'gdp_rank': [],
        'pop_rank': [],
        'gdp_per_population_rank': []
    }
    expected_df = pd.DataFrame(expected_data)

    expected_df.country_code = expected_df.country_code.astype('object')
    expected_df.country_name = expected_df.country_name.astype('object')
    expected_df.weak_impact_rank = expected_df.weak_impact_rank.astype('int64')
    expected_df.strong_impact_rank = expected_df.strong_impact_rank.astype('int64')
    expected_df.gdp_rank = expected_df.gdp_rank.astype('int64')
    expected_df.pop_rank = expected_df.pop_rank.astype('int64')
    expected_df.gdp_per_population_rank = expected_df.gdp_per_population_rank.astype('int64')

    pd.testing.assert_frame_equal(result, expected_df)


def test_create_rank_dataframe_tiebreakers():
    """Test the function with tiebreakers."""
    data_with_ties = {
        'country_name': ['United States', 'France', 'Germany', 'Italy'],
        'country_code': ['US', 'FR', 'DE', 'IT'],
        'weak_impact': [450, 450, 450, 450],
        'strong_impact': [9.0, 9.0, 9.0, 9.0]
    }
    merged_data_with_ties = {
        'country_code': ['US', 'FR', 'DE', 'IT'],
        'country_name': ['United States', 'France', 'Germany', 'Italy'],
        'population': [331000000, 67000000, 83000000, 60000000],
        'gdp': [21000000000000, 2600000000000, 3800000000000, 2000000000000],
        'gdp_per_population': [63531, 38805, 45783, 33333]
    }
    impact_df_with_ties = pd.DataFrame(data_with_ties)
    merged_df_with_ties = pd.DataFrame(merged_data_with_ties)
    result = a.create_rank_dataframe(impact_df_with_ties, merged_df_with_ties)
    expected_data = {
        'country_name': ['United States', 'France', 'Germany', 'Italy'],
        'country_code': ['US', 'FR', 'DE', 'IT'],
        'weak_impact_rank': [2, 2, 2, 2],
        'strong_impact_rank': [2, 2, 2, 2],
        'gdp_rank': [1, 3, 2, 4],
        'pop_rank': [1, 3, 2, 4],
        'gdp_per_population_rank': [1, 3, 2, 4]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


# Test the compute_hegemony function

@pytest.fixture
def rank_data():
    """Create a DataFrame with rank data."""
    data = {
        'country_name': ['United States', 'France', 'Germany'],
        'pop_rank': [1, 3, 2],
        'gdp_rank': [1, 3, 2],
        'gdp_per_population_rank': [1, 3, 2],
        'weak_impact_rank': [1, 2, 3],
        'strong_impact_rank': [1, 2, 3]
    }
    return pd.DataFrame(data)


def test_compute_hegemony_population(rank_data):
    """Test the function with population data."""
    result = a.compute_hegemony(rank_data, 'population', 'pop_rank')
    expected_data = {
        'Country Name': ['United States', 'France', 'Germany'],
        'Country Population Rank': [1, 3, 2],
        'Weak Impact Rank': [1, 2, 3],
        'Strong Impact Rank': [1, 2, 3],
        'Weak Hegemony Indicator': [0, 1, -1],
        'Strong Hegemony Indicator': [0, 1, -1]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_compute_hegemony_gdp(rank_data):
    """Test the function with GDP data."""
    result = a.compute_hegemony(rank_data, 'gdp', 'gdp_rank')
    expected_data = {
        'Country Name': ['United States', 'France', 'Germany'],
        'Country Gdp Rank': [1, 3, 2],
        'Weak Impact Rank': [1, 2, 3],
        'Strong Impact Rank': [1, 2, 3],
        'Weak Hegemony Indicator': [0, 1, -1],
        'Strong Hegemony Indicator': [0, 1, -1]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_compute_hegemony_gdp_per_population(rank_data):
    """Test the function with GDP per population data."""
    result = a.compute_hegemony(rank_data, 'gdp_per_population', 'gdp_per_population_rank')
    expected_data = {
        'Country Name': ['United States', 'France', 'Germany'],
        'Country GdpPerPopulation Rank': [1, 3, 2],
        'Weak Impact Rank': [1, 2, 3],
        'Strong Impact Rank': [1, 2, 3],
        'Weak Hegemony Indicator': [0, 1, -1],
        'Strong Hegemony Indicator': [0, 1, -1]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_compute_hegemony_empty_df():
    """Test the function with an empty DataFrame."""
    empty_df = pd.DataFrame(
        columns=['country_name', 'pop_rank', 'gdp_rank',
                 'gdp_per_population_rank', 'weak_impact_rank', 'strong_impact_rank'])
    result = a.compute_hegemony(empty_df, 'population', 'pop_rank')
    expected_data = {
        'Country Name': [],
        'Country Population Rank': [],
        'Weak Impact Rank': [],
        'Strong Impact Rank': [],
        'Weak Hegemony Indicator': [],
        'Strong Hegemony Indicator': []
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['Country Name'] = expected_df['Country Name'].astype('object')
    expected_df['Country Population Rank'] = expected_df['Country Population Rank'].astype('object')
    expected_df['Weak Impact Rank'] = expected_df['Weak Impact Rank'].astype('object')
    expected_df['Strong Impact Rank'] = expected_df['Strong Impact Rank'].astype('object')
    expected_df['Weak Hegemony Indicator'] = (expected_df['Weak Hegemony Indicator'].
                                              astype('object'))
    expected_df['Strong Hegemony Indicator'] = (expected_df['Strong Hegemony Indicator'].
                                                astype('object'))

    pd.testing.assert_frame_equal(result, expected_df)


def test_compute_hegemony_missing_values():
    """Test the function with missing values."""
    data_with_missing = {
        'country_name': ['United States', 'France', 'Germany'],
        'pop_rank': [1, 3, None],
        'gdp_rank': [1, None, 2],
        'gdp_per_population_rank': [1, 3, 2],
        'weak_impact_rank': [1, 2, 3],
        'strong_impact_rank': [1, None, 3]
    }
    df_with_missing = pd.DataFrame(data_with_missing)
    result = a.compute_hegemony(df_with_missing, 'gdp', 'gdp_rank')
    expected_data = {
        'Country Name': ['United States', 'France', 'Germany'],
        'Country Gdp Rank': [1, None, 2],
        'Weak Impact Rank': [1, 2, 3],
        'Strong Impact Rank': [1, None, 3],
        'Weak Hegemony Indicator': [0, None, -1],
        'Strong Hegemony Indicator': [0, None, -1]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


# Test the calculate_career_progression function
@pytest.fixture
def merged_data3():
    """Create a DataFrame with merged data."""
    data = {
        'director_id': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3],
        'director_name': ['Director A', 'Director A', 'Director A', 'Director A',
                          'Director B', 'Director B', 'Director B', 'Director B',
                          'Director C', 'Director C'],
        'year': [2000, 2001, 2002, 2003, 2000, 2001, 2002, 2003, 2000, 2001],
        'average_rating': [7.0, 7.5, 8.0, 8.5, 6.0, 6.5, 7.0, 7.5, 9.0, 9.5],
        'num_of_votes': [100, 150, 200, 250, 100, 150, 200, 250, 300, 350]
    }
    return pd.DataFrame(data)


@pytest.fixture
def eligible_directors():
    """Return a Series with eligible directors."""
    return pd.Series([1, 2, 3])


def test_calculate_career_progression_basic(merged_data3):
    """Test the function with basic data."""
    n = 4
    result = a.calculate_career_progression(merged_data3, n, pd.Series([1, 2]))
    expected_data = {
        'directors': ['Director A', 'Director B'],
        'first_avg_rating': [7.25, 6.25],
        'first_num_of_votes': [250, 250],
        'last_avg_rating': [8.25, 7.25],
        'last_num_of_votes': [450, 450],
        'rating_diff': [1.0, 1.0],
        'votes_diff': [200, 200]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_career_progression_half_films(merged_data3, eligible_directors):
    """Test the function with half the number of films."""
    n = 2
    result = a.calculate_career_progression(merged_data3, n, eligible_directors)
    expected_data = {
        'directors': ['Director A', 'Director B', 'Director C'],
        'first_avg_rating': [7.0, 6.0, 9.0],
        'first_num_of_votes': [100, 100, 300],
        'last_avg_rating': [8.5, 7.5, 9.5],
        'last_num_of_votes': [250, 250, 350],
        'rating_diff': [1.5, 1.5, 0.5],
        'votes_diff': [150, 150, 50]
    }
    expected_df = pd.DataFrame(expected_data)
    pd.testing.assert_frame_equal(result, expected_df)


def test_calculate_career_progression_empty_df(eligible_directors):
    """Test the function with an empty DataFrame."""
    empty_df = pd.DataFrame(
        columns=['director_id', 'director_name', 'year', 'average_rating', 'num_of_votes'])
    result = a.calculate_career_progression(empty_df, 4, eligible_directors)
    expected_data = {
        'first_avg_rating': [],
        'first_num_of_votes': [],
        'directors': [],
        'last_avg_rating': [],
        'last_num_of_votes': [],
        'rating_diff': [],
        'votes_diff': []
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df.directors = expected_df.directors.astype('object')
    expected_df.first_avg_rating = expected_df.first_avg_rating.astype('object')
    expected_df.first_num_of_votes = expected_df.first_num_of_votes.astype('object')
    expected_df.last_avg_rating = expected_df.last_avg_rating.astype('object')
    expected_df.last_num_of_votes = expected_df.last_num_of_votes.astype('object')
    expected_df.rating_diff = expected_df.rating_diff.astype('object')
    expected_df.votes_diff = expected_df.votes_diff.astype('object')

    pd.testing.assert_frame_equal(result, expected_df)
