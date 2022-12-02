import pandas as pd
from tqdm import tqdm
import tweepy
  # Using readlines()
file1 = open('non_conspiracy.txt', 'r')
Lines = file1.readlines()
df = pd.DataFrame(columns=['text', 'labels'])

file2 = open('5g_corona_conspiracy.txt', 'r')
Lines2 = file2.readlines()
  
count = 0
# Strips the newline character
client = tweepy.Client(bearer_token='AAAAAAAAAAAAAAAAAAAAAJOtiwEAAAAAehv64jIqxW5aTmeLRMDHHQBIYQk%3DhLhLnodFGBxv607cHkMEBhUK2H2OswG8lu9RVIf07u5Nsmcvue', wait_on_rate_limit=True)
#len(Lines)
for line in range(1000):
    count += 1
    print(count)
    tweet = client.get_tweet(id=str(Lines[line].strip()))
    if tweet.data:
        new_row = {'text':tweet.data.text, 'labels':0}
        df = pd.concat([df, pd.DataFrame.from_records([new_row])])

for line2 in range(1000):
    count += 1
    print(count)
    tweet = client.get_tweet(id=str(Lines2[line2].strip()))
    if tweet.data:
        new_row = {'text':tweet.data.text, 'labels':1}
        df = pd.concat([df, pd.DataFrame.from_records([new_row])])

df2 = df.sample(frac=1)
df2.to_csv("hello1.csv", index=False)