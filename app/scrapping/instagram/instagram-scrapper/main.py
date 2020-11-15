import pandas as pd
from utils.scraper import *
from utils.classifier import *
from utils.db_controller import *
from utils.json_reader import *

print('Process started... "Scraping profiles"')
scraper = Scraper()
print('Process ended... "Scraping profiles"')

print('Process started... "Reading JSON files"')
reader = json_reader()
posts, comments = reader.get_df()
print('Process ended... "Reading JSON FILES"')

print('Process started... "Classifying comments"')
classif = classifier(comments.copy())
comments = classif.get_df()
print('Process ended... "Classifying comments"')

print('Process started... "Inserting into DB"')
db = db_controller(posts, comments)
db.insert_into()
print('Process ended... "Inserting into DB"')

print('Cleaning the JSON files.')
reader.clean_files()