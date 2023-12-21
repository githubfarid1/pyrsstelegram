import feedparser
from datetime import datetime
from dateutil import parser as dparser
import humanize
import time
import requests
from dotenv import load_dotenv
import os
from playsound import playsound

load_dotenv()
old_entries = []
ORGID=os.getenv("ORGID")
SECURITY_TOKEN=os.getenv("SECURITY_TOKEN")
TOPIC=os.getenv("TOPIC")
USER_ID=os.getenv("USER_ID")
POST_AGE=os.getenv("POST_AGE")
while True:
    #web scraper
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
                print(message)
                playsound('sound1.wav')
    time.sleep(60)
