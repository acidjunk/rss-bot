from pydantic.networks import AnyHttpUrl
import feedparser
from .config import Settings


def parse_feed(url: AnyHttpUrl):
    feed = feedparser.parse(url)
    # todo: implement some error handling + filtering?
    return feed

