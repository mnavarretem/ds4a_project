# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 08:36:32 2020
Description: Functions to perform data analytics in Google Colab.
@author: Henry
"""
# Do the Imports
import pandas as pd                     #Package to manage dataframes
import os                               #Operative system package
import sys                              #System package
from autocorrect import Speller         #Speller Package
import time                             #Package for measuring processing time
import nltk
import time
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def stopwords_correction(df, column):
    "Eliminate stopwords from the processed comment"
    print('working on it!')
    stopWords_ls = stopwords.words("spanish")
    df[column] = df[column].apply(lambda x: " ".join([i for i in nltk.word_tokenize(x.lower()) if i not in stopWords_ls]) if not pd.isnull(x) else x)
    return df

def spell_correction(df, column_inp, column_out, spell):
    # Perform spell correction on a string column of a pandas dataframe. Return the same dataframe with a new column
    # with the spell correction
    print('working on it!')
    df[column_out] = df[column_inp].apply(lambda x: " ".join([spell(i) for i in nltk.word_tokenize(x.lower())]) if not pd.isnull(x) else x)
    return df

def loading_data(filename, basepath, extension):
    # Asumptions: The processed file is saved in the same folder with the pattern filename+'P'
    # Exist a column named "Comment" for which it is performed the data processing
    # Function  read csv files and return a pandas dataframe, exist the csv file.
    # First check if the processed file exist, this is due the fact that performing spell correcting is time demanding, so it is
    # better to save and load the result onces the comments are processed
    processed_filename = filename+'P'
    processed_path = os.path.join(basepath,processed_filename+'.'+extension)
    #Check if the processed file exist, if exist load this file.
    if os.path.exists(processed_path):
        data = pd.read_csv(processed_path)
    else:
        start_time = time.time()
        #Load the Speller
        spell = Speller(lang='es')
        #load the crude data
        data_init = pd.read_csv(os.path.join(basepath, filename+'.'+extension))
        #Perform spell correction and use lower letters to the comment column
        data = spell_correction(data_init, 'Comment', 'processed comment', spell)
        #Eliminates stopwords.
        data = stopwords_correction(data, 'processed comment')      
        #Save file with the format of processed file
        try:
            data.to_csv(processed_path)
        except:
            print("Oops!", sys.exc_info()[0], "occurred.")
            raise Exception("Couldn't save the dataframe") 
        print(time.time() - start_time)
    return data


# Following code grabbed from:
# https://towardsdatascience.com/a-complete-exploratory-data-analysis-and-visualization-for-text-data-29fb1b96fb6a
# we will use it in our context to create some visualizations.
def get_top_n_words(corpus, n=1,k=1):
    stopWords_ls = stopwords.words("spanish")
    vec = CountVectorizer(ngram_range=(k,k),stop_words = stopWords_ls).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]














