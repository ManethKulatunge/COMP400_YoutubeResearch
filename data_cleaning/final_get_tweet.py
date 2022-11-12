import pandas as pd
import tweepy

def main():
    df = pd.read_csv("dataset_20220511.csv")

    client = tweepy.Client(bearer_token='XXXXXXX', wait_on_rate_limit=True)
    for row in range(df.shape[0]):
        id_val=str(df.loc[row]['tweet_ID'])
        print(id_val)
        tweet = client.get_tweet(id=id_val)
        if tweet.data:
            df.iloc[row,0] = tweet.data.text
        else:
            df.iloc[row,0] = ""
    n = 2
    df.drop(columns=df.columns[-n:], axis=1,  inplace=True)
    df.drop(df[df['tweet_ID'] == ""].index, inplace = True)
    df = df.rename(columns={'tweet_ID': 'text', 'conspiracy_or_not': 'labels'})
    df.to_csv("cleaned_tweets_dataset.csv", index=False)

if __name__ == "__main__":
    main()