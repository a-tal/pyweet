"""OAuth handling for pyweet."""


import os
import codecs

import twitter

from pyweet.settings import Settings


def get_oauth():
    """Authenticate/register."""

    # I realize this isn't actually secret. The key/secret combo is linked to
    # your account though, if you do feel the need to abuse it
    secret = str(codecs.decode(Settings.API_SECRET, "rot-13"))
    if not os.path.exists(Settings.AUTH_FILE):
        twitter.oauth_dance(
            "pyweet",
            Settings.API,
            secret,
            Settings.AUTH_FILE,
        )

    token, user_secret = twitter.read_token_file(Settings.AUTH_FILE)
    return twitter.OAuth(token, user_secret, Settings.API, secret)
