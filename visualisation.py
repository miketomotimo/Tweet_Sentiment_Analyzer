import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class visualise:
    @staticmethod
    def sentiment_wheel(df, segment):
        data = {'Positive': [], 'Negative': [], 'Neutral': []}

        # categorise the tweets into different lists in the data dictionary
        for tweet, score in zip(df['Tweet'], df['Score']):
            if score >= 0.05:
                data['Positive'].append(tweet)
            if score <= -0.05:
                data['Negative'].append(tweet)
            else:
                data['Neutral'].append(tweet)

        # plot the pie chart
        plt.pie([len(value) for value in data.values()], labels=list(data.keys()), autopct='%1.1f%%')
        plt.title('Sentiment Wheel')
        plt.show()

    @staticmethod
    def sentiment_over_time(df):
        # sentiment per month
        df.index = pd.to_datetime(df.index)
        grouped_data = df['Score'].resample('M')
        monthly_avg = grouped_data.mean()

        # creating dataframe containing all the month/year combinations that appear in the code
        # [1] indexing due to each element containing a Timestamp and the compound score
        mean_sentiment_per_month = {'Months': [value[0].strftime('%Y-%m') for value in monthly_avg.items()], 'Average Sentiment': [value[1] for value in monthly_avg.items()]}

        plt_data = pd.DataFrame(mean_sentiment_per_month)
        ax = plt_data.plot.scatter(x='Months', y='Average Sentiment')
        plt.xticks(rotation=90)
        plt.show()

    @staticmethod
    def user_ranking(df):
        # if there are two or more tweets by the same user:
        # groupby() groups the rows of the DataFrame based on the unique values, .agg() applies aggregation fuctions
        # to the other two columns (mean for the score and list for the tweet)
        user_rank = df.groupby('UserName').agg({'Score': 'mean', 'Tweet': list}).reset_index()

        # sort the dataframe based on the column 'Score', the
        # ascending parameter is set to false so the df will be sorted descending
        user_rank = user_rank.sort_values('Score', ascending=False)
        print(user_rank)
















        
