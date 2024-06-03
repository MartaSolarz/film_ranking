"""Tests for the data_analysis.data_processing file."""
import pytest
import pandas as pd
import numpy as np

import data_analysis.data_processing as dp


# Test process_world_bank_data function
@pytest.fixture
def mock_world_bank_data():
    """Fixture for the World Bank data."""
    return pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Series Name': ['Population, total', 'Population, total', 'Population, total'],
        'Series Code': ['SP.POP.TOTL', 'SP.POP.TOTL', 'SP.POP.TOTL'],
        'Country Name': ['United States', 'United Kingdom', 'France'],
        '2000 [YR2000]': [300000000, 60000000, 65000000],
        '2001 [YR2001]': [305000000, 60500000, 65500000]
    })


def test_process_world_bank_data(mock_world_bank_data):
    """Test processing the World Bank data - happy path."""
    processed_df = dp.process_world_bank_data(mock_world_bank_data.copy(), 'Population')

    expected_df = pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA', 'USA', 'GBR', 'FRA'],
        'Year': [2000, 2000, 2000, 2001, 2001, 2001],
        'Population': [300000000, 60000000, 65000000, 305000000, 60500000, 65500000]
    })

    pd.testing.assert_frame_equal(processed_df.reset_index(drop=True), expected_df)


def test_process_world_bank_data_missing_column(mock_world_bank_data):
    """Test processing the World Bank data with a missing column."""
    incomplete_df = mock_world_bank_data.drop(columns=['Series Name'])

    with pytest.raises(KeyError, match=r"\['Series Name'\] not found in axis"):
        dp.process_world_bank_data(incomplete_df, 'Population')


def test_process_world_bank_data_with_nan(mock_world_bank_data):
    """Test processing the World Bank data with NaN values."""
    nan_df = mock_world_bank_data.copy()
    nan_df.at[0, '2000 [YR2000]'] = np.nan

    processed_df = dp.process_world_bank_data(nan_df, 'Population')

    expected_df = pd.DataFrame({
        'Country Code': ['GBR', 'FRA', 'USA', 'GBR', 'FRA'],
        'Year': [2000, 2000, 2001, 2001, 2001],
        'Population': [60000000.0, 65000000.0, 305000000.0, 60500000.0, 65500000.0]
    })

    pd.testing.assert_frame_equal(processed_df.reset_index(drop=True), expected_df)


# Test filter_years function
@pytest.fixture
def mock_basics_df():
    """Fixture for the basics dataframe."""
    return pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003', 'tt0000004'],
        'titleType': ['movie', 'movie', 'movie', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3', 'Title4'],
        'startYear': [2000, 2001, 2002, 2003]
    })


@pytest.fixture
def mock_population_df():
    """Fixture for the population dataframe."""
    return pd.DataFrame({
     'Country Code': ['DEU', 'USA', 'GBR', 'FRA'],
     'Year': [1999, 2000, 2001, 2002],
     'Population': [80000000, 300000000, 60000000, 65000000]
    })


@pytest.fixture
def mock_gdp_df():
    """Fixture for the GDP dataframe."""
    return pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [2000, 2001, 2002],
        'GDP': [1000000000, 200000000, 300000000]
    })


def test_filter_years_happy_path(
        mock_basics_df, mock_population_df, mock_gdp_df
):
    """Test filtering the dataframes - happy path."""
    filtered_basics, filtered_population, filtered_gdp = dp.filter_years(
        mock_basics_df.copy(), mock_population_df.copy(), mock_gdp_df.copy(),
        2000, 2002
    )

    expected_basics = pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'movie', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3'],
        'startYear': [2000, 2001, 2002]
    })

    expected_population = pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [2000, 2001, 2002],
        'Population': [300000000, 60000000, 65000000]
    })

    expected_gdp = pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [2000, 2001, 2002],
        'GDP': [1000000000, 200000000, 300000000]
    })

    pd.testing.assert_frame_equal(filtered_basics.reset_index(drop=True), expected_basics)
    pd.testing.assert_frame_equal(
        filtered_population.reset_index(drop=True), expected_population,
    )
    pd.testing.assert_frame_equal(filtered_gdp.reset_index(drop=True), expected_gdp)


def test_filter_years_no_common_years(mock_basics_df):
    """Test filtering the dataframes with no common years."""
    mock_population_df_no_common = pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [1989, 2001, 2005],
        'Population': [300000000, 60000000, 65000000]
    })
    mock_gdp_df_no_common = pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [1990, 2002, 2006],
        'GDP': [1000000000, 200000000, 300000000]
    })

    with pytest.raises(
            ValueError,
            match="No common years found between the datasets."):
        dp.filter_years(
            mock_basics_df, mock_population_df_no_common,
            mock_gdp_df_no_common, 2000, 2002)


def test_filter_years_within_range(
        mock_basics_df, mock_population_df, mock_gdp_df
):
    """Test filtering the dataframes within a provided range."""
    filtered_basics, filtered_population, filtered_gdp = dp.filter_years(
        mock_basics_df, mock_population_df, mock_gdp_df,
        2001, 2001
    )

    expected_basics = pd.DataFrame({
        'tconst': ['tt0000002'],
        'titleType': ['movie'],
        'primaryTitle': ['Title2'],
        'startYear': [2001]
    })

    expected_population = pd.DataFrame({
        'Country Code': ['GBR'],
        'Year': [2001],
        'Population': [60000000]
    })

    expected_gdp = pd.DataFrame({
        'Country Code': ['GBR'],
        'Year': [2001],
        'GDP': [200000000]
    })

    pd.testing.assert_frame_equal(filtered_basics.reset_index(drop=True), expected_basics)
    pd.testing.assert_frame_equal(
        filtered_population.reset_index(drop=True), expected_population,
    )
    pd.testing.assert_frame_equal(filtered_gdp.reset_index(drop=True), expected_gdp)


def test_filter_years_missing_years(
        mock_population_df, mock_gdp_df,
):
    """Test filtering the dataframes with missing years."""
    mock_basics_df_missing_years = pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'movie', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3'],
        'startYear': [2000, np.NaN, 2002]
    })

    filtered_basics, filtered_population, filtered_gdp = dp.filter_years(
        mock_basics_df_missing_years, mock_population_df,
        mock_gdp_df, 2000, 2002
    )

    expected_basics = pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000003'],
        'titleType': ['movie', 'movie'],
        'primaryTitle': ['Title1', 'Title3'],
        'startYear': [2000.0, 2002.0]
    })

    expected_population = pd.DataFrame({
        'Country Code': ['USA', 'FRA'],
        'Year': [2000, 2002],
        'Population': [300000000, 65000000]
    })

    expected_gdp = pd.DataFrame({
        'Country Code': ['USA', 'FRA'],
        'Year': [2000, 2002],
        'GDP': [1000000000, 300000000]
    })

    pd.testing.assert_frame_equal(filtered_basics.reset_index(drop=True), expected_basics)
    pd.testing.assert_frame_equal(
        filtered_population.reset_index(drop=True), expected_population,
    )
    pd.testing.assert_frame_equal(filtered_gdp.reset_index(drop=True), expected_gdp)


# Test merge_data function
@pytest.fixture
def basics_df():
    """Fixture for the basics dataframe."""
    return pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'movie', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3'],
        'startYear': [2000, 2001, 2002]
    })


@pytest.fixture
def ratings_df():
    """Fixture for the ratings dataframe."""
    return pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'averageRating': [7.5, 8.0, 6.5],
        'numVotes': [1500, 3000, 2500]
    })


@pytest.fixture
def akas_df():
    """Fixture for the akas dataframe."""
    return pd.DataFrame({
        'titleId': ['tt0000001', 'tt0000002', 'tt0000003'],
        'region': ['US', 'GB', 'FR']
    })


@pytest.fixture
def crew_df():
    """Fixture for the crew dataframe."""
    return pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'directors': ['nm0000001', 'nm0000002', 'nm0000003']
    })


@pytest.fixture
def name_df():
    """Fixture for the name dataframe."""
    return pd.DataFrame({
        'nconst': ['nm0000001', 'nm0000002', 'nm0000003'],
        'primaryName': ['Director1', 'Director2', 'Director3']
    })


@pytest.fixture
def countries_df():
    """Fixture for the countries dataframe."""
    return pd.DataFrame({
        'alpha-2': ['US', 'GB', 'FR'],
        'alpha-3': ['USA', 'GBR', 'FRA'],
        'name': ['United States', 'United Kingdom', 'France']
    })


@pytest.fixture
def population_df():
    """Fixture for the population dataframe."""
    return pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [2000, 2001, 2002],
        'Population': [300000000, 60000000, 65000000]
    })


@pytest.fixture
def gdp_df():
    """Fixture for the GDP dataframe."""
    return pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA'],
        'Year': [2000, 2001, 2002],
        'GDP': [1000000000, 200000000, 300000000]
    })


def test_merge_data_happy_path(
        basics_df, ratings_df, akas_df, crew_df, name_df,
        countries_df, population_df, gdp_df,
):
    """Test merging dataframes - happy path."""
    merged_df = dp.merge_data(
        basics_df, ratings_df, akas_df, crew_df, name_df, countries_df, population_df, gdp_df
    )

    expected_df = pd.DataFrame({
        'titleId': ['tt0000001', 'tt0000002', 'tt0000003'],
        'region': ['US', 'GB', 'FR'],
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'movie', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3'],
        'startYear': [2000, 2001, 2002],
        'averageRating': [7.5, 8.0, 6.5],
        'numVotes': [1500, 3000, 2500],
        'directors': ['nm0000001', 'nm0000002', 'nm0000003'],
        'nconst': ['nm0000001', 'nm0000002', 'nm0000003'],
        'primaryName': ['Director1', 'Director2', 'Director3'],
        'alpha-2': ['US', 'GB', 'FR'],
        'alpha-3': ['USA', 'GBR', 'FRA'],
        'name': ['United States', 'United Kingdom', 'France'],
        'Country Code_x': ['USA', 'GBR', 'FRA'],
        'Year_x': [2000, 2001, 2002],
        'Population': [300000000, 60000000, 65000000],
        'Country Code_y': ['USA', 'GBR', 'FRA'],
        'Year_y': [2000, 2001, 2002],
        'GDP': [1000000000, 200000000, 300000000]
    })

    pd.testing.assert_frame_equal(merged_df, expected_df)


def test_merge_data_missing_column(
        basics_df, ratings_df, akas_df, crew_df, name_df,
        countries_df, population_df, gdp_df,
):
    """Test merging dataframes with a missing column."""
    incomplete_akas_df = akas_df.drop(columns=['region'])

    with pytest.raises(KeyError):
        dp.merge_data(
            basics_df, ratings_df, incomplete_akas_df, crew_df, name_df,
            countries_df, population_df, gdp_df,
        )


def test_merge_data_missing_data(
        basics_df, ratings_df, akas_df, crew_df, name_df,
        countries_df, population_df, gdp_df,
):
    """Test merging dataframes with missing data."""
    incomplete_population_df = population_df.drop(population_df.index[1])

    merged_df = dp.merge_data(
        basics_df, ratings_df, akas_df, crew_df, name_df,
        countries_df, incomplete_population_df, gdp_df,
    )

    expected_df = pd.DataFrame({
        'titleId': ['tt0000001', 'tt0000003'],
        'region': ['US', 'FR'],
        'tconst': ['tt0000001', 'tt0000003'],
        'titleType': ['movie', 'movie'],
        'primaryTitle': ['Title1', 'Title3'],
        'startYear': [2000, 2002],
        'averageRating': [7.5, 6.5],
        'numVotes': [1500, 2500],
        'directors': ['nm0000001', 'nm0000003'],
        'nconst': ['nm0000001', 'nm0000003'],
        'primaryName': ['Director1', 'Director3'],
        'alpha-2': ['US', 'FR'],
        'alpha-3': ['USA', 'FRA'],
        'name': ['United States', 'France'],
        'Country Code_x': ['USA', 'FRA'],
        'Year_x': [2000, 2002],
        'Population': [300000000, 65000000],
        'Country Code_y': ['USA', 'FRA'],
        'Year_y': [2000, 2002],
        'GDP': [1000000000, 300000000]
    })

    pd.testing.assert_frame_equal(merged_df, expected_df, check_dtype=False)


def test_merge_data_type_mismatch(
        basics_df, ratings_df, akas_df, crew_df, name_df,
        countries_df, population_df, gdp_df,
):
    """Test merging dataframes with type mismatch."""
    basics_df['startYear'] = basics_df['startYear'].astype(str)  # Introduce a type mismatch

    with pytest.raises(ValueError):
        dp.merge_data(basics_df, ratings_df, akas_df, crew_df, name_df,
                      countries_df, population_df, gdp_df)


# Test clean function
@pytest.fixture
def merged_df_fixture():
    """Fixture for the merged dataframe."""
    return pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003', 'tt0000004'],
        'titleId': ['tt0000001', 'tt0000002', 'tt0000003', 'tt0000004'],
        'titleType': ['movie', 'movie', 'short', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3', 'Title4'],
        'startYear': [2000, 2001, 2002, 2003],
        'averageRating': [7.5, 8.0, 6.5, 9.0],
        'numVotes': [1500, 3000, 2500, 4000],
        'directors': ['nm0000001', 'nm0000002', 'nm0000003', 'nm0000004'],
        'nconst': ['nm0000001', 'nm0000002', 'nm0000003', 'nm0000004'],
        'primaryName': ['Director1', 'Director2', 'Director3', 'Director4'],
        'alpha-2': ['US', 'GB', 'FR', 'DE'],
        'alpha-3': ['USA', 'GBR', 'FRA', 'DEU'],
        'region': ['US', 'GB', 'FR', 'DE'],
        'Country Code_x': ['USA', 'GBR', 'FRA', 'DEU'],
        'Country Code_y': ['USA', 'GBR', 'FRA', 'DEU'],
        'name': ['United States', 'United Kingdom', 'France', 'Germany'],
        'Year_x': [2000, 2001, 2002, 2003],
        'Year_y': [2000, 2001, 2002, 2003],
        'Population': [300000000, 60000000, 65000000, 80000000],
        'GDP': [1000000000, 200000000, 300000000, 400000000]
    })


def test_clean_happy_path(merged_df_fixture):
    """Test cleaning the merged dataframe - happy path."""
    cleaned_df = dp.clean(merged_df_fixture)

    expected_df = pd.DataFrame({
        'title_id': ['tt0000001', 'tt0000002', 'tt0000004'],
        'title': ['Title1', 'Title2', 'Title4'],
        'average_rating': [7.5, 8.0, 9.0],
        'num_of_votes': [1500, 3000, 4000],
        'director_id': ['nm0000001', 'nm0000002', 'nm0000004'],
        'director_name': ['Director1', 'Director2', 'Director4'],
        'country_code': ['US', 'GB', 'DE'],
        'country_name': ['United States', 'United Kingdom', 'Germany'],
        'year': [2000, 2001, 2003],
        'population': [300000000, 60000000, 80000000],
        'gdp': [1000000000, 200000000, 400000000],
        'gdp_per_population': [3.333333, 3.333333, 5.000000]
    }).set_index('title_id')

    pd.testing.assert_frame_equal(cleaned_df, expected_df)


def test_clean_missing_column(merged_df_fixture):
    """Test cleaning the merged dataframe with a missing column."""
    incomplete_df = merged_df_fixture.drop(columns=['Country Code_x'])

    with pytest.raises(KeyError):
        dp.clean(incomplete_df)


def test_clean_with_duplicates(merged_df_fixture):
    """Test cleaning the merged dataframe with duplicates."""
    duplicated_df = pd.concat([merged_df_fixture, merged_df_fixture])

    expected_df = pd.DataFrame({
        'title_id': ['tt0000001', 'tt0000002', 'tt0000004'],
        'title': ['Title1', 'Title2', 'Title4'],
        'average_rating': [7.5, 8.0, 9.0],
        'num_of_votes': [1500, 3000, 4000],
        'director_id': ['nm0000001', 'nm0000002', 'nm0000004'],
        'director_name': ['Director1', 'Director2', 'Director4'],
        'country_code': ['US', 'GB', 'DE'],
        'country_name': ['United States', 'United Kingdom', 'Germany'],
        'year': [2000, 2001, 2003],
        'population': [300000000, 60000000, 80000000],
        'gdp': [1000000000, 200000000, 400000000],
        'gdp_per_population': [3.333333, 3.333333, 5.000000]
    }).set_index('title_id')

    pd.testing.assert_frame_equal(dp.clean(duplicated_df), expected_df)


def test_clean_type_mismatch(merged_df_fixture):
    """Test cleaning the merged dataframe with type mismatch."""
    merged_df_fixture['GDP'] = merged_df_fixture['GDP'].astype(str)

    with pytest.raises(TypeError):
        dp.clean(merged_df_fixture)
