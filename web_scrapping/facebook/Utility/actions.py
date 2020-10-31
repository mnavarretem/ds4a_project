import json
import re

import pandas as pd
import scraper as sc
from bs4 import BeautifulSoup
from robot.api import logger

path = {"post": "data/{}_fb_posts.json",
        "reactions": "data/{}_fb_reactions.json"
        }


def get_posts_ids(client):
    with open(path["post"].format(client)) as file:
        data = json.load(file)
        ids = [post['post_id'] for post in data]
    return ids


def get_reactions_ids(client):
    with open(path["reactions"].format(client)) as file:
        data = json.load(file)
        ids = [id for id in data]
    return ids


def update_last_posts(client, n=10):
    ids = get_posts_ids(client)
    posts = [post for post in sc.get_posts(client, pages=n) if not post['post_id'] in ids]
    with open(path["post"].format(client), 'r') as json_file:
        old = json.load(json_file)
        new = posts + old
    with open(path["post"].format(client), 'w') as json_file:
        json.dump(new, json_file, default=str)


def get_pending_reactions_ids(client):
    post_ids = set(get_posts_ids(client))
    react_ids = set(get_reactions_ids(client))
    pending_reactions_ids = post_ids.difference(react_ids)
    return pending_reactions_ids


def get_posts_url(page):
    file_path = path["post"].format(page)
    update_last_posts(page, 10)
    pending_reactions_ids = get_pending_reactions_ids(page)
    urls = []
    with open(file_path, 'r') as json_file:
        posts = json.load(json_file)
        for post in posts:
            if post["post_id"] in pending_reactions_ids:
                url = "https://www.facebook.com/{}/posts/{}".format(page, post["post_id"])
                urls.append([post["post_id"], url])
    # logger.console(urls)
    # print(urls)
    return urls


print(get_posts_url("epk"))


def write_reactions_json(page, reactions_dict):
    file_path = path["reactions"].format(page)
    with open(file_path, 'w') as json_file:
        json.dump(reactions_dict, json_file)


def get_comments(html_source):
    soup = BeautifulSoup(html_source, 'html.parser')
    # logger.console(soup)
    logger.console(extract_comments(soup))


def extract_comments(item):
    # logger.console(item)
    postComments = item.findAll("div", {"class": "_4eek"})
    comments = dict()
    # print(postDict)
    for comment in postComments:
        if comment.find(class_="_6qw4") is None:
            continue

        commenter = comment.find(class_="_6qw4").text
        comments[commenter] = dict()

        comment_text = comment.find("span", class_="_3l3x")

        if comment_text is not None:
            comments[commenter]["text"] = comment_text.text

        comment_link = comment.find(class_="_ns_")
        if comment_link is not None:
            comments[commenter]["link"] = comment_link.get("href")

        comment_pic = comment.find(class_="_2txe")
        if comment_pic is not None:
            comments[commenter]["image"] = comment_pic.find(class_="img").get("src")

        commentList = item.find('ul', {'class': '_7791'})
        if commentList:
            comments = dict()
            comment = commentList.find_all('li')
            if comment:
                for litag in comment:
                    aria = litag.find("div", {"class": "_4eek"})
                    if aria:
                        commenter = aria.find(class_="_6qw4").text
                        comments[commenter] = dict()
                        comment_text = litag.find("span", class_="_3l3x")
                        if comment_text:
                            comments[commenter]["text"] = comment_text.text
                            # print(str(litag)+"\n")

                        comment_link = litag.find(class_="_ns_")
                        if comment_link is not None:
                            comments[commenter]["link"] = comment_link.get("href")

                        comment_pic = litag.find(class_="_2txe")
                        if comment_pic is not None:
                            comments[commenter]["image"] = comment_pic.find(class_="img").get("src")

                        repliesList = litag.find(class_="_2h2j")
                        if repliesList:
                            reply = repliesList.find_all('li')
                            if reply:
                                comments[commenter]['reply'] = dict()
                                for litag2 in reply:
                                    aria2 = litag2.find("div", {"class": "_4efk"})
                                    if aria2:
                                        replier = aria2.find(class_="_6qw4").text
                                        if replier:
                                            comments[commenter]['reply'][replier] = dict()

                                            reply_text = litag2.find("span", class_="_3l3x")
                                            if reply_text:
                                                comments[commenter]['reply'][replier][
                                                    "reply_text"] = reply_text.text

                                            r_link = litag2.find(class_="_ns_")
                                            if r_link is not None:
                                                comments[commenter]['reply']["link"] = r_link.get("href")

                                            r_pic = litag2.find(class_="_2txe")
                                            if r_pic is not None:
                                                comments[commenter]['reply']["image"] = r_pic.find(
                                                    class_="img").get("src")
    return comments


def extract_reaction(html):
    reactions = ["Me gusta", "Me encanta", "Me enfada", "Me importa", "Me asombra", "Me divierte", "Me entristece"]
    reactions_dict = {}
    for reaction in reactions:
        reaction_pattern = r"aria-label(.*?){}(.*?)\d+".format(reaction)
        reaction_match = re.search(reaction_pattern, html)
        if reaction_match:
            number_match = reaction_match.group().split()[-1].strip()
            if "mil" in number_match:
                number_match = float(number_match.split("&")[0]) * 1000
            reactions_dict[reaction] = int(number_match)
        else:
            reactions_dict[reaction] = None
    # logger.console(reactions_dict)
    return reactions_dict


def convert_json_to_csv(page):
    post_path = path["post"].format(page)
    react_path = path["reactions"].format(page)
    df_posts = pd.read_json(post_path)
    # Avoid converting postid numbers as epoch date and transpose data
    df_react = pd.read_json(react_path, convert_axes=False).transpose()
    df_react = df_react.reset_index().rename(columns={'index': 'post_id'})
    df_posts.to_csv("data/csv/{}_fb_posts.csv".format(page), index=None)
    df_react.to_csv("data/csv/{}_fb_reactions.csv".format(page), index=None)
