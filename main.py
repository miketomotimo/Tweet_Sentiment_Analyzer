import wx
from sentiment_analyzer import SentimentAnalyzer as sa
from sentiment_analyzer import Tools
import pandas as pd

""" Objective: Add all data in the format (username: "", tweet: "", score: <int>) to file_with_scores.csv
Steps:
1. create a loop that goes through each tweet individually
    a. Loop will work like this:
    b. df["UserName"] = favourite_tweets["UserName"] <- This works!
    c. df["Tweet"] = favourite_tweets["Tweet"]
    d. 
2. sentiment analysis for each tweet, create a list of [UserName, Tweet, Score]
3. add the list to another list looks like this: [[UserName, Tweet, Score], [UserName, Tweet, Score]]
4. add all of that to a dataframe
"""


def main():
    # reads the favorite tweets csv
    favourite_tweets = pd.read_csv("favorite-tweets.csv")
    # dictionary to store the names and scores of tweets (name: score)

    # Menu.main_menu()

    # for tweet in favourite_tweets:
    name_tweet_score = pd.DataFrame(columns=['UserName', 'Tweet', "Score"])
    name_tweet_score['UserName'] = favourite_tweets['UserName']
    name_tweet_score['Tweet'] = favourite_tweets['Text']
    name_tweet_score.index = [Tools.string_to_datetime(date) for date in favourite_tweets['CreatedAt']]
    name_tweet_score['Score'] = [sa.sentiment_processing(sa.tweet_formatter(tweet)) for tweet in name_tweet_score['Tweet']]

    name_tweet_score = name_tweet_score.dropna(subset=['Tweet'])

    # keyword filter
    keyword = input("Enter a keyword: ")
    if keyword:
        name_tweet_score = name_tweet_score[name_tweet_score["Tweet"].str.contains(keyword, case=False)]

    # visualisation
    sa.visualise(name_tweet_score)


if __name__ == "__main__":
    # nltk.download('vader_lexicon')
    # nltk.download('wordnet')
    main()
