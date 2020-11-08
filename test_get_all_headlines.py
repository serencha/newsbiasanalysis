import pytest
import pandas as pd
import datatest as dt


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
# get_all_headlines('president')
def df():
    return pd.read_csv('csv_files/president.csv')


@pytest.mark.mandatory
# Test if the columns are as expected.
def test_columns(df):
    dt.validate(
        df.columns,
        {'author', 'title', 'description', 'url', 'urlToImage',
         'publishedAt', 'content', 'source.id', 'source.name',
         'leaning', 'keyword'},
    )


# Test to see that all 5 bias ratings are used in the DataFrame.
def test_rating(df):
    dt.validate.superset(
        df['leaning'],
        {'left', 'mod_left', 'moderate', 'mod_right', 'right'},
    )


# Test if object types of columns are as expected.
def test_title(df):
    dt.validate(df['title'], str)


def test_name(df):
    dt.validate(df['source.name'], str)


def test_keyword(df):
    dt.validate(df['keyword'], str)
