# News Bias Analysis

News Bias Analysis is a Python library for analyzing sentiment in top news headlines, and finding trends in polarity scores across news sources with different bias ratings. These ratings are found from [allsides.com](allsides.com), and include: far left, left, moderate, right, and far right.

### Installation
Use the package manager pip to install necessary libraries.
NewsAPI is used to query top news headlines. Pandas and JSON are used to process the data. NLTK is used to perform sentiment analysis. Seaborn and Matplotlib are used to graph the findings.
```bash
pip install newsapi-python
pip install pandas
pip install json
pip install nltk
pip install seaborn
pip install matplotlib
```

### Usage
```python
import headlineanalysis as ha
import plotsentiment as ps

ha.get_json('hello', left) # returns JSON string with top news headlines
# with keyword 'hello' from news sources with left bias ratings.
ha.get_headlines('json_files/hello_left.json') # returns a pandas DataFrame
# with data from the JSON file.
ha.get_all_headlines('hello') # returns a DataFrame with top news headlines
# from news sources categorized by bias ratings.
ha.use_sentiment_analysis('csv_files/hello.csv')
# returns a DataFrame with polarity scores of headlines

ps.plot_scatter_posneg('sentiment_csv_files/hello.csv') # saves scatterplot png
ps.pivot_heatmap(['sentiment_csv_files/hello.csv'], 'pos') # returns a pivot
# table of mean polarity scores and keywords
ps.plot_heatmap(['sentiment_csv_files/hello.csv'], 'pos') # saves a heatmap png
ps.melt_barplot('sentiment_csv_files/hello.csv') # returns an unpivoted table
ps.barplot_polarity('sentiment_csv_files/hello.csv') # saves a barplot png
```
### Contributors
- Serena Chang, Olin College of Engineering