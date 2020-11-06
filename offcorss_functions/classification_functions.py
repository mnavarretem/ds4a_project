#import

import re
import nltk   
import sklearn
import pandas as pd

from nltk import word_tokenize  
from nltk.stem import SnowballStemmer 
from nltk.corpus import stopwords 
from string import punctuation  

from sklearn.feature_extraction.text import CountVectorizer

nltk.download('stopwords')

#..........................................................................................................................
# Define variables 
#..........................................................................................................................

# inicializar el extractor de raices lexicales
stemmer   = SnowballStemmer('spanish')

# inicializar la lista de palabras ignoradas 
non_words = list(punctuation)  

# agregar a la lista los signos de apertura y los digitos [1-9]
non_words.extend(['¿', '¡'])  
non_words.extend(map(str,range(10)))

# stop words should be updated to accept important words in our context (mostly for bigrams and trigrams)
nostopwords  = ['no','muy','pero','eso']
stopWords_ls = stopwords.words("spanish")
stopWords_ls = [word for word in stopWords_ls if word not in nostopwords]


# Open lexical dictionary
#known_words = pd.read_csv('OFFCORSS_lexicon.csv')

#..........................................................................................................................
# Define functions 
#..........................................................................................................................
# funcion de extraccion de raices lexicales
def stem(word):
    return stemmer.stem(word)

#..........................................................................................................................
# funcion de extraccion de raices lexicales sobre una lista
def stem_tokens(tokens):  
    stemmed = []
    for item in tokens:
        stemmed.append(stem(item))
    return stemmed

#..........................................................................................................................
# funcion de disgregacion de palabras 
def tokenize(text):  
    qgrams=[];
    trigrams=[];
    bigrams=[];
    text=text.lower()
    text = ''.join([c for c in text if c not in non_words])
    unigrams =  word_tokenize(text)
    #tokens = [t for t in tokens if t not in stopwords]
    if len(unigrams)>1:
        bigrams=[ x.lower()+" "+y.lower() for (x,y) in zip(unigrams,unigrams[1:])]
    if len(unigrams)>2:
        trigrams=[ x.lower()+" "+y.lower() for (x,y) in zip(bigrams,unigrams[2:])]
    if len(unigrams)>3:
        qgrams=[ x.lower()+" "+y.lower() for (x,y) in zip(trigrams,unigrams[3:])]
    tokens=qgrams+trigrams+bigrams+unigrams
    tokens = stem_tokens(tokens)
    return tokens

#..........................................................................................................................
# Convert words to ngrams
def words_to_ngrams(words, n, sep=" "):
    ngrams = [sep.join(words[i:i+n]) for i in range(len(words)-n+1)]
    return  ngrams

#..........................................................................................................................
# get unique words 
def get_unique_tokens(comment_ls):
    
    words_ls = []
    
    for text in comment_ls:
        text  = " ".join(re.findall("[a-zA-Z]+", text))
        words =  word_tokenize(text)
        words = [word for word in words if word not in stopWords_ls]
        
        words_ls.append(list(set(words)))
        
    words_ls = [item for sublist in words_ls for item in sublist]    
     
    return list(set(words_ls))

#..........................................................................................................................
# get tokens
def get_tokenized(text):
    
    words =  word_tokenize(text)    
    words = [str.strip(word) for word in words if word not in stopWords_ls]
    
    # get ngrams
    ugrams = words_to_ngrams(words,1)
    bgrams = words_to_ngrams(words,2)
    tgrams = words_to_ngrams(words,3)
    
    ngrams = [ugrams,bgrams,tgrams]
    
    return  [item for sublist in ngrams for item in sublist]
#..........................................................................................................................
# get comment tokens
def get_comment_tokens(test_comment):
    
    words =  word_tokenize(test_comment)  
    words = [str.strip(word) for word in words if word not in stopWords_ls]
    comment_tokens = " ".join(words)
    
    return comment_tokens,words

#..........................................................................................................................
# Define features for classification
def get_comment_features(test_comment,known_words):

    test_comment = test_comment.replace(" . ", " ").replace(" , ", " ").replace(" .", "")

    tokens = get_tokenized(test_comment)
    tokens = stem_tokens(tokens)

    elem_scores = []
    scores_vals = []

    for cur_word in tokens:
        if cur_word in known_words['stem'].values:
            element   = known_words[known_words['stem'] == cur_word]
            cur_score = element.score.values[0] 
        else:
            cur_score = 0

        elem_scores.append((cur_word,cur_score))
        scores_vals.append(cur_score)

    if len(scores_vals) > 0 :   
        features_comment = [sum(scores_vals) / len(scores_vals),sum(scores_vals),len(scores_vals), min(scores_vals), max(scores_vals)]
    else:
        features_comment = [0,0,0,0,0]
    
    return features_comment
