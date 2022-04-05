import feedparser
from datetime import datetime
from dateutil import parser as dparser

import humanize
import time
import requests

class RssTelegram():
    # old_entries = []
    TOKEN = "1826066081:AAFQM3UG973Ufa1J22PKNs0cmIzSgBTuADU"
    POST_AGE = 600 #10 minutes
    FIRST_MESSAGE = "RSS reader is ready to scrap..!!"

    def __init__(self, chat_id, rss_url):
        self.chat_id = chat_id
        self.rss_url = rss_url
        self.old_entries = []
        telegram_url = f"https://api.telegram.org/bot{RssTelegram.TOKEN}/sendMessage?chat_id={chat_id}&text={RssTelegram.FIRST_MESSAGE}"
        requests.get(telegram_url)

    def send_rss(self):
        # delete old entries to 50
        if len(self.old_entries) >= 100:
            while len(self.old_entries) >= 50:
                self.old_entries.pop()

        NewsFeed = feedparser.parse(self.rss_url)
        now = datetime.utcnow().replace(second=0, microsecond=0)
        for feed in NewsFeed.entries:
            published = feed.published
            dt = dparser.parse(published)
            dt = dt.replace(tzinfo=None,second=0, microsecond=0)
            diff = now-dt
            second = int(diff.total_seconds())
            if second <= RssTelegram.POST_AGE:
                if feed.id not in self.old_entries:
                    title = feed.title
                    link = feed.link
                    diff_human = humanize.naturaltime(diff)
                    message = f"{title}\n {link}\n{diff_human}"
                    telegram_url = f"https://api.telegram.org/bot{RssTelegram.TOKEN}/sendMessage?chat_id={self.chat_id}&text={message}"
                    r = requests.get(telegram_url)
                    print(r)
                    self.old_entries.append(feed.id)
        time.sleep(2)


webscraper = RssTelegram("@webscraper_upwork", "https://www.upwork.com/ab/feed/topics/rss?securityToken=aba9cbbfce7d30a4fcd4816297a2514c0e693b730686ebbb39e1b18645bdefb8b0884f90f4e37bd1b2d974aa4a0ba5e9b1f6f207a32fad1bcecb47651256f674&userUid=753956258459901952&orgUid=753956258464096257&topic=5648591")
opencart = RssTelegram("@laravelopencartfrd", "https://www.upwork.com/ab/feed/topics/rss?securityToken=aba9cbbfce7d30a4fcd4816297a2514c0e693b730686ebbb39e1b18645bdefb8b0884f90f4e37bd1b2d974aa4a0ba5e9b1f6f207a32fad1bcecb47651256f674&userUid=753956258459901952&orgUid=753956258464096257&topic=2339733")
# opencart = RssTelegram("@laravelopencartfrd", "https://www.upwork.com/ab/feed/topics/rss?securityToken=aba9cbbfce7d30a4fcd4816297a2514c0e693b730686ebbb39e1b18645bdefb8b0884f90f4e37bd1b2d974aa4a0ba5e9b1f6f207a32fad1bcecb47651256f674&userUid=753956258459901952&orgUid=753956258464096257&topic=5304553")


while True:
    webscraper.send_rss()
    opencart.send_rss()
    time.sleep(60)
    