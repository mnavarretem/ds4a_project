
# coding: utf-8

# **Facebook CSV concatenate**

import pandas as pd

# Import CSVs
epk_posts = pd.read_csv("data/csv/epk_fb_posts.csv")
epk_reactions = pd.read_csv("data/csv//epk_fb_reactions.csv")
offcorss_posts = pd.read_csv("data/csv/offcorss_fb_posts.csv")
offcorss_reactions = pd.read_csv("data/csv/offcorss_fb_reactions.csv")
polito_posts = pd.read_csv("data/csv/PolitoColombia_fb_posts.csv")
polito_reactions = pd.read_csv("data/csv/PolitoColombia_fb_reactions.csv")

#Merging Posts and Reactions
offcorss = offcorss_posts.merge(offcorss_reactions, on='post_id')
offcorss.loc[:, 'brand_username'] = 'offcorss'
epk = epk_posts.merge(epk_reactions, on='post_id')
epk.loc[:, 'brand_username'] = 'epk'
polito = polito_posts.merge(polito_reactions, on='post_id')
polito.loc[:, 'brand_username'] = 'polito'

#Integrate Facebook DF
facebook = offcorss.append(epk)
facebook = facebook.append(polito)

#Lengh check
print(len(epk))
print(len(polito))
print(len(offcorss))
print(len(facebook))

#Replace NaN for Zero in last columns
facebook['Me gusta'].fillna(0, inplace=True)
facebook['Me encanta'].fillna(0, inplace=True)
facebook['Me enfada'].fillna(0, inplace=True)
facebook['Me importa'].fillna(0, inplace=True)
facebook['Me asombra'].fillna(0, inplace=True)
facebook['Me divierte'].fillna(0, inplace=True)
facebook['Me entristece'].fillna(0, inplace=True)
facebook['likes'].fillna(0, inplace=True)

#Export CSV
facebook.to_csv('data/csv/facebook.csv', index = True)

