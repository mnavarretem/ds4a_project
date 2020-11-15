# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 08:36:32 2020
Description: Functions to perform data analytics in Google Colab.
@author: Henry
"""
# Do the Imports
import pandas as pd                     #Package to manage dataframes
import nltk
import time
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


def stopwords_correction(df, column):
    "Eliminate stopwords from the processed comment"
    print('working on it!')
    stopWords_ls = stopwords.words("spanish")
    df[column] = df[column].apply(lambda x: " ".join([i for i in nltk.word_tokenize(x.lower()) if i not in stopWords_ls]) if not pd.isnull(x) else x)
    return df


# Following code grabbed from:
# https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a
# we will use it in our context to create some visualizations.
def get_top_n_words(corpus, n=1,k=1):
    stopWords_ls = stopwords.words("spanish")
    vec = CountVectorizer(ngram_range=(k,k),stop_words = stopWords_ls).fit(corpus.values.astype('U'))
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]