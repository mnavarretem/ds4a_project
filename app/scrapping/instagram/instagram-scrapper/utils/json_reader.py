import pandas as pd
# import numpy as np 
import json
import glob
import os 
import preprocessor as p
from datetime import datetime
from functions.data_exploring import *

class json_reader:
    '''
        This object read all the .json files from the data folder and returns two data frames with the format of the DB. It also has methods for cleaning those folders.
    '''
    def __init__(self):
        self.post_names = glob.glob(os.path.join('data', 'posts', '*.json'))
        self.comm_names = glob.glob(os.path.join('data', 'comments', '*.json'))
        self.read_files()
        self.updating_columns()


    '''
        This function reads all the JSON files in the data folder and generates two dataframes, one of post and other for comments.
    '''

    def read_files(self):
        post_dfs = []
        for name in self.post_names:
            post_dfs.append(pd.read_json(name))
        self.posts = pd.concat(post_dfs, ignore_index=True)

        comm_dfs = []
        for name in self.comm_names:
            comm_dfs.append(pd.read_json(name))
        self.comments = pd.concat(comm_dfs, ignore_index=True)
    

    '''
        This function generates new columns for the dataframes (like hashtags or processed comment) and transform the time column into date format.
    '''

    def updating_columns(self):
        # Creating other columns for post
        self.posts['hashtags'] = self.posts.text.apply(lambda t: [h.match for h in p.parse(t).hashtags] if p.parse(t).hashtags else None)
        self.posts['time'] = self.posts.time.apply(datetime.fromtimestamp)

        # Creating other
        self.comments['time'] = self.comments.time.apply(datetime.fromtimestamp)
        self.comments['processed_comment'] = self.comments.text.str.lower()
        self.comments = stopwords_correction(self.comments, 'processed_comment')
    
    '''
        This function returns the dataframes created.
    '''

    def get_df(self):
        return self.posts, self.comments


    '''
        This function deletes all the JSON files in the data folder.
    '''

    def clean_files(self):
        print('Clean process started.')
        for post in self.post_names:
            os.remove(post)
        
        for comm in self.comm_names:
            os.remove(comm)
        print('Clean process ended.')
