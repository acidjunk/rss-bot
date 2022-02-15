from typing import List

from pydantic.env_settings import BaseSettings
from pydantic.networks import AnyHttpUrl


class Settings(BaseSettings):
    RETWEET_MAX: int = 5
    RSS_LIST: List[AnyHttpUrl] = ["https://jazzlimburg.nl/content_category/muzikant/feed/",
                                  "https://jazzlimburg.nl/content_category/award/feed/"]


settings = Settings()