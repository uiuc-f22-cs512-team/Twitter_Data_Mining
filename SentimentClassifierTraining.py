import Bayes
import Utils
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')
from math import *

# nltk
import nltk
from nltk.tokenize import RegexpTokenizer

import pandas as pd
import numpy as np
import matplotlib as nlp

from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import ComplementNB
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle


def process_tweet_content(tweet):
    tweet = Utils.clean_tweets(tweet)
    tweet = Utils.convert_abbrev_in_text(tweet)
    print("processed tweet: ", tweet)

def load_data():
    tweets=pd.read_csv('./data/twitter_sentiment_noemoticon.csv',encoding='latin', 
                   names = ['sentiment','id','date','query','user','tweet'])
    return tweets

def preprocess_data(tweets):    
    # sample a small debug dataset
    data = tweets.sample(n=50000)
    print("Dataset shape:", data.shape)

    # replace sentiment values to 0 (negative) or 1 (positive)
    data['sentiment']=data['sentiment'].replace(4,1)

    # remove unused features
    data.drop(['date','query','user'], axis=1, inplace=True)
    data.drop('id', axis=1, inplace=True)

    data['tweet'] = data['tweet'].astype('str')

    positives = data['sentiment'][data.sentiment == 1 ]
    negatives = data['sentiment'][data.sentiment == 0 ]

    print('Total length of the data is:         {}'.format(data.shape[0]))
    print('No. of positve tagged sentences is:  {}'.format(len(positives)))
    print('No. of negative tagged sentences is: {}'.format(len(negatives)))

    #Stop Words: A stop word is a commonly used word (such as “the”, “a”, “an”, “in”) 
    #that a search engine has been programmed to ignore,
    #both when indexing entries for searching and when retrieving them as the result of a search query.

    data['processed_tweets'] = data['tweet'].apply(lambda x: Utils.clean_tweets(x))
    data['processed_tweets'] = data['processed_tweets'].apply(lambda x: Utils.convert_abbrev_in_text(x))
    return data

def train_test_split_data(data):
    train_data, test_data = train_test_split(data, test_size=0.20,random_state=0)
    train_data = train_data.reset_index()
    test_data = test_data.reset_index()
    X_train=train_data['processed_tweets']
    y_train=train_data['sentiment']
    X_test=test_data['processed_tweets']
    y_test=test_data['sentiment']
    return X_train, y_train, X_test, y_test


def train_bayes_classifiers():
    tweets = load_data()
    data = preprocess_data(tweets)
    X_train, y_train, X_test, y_test = train_test_split_data(data)

    # perform bigram bayes
    predicted_labels_bigram = Bayes.bigramBayes(X_train, y_train, X_test)

    # perform naive bayes
    predicted_labels_naive = Bayes.naiveBayes(X_train, y_train, X_test)

    # evaluate bigram bayes
    accuracy, false_positive, false_negative, true_positive, true_negative = Utils.compute_accuracies(predicted_labels_bigram,y_test)
    nn = len(y_test)
    Utils.print_stats(accuracy, false_positive, false_negative, true_positive, true_negative, nn, "Bigram Bayes")

    # evaluate naive bayes
    accuracy, false_positive, false_negative, true_positive, true_negative = Utils.compute_accuracies(predicted_labels_naive,y_test)
    Utils.print_stats(accuracy, false_positive, false_negative, true_positive, true_negative, nn, "Naive Bayes")

    # Tokenization
    data = shuffle(data).reset_index(drop=True)
    tokenized_data=data['processed_tweets'].apply(lambda x: x.split())
    tokenized_data.head(5)

    token = RegexpTokenizer(r'[a-zA-Z0-9]+')
    cv = CountVectorizer(stop_words='english',ngram_range = (1,1),tokenizer = token.tokenize)
    text_counts = cv.fit_transform(data['processed_tweets'].values.astype('U'))

    X=text_counts
    y=data['sentiment']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20,random_state=0)

    # perform Complement Naive Bayes
    cnb = ComplementNB()
    cnb.fit(X_train, y_train)
    cross_cnb = cross_val_score(cnb, X, y,n_jobs = -1)

    # evaluate Complement Naive Bayes
    print("Cross Validation score = ",cross_cnb)                
    print ("Train accuracy ={:.2f}%".format(cnb.score(X_train,y_train)*100))
    print ("Test accuracy ={:.2f}%".format(cnb.score(X_test,y_test)*100))
    # train_acc_cnb=cnb.score(X_train,y_train)
    # test_acc_cnb=cnb.score(X_test,y_test)

    yh = cnb.predict(X_test)
    accuracy, false_positive, false_negative, true_positive, true_negative = Utils.compute_accuracies(yh.tolist(),y_test.tolist())
    nn = len(y_test)
    Utils.print_stats(accuracy, false_positive, false_negative, true_positive, true_negative, nn, "Complement Naive Bayes")

    return cnb

def main():
    train_bayes_classifiers()
    
main()