"""Attempting to improve the signal->noise ratio for pyweet."""


import time


class AntiSpam(object):
    """Stores tweets with timestamps to prevent some spam."""

    tweet_store = {}
    timeout = 600

    @staticmethod
    def is_spam(tweet_text):
        """Ensures the tweet text is unique to the last 10 minutes.

        Returns:
            True if the tweet has been seen recently
        """

        now = int(time.time())
        AntiSpam.clear(now)
        if tweet_text in AntiSpam.tweet_store:
            return True
        else:
            AntiSpam.tweet_store[tweet_text] = now

    @staticmethod
    def clear(now=None):
        """Remove old entries."""

        if now is None:
            now = int(time.time())

        pops = []
        for text, timestamp in AntiSpam.tweet_store.items():
            if now - timestamp > AntiSpam.timeout:
                pops.append(text)

        for popper in pops:
            AntiSpam.tweet_store.pop(popper)
