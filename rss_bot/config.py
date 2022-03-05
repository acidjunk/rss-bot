from typing import Optional

from pydantic.env_settings import BaseSettings


class Settings(BaseSettings):
    MAX_RETWEET: int = 5
    MAX_DAILY_TWEETS: int = 5
    MAX_ARTICLE_AGE: int = 10
    PREFERRED_TIME_SLOTS: list[int] = [8, 9, 10, 12, 13, 14, 17, 18, 20, 22]
    TWITTER_CREDS: Optional[str] = None
    MAX_SLEEP: int = 600


settings = Settings()
