"""Yet another command line twitter util.

Usage:

    pyweet [search phrase] [options]

Options:
    -u <screen name>: search tweets from a certain user
    -<integer>: maximum number of tweets (default is -3, overriden by -s)
    -s: stream tweets, runs until you kill it with ^c
    -t: display the timestamp of the tweet
    -d: display the date of the tweet
    -n: disable the antispam features

Note that stream does not work for your user page due to a bug in the upstream
module and/or API changes...
"""


import os
import sys
import json
import time
import twitter
import traceback
from functools import wraps
from datetime import datetime
from xml.sax.saxutils import unescape


class Settings(object):
    """Basic settings object for pyweet."""

    API = "rgIYSFIeGBxVXOPy22QzA"
    API_SECRET = "IK7buBUcWz1zKyTK6KF08WpG4Ic8w83DuEAb1FIErio"
    AUTH_FILE = os.path.expanduser("~/.pyweet")


class AntiSpam(object):
    """Stores tweets with timestamps to prevent some spam."""

    tweet_store = {}

    @staticmethod
    def is_spam(tweet_text):
        """Ensures the tweet text is unique to the last 10 minutes.

        Returns:
            True if the tweet has been seen recently
        """

        now = int(time.time())
        AntiSpam._clear_store(now)
        if tweet_text in AntiSpam.tweet_store:
            return True
        else:
            AntiSpam.tweet_store[tweet_text] = now

    @staticmethod
    def _clear_store(now):
        """Remove old entries."""

        pops = []
        for text, timestamp in AntiSpam.tweet_store.items():
            if now - timestamp > 600:
                pops.append(text)

        for popper in pops:
            AntiSpam.tweet_store.pop(popper)


def get_twit(func):
    """Performs oauth and provides the twitter object as kwarg 'twit'."""

    @wraps(func)
    def _get_twit(*args, **kwargs):
        """Instantiates a Twitter object based on streaming or RESTful."""

        settings = kwargs.get("settings", {})

        def _lookup_uid(twit):
            """Updates settings, adding the `uid` key."""

            uid = twit.users.lookup(screen_name=settings["user"])[0]["id"]
            settings.update({"uid": uid})

        if not "twit" in kwargs or kwargs["twit"] is None:
            oauth = _get_oauth()
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
            kwargs.update({"twit": twit, "settings": settings})

        return func(*args, **kwargs)

    return _get_twit


def _get_oauth():
    """Authenticate/register."""

    if not os.path.exists(Settings.AUTH_FILE):
        twitter.oauth_dance(
            "pyweet",
            Settings.API,
            Settings.API_SECRET,
            Settings.AUTH_FILE,
        )

    token, secret = twitter.read_token_file(Settings.AUTH_FILE)
    return twitter.OAuth(token, secret, Settings.API, Settings.API_SECRET)


def _print_tweet(tweet, settings):
    """Format and print the tweet dict.

    Returns:
        boolean status of if the tweet was printed
    """

    tweet_text = tweet.get("text")
    if tweet_text is None or (not settings["spam"] and
       AntiSpam.is_spam(tweet_text)):
        return False

    for encoding in ["utf-8", "latin-1"]:
        try:
            tweet_text.decode(encoding)
        except UnicodeEncodeError:
            pass
        else:
            break
    else:
        return False

    if settings.get("json"):
        print(json.dumps(tweet, indent=4, sort_keys=True))
    else:
        prepend = []
        if settings.get("date") or settings.get("time"):
            date = _parse_date(tweet["created_at"])
            if settings.get("date"):
                prepend.append("{0:%b} {1}".format(
                    date,
                    int(datetime.strftime(date, "%d")),
                ))
            if settings.get("time"):
                prepend.append("{0:%H}:{0:%M}:{0:%S}".format(date))

        print("{}{}@{}: {}".format(
            " ".join(prepend),
            " " * int(prepend != []),
            tweet.get("user", {}).get("screen_name", ""),
            unescape(tweet_text),
        ))

    return True


def _parse_date(date_str):
    """Parse out a datetime object from string using Twitter's formatting."""

    major = sys.version_info.major
    minor = sys.version_info.minor
    if major > 3 or (major == 3 and minor >= 2):  # python4 support :p
        date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
    else:
        # bug in datetime's %z on py < 3.2 http://bugs.python.org/issue6641
        time_ = date_str.split(" ")
        date_str = " ".join([x for x in time_ if not x.startswith(("+", "-"))])
        date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")

    return date


def _streamed_search(twit=None, settings=None):
    """Stream a search query to the console."""

    kwargs = {}
    if settings.get("search"):
        kwargs.update({"track": ",".join(settings["search"])})
    if settings.get("user"):
        kwargs.update({"follow": settings["uid"]})

    for tweet in twit.statuses.filter(**kwargs):
        if tweet:
            _print_tweet(tweet, settings)


@get_twit
def print_tweets(twit=None, settings=None):
    """Find some tweets and print them to console."""

    if settings["stream"] and (settings["search"] or settings["user"]):
        return _streamed_search(twit, settings)
    elif settings.get("uid"):
        tweets = twit.statuses.user_timeline(user_id=settings["uid"])
    elif settings["search"]:
        tweets = twit.search.tweets(q=",".join(settings["search"]))["statuses"]
    else:
        tweets = twit.statuses.home_timeline()

    max_tweets = settings["max"]
    for i, tweet in enumerate(tweets):
        if not _print_tweet(tweet, settings):
            max_tweets += 1
        if (i + 1) >= max_tweets:
            break


def parse_args():
    """Parses the command line for user run-time settings.

    Returns:
        dictionary with the following keys::

            user: string user name to search for tweets from
            search: string to search for tweets with
            max_tweets: integer max number of tweets to display
            stream: boolean to stream the tweets instead of printing once
            date: boolean to display the date ahead of the tweet
            time: boolean to display the time ahead of the tweet
            json: boolean to display the tweet's json structure instead
            spam: boolean to skip the anti spam measures
    """

    settings = {
        "max": 3,
        "search": [],
        "stream": False,
        "user": None,
        "date": False,
        "time": False,
        "json": False,
        "spam": False,
    }
    max_set = False
    get_next = False
    for arg in sys.argv[1:]:
        if get_next:
            settings[get_next] = arg
            get_next = False
            continue

        arg_copy = arg
        while arg.startswith("-"):
            arg = "".join(arg[1:])

        if arg == "s":
            settings["stream"] = True
        elif arg == "u":
            get_next = "user"
        elif arg == "d":
            settings["date"] = True
        elif arg == "t":
            settings["time"] = True
        elif arg == "j":
            settings["json"] = True
        elif arg == "n":
            settings["spam"] = True
        elif arg == "h":
            raise SystemExit(__doc__.strip())
        elif not max_set:
            try:
                settings["max"] = int(arg)
                max_set = True
            except (TypeError, ValueError):
                settings["search"].append(arg_copy)
        else:
            settings["search"].append(arg_copy)

    return settings


def main():
    """Main loop. Except KeyboardInterrupts and a global except all."""

    try:
        print_tweets(settings=parse_args())
    except KeyboardInterrupt:
        pass
    except Exception as error:
        try:
            reply = raw_input("Errored. Would you like to see the traceback? ")
        except KeyboardInterrupt:
            raise SystemExit(1)
        else:
            if reply.lower().startswith("y"):
                raise SystemExit(traceback.format_exc().strip())
    raise SystemExit


if __name__ == "__main__":
    main()
