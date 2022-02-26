import json
import os
import sys
import textwrap
import time

import structlog
import typer

from rss_bot.config import settings
from rss_bot.feed_parser import download_feed, feed_has_changed, get_full_path, parse_feed
from rss_bot.stripper import strip_tags

logger = structlog.get_logger()

app = typer.Typer()

# Init info about feeds
feed_info = False
with open("config.json") as file:
    feed_info = json.loads(file.read())
if not feed_info:
    logger.info("Failed to read json. You'll need a config.json in this folder!")
    sys.exit()


@app.command()
def handle_one_feed(index: int, interactive: bool = True, force: bool = False):
    feed = feed_info[index]
    typer.echo(f"Starting bot for one feed: {feed['name']}")

    # Todo: refactor double code (but keep typer.echo vs structlog intact
    url = feed["url"]

    download_feed(url)
    if not feed_has_changed(url) or not force:
        logger.info("Feed data hasn't changed since last run", url=url)
    else:
        file_name = get_full_path(url)
        rss = parse_feed(file_name)

        post = rss.entries[0]
        prefix = "Limburgse jazz muzikant: " if "muzikant" in url else "Info over de Award: "
        summary = textwrap.shorten(strip_tags(post.summary), width=132).rsplit(". ", 1)[0] + "."
        tweet = f"{prefix}\n{summary}\n\nMeer info: {post.link}\n"
        logger.info("Tweeting", tweet=tweet)
        if interactive:
            answer = input("Tweet? y/n")
            if not answer == "y":
                sys.exit()
        os.system(f'tweet send "{tweet}"')
        logger.info("Sleeping", seconds=600)


@app.command()
def show_feed_info():
    typer.echo(f"Loaded config for {len(feed_info)} feeds:")
    """Show info about the configured feeds."""
    for index, feed in enumerate(feed_info):
        typer.echo(f"Index: {index} =>")
        typer.echo(feed)


@app.command()
def bot():
    """Tweet without human interaction."""
    for feed in feed_info:
        url = feed["url"]
        download_feed(url)
        # Todo: enable before going live
        if not feed_has_changed(url):
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
            # os.system(f'tweet send "{tweet}"')
            logger.info("Sleeping", seconds=600)
            time.sleep(600)


if __name__ == "__main__":
    app()


#
#

