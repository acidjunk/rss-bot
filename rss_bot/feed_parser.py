import filecmp
import os
import textwrap

import feedparser
import requests
from pydantic.networks import AnyHttpUrl
from slugify import slugify

from rss_bot.stripper import strip_tags


def get_full_path(url: AnyHttpUrl, new: bool = False):
    file_name = slugify(url)
    if new:
        return os.path.join("data", f"new_{file_name}.xml")
    return os.path.join("data", f"{file_name}.xml")


def download_feed(url: AnyHttpUrl):
    r = requests.get(url, allow_redirects=True)
    open(get_full_path(url, new=True), "wb").write(r.content)


def feed_has_changed(url: AnyHttpUrl):
    new_file_name = get_full_path(url, new=True)
    file_name = get_full_path(url)
    if not os.path.exists(file_name) and os.path.exists(new_file_name):
        os.rename(new_file_name, file_name)
        return True

    if not os.path.exists(file_name) and not os.path.exists(new_file_name):
        raise ValueError("Nothing to compare")

    if not filecmp.cmp(file_name, new_file_name, shallow=True):

        # os.replace(new_file_name, file_name)
        return True

    # Files are identical: so no changes needed
    os.remove(new_file_name)
    return False


def parse_feed(file_name):
    feed = feedparser.parse(file_name)
    # todo: implement some error handling + filtering?
    return feed


def generate_tweet(rss_item, feed):
    prefix = feed["prefix"]
    if feed.get("showTitle") is True:
        prefix = f"{prefix}: {rss_item.title}\n"

    summary = textwrap.shorten(strip_tags(rss_item.summary), width=132).rsplit(". ", 1)[0] + "."
    tweet = f"{prefix}\n{summary}\n\n{feed['moreInfo']}: {rss_item.link}\n"
    return tweet
