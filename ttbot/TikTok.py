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

    def get_recommended(self):
        """ Get current users recommended list """
        response = requests.get("https://m.tiktok.com/api/recommend/item_list/",
            params={"aid": 1988, "count": 30},
            #params={"aid": 1988, "count": 30, "from_page": "fyp"},
            cookies=self.cookies)
        return response.json()["itemList"]

    """ Functions below this are nonfunctional """

    def get_direct_link(self, aweme_id):
        response = requests.get("")
        pass

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

    """ Functions below this are blocked; response.content is b'blocked' """

    def follow_user(self, user_id):
        print(user_id)
        params = {"aid": "1988", "user_id": int(user_id), "type": 1, "from": 19, "channel_id": 3, "from_pre": 0, "fromWeb": 1, "history_len": 8}
        response = requests.post("https://m.tiktok.com/api/commit/follow/user/",
            params=params,
            cookies=self.cookies)
        print(response.content)
        #print(response.json())
        return response.json()

    def unfollow_user(self, user_id):
        print(user_id)
        params = {"aid": "1988", "user_id": int(user_id), "type": 0, "from": 19, "channel_id": 3, "from_pre": 0, "fromWeb": 1, "history_len": 8}
        response = requests.post("https://m.tiktok.com/api/commit/follow/user/",
            params=params,
            cookies=self.cookies)
        print(response)
        #print(response.json())
        return response.json()

    def like_video(self, aweme_id):
        params = {
			"aid": "1988",
			"app_name": "tiktok_web",
			"device_platform": "web_pc",
			"device_id": "6917070983203554822",
			"region": "US",
			"priority_region": "US",
			"os": "linux",
			"referer": "",
			"root_referer": "",
			"cookie_enabled": "true",
			"screen_width": "1920",
			"screen_height": "1080",
			"browser_language": "en-US",
			"browser_platform": "Linux x86_64",
			"browser_name": "Mozilla",
			"browser_version": "5.0 (X11)",
			"browser_online": "true",
			"verifyFp": "verify_ks0nmaje_sA7k2Sag_Jf1C_4cqm_8Gif_PT68xdKccR2P",
			"app_language": "en",
			"timezone_name": "America/New_York",
			"is_page_visible": "true",
			"focus_state": "true",
			"is_fullscreen": "false",
			"history_len": "10",
			"aweme_id": "6992652869715430662",
			"type": "1",
			"channel_id": "3",
			"msToken": "FD4GMcmbKhcMZih0xNojNI7oriEwoziTRtd9UKkqFS4MUKuV2xPtA2hXmWDvSqzMkFjAAs9_-Znk7luZBjZehl0zRedu-FQUFa3bed_f4q8630Ek3tb1cMuzXXFfMjkcEnKi",
			"X-Bogus": "DFSzsIVuPCE4iL7KSPoVL47r4IX2",
			"_signature": "_02B4Z6wo00001xUIiNgAAIDBwbdPvyrqcksVCYxAAKRZ1c"
		}
        response = requests.post("https://m.tiktok.com/api/commit/item/digg/",
            params=params,#{"aid": 1988, "aweme_id": aweme_id},
            cookies=self.cookies)
        print(response.content)
        print(response.json())
        return response.json()

    def get_video_comments(self, aweme_id):
        response = requests.get("https://www.tiktok.com/api/comment/list/",
            params={"aid": 1988, "aweme_id": aweme_id, "count": 20, "cursor": 0, "current_region": "US"},
            #params={"aid": 1988, "count": 30, "from_page": "fyp"},
            cookies=self.cookies)
        print(response.content)
        print(response.json())
        return response.json()
