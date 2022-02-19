from rss_bot.config import settings
from rss_bot.feed_parser import download_feed, feed_has_changed, get_full_path, parse_feed
import structlog

logger = structlog.get_logger()


for url in settings.RSS_LIST:
    # download_feed(url)
    # if not feed_has_changed(url):
    #     logger.info("Feed data hasn't changed since last run", url=url)
    file_name = get_full_path(url)
    feed = parse_feed(file_name)
    first = feed["entries"][0]
    print(f"Title: {first['title']}")
    print(f"Summary: {first['summary']}")
    print(f"Summary: {first['summary']}")
    print
