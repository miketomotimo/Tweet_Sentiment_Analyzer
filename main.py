import wx
from sentiment_analyzer import SentimentAnalyzer as sa
from sentiment_analyzer import Tools
import pandas as pd
from GUI import MainFrame

def main():
    try:
        # reads the favorite tweets csv
        favourite_tweets = pd.read_csv("favorite-tweets.csv")
        # dictionary to store the names and scores of tweets (name: score)

        # for tweet in favourite_tweets:
        name_tweet_score = pd.DataFrame(columns=['UserName', 'Tweet', "Score"])
        name_tweet_score['UserName'] = favourite_tweets['UserName']
        name_tweet_score['Tweet'] = favourite_tweets['Text']
        name_tweet_score.index = [Tools.string_to_datetime(date) for date in favourite_tweets['CreatedAt']]
        name_tweet_score['Score'] = [sa.sentiment_processing(sa.tweet_formatter(tweet)) for tweet in
                                     name_tweet_score['Tweet']]

        name_tweet_score = name_tweet_score.dropna(subset=['Tweet'])

        # GUI
        app = wx.App()
        Frame = MainFrame(None, name_tweet_score)
        Frame.Show()
        app.MainLoop()

    except:
        # in the case that file is lost
        print("File not Found, to recover file, re-download through the this app's github page at:"
              " https://github.com/miketomotimo/Tweet_Sentiment_Analyzer")


if __name__ == "__main__":
    main()
