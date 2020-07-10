# Twitter-Search-Sentiment-Analysis

Gets the amount of positive and negatives tweets mentioning a specified search term and write the results to a file. 

Uses tweepy to get the tweets and textblob to perform the sentiment analysis

Can be run once, returning the amount of positive and negative tweets for the search term and amount of tweets

Or run forever in specified intervals and write the results to a file

### Dependencies

Python 3 is recommended

Installation:
```
pip install requirements.txt 
```

## Usage

The program can be from the command terminal.

For it to work, consumer_key, consumer_secret, access_token and access_token_secret must be added to "keys.txt"

```
python3 TwitterSent.py --search %SearchTerm% --interval %IntervalMinutes% --amount %ResultAmount% --filename %PathToResultFile%  
```

For example, the following command will get the 50 most recent tweets mentioning "Apples" and write the amount of positive and negative tweets to the file "output.txt". It will do this every 30 minutes until the program is stopped.

```
python3 TwitterSent.py —search Apples —interval 30 --amount 50 --filename output.txt  
```
#### Parameters:

Parameter 			        | Flag 	| Description
------------------------|------------|------------
Search term     	| `--search`	| The keyword/string that is searched for on twitter
Run interval (minutes)           | `--interval`	| The amount of minutes the program waits before running again after the first time 
Amount of tweets 			        | `--amount`	| How many tweets it gathers and performs sentiment analysis on
Output filename     	| `--filename`	| The filename of the file which contains the time and results from each run. It will be created if it does not already exist


It can also be used a package. Example in example.py

```
>>> from TwitterSent import TwitterSentiments
>>> tw = TwitterSentiments(consumer_key=consumer_key, consumer_secret=consumer_secret,
                       access_token=access_token, access_token_secret=access_token_secret)
>>> positive_sentiments, negative_sentiments = tw.run(searchTerm="Test search", amount=100)
```
