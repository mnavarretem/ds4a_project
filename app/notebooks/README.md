# Notebooks
This section contains all the notebooks that were used for the exploratory data analysis, the implementation of a model for sentiment analysis and the use of that model to predict the sentiment analysis of all the datasets that we have (nps, survey responses and instagram comments).

## Exploratory Data Analysis (EDA)
All the basics analysis were compiled in three notebooks:
* **data_exploring.ipynb**: in this notebook we have made a first analysis of the `nps_responses` and `satisfaction_ratings`, analysing the frequency of the words and n-grams that appear in each dataset. Also, we have made an analysis over time.
* **data_analysis.ipynb**: in this notebook we have cleaned and analyzed semantically the data. Also, here is documented all the fields that appear in the datasets. The previous analysis that we have made in the data_exploring was complemented.
* **Instagram_Posts.ipynb**: in this notebook we have made an analysis of the post and commentaries of instagram, comparing offcorss with the competitors. We have shown some interesting features like the variation of number of posts and number of likes over time, and the most common words and n-grams in the posts and comments.

## Training the model
The sentiment analysis model was based on a spanish lexicon model for sentiment analysis named `sentec` (we have left a copy of the original repository in the folder).
 
* **sentWord.ipynb**: this notebook contains the process to translate the dataset of the `SentiWordNet.csv` in order to have a core for doing the sentiment analysis model based on lexicon.
* **Semantic analysis.ipynb**: this notebook contains the implementation of the model for sentiment analysis based on lexicon. We have implemented different models (logit, Support Vector Machines, random forest, Naive Bayes classifier) and compared them using cross validation. After that, we noticed that the one with the best performance was the logit model.

## Predicting the sentiment and recognizing products
Now that we have the trained model, we present here the application of the model to predict the sentiment of all the commentaries that we have from the customers (in nps, rating survey and instagram comments).
 
* **preprocess_ventas.ipynb**: In this notebook we propress the sales information that offcorss have provided us, and from them we have extracted the most common products in a csv file named `offcorss_products.csv`.
* **preprocess_nps_comments.ipynb**, **preprocess_satisfaction_comments.ipynb**: these notebooks contain the preprocess corpus applied for each dataset that contains customer responses.
* **process_integrate_survey_responses.ipynb**: this notebook contains an analysis of the `satisfaction rating` compared with the sales information.