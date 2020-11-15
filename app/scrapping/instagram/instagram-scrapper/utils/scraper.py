from urllib.request import urlopen
import json 
import os

class Scraper:

    '''
        This object scrap the last 12 instagram posts and comments from all the profiles that appears in the companies.txt file.
    '''

    def __init__(self):
        self.read_companies()
        self.scrap_all()


    '''
        Those functions get the URL needed for extract the data. There is one link for profiles and other for posts.
    '''
    def get_profile(self, username):
        return f"https://www.instagram.com/{username}/?__a=1&is_video=true"
    
    def get_post(self, shortcode):
        return f"https://www.instagram.com/p/{shortcode}/?__a=1"
    

    '''
        Those functions reads the JSON files from the links needed, and returns the object that contains all the information needed.
    '''
    def profile(self, username):
        url = self.get_profile(username)
        response = urlopen(url)

        text = response.read().decode('utf-8')
        json_obj = json.loads(text)

        return json_obj["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]
    
    def post_comments(self, postID):
        url = self.get_post(postID)
        response = urlopen(url)

        string = response.read().decode('utf-8')
        json_obj = json.loads(string)

        return json_obj["graphql"]["shortcode_media"]["edge_media_to_parent_comment"]["edges"]


    '''
        This function makes a list of the profiles names that appears in the comapies.txt file.
    '''

    def read_companies(self):
        f = open('companies.txt', 'r')
        self.companies = [c.rstrip() for c in f]
        f.close()


    '''
        This function get all the information neede from the JSON files extracted from the web, and clean them in order to get only the information needed.
        Generates JSON files for post and comments in the data folder. Those will be used later in the classifier.
    '''

    def scrap_all(self):
        for user in self.companies:
            posts = self.profile(user)
            data_post = []
            for p in posts:
                data_post.append(self.clean_post(p['node'], user))
                comments = []
                for com in self.post_comments(p['node']['shortcode']):
                    comments.extend(self.clean_comment(com['node'], user, p['node']['id']))
                if comments != []:
                    with open(os.path.join('data', 'comments', f"{p['node']['shortcode']}-{user}.json"), 'w', encoding="utf-8") as json_file:
                        json.dump(comments, json_file, ensure_ascii=False)
            
            with open(os.path.join('data', 'posts', f'{user}-last.json'), 'w', encoding="utf-8") as json_file:
                json.dump(data_post, json_file, ensure_ascii=False)


    '''
        Those funtions takes JSON file with certain format and returns a JSON object only with the information needed for the database.
    '''

    def clean_post(self, post, username):
        clean_data = {
            "post_id": post['id'],
            "text": post['edge_media_to_caption']['edges'],
            "time": post['taken_at_timestamp'],
            "type": post['__typename'],
            "is_ad": False,
            "is_video": post['is_video'],
            "post_url": "https://www.instagram.com/p/" + post['shortcode'] + "/",
            "total_reactions": post['edge_media_preview_like']['count'],
            "total_comments": post['edge_media_to_comment']['count'],
            "brand_username": username
        }

        if len(clean_data['text']) == 0:
            clean_data['text'] = ''
        else:
            clean_data['text'] = clean_data['text'][0]['node']['text']
        
        return clean_data

    def clean_comment(self, comm, username, post_id):
        clean_data = {
            "rootpost_id":post_id,
            "parentpost_id":comm['id'],
            "responsepost_id":comm['id'],
            "brand_username":username,
            "text":comm['text'],
            "time":comm['created_at'],
            "likes":comm['edge_liked_by']['count'],
            "username":comm['owner']['username']
        }

        all_ans = [clean_data]

        for ans in comm['edge_threaded_comments']['edges']:
            clean_ans = {
                "rootpost_id":post_id,
                "parentpost_id":comm['id'],
                "responsepost_id":ans['node']['id'],
                "brand_username":username,
                "text":ans['node']['text'],
                "time":ans['node']['created_at'],
                "likes":ans['node']['edge_liked_by']['count'],
                "username":ans['node']['owner']['username']
            }
            all_ans.append(clean_ans)
        
        return all_ans