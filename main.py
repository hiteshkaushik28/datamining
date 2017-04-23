# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import pandas as pd
import re
import matplotlib.pyplot as plt


# Variables that contains the user credentials to access Twitter API
access_token = '4790392156-PmSnkPUjKMKiOt6I9MQ9e1eo1ifipgyjkjKxVRc'
access_token_secret = 'pXbmykF6K2CiFsR7qZeMEDJv0QDcfQaFrA7OWyGqq2kSf'
consumer_key = 'aBPLr9qKTzNQCPND5m7D2Qo0O'
consumer_secret = 'cv8wE2327oAv37kPEK1nfhAt8sVMOYjto7mCA2JPNDFNB4gAzm'

# open file where json data is to be stored
f = open('C:\Users\Asus\Desktop\language.txt', 'w')


# This is a basic listener that just prints received tweets to stdout.
"""class StdOutListener(StreamListener):
    def on_data(self, data):
     # f.write(data)
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    # This handles Twitter authentification and the connection to Twitter Streaming API
   l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the language names
    stream.filter(track=['python', 'javascipt', 'c++', 'rubyonrails', 'java'])

"""
# Reading the data from the output file into an array

tweets_data_path = 'C:\Users\Asus\Desktop\languagess.txt'
tweets_data = []
tweets_file = open(tweets_data_path, 'r')
for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue


print len(tweets_data)

# structuring the tweets into PANDA DateFrame
tweets = pd.DataFrame()

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
tweets['lang'] = map(lambda tweet: tweet['lang'], tweets_data)
tweets['country'] = map(lambda tweet: tweet['place']['country'] if tweet['place'] is not None else None, tweets_data)

tweets_by_lang = tweets['lang'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Languages', fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 languages', fontsize=15, fontweight='bold')
tweets_by_lang[:5].plot(ax=ax, kind='bar', color='red')

tweets_by_country = tweets['country'].value_counts()

fig, ax = plt.subplots()
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=10)
ax.set_xlabel('Countries', fontsize=15)
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Top 5 countries', fontsize=15, fontweight='bold')
tweets_by_country[:5].plot(ax=ax, kind='bar', color='blue')


def word_in_text(word, text):
    if text is None:
        return False
    word = word.lower()
    text = text.lower()
    match = re.search(word, text)
    if match:
        return True
    else:
        return False

tweets['python'] = tweets['text'].apply(lambda tweet: word_in_text('python', tweet))
tweets['javascript'] = tweets['text'].apply(lambda tweet: word_in_text('javascript', tweet))
tweets['ruby'] = tweets['text'].apply(lambda tweet: word_in_text('ruby', tweet))
tweets['java'] = tweets['text'].apply(lambda tweet: word_in_text('java', tweet))



print tweets['python'].value_counts()[True]
print tweets['javascript'].value_counts()[True]
print tweets['ruby'].value_counts()[True]
print tweets['java'].value_counts()[True]


prglangs = ['python', 'javascript', 'ruby', 'java']
tweets_by_prg_lang = [tweets['python'].value_counts()[True], tweets['javascript'].value_counts()[True], tweets['ruby'].value_counts()[True], tweets['java'].value_counts()[True]]

x_pos = list(range(len(prglangs)))
width = 0.6
fig, ax = plt.subplots()
plt.bar(x_pos, tweets_by_prg_lang, width, alpha=1, color='black')

# Setting axis labels and ticks
ax.set_ylabel('Number of tweets', fontsize=15)
ax.set_title('Ranking: python vs. javascript vs. ruby vs. java ', fontsize=10, fontweight='bold')
ax.set_xticks([p + 0.4 * width for p in x_pos])
ax.set_xticklabels(prglangs)
# plt.show()
plt.grid()

plt.savefig('tweet_by_prg_language_1', format='png')


tweets['relevant'] = tweets['text'].apply(lambda tweet: word_in_text('programming', tweet) or word_in_text('tutorial', tweet))


# extracting links from the tweets


def extract_link(text):
    regex = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

tweets_relevant = tweets[tweets['relevant'] == True]
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']

# printing the links with links present in them
print tweets_relevant_with_link[tweets_relevant_with_link['python'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['javascript'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['ruby'] == True]['link']

