import os
import textwrap
import time

import structlog

from rss_bot.config import settings
from rss_bot.feed_parser import download_feed, feed_has_changed, get_full_path, parse_feed
from rss_bot.stripper import strip_tags

logger = structlog.get_logger()


for url in settings.RSS_LIST:
    # download_feed(url)
    # Todo: enable before going live
    # if not feed_has_changed(url):
    if 0:
        logger.info("Feed data hasn't changed since last run", url=url)
    else:
        file_name = get_full_path(url)
        feed = parse_feed(file_name)

        # I AM TESTING IT WITH 4 ITEMS MAX AND WHEN THAT WORKS OK MANUALLY: CRONTAB!
        # Sorted old -> new
        # for post in feed.entries:

        # With title and stripped summary
        # post = feed.entries[1]
        # prefix = "Limburgse jazz muzikant: " if "muzikant" in url else "Info over de Award: "
        # summary = textwrap.shorten(strip_tags(post.summary), width=120, placeholder=" ...")
        # tweet = f"{prefix}{post.title}\n{summary}\n\nMeer info: {post.link}\n"
        # logger.info("Tweeting", tweet=tweet)
        # os.system(f'tweet send "{tweet}"')
        # sys.exit()

        # Without title and stripped the last dot if possible
        post = feed.entries[0]
        prefix = "Limburgse jazz muzikant: " if "muzikant" in url else "Info over de Award: "
        summary = textwrap.shorten(strip_tags(post.summary), width=132).rsplit(". ", 1)[0] + "."
        tweet = f"{prefix}\n{summary}\n\nMeer info: {post.link}\n"
        logger.info("Tweeting", tweet=tweet)
        os.system(f'tweet send "{tweet}"')
        logger.info("Sleeping", seconds=600)
        time.sleep(600)
