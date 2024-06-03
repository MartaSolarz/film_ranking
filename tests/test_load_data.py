"""Tests for data_analysis.load_data file."""
import pandas as pd
import pytest

from data_analysis.load_data import load_data


# Test load_data function
def test_load_data_csv():
    """Test loading a CSV file."""
    df = load_data("./tests/mocks/test.csv")
    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(df, expected_df)


def test_load_data_tsv():
    """Test loading a TSV file."""
    df = load_data("./tests/mocks/test.tsv")
    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(df, expected_df)


def test_load_data_invalid_format():
    """Test loading a file with an invalid format."""
    with pytest.raises(
            ValueError,
            match="Invalid file format. Only CSV and TSV files are supported."):
        load_data("invalid_file_format.txt")


def test_load_data_empty_file():
    """Test loading an empty file."""
    with pytest.raises(ValueError, match="The file is empty."):
        load_data("./tests/mocks/empty.csv")
