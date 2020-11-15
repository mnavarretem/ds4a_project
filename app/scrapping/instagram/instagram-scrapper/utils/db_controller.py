import pandas as pd
from sqlalchemy import create_engine, text
from utils.db_credentials import *

class db_controller:
    '''
        This object takes in two datafames (posts and comments) and insert into the database with the credentials of db_credentials.py file.
    '''

    def __init__(self, posts, comments):
        self.posts = posts.reset_index()
        self.comments = comments.reset_index()
        self.engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')
        self.order_df()
    

    '''
        This functions splits the post dataframe into two dataframes that match the structure and name of the tables in the database.
    '''

    def order_df(self):
        self.ig_posts = self.posts[['index', 'post_id', 'text', 'time', 'type', 'is_video', 'is_ad', 'post_url', 'hashtags', 'brand_username']].rename(columns={'index':'id_inst', 'post_id':'id_post', 'time':'date_post', 'type':'post_type'})
        self.ig_reactions = self.posts[['index', 'post_id', 'brand_username', 'total_reactions', 'total_comments']].rename(columns={'index':'id_react'})
        self.ig_response = self.comments.copy().rename(columns={'index':'id_response', 'time':'post_date'})


    '''
        This function deletes all the repeated rows of the database.
    '''

    def delete_repeated(self):
        with self.engine.connect() as connection:
            ids = ', '.join(list(self.ig_posts.id_post.astype('str')))
            connection.execute(f'DELETE FROM instagram_reactions WHERE post_id IN ({ids})')
            connection.execute(f'DELETE FROM instagram_response WHERE rootPost_id IN ({ids})')
            connection.execute(f'DELETE FROM instagram_post WHERE id_post IN ({ids})')


    '''
        This function insters into the database the extracted data.
    '''

    def insert_into(self):
        try:
            self.delete_repeated()
            self.ig_posts.to_sql(name="instagram_post", con=self.engine, index=False, if_exists='append')
            self.ig_reactions.to_sql(name="instagram_reactions", con=self.engine, index=False, if_exists='append')
            self.ig_response.to_sql(name="instagram_response", con=self.engine, index=False, if_exists='append')
        except Exception as error:
            print("Error inserting the data: ",error)