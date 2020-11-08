import pytest
import pandas as pd
import datatest as dt


@pytest.fixture(scope='module')
@dt.working_directory(__file__)


def df():
    return pd.read_csv('sentiment_csv_files/president.csv')


# Test the types of the column objects.
def test_scores(df):
    dt.validate(df['scores'], str)


def test_pos(df):
    dt.validate(df['pos'], float)


def test_neg(df):
    dt.validate(df['neg'], float)


def test_compound(df):
    dt.validate(df['compound'], float)
