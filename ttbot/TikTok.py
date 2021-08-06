import os
import json
import requests
import sys

class TikTok:
    def __init__(self, cookies=None):
        # Initialize cookies
        if cookies == None:
            try:
                with open("cookies.json", 'r') as f:
                    self.cookies = json.loads(f.read())
            except Exception:
                sys.exit("Error: Cookies not defined. Either add cookies to cookies.json file in current directory or pass cookies dictionary to TikTok instance")
        else:
            self.cookies = cookies


    def get_comment_mentions(self):
        """ Get user mentions, when somebody @ the user in a comment """
        # Query tiktok api
        response = requests.get("https://www.tiktok.com/api/notice/multi/",
            params={"group_list": '[{"group":6,"hasMore":1,"min_time":0,"max_time":0,"is_mark_read":1,"count":20}]'},
            cookies=self.cookies)

        # Handle abnormal responses
        if response.json()["status_code"] == 8:
            # Login expired
            print("Login expired")
            return []
        if len(response.json()["notice_lists"]) == 0:
            # No mentions
            return []

        # Format list to only include necessary data
        mention_list = response.json()["notice_lists"][0]["notice_list"]
        formatted_mentions = []
        for item in mention_list:
            if item["type"] == 45:
                # type==45 is double checking that the notification is a mention
                # I think that follows show up in this request group and are listed as type 33
                if item["at"]["title"] != "":
                    # If title is not blank, the mention is not a comment, it is a post
                    continue
                formatted_mentions.append({
                    "aweme_id": item["at"]["aweme"]["aweme_id"],
                    "comment_id": item["at"]["schema_url"].split('=')[1],
                    "content": item["at"]["content"],
                    "has_read": item["has_read"]
                })

        return formatted_mentions

    def get_likes(self):
        """ Get likes, might only be returning video likes """
        response = requests.get("https://www.tiktok.com/api/notice/multi/",
            params={"group_list": '[{"group":3,"hasMore":1,"min_time":0,"max_time":0,"is_mark_read":1,"count":30}]'},
            cookies=self.cookies)

        # Handle abnormal responses
        if response.json()["status_code"] == 8:
            # Login expired
            print("Login expired")
            return []
        if len(response.json()["notice_lists"]) == 0:
            # No mentions
            return []

        likes_list = response.json()["notice_lists"][0]["notice_list"]
        formatted_likes = []
        for item in likes_list:
            formatted_likes.append({
                "aweme_id": item["digg"]["aweme"]["aweme_id"],
                "user_id": item["digg"]["from_user"][0]["uid"],
                "username": item["digg"]["from_user"][0]["nickname"],
                "has_read": item["has_read"],
                "create_time": item["create_time"]
            })
        return fromatted_likes

    def get_follows(self):
        """ Get new follower notifications """
        response = requests.get("https://www.tiktok.com/api/notice/multi/",
            params={"group_list": '[{"group":7,"hasMore":1,"min_time":0,"max_time":0,"is_mark_read":1,"count":30}]'},
            cookies=self.cookies)

        # Handle abnormal responses
        if response.json()["status_code"] == 8:
            # Login expired
            print("Login expired")
            return []
        if len(response.json()["notice_lists"]) == 0:
            # No mentions
            return []

        follows_list = response.json()["notice_lists"][0]["notice_list"]
        formatted_follows = []
        for item in follows_list:
            formatted_follows.append({
                "user_id": item["user_id"],
                "username": item["follow"]["from_user"]["unique_id"],
                #"user_id": item["follow"]["from_user"]["uid"], #not sure if this is the correct user id or not
                "has_read": item["has_read"],
                "create_time": item["create_time"]
            })
        return formatted_follows

    def post_comment(self, aweme_id, text):
        """ Post a comment to video with id aweme_id and content of text """
        params = {"aid": "1988", "text": str(text), "aweme_id": str(aweme_id)}
        headers = {'Referer': f'https://www.tiktok.com/video/{str(aweme_id)}?lang=en&is_copy_url=1&is_from_webapp=v1'}
        response = requests.post("https://www.tiktok.com/api/comment/publish/",
            headers=headers,
            params=params,
            cookies=self.cookies)
        if response.json()["status_msg"] == "Comment sent successfully":
            # return created comment id if comment added successfully
            return response.json()["comment"]["cid"]

    def reply_to_comment(self, reply_to_cid, aweme_id, text):
        """ NONFUNCTIONAL; Post a comment to video with id aweme_id and content of text """
        params = {"aid": "1988", "text": str(text), "aweme_id": str(aweme_id), "reply_to_reply_id": str(reply_to_cid)}
        headers = {'Referer': f'https://www.tiktok.com/video/{str(aweme_id)}?lang=en&is_copy_url=1&is_from_webapp=v1'}
        response = requests.post("https://www.tiktok.com/api/comment/publish/",
            headers=headers,
            params=params,
            cookies=self.cookies)
        print(response.json())
        if response.json()["status_msg"] == "Comment sent successfully":
            # return created comment id if comment added successfully
            return response.json()["comment"]["cid"]
