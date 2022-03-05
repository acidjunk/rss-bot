import json
import os
import sys
from random import randint

import structlog
import typer

from rss_bot.config import settings
from rss_bot.feed_parser import download_feed, feed_has_changed, get_full_path, parse_feed, generate_tweet
from rss_bot.tweeter import send_tweet

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
    if not feed_has_changed(url) and not force:
        logger.info("Feed data hasn't changed since last run", url=url)
    else:
        file_name = get_full_path(url)
        rss = parse_feed(file_name).entries

        try:
            tweet = generate_tweet(rss[0], feed)
            logger.info("Generated tweet", tweet=tweet)
        except:
            logger.error("Error with twitter message", rss_item=rss[0], feed=feed)
            sys.exit()
        if interactive:
            answer = input("Tweet? y/n")
            if not answer == "y":
                sys.exit()
        send_tweet(tweet)

        logger.info("Sleeping", seconds=600)


@app.command()
def show_feed_info():
    typer.echo(f"Loaded config for {len(feed_info)} feeds:")
    """Show info about the configured feeds."""
    for index, feed in enumerate(feed_info):
        typer.echo(f"Index: {index} =>")
        typer.echo(feed)


@app.command()
def bot(interactive: bool = False):
    """Tweet without human interaction."""
    index = 0
    if os.path.exists("data/counter.txt"):
        with open("data/counter.txt") as f:
            index = int(f.read())
        if index >= len(feed_info) - 1:
            index = 0
        else:
            index += 1
        with open("data/counter.txt", "w") as f:
            f.write("%d" % index)
    else:
        with open("data/counter.txt", "w") as f:
            f.write("%d" % index)

    logger.info("Determined and stored new index", index=index)

    feed = feed_info[index]
    url = feed["url"]
    download_feed(url)
    if not feed_has_changed(url):
        logger.info("Feed data hasn't changed since last run", url=url)
    else:
        file_name = get_full_path(url)
        rss = parse_feed(file_name).entries

        # second safety net: URI only once (some feeds change on disk, because they have dynamic id's)
        url_list = []
        if os.path.exists("data/tweets.txt"):
            with open("data/tweets.txt") as f:
                url_list = f.read().split("\n")
                # print(url_list)
            if rss[0].link in url_list:
                logger.warning("RSS problems. Skipping tweet based on non unique link", link=rss[0].link)
                sys.exit()
            with open("data/tweets.txt", mode="wt", encoding="utf-8") as f:
                url_list.append(rss[0].link)
                f.write('\n'.join(url_list))
        else:
            with open("data/tweets.txt", mode="wt", encoding="utf-8") as f:
                f.write(rss[0].link)

        try:
            tweet = generate_tweet(rss[0], feed)
            logger.info("Generated tweet", tweet=tweet)
        except:
            logger.error("Error with twitter message", rss_item=rss[0], feed=feed)
            sys.exit()

        if interactive:
            answer = input("Tweet? y/n")
            if not answer == "y":
                sys.exit()
            send_tweet(tweet)
        else:
            logger.info("Sleeping", seconds=randint(0, settings.MAX_SLEEP - 10))
            send_tweet(tweet)


if __name__ == "__main__":
    app()


#
#
