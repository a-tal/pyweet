"""Pyweet wrapper functions."""


import twitter
from functools import wraps

from pyweet.oauth import get_oauth


def get_twit(func):
    """Performs oauth and provides the twitter object as kwarg 'twit'."""

    @wraps(func)
    def _get_twit(*args, **kwargs):
        """Instantiates a Twitter object based on streaming or RESTful."""

        settings = kwargs.get("settings", {})
        _twit = None

        def _lookup_uid(twit):
            """Updates settings, adding the `uid` key."""

            uid = twit.users.lookup(screen_name=settings["user"])[0]["id"]
            settings.update({"uid": uid})

        if not "twit" in kwargs or kwargs["twit"] is None:
            oauth = get_oauth()
            if settings.get("stream") and (settings.get("search") or
               settings.get("user")):
                if settings.get("user"):
                    # the screen_name->uid lookup is only available RESTfully
                    twit_rest = twitter.Twitter(auth=oauth)
                    _lookup_uid(twit_rest)
                twit = twitter.TwitterStream(auth=oauth)
            else:
                twit = twitter.Twitter(auth=oauth)
                settings["stream"] = False
                if settings.get("user"):
                    _lookup_uid(twit)
            _twit = twit
        else:
            _twit = kwargs["twit"]

        kwargs.update({"twit": _twit, "settings": settings})
        return func(*args, **kwargs)

    return _get_twit
