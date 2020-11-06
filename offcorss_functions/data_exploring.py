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
from nltk.corpus import stopwords       #Natural language processint toolkit stopwords packages


def loading_data(data_path):
    # Function that read csv files and return a pandas dataframe
    data = pd.read_csv(data_path)
    return data


def spell_correction(df, column_inp, column_out, spell):
    # Perform spell correction on a string column of a pandas dataframe. Return the same dataframe with a new column
    # with the spell correction
    print('working on it!')
    df[column_out] = df[column_inp].apply(lambda x: " ".join([spell(i) for i in x.lower().split()]) if not pd.isnull(x) else x)
    return df


def word_count(df, column):
    # Count the number of words on a pandas dataframe column and remove stop words. The input is a dataframe and the
    # column name for which the words will be counted. It outputs a dataframe with the words and the counts.
    count_word = df[column].str.split(expand=True).stack().value_counts().reset_index()
    stop = stopwords.words('spanish')
    word_list = count_word['index']
    drop_index = [i for i in range(len(word_list)) if word_list[i] in stop]
    count_word.drop(drop_index, axis=0, inplace=True)
    return count_word


def save_dfdata(df,name):
    # Save a dataframe in a csv file
    try:
        df.to_csv('data/'+name+'.csv')
    except:
        print("Oops!", sys.exc_info()[0], "occurred.")
        raise Exception("Couldn't save the dataframe")


def _main_():
    processed_file_datasatisfaction = 'satisfaction_ratingP'
    processed_file_npsresponse = 'NPS_responsesP'
    if os.path.exists(os.path.join(os.getcwd(),'data',processed_file_datasatisfaction+'.csv')):
        data_satisfaction = loading_data(os.path.join(os.getcwd(),'data',processed_file_datasatisfaction+'.csv'))
    else:
        start_time = time.time()
        spell = Speller(lang='es')
        data_satisfaction = loading_data('data/satisfaction_Ratings.csv')
        data_satisfaction = spell_correction(data_satisfaction, 'Comment', 'processed comment', spell)
        save_dfdata(data_satisfaction, processed_file_datasatisfaction)
        print(time.time() - start_time)

    if os.path.exists(os.path.join(os.getcwd(), 'data', processed_file_npsresponse+'.csv')):
        data_responses = loading_data(os.path.join(os.getcwd(), 'data', processed_file_npsresponse+'.csv'))
    else:
        start_time = time.time()
        spell = Speller(lang='es')
        data_responses = loading_data('data/NPS_Responses.csv')
        data_responses = spell_correction(data_responses, 'Comment', 'processed comment', spell)
        save_dfdata(data_responses, processed_file_npsresponse)
        print(time.time() - start_time)

    print('there are ' + str(len(data_satisfaction['Ticket Id'].unique())) + ' unique tickets')
    print('there are ' + str(len(data_satisfaction)) + ' tickets')
    duplicate_tickets = data_satisfaction.groupby('Ticket Id').size().sort_values(ascending=False).reset_index(name ='tickets count')
    duplicate_example = data_satisfaction[data_satisfaction['Ticket Id'] == duplicate_tickets['Ticket Id'][3]]

    satisfaction_wordcount = word_count(data_satisfaction, 'processed comment')
    print('finished...')


if __name__ == '__main__':
    _main_()













