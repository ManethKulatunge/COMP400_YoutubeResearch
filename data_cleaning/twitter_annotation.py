import pandas as pd
import tweepy
import re

def datacleaning(text):
    stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from", "rt"]
    temp = text.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)
    temp = temp.split()
    temp = [w for w in temp if not w in stopwords]
    temp = " ".join(word for word in temp)
    return temp


def main():
    df = pd.read_csv("dataset_20220511.csv")

    client = tweepy.Client(bearer_token='XXXXXX', wait_on_rate_limit=True)
    
    for row in range(df.shape[0]):
        id_val=str(df.loc[row]['tweet_ID'])
        print(id_val)
        tweet = client.get_tweet(id=id_val)
        if tweet.data:
            tweet_text = tweet.data.text
            cleaned_text = datacleaning(tweet_text)
            df.iloc[row,0] = cleaned_text
        else:
            df.iloc[row,0] = ""
    n = 2
    df.drop(columns=df.columns[-n:], axis=1,  inplace=True)
    df.drop(df[df['tweet_ID'] == ""].index, inplace = True)
    df.to_csv("cleaned_tweets_dataset.csv", index=False)

if __name__ == "__main__":
    main()