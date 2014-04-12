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


import sys
import json
from datetime import datetime
from xml.sax.saxutils import unescape

from pyweet.wraps import get_twit
from pyweet.spam import AntiSpam


def print_tweet(tweet, settings):
    """Format and print the tweet dict.

    Returns:
        boolean status of if the tweet was printed
    """

    tweet_text = tweet.get("text")
    if tweet_text is None or (not settings["spam"] and
       AntiSpam.is_spam(tweet_text)):
        return False

    if sys.version_info[0] == 2:
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
            date = parse_date(tweet["created_at"])
            if settings.get("date"):
                prepend.append("{0:%b} {1}".format(
                    date,
                    int(datetime.strftime(date, "%d")),
                ))
            if settings.get("time"):
                prepend.append("{0:%H}:{0:%M}:{0:%S}".format(date))

        print("{0}{1}@{2}: {3}".format(
            " ".join(prepend),
            " " * int(prepend != []),
            tweet.get("user", {}).get("screen_name", ""),
            unescape(tweet_text),
        ))

    return True


def parse_date(date_str):
    """Parse out a datetime object from string using Twitter's formatting."""

    major = sys.version_info[0]
    minor = sys.version_info[1]
    if major > 3 or (major == 3 and minor >= 2):  # python4 support :p
        date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
    else:
        # bug in datetime's %z on py < 3.2 http://bugs.python.org/issue6641
        time_ = date_str.split(" ")
        date_str = " ".join([x for x in time_ if not x.startswith(("+", "-"))])
        date = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")

    return date


def streamed_search(twit=None, settings=None):
    """Stream a search query to the console."""

    kwargs = {}
    if settings.get("search"):
        kwargs.update({"track": ",".join(settings["search"])})
    if settings.get("user"):
        kwargs.update({"follow": settings["uid"]})

    for tweet in twit.statuses.filter(**kwargs):
        if tweet:
            print_tweet(tweet, settings)


@get_twit
def print_tweets(twit=None, settings=None):
    """Find some tweets and print them to console."""

    if settings["stream"] and (settings["search"] or settings["user"]):
        return streamed_search(twit, settings)
    elif settings.get("uid"):
        tweets = twit.statuses.user_timeline(user_id=settings["uid"])
    elif settings["search"]:
        tweets = twit.search.tweets(q=",".join(settings["search"]))["statuses"]
    else:
        tweets = twit.statuses.home_timeline()

    max_tweets = settings["max"]
    for i, tweet in enumerate(tweets):
        if not print_tweet(tweet, settings):
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

    if settings["stream"] and not (settings["search"] or settings["user"]):
        raise SystemExit(
            __doc__ + "Streaming requires search phrases or the -u flag"
        )

    return settings
