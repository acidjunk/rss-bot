from typing import List

from pydantic.env_settings import BaseSettings
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    MAX_RETWEET: int = 5
    MAX_DAILY_TWEETS: int = 5
    MAX_ARTICLE_AGE: int = 10
    RSS_LIST: list[AnyHttpUrl] = [
        "https://jazzlimburg.nl/content_category/muzikant/feed/",
        "https://jazzlimburg.nl/content_category/award/feed/",
    ]
    PREFERRED_TIME_SLOTS: list[int] = [8, 9, 10, 12, 13, 14, 17, 18, 20, 22]


settings = Settings()
