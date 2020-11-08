import headlineanalysis as ha
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

_leaning = ['left', 'mod_left', 'moderate', 'mod_right', 'right']
leaning_labels = ['Far Left', 'Left', 'Moderate', 'Right', 'Far Right']

"""
Make a scatter plot showing the positive and negative
polarity scores of news headlines for one keyword. Points are
color coded by media bias rating. Left news sources are more blue
and right news sources are more red.

Args:
    csv_file: A string containing the path to a CSV file. This file
    should have top news headlines queried by one keyword, and the
    polarity scores of them.

Returns:
    A png file with a scatter plot saved in the current relative
    directory.

"""


def plot_scatter_posneg(csv_file):
    df = pd.read_csv(csv_file)
    # Keyword objects should all be the same in this DataFrame.
    keyword = df.keyword[0]
    # Graph scatterplot with changing colors based on the bias rating.
    sns.scatterplot(data=df, x='neg', y='pos',
                    hue='leaning',
                    s=100,
                    hue_order=_leaning,
                    palette='coolwarm')
    plt.xlabel('Negative Polarity Scores')
    plt.ylabel('Positive Polarity Scores')
    plt.title(f'Polarity Scores for Headlines with \"{keyword.capitalize()}\"')
    plt.savefig(f'png_files/{keyword}_posvneg.png')
    plt.show()


"""
Make a pivot table of the mean scores against political
bias rating for each keyword.

Args:
    list_dfs: A list of DataFrames.
    score: A string with 'compound', 'pos', or 'neg'.

Returns:
    A pivot table of mean polarity scores against bias rating for
    each keyword.
"""


def pivot_heatmap(list_csvs, score):
    heatmap_df = pd.DataFrame()
    frames = []
    # Constructing a pivot table
    for csv_file in list_csvs:
        df = pd.read_csv(csv_file)
        keyword = df.loc[0, 'keyword']
        new_df = df[['leaning', score]]
        new_df['leaning'].astype('category')
        table = pd.pivot_table(new_df, index=['leaning'])
        table = table.rename(columns={'leaning': 'leaning', score: keyword})
        frames.append(table)
        heatmap_df = pd.concat(frames, axis=1)

    # Re-index leanings to have 'moderate' in the center.
    indexed_table = heatmap_df.reindex(_leaning)
    return indexed_table


"""
Get a heat map with political leaning of sources plotted against a certain
polarity score (compound, positive, or negative). This function takes a number
of DataFrames that contain top headlines for a certain topic and the polarity
scores for the titles. It then makes a pivot table of the mean scores against
bias rating for each keyword. The pivot table is used to generate a heatmap.

Args:
    list_dfs: A list of DataFrames.
    score: A string with 'compound', 'pos', or 'neg'.

Returns:
    A png file with a heatmap saved in the current relative directory.
"""


def plot_heatmap(list_csvs, score):
    table = pivot_heatmap(list_csvs, score)
    # Plotting the heatmap
    sns.heatmap(table, center=0,
                linewidths=0.5,
                cmap='Blues_r',
                square=True,
                yticklabels=leaning_labels)
    plt.xlabel('Keyword')
    plt.ylabel('Bias Rating')
    plt.title(f'Mean {score.capitalize()} Polarity Scores by Bias Rating')
    plt.savefig(f'png_files/{score}_heatmap.png')
    plt.show()


"""
Unpivot a DataFrame to make score type an identifier variable.
This is in preparation for plotting different types of scores on
one barplot.

Args:
    csv_file: A string containing the path to a CSV file.
    scoretypes: A list specifying the scores that are to be graphed. If
    nothing is inputted, the default is ['neg', 'compound', 'pos'].

Returns:
    A new DataFrame with score types as an identifier variable.
"""


def melt_barplot(csv_file, scoretypes=['neg', 'compound', 'pos']):
    df = pd.read_csv(csv_file)
    keyword = df.keyword[0]
    new_df = pd.melt(df, id_vars=['publishedAt', 'source.name', 'leaning'],
                     value_vars=scoretypes,
                     value_name='polarity_score',
                     var_name='type_score')
    new_df = new_df.groupby(['leaning', 'source.name', 'type_score'])\
        .polarity_score.mean()
    new_df = new_df.reset_index()
    new_df.leaning = pd.Categorical(new_df.leaning,
                                    categories=_leaning,
                                    ordered=True)
    new_df.sort_values(['leaning', 'source.name', 'polarity_score'],
                       inplace=True)
    new_df['keyword'] = [keyword] * len(new_df)
    new_df.reset_index(drop=True, inplace=True)
    return new_df


"""
Make a horizontal bar chart that graphs mean polarity scores of news sources.
News sources are sorted by bias rating (far left sources are at the top, far
right sources are at the bottom of the y-axis).

Args:
    csv_file: A string containing the path to a CSV file.
    scoretypes: A list specifying the scores that are to be graphed. If
    nothing is inputted, the default is ['neg', 'compound', 'pos'].

Returns:
    A png file with a barplot saved in the current relative directory.
"""


def barplot_polarity(csv_file, scoretypes=['neg', 'compound', 'pos']):
    df = melt_barplot(csv_file, scoretypes)
    keyword = df.keyword[0]
    # If the list only contains one score type,
    # having different hues becomes unnecessary.
    if len(scoretypes) > 1:
        plt.figure(num=None, figsize=(18, 10), dpi=80)
        sns.barplot(y='source.name',
                    x='polarity_score',
                    hue='type_score',
                    data=df,
                    palette='RdYlGn',
                    hue_order=scoretypes)
        plt.xlabel('Polarity Scores')
        plt.title(f'Polarity Scores of Headlines'
                  f' with \"{keyword.capitalize()}\"')
    else:
        plt.figure(num=None, figsize=(18, 10), dpi=80)
        sns.barplot(y='source.name',
                    x='polarity_score',
                    color='lightblue',
                    data=df)
        plt.xlabel('Polarity Scores')
        plt.title(f'{scoretypes[0].capitalize()} Scores of Headlines'
                  f' with \"{keyword.capitalize()}\"')
    plt.ylabel('News Source')
    plt.savefig(f'png_files/{keyword}_bar.png')
    plt.show()
