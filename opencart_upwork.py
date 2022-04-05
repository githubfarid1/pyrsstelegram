import feedparser
from datetime import datetime
from dateutil import parser as dparser

import humanize
import time
import requests

post_age = 600 #10 minutes
old_entries = []
TOKEN = "1826066081:AAFQM3UG973Ufa1J22PKNs0cmIzSgBTuADU"
CHAT_ID = "@laravelopencartfrd"
MESSAGE = "RSS reader every 60 seconds"
#initialize message
telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={MESSAGE}"
requests.get(telegram_url)

while True:
    #opencart
    rssurl = "https://www.upwork.com/ab/feed/topics/rss?securityToken=aba9cbbfce7d30a4fcd4816297a2514c0e693b730686ebbb39e1b18645bdefb8b0884f90f4e37bd1b2d974aa4a0ba5e9b1f6f207a32fad1bcecb47651256f674&userUid=753956258459901952&orgUid=753956258464096257&topic=2339733"
    NewsFeed = feedparser.parse(rssurl)
    now = datetime.utcnow().replace(second=0, microsecond=0)
    for feed in NewsFeed.entries:
        published = feed.published
        dt = dparser.parse(published)
        dt = dt.replace(tzinfo=None,second=0, microsecond=0)
        diff = now-dt
        second = int(diff.total_seconds())
        if second <= post_age:
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
