# ttbot
Unofficial api for TikTok bots

## Install
```
pip install ttbot
```
## Config
To use the bot, the bot needs access to tiktok cookies. To pass cookies to the bot, paste cookies in a file called `cookies.json` in the same folder as your main python file. If this is not possible, set a cookies variable to the cookies json and pass it to each bot function.

### Getting cookies
To get the cookies json, go to TikTok on your computer, open dev tools, select network tab, and then click on the notifications button in TikTok. Then, click on the network request that starts with "/api/notice/multi". Go to the cookies tab of this request, right click on the text, and then click on copy all. Save this as a variable and pass into ttbot instance as a parameter.

## Example
Running this code will print a list of comments that you were mentioned in.
```
import ttbot

mentions = ttbot.get_comment_mentions()

for item in mentions:
    print("-----")
    print("Video id: " + item["aweme_id"])
    print("Comment id: " + item["comment_id"])
    print("Comment content: " + item["content"])
    print("Has read: " + str(item["has_read"]))
```
Note that you have to run `ttbot.get_comment_mentions()` every time you want to check for updates to mentions, so you might want to add a loop with `time.sleep(30)` or `time.sleep(60)`.
