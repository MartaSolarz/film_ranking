import pytest
import pandas as pd
import numpy as np

from data_analysis.data_processing import load_data, process_world_bank_data, filter_years


# Test load_data function
def test_load_data_csv():
    df = load_data("./tests/mocks/test.csv")
    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(df, expected_df)


def test_load_data_tsv():
    df = load_data("./tests/mocks/test.tsv")
    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(df, expected_df)


def test_load_data_invalid_format():
    with pytest.raises(ValueError, match="Invalid file format. Only CSV and TSV files are supported."):
        load_data("invalid_file_format.txt")


def test_load_data_empty_file():
    with pytest.raises(ValueError, match="The file is empty."):
        load_data("./tests/mocks/empty.csv")


# Test process_world_bank_data function

MOCK_WORLD_BANK_DATA = pd.DataFrame({
    'Country Code': ['USA', 'GBR', 'FRA'],
    'Series Name': ['Population, total', 'Population, total', 'Population, total'],
    'Series Code': ['SP.POP.TOTL', 'SP.POP.TOTL', 'SP.POP.TOTL'],
    'Country Name': ['United States', 'United Kingdom', 'France'],
    '2000 [YR2000]': [300000000, 60000000, 65000000],
    '2001 [YR2001]': [305000000, 60500000, 65500000]
})


def test_process_world_bank_data():
    processed_df = process_world_bank_data(MOCK_WORLD_BANK_DATA, 'Population')

    expected_df = pd.DataFrame({
        'Country Code': ['USA', 'GBR', 'FRA', 'USA', 'GBR', 'FRA'],
        'Year': [2000, 2000, 2000, 2001, 2001, 2001],
        'Population': [300000000, 60000000, 65000000, 305000000, 60500000, 65500000]
    })

    pd.testing.assert_frame_equal(processed_df, expected_df)


def test_process_world_bank_data_missing_column():
    incomplete_df = MOCK_WORLD_BANK_DATA.drop(columns=['Series Name'])

    with pytest.raises(KeyError, match=r"\['Series Name'\] not found in axis"):
        process_world_bank_data(incomplete_df, 'Population')


def test_process_world_bank_data_with_nan():
    nan_df = MOCK_WORLD_BANK_DATA.copy()
    nan_df.at[0, '2000 [YR2000]'] = np.nan

    processed_df = process_world_bank_data(nan_df, 'Population')

    expected_df = pd.DataFrame({
        'Country Code': ['GBR', 'FRA', 'USA', 'GBR', 'FRA'],
        'Year': [2000, 2000, 2001, 2001, 2001],
        'Population': [60000000.0, 65000000.0, 305000000.0, 60500000.0, 65500000.0]
    })

    pd.testing.assert_frame_equal(processed_df.reset_index(drop=True), expected_df)

# Test filter_years function


MOCK_BASICS_DF = pd.DataFrame({
    'tconst': ['tt0000001', 'tt0000002', 'tt0000003', 'tt0000004'],
    'titleType': ['movie', 'movie', 'movie', 'movie'],
    'primaryTitle': ['Title1', 'Title2', 'Title3', 'Title4'],
    'startYear': [2000, 2001, 2002, 2003]
})

MOCK_POPULATION_DF = pd.DataFrame({
    'Country Code': ['DEU', 'USA', 'GBR', 'FRA'],
    'Year': [1999, 2000, 2001, 2002],
    'Population': [80000000, 300000000, 60000000, 65000000]
})

MOCK_GDP_DF = pd.DataFrame({
    'Country Code': ['USA', 'GBR', 'FRA'],
    'Year': [2000, 2001, 2002],
    'GDP': [1000000000, 200000000, 300000000]
})


def test_filter_years_happy_path():
    filtered_basics, filtered_population, filtered_gdp = filter_years(
        MOCK_BASICS_DF, MOCK_POPULATION_DF, MOCK_GDP_DF, 2000, 2002
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
    pd.testing.assert_frame_equal(filtered_population.reset_index(drop=True), expected_population)
    pd.testing.assert_frame_equal(filtered_gdp.reset_index(drop=True), expected_gdp)


def test_filter_years_no_common_years():
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

    with pytest.raises(ValueError, match="No common years found between the datasets."):
        filter_years(MOCK_BASICS_DF, mock_population_df_no_common, mock_gdp_df_no_common, 2000, 2002)


def test_filter_years_within_range():
    filtered_basics, filtered_population, filtered_gdp = filter_years(
        MOCK_BASICS_DF, MOCK_POPULATION_DF, MOCK_GDP_DF, 2001, 2001
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
    pd.testing.assert_frame_equal(filtered_population.reset_index(drop=True), expected_population)
    pd.testing.assert_frame_equal(filtered_gdp.reset_index(drop=True), expected_gdp)


def test_filter_years_missing_years():
    mock_basics_df_missing_years = pd.DataFrame({
        'tconst': ['tt0000001', 'tt0000002', 'tt0000003'],
        'titleType': ['movie', 'movie', 'movie'],
        'primaryTitle': ['Title1', 'Title2', 'Title3'],
        'startYear': [2000, np.NaN, 2002]
    })

    filtered_basics, filtered_population, filtered_gdp = filter_years(
        mock_basics_df_missing_years, MOCK_POPULATION_DF, MOCK_GDP_DF, 2000, 2002
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
    pd.testing.assert_frame_equal(filtered_population.reset_index(drop=True), expected_population)
    pd.testing.assert_frame_equal(filtered_gdp.reset_index(drop=True), expected_gdp)

# Test merge_data function

# Test clean function
