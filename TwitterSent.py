import tweepy
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import time
import os
import sys


class TwitterSentiments:

    def __init__(self, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

        # Get keys from file if not already passed
        if not (self.consumer_key or self.consumer_secret or self.access_token or self.access_token_secret):

            with open('keys.txt', 'r') as f:
                contents = f.readlines()
                self.consumer_key = contents[0].split(":")[1].strip(" ").rstrip()
                self.consumer_secret = contents[1].split(":")[1].strip(" ").rstrip()
                self.access_token = contents[2].split(":")[1].strip(" ").rstrip()
                self.access_token_secret = contents[3].split(":")[1].strip(" ").rstrip()

        # Connect to API
        connect = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        connect.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(connect)

    def run(self, searchTerm=None, popular = False, amount=10, write_to_file = False, filename="sentiments.txt"):

        # Popular or recent tweets
        stype = "recent" if not popular else "popular"

        # Get the tweets
        tweets = self.api.search(q=searchTerm, result_type=stype, count=amount)

        # Clean tweets and perform sentiment analysis
        positive_tweets = 0
        negative_tweets = 0

        for tweet in tweets:

            # Remove usernames
            cleaned_tweet = re.sub(r"(^|[^@\w])@(\w{1,15})\b", "", tweet.text)

            # Remove "RT"
            cleaned_tweet = cleaned_tweet.replace("RT", "")

            # Remove urls
            cleaned_tweet = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', cleaned_tweet)

            # Get sentiment
            tblob = TextBlob(cleaned_tweet, analyzer=NaiveBayesAnalyzer())

            if tblob.sentiment.classification == "pos":
                positive_tweets += 1
            else:
                negative_tweets += 1

        if write_to_file:
            # Create header if file does not exist
            if os.path.exists(filename) == False:

                with open(filename, 'a') as outfile:
                    outfile.write("time, positive_tweets, negative_tweets\n")

            # Write time, amount of positive and negatives tweets to file
            with open(filename, 'a') as outfile:
                outfile.write(str(time.time()) + ", " + str(positive_tweets) + ", " + str(negative_tweets) + "\n")

        return positive_tweets, negative_tweets

    def interval_run(self, interval_minutes=60, searchTerm=None, popular = False, amount=10, write_to_file = False,
                     filename="sentiments.txt"):

        amount_of_runs = 0

        print("Starting twitter sentiment analyzer.")
        print("Searching for:", searchTerm)
        print("Analysing", amount, "tweets every", interval_minutes, "minutes.")

        if popular:
            print("Tweets sorted by popularity.")
        else:
            print("Tweets sorted by recent.")

        if write_to_file:
            print("Writing to file:", filename)

        while True:

            print("_________________________________________________________________________")
            print("Run:", amount_of_runs)

            pos_sentiment, neg_sentiment = self.run(searchTerm=searchTerm, popular=popular, amount=amount,
                                                    write_to_file=write_to_file, filename=filename)

            print("Time:", time.time(), "Positive tweets:", pos_sentiment, "Negative tweets", neg_sentiment)

            amount_of_runs += 1

            time.sleep(interval_minutes * 60)


if __name__ == '__main__':

    # Parse arguments to method call
    if len(sys.argv) > 1:

        for index in range(len(sys.argv)):

            if sys.argv[index] == "--search":
                searchTerm = str(sys.argv[index + 1])

            if sys.argv[index] == "--interval":
                interval = int(sys.argv[index + 1])

            if sys.argv[index] == "--amount":
                amount = int(sys.argv[index + 1])

            if sys.argv[index] == "--filename":
                filename = str(sys.argv[index + 1])


        ts = TwitterSentiments()
        ts.interval_run(searchTerm=searchTerm, amount=amount, write_to_file=True, filename=filename,
                        interval_minutes=interval)
    else:
        print("No arguments found. Specify --search, --interval, --amount and --filename")
