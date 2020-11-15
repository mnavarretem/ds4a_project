import pandas as pd
import numpy as np
import os
from functions.sentiment_analysis import *
import pickle

class classifier:
    '''
        This object takes in a dataset with a column named text, and do a sentiment analysis
        and a products classification based on the products that appears in the OFFCORSS_products
        dataset.
    '''

    def __init__(self, comments):
        self.comments = comments
        self.model_import()
        self.classify_df()
    

    '''
        This function import the model and the CSV files needed for the features extraction used in the model prediction.
    '''

    def model_import(self):
        products_file  = os.path.join('model', 'OFFCORSS_products.csv')
        self.products_words = pd.read_csv(products_file).drop(columns = 'Unnamed: 0')

        known_file = os.path.join('model', 'OFFCORSS_lexicon.csv')
        self.known_words = pd.read_csv(known_file)

        f = open(os.path.join("model", "classifier.pickle"), 'rb')
        self.logit_fit = pickle.load(f)
        f.close()


    '''
        This function get the features needed for the sentiment analysis. Is get the scores and classification for each comment. It also get the tokens and the products associed with the comments and merge them with the original comments dataset.
    '''

    def classify_df(self):
        data_responses = self.comments.reset_index(drop = True)

        vt_comment = []
        vt_tokens  = []
        vt_products= np.empty((0,len(self.products_words)), int)

        vt_mean    = []
        vt_sum     = []
        vt_size    = []
        vt_min     = []
        vt_max     = []
        vt_sentim  = []

        products_stm = stem_tokens(self.products_words.products)
        nm_lenData   = len(data_responses)

        for idx in range(0,nm_lenData):    
            
            # Get comment
            cur_comm = data_responses.loc[idx,['text']].values[0]
            
            # Get tokenized comment
            tokens, words = get_comment_tokens(cur_comm)
            
            # get products array
            product_inComments = np.in1d(products_stm, stem_tokens(words), assume_unique=True)
            product_inComments = product_inComments.astype(int) 
            product_inComments = product_inComments.reshape(1, len(self.products_words))

            
            # get classifier features    
            features_comment = get_comment_features(cur_comm, self.known_words)
            
            nm_mean = features_comment[0]
            nm_sum  = features_comment[1]
            nm_size = features_comment[2]
            nm_min  = features_comment[3]
            nm_max  = features_comment[4]
            
            # append classifier features
            vt_comment.append(cur_comm)
            vt_mean.append(nm_mean)
            vt_sum.append(nm_sum)
            vt_size.append(nm_size)
            vt_min.append(nm_min)
            vt_max.append(nm_max)
            
            # append comments tokens and products
            vt_tokens.append(tokens)
            vt_products = np.append(vt_products, product_inComments, axis=0)
            
        features_df = pd.DataFrame({'comment':vt_comment,'mean':vt_mean,'sum':vt_sum,'size':vt_size,
                                    'min':vt_min,'max':vt_max})

        tokens_df = pd.DataFrame({'comment':vt_comment,'tokens':vt_tokens})
        products_df = pd.DataFrame(vt_products, columns = self.products_words.products)

        score_df = self.sentiment_classify(features_df)

        self.merge_datasets(score_df, tokens_df, products_df)
    

    '''
        This function takes in a dataframe of features and returns the score and sentiment predicted for each row of the dataset.
    '''

    def sentiment_classify(self, features):
        vt_scoreLim = [1/3,2/3]

        comment_score = features.copy()
        comment_score['Intercept'] = 1.0
        
        comment_score["score"] = self.logit_fit.predict(comment_score[['Intercept',"mean", "sum", "max"]])

        vt_good = (comment_score["score"] >= vt_scoreLim[1])
        vt_bad = (comment_score["score"] <= vt_scoreLim[0])
        vt_neutral = (comment_score["score"] > vt_scoreLim[0]) & (comment_score["score"] < vt_scoreLim[1])

        comment_score["class"] = 'na'
        comment_score.loc[vt_good, "class"] = 'good'
        comment_score.loc[vt_bad, "class"] = 'bad'
        comment_score.loc[vt_neutral, "class"] = 'neutral'

        return comment_score
    

    '''
        This function merge the columns of the comments with the new columns of the classification.
    '''

    def merge_datasets(self, score, tokens, products):
        self.comments = pd.merge(self.comments, score[["score", "class"]], left_index = True, right_index=True)
        self.comments = pd.merge(self.comments, tokens[["tokens"]], left_index = True, right_index=True)
        self.comments = pd.merge(self.comments, products, left_index = True, right_index=True)


    '''
        This function returns the dataframe created.
    '''

    def get_df(self):
        return self.comments
