from rss_bot.config import settings
from rss_bot.feed_parser import parse_feed

for url in settings.RSS_LIST:
    feed = parse_feed(url)
    print(feed)
