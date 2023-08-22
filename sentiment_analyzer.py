import nltk
import numpy as np
import pandas as pd
import re
import string
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize  # tokenize
from nltk.corpus import stopwords  # stopwords
from nltk.stem import WordNetLemmatizer  # lemmatizer
import matplotlib.pyplot as plt

# Definitions
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

class Tools:
    # formats the tweets from a list to a sentence without links
    @staticmethod
    def tweet_formatter(text):
        text = str(text) if text != str(text) else text
        # removes spaces between words and punctuation (e.g. "Hey ..." -> "Hey...")
        text = re.sub(r'\s*([{}])'.format(re.escape(string.punctuation)), r'\1', text)
        # removes all instances of hyperlinks in the text
        text = re.sub(r'http[s]?://\S+|www\.\S+', '', text)
        return text

    # changes the index of a dataframe to a date in which the tweet was created
    @staticmethod
    def string_to_datetime(date_string):
        date_obj = pd.to_datetime(date_string, format="%B %d, %Y at %I:%M%p").date()
        return date_obj


class SentimentAnalyzer(Tools):
    @staticmethod
    def sentiment_processing(text):
        text = str(text) if type(text) != str else text
        # changes the format of the tweet from a list to a sentence without links
        formatted_tweet = SentimentAnalyzer.tweet_formatter(text)

        tokened_list = word_tokenize(formatted_tweet)
        # stopword removal
        filtered_list = [word for word in tokened_list if word not in stop_words]
        # lemmatization
        lemmatized_list = [lemmatizer.lemmatize(word) for word in filtered_list]

        formatted_tweet = ' '.join(lemmatized_list)

        # sentiment analyzer using the polarity_scores method
        polarity_scores = sia.polarity_scores(formatted_tweet)
        return polarity_scores['compound']  # only returns the overall score of the tweet


