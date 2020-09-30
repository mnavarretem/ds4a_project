import json
from facebook_scraper import get_posts

clients = ["offcorss", "epk", "PolitoColombia"]

def scrap_facebook_post(n = 100):

    for client in clients:
        posts = []
        with open('../data/{}_fb_posts.json'.format(client), 'w') as json_file:
            for post in get_posts(client, pages=n):
                posts.append(post)
            json.dump(posts, json_file, default=str)
