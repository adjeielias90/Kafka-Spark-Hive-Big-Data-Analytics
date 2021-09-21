from numpy.core.arrayprint import str_format
import pandas as pd
# from googletrans import Translator, constants
# from pprint import pprint
# from textblob import TextBlob as tb
from textblob import TextBlob
from textblob.en.sentiments import NaiveBayesAnalyzer
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt

# assign column names to variable
col_names = ['tweet']

# read our data from hive as a pandas dataframe, pass column names as columns
big_data = pd.read_csv('./datasets/big_data.csv', sep="\n", names=col_names)
programming = pd.read_csv('./datasets/programming.csv', sep="\n", names=col_names)
olympics = pd.read_csv('./datasets/olympics.csv', sep="\n", names=col_names)

# load our kabul datatset from twitter
# however, most of our dataset is not in english. Unfortunately this is one of the drawbacks of data mining.
# data may not be in the format we expect
kabul = pd.read_csv('./datasets/kabul.csv', sep="\n", names=col_names)

# custom method to use naive bayes algo to analyze and classify sentiments
def get_sentiment(tweet):
    tweet_blob_object = TextBlob(str(tweet), analyzer=NaiveBayesAnalyzer())
    sentiment = tweet_blob_object.sentiment
    print(tweet +": "+ sentiment[0])
    return sentiment[0]

# create a sentiment column and pass output of our sentiment classifier to it
olympics['sentiment'] = pd.Series(dtype=str)
# olympics['sentiment_value'] = pd.Series(dtype=str)
olympics['sentiment'] = olympics['tweet'].apply(lambda tweet: get_sentiment(tweet))


programming['sentiment'] = pd.Series(dtype=str)
programming['sentiment'] = programming['tweet'].apply(lambda tweet: get_sentiment(tweet))



# print(olympics.head())

# implace string data with integers to facilitate data visualization
olympics.sentiment = olympics.sentiment.replace({'pos': 1, 'neg': 0})
programming.sentiment = programming.sentiment.replace({'pos': 1, 'neg': 0})

# plot our graphs to visualize data
olympics['sentiment'].plot(kind='hist', bins=10, figsize=(8,10), title="2021 Olympics Sentiments: Positive:1, Negative: 0")
plt.show()

programming['sentiment'].plot(kind='hist', bins=10, figsize=(8,10), title="2021 Programming Sentiments: Positive:1, Negative: 0")
plt.show()

# save results of our analyses to disk as csv files
olympics.to_csv(r'./analyzed_data/olympics.csv', index=True, header=True)
programming.to_csv(r'./analyzed_data/programming.csv', index=True, header=True)


# print(olympics.head())
# olympic_sentiments = pd.DataFrame(columns = ['tweet', 'sentiment'])


'''
    After streaming our data into hive, the data in our warehouse isnt't useful until we can
    do something with it. We make our data useful by exporting it from our warehouse into files
    dpending on the topics we assigned in our Kafka producer. For the purpose of our exercise,
    we selected tweets about programming and the olympics.

    Our data is not if a format we can directly represent visually, so we run some data pre-processing
    to convert the data into a format that will be acceptable by our visualization process.
    We do this by using a python library called pandas, which loads our data into a dataframe
    from the CSV files. We also create an extra column on our data, "sentiment", where we store
    the sentiment expressed(positive or negative) about the topic.
    We will use some pretty basic machine learning for this.

    We then use a generic library which has natural languauge processing libraries inbuilt to try and
    make sense and meaning from our data. In view of this we use the naive bayes analyzer which uses probabilities
    based on the bayes theorem to determine strong independent assumptions between features.
    We store the result of the classification into a sentiment column in our pandas dataframe.
    Sentiment of a tweet may be either positive or negative, but never both or none.

    While this algorithm is far from perfect and we can definitely achieve better accuracy
    with a custom sentiment classifier we wrote from scratch, it gives us a wide view of how things
    can be.

    We can then run a transformation and convert all poisitive sentiments to 1
    negative sentiments to 0, so we can visualize our data with matplotlib.
    We will also visualize our data we plotly later, once we export our data frames
    as csv files.


    Yes, you have done all that, but what can you actually do with this information, one may ask?
    
    To answer the question, let consider the scenario that we are the committee responsible for the olympics
    Now with this information, we can actually determine opinion about our performance and
    positive or negative sentiments surrounding our program.

    If sentiments surrouding the olympics are largely positive on social media and
    other personalized public data sources, we can say with confidence that people like
    our events, and we can continue doing what ever we are doing.
    However if sentiments are mostly negative, then we can confidently assume we aren't doing
    everything right and some changes and improvments can be made.
    In short, we are able to make informed decisions based on data, and this is just on scenario of many you can
    think of
    
    This is one of the main points of Big Data. 

'''