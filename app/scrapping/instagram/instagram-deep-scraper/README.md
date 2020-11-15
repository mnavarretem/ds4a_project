# Instagram Deep Scraper

This section contains all the pipeline of data acquisition, data cleaning, data processing, sentiment analysis and product recognition for all the posts (and comments) from OFFCORSS and their competitors in instagram.
 
We have called it *deep scraping* because in this section we describe how we get all the long historic instagram publications (from january of 2019 to october 2020). Another development was made to extract all the recent posts and comments, and refresh them into the database.
 
From this directory, it would be interesting to highlight what you are going to find in all notebooks and directories:
* **01_deep_scraper.ipynb:** This notebook describes how we do the data scraping with a python library.
* **02_creating_CSV.ipynb:** This notebook describes how we take all the `.json` files, clean the needed columns and unificated them into three `csv` files.
* **03_sentiment_products.ipynb:** This notebook describes how we take all the instagram comments (in the instagram_responses CSV) and apply the trained model to get a score and a description of the sentiment that the comment has.
* The folders named **offcorss**, **epk** and **politokids** contain all the `.json` files that we got in the scraping. 
* The **data** folder contains the clean `csv` files.