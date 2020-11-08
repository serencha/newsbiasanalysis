import pytest
import pandas as pd
import datatest as dt
import plotsentiment as ps


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    return ps.melt_barplot('sentiment_csv_files/president.csv')


# Test the column names.
def test_columns(df):
    dt.validate(
        df.columns,
        {'leaning', 'source.name', 'type_score', 'polarity_score', 'keyword'},
    )


# Test to check that certain columns have a limited amount of
# unique values.
def test_keyword(df):
    assert len(df.keyword.unique()) == 1


def test_scores(df):
    assert len(df.type_score.unique()) == 3


def test_leaning(df):
    assert len(df.leaning.unique()) == 5


# Test the types of the column objects.
def test_score_type(df):
    dt.validate(df['polarity_score'], float)
