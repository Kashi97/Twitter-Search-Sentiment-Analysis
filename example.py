from TwitterSent import TwitterSentiments

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

tw = TwitterSentiments(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret)

# Get the amount of positive and negative tweets of the 100 most recent tweets mentioning "Apples, sorted by popularity"
positive_sentiments, negative_sentiments = tw.run(searchTerm="Apples", popular=True, amount=100)

print("Tweets mentioning Apples")
print("Positive:", positive_sentiments)
print("Negative:", negative_sentiments)