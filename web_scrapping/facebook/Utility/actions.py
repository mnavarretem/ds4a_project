import json
import re

from bs4 import BeautifulSoup
from robot.api import logger


def get_posts_url(page):
    file_path = "data/{}_fb_posts.json".format(page)
    with open(file_path, 'r') as json_file:
        posts = json.load(json_file)
        urls = [(post["post_id"], post["post_url"]) for post in posts]
        #logger.console(urls)
        #print(urls)
    return urls

def write_reactions_json(page, reactions_dict):
    file_path = "data/{}_fb_reactions.json".format(page)
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
            reactions_dict[reaction] = number_match
        else:
            reactions_dict[reaction] = None
    # logger.console(reactions_dict)
    return reactions_dict

