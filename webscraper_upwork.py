import feedparser
from datetime import datetime
from dateutil import parser as dparser

import humanize
import time
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# post_age = 600 #10 minutes
old_entries = []
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MESSAGE = "RSS reader every 60 seconds"
ORGID=os.getenv("ORGID")
SECURITY_TOKEN=os.getenv("SECURITY_TOKEN")
TOPIC=os.getenv("TOPIC")
USER_ID=os.getenv("USER_ID")
POST_AGE=os.getenv("POST_AGE")

telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}"
requests.get(telegram_url)
while True:
    rssurl = f"https://www.upwork.com/ab/feed/topics/rss?securityToken={SECURITY_TOKEN}&userUid={USER_ID}&orgUid={ORGID}&topic={TOPIC}"
    NewsFeed = feedparser.parse(rssurl)
    now = datetime.utcnow().replace(second=0, microsecond=0)
    for feed in NewsFeed.entries:
        published = feed.published
        dt = dparser.parse(published)
        dt = dt.replace(tzinfo=None,second=0, microsecond=0)
        diff = now-dt
        second = int(diff.total_seconds())
        if second <= int(POST_AGE):
            if feed.id not in old_entries:
                title = feed.title
                link = feed.link
                diff_human = humanize.naturaltime(diff)
                message = f"{title}\n {link}\n{diff_human}"
                old_entries.append(feed.id)
                telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
                r = requests.get(telegram_url)
                print(r)
                old_entries.append(feed.id)
    time.sleep(60)
