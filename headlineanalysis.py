from newsapi import NewsApiClient
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import json
import apikeys

# Init
# My API key. To get your own, go to newsapi.org
newsapi = NewsApiClient(api_key=apikeys.my_api_key)

# Political news sources by bias rating (allsides.com)
left = 'the-huffington-post, newsweek, msnbc, buzzfeed'
mod_left = 'politico, time, the-washington-post, the-verge,\
    nbc-news, cnn, cbs-news, bloomberg, abc-news'
moderate = 'the-wall-street-journal, the-hill, reuters, bbc-news'
mod_right = 'fox-news, the-washington-times'
right = 'the-american-conservative, breitbart-news'
_leaning = ['left', 'mod_left', 'moderate', 'mod_right', 'right']


"""
Query top U.S. headlines in the past month by a keyword and a handful of
news sources that share the same media bias rating. Save results into a JSON
file.

Args:
    keyword: A string with the keyword to be queried.
    leaning: A string with the desired bias rating to be queried.

Returns:
    A saved JSON file in the current relative directory.

"""


def get_json(keyword, leaning):
    sources = eval(leaning)
    headlines_json = newsapi.get_top_headlines(q=keyword,
                                               sources=sources,
                                               language='en')
    json_file = f'json_files/{keyword}_{leaning}_headlines.json'
    with open(json_file, 'w') as f:
        json.dump(headlines_json, f)
    return json_file


"""
Query top U.S. headlines in the past month by a keyword and a handful of
news sources that share the same media bias rating. This function converts
the JSON string with the top headlines into a pandas DataFrame.

Args:
    json_file: A string with the path the the json file.

Returns:
    A pandas DataFrame with the following columns: 'author', 'title',
    'description', 'url', 'urlToImage', 'publishedAt', 'content', 'source.id',
    and 'source.name'.

"""


def get_headlines(json_file):
    with open(json_file) as f:
        headlines_json = json.load(f)
    flat_table = pd.json_normalize(headlines_json)
    # flat_table is a DataFrame with 1 row and 3 columns:
    # 'status', 'total results', and 'articles'. The headlines
    # are in a JSON string in the only row of the articles column.
    articles = flat_table.articles
    json_list = articles[0]
    headlines = pd.json_normalize(json_list)
    return headlines


"""
Get all top headlines queried by a keyword and list of bias ratings
into a DataFrame. The default value for leanings is a list of all bias
ratings. Valid objects for this list are 'left', 'mod_left', 'moderate',
'mod_right', and 'right'. Within the DataFrame, classify each result
by news bias rating and keyword. Save this DataFrame into a CSV file
named after the keyword.

Args:
    keyword: A string with the keyword to be queried.

Returns:
    A csv file saved in the current relative directory.

"""


def get_all_headlines(keyword, leanings=_leaning):
    frames = []
    # Add headlines of listed bias ratings to the same DataFrame
    for leaning in leanings:
        json_file = get_json(keyword, leaning)
        df = get_headlines(json_file)
        df['leaning'] = leaning
        df['keyword'] = keyword
        frames.append(df)
    all_headlines = pd.concat(frames)
    # Reset index so each row has a unique index. Retrieving values
    # will be easier.
    all_headlines.reset_index(drop=True, inplace=True)
    all_headlines.to_csv(f'csv_files/{keyword}.csv', index=False)


"""
Fetch a DataFrame from a csv file. Conduct sentiment analysis on each
news headline, and save the polarity scores along with the original data
into a new csv file. The headlines are in the 'titles' column.

Args:
    csv_file: A string containing the path to a csv file. The csv file
    should contain a DataFrame with the following columns: 'author',
    'title', 'description', 'url', 'urlToImage', 'publishedAt', 'content',
    'source.id', and 'source.name'.

Returns:
    A csv file with added columns: 'scores', 'compound', 'pos', 'neg'.
    These columns contain the polarity scores of the headlines. The 'scores'
    column has objects that are dictionaries. The other columns all have float
    objects.
"""


def use_sentiment_analysis(csv_file):
    df = pd.read_csv(csv_file)
    sid = SentimentIntensityAnalyzer()
    df.dropna(inplace=True)
    # Perform sentiment analysis and add results (in the form of a dictionary)
    # into the 'scores' column.
    df['scores'] = df['title'].apply(lambda txt: sid.polarity_scores(txt))
    # Retrieve float values from the dictionary and add to individual columns.
    df['compound'] = df['scores'].apply(lambda sc_dict: sc_dict['compound'])
    df['pos'] = df['scores'].apply(lambda sc_dict: sc_dict['pos'])
    df['neg'] = df['scores'].apply(lambda sc_dict: sc_dict['neg'])
    # Save CSV file with path in format:'sentiment_csv_files/{keyword}.csv'
    df.to_csv(f'sentiment_csv_files/{csv_file[9:]}', index=False)
