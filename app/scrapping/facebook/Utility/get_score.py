
# coding: utf-8

import numpy as np
import pandas as pd
import nltk
from sentiment_analysis import *

nltk.download('punkt')

df = pd.read_csv('data/csv/facebook.csv', delimiter=",")

df["Me encanta"] = df["Me encanta"].fillna(value=0)
df["Me enfada"] = df["Me enfada"].fillna(value=0)
df["Me asombra"] = df["Me asombra"].fillna(value=0)
df["Me divierte"] = df["Me divierte"].fillna(value=0)
df["Me entristece"] = df["Me entristece"].fillna(value=0)
df["Me importa"] = df["Me importa"].fillna(value=0)

df["Pos"] = df["Me encanta"].astype("int") + df["Me divierte"].astype("int")
df["Neg"] = df["Me enfada"] + df["Me entristece"]
df["Neu"] = df["Me asombra"] + df["Me importa"]


df["score"] = 0.5*(df.Pos - df.Neg)/(df.Pos + df.Neg + df.Neu + 1) + 0.5

products_file  = 'Utility/offcorss_products.csv'
products_words = pd.read_csv(products_file).drop(columns = 'Unnamed: 0')
data_responses = df.copy()

vt_tokens  = []
vt_products= np.empty((0,len(products_words)), int)

products_stm = stem_tokens(products_words.products)
nm_lenData   = len(data_responses)

for idx in range(0,nm_lenData):    
    
    # Get comment
    cur_comm = data_responses.loc[idx,['text']].values[0]
    
    # Get tokenized comment
    tokens, words = get_comment_tokens(str(cur_comm))
    
    # get products array
    product_inComments = np.in1d(products_stm, stem_tokens(words), assume_unique=True)
    product_inComments = product_inComments.astype(int) 
    product_inComments = product_inComments.reshape(1, len(products_words))
    
    # append comments tokens and products
    vt_products = np.append(vt_products, product_inComments, axis=0)
    
products_df = pd.DataFrame(vt_products, columns = products_words.products)

df2 = pd.merge(df.drop(columns=["Neg", "Pos", "Neu"]), products_df, left_index = True, right_index=True)


df.loc[df.text.isnull(), 'text'] = ''

df.reset_index(drop=True, inplace=True)

df2.to_csv('data/csv/facebook_tables.csv', encoding="utf-8-sig")

