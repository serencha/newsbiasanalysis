import pytest
import pandas as pd
import datatest as dt
import plotsentiment as ps


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    return ps.pivot_heatmap(['sentiment_csv_files/president.csv',
                            'sentiment_csv_files/election.csv'], 'pos')


# Test for the column names.
def test_columns(df):
    dt.validate(
        df.columns,
        {'president', 'election'},
    )


# Test the types of the column objects.
def test_president(df):
    dt.validate(df['president'], float)


def test_election(df):
    dt.validate(df['election'], float)
