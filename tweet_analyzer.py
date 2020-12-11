import re
import json
import pandas as pd
from pandas.io import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def clean_tweet(tweet):
    # this method just cleans up the text in a tweet which removes emojis and symbols. it made it easier to analyse
    return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', tweet).split())


def sentiment_machine(sentence):
    score = analyser.polarity_scores(sentence)
    return score


def create_my_df():
    my_df = pd.read_json('data/results.json', orient='records')
    my_df['clean_tweet'] = my_df['tweet'].apply(lambda x: clean_tweet(x))
    my_df['sentiment'] = my_df['clean_tweet'].apply(lambda x: 'NaN' if pd.isnull(x) else sentiment_machine(x))
    my_df['compound'] = my_df['sentiment'].apply(lambda score_dict: score_dict['compound'])
    my_df['comp_score'] = my_df['compound'].apply(lambda c: 'positive' if c > 0.05 else ('negative' if c < -0.05 else 'neutral'))
    del my_df['tweet']
    del my_df['sentiment']
    del my_df['compound']

    my_json = my_df.to_json(orient='index')
    parsed = json.loads(my_json)
    parsed = json.dumps(parsed)

    return parsed





