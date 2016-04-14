"""Adds some color to the tweets."""


import re
from blessings import Terminal


class Term(object):
    """Static class to store terminal color info."""

    @staticmethod
    def colors():
        """Returns the colors in use for this terminal."""

        if not hasattr(Term, "_colors"):
            Term._colors = {}
            term = Terminal()
            if term.color:
                Term._colors["text"] = term.normal
                if term.number_of_colors >= 256:
                    Term._colors["name"] = term.color(35)
                    Term._colors["url"] = term.color(45)
                    Term._colors["hashtag"] = term.color(227)
                else:
                    Term._colors["name"] = term.color(4)
                    Term._colors["url"] = term.color(6)
                    Term._colors["hashtag"] = term.color(3)
        return Term._colors

    @staticmethod
    def patterns():
        """Returns the patterns used for searching."""

        if not hasattr(Term, "_patterns"):
            Term._patterns = {}
            if Term.colors():
                Term._patterns["url"] = re.compile(
                    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|'
                    r'(?:%[0-9a-fA-F][0-9a-fA-F]))+'
                )
                Term._patterns["name"] = re.compile(r'(^|[^@\w])@(\w{1,15})\b')
                Term._patterns["hashtag"] = re.compile(r'(^|[ ])#\w+')
        return Term._patterns


def highlight_tweet(tweet):
    """Highlights the tweet with console colors if supported."""

    if not Term.colors():
        return tweet

    return _re_hl(_re_hl(_re_hl(tweet, "name"), "hashtag"), "url")


def _re_hl(tweet, re_name):
    """Highlights the tweet with the color and pattern of name."""

    words = []
    colors = Term.colors()
    patterns = Term.patterns()
    last_match = 0
    for match in re.finditer(patterns[re_name], tweet):
        span = match.span()
        bump = int(span[0] != 0) and re_name != "url"
        words.append(tweet[last_match:span[0] + bump])
        word = "{0}{1}{2}".format(
            colors[re_name],
            tweet[span[0] + bump:span[1]],
            colors["text"],
        )
        words.append(word)
        last_match = span[1]

    words.append(tweet[last_match:])
    return "".join(words)
