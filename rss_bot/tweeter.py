import os

import structlog as structlog

from rss_bot.config import settings

logger = structlog.get_logger()


def send_tweet(tweet):
    if settings.TWITTER_CREDS:
        logger.info("Twittering with non default account", account=settings.TWITTER_CREDS)
        os.system(f'{settings.TWITTER_BIN} -c {settings.TWITTER_CREDS} send "{tweet}"')
    else:
        logger.info("Twittering with default account")
        os.system(f'{settings.TWITTER_BIN} send "{tweet}"')
