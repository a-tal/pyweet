"""Test environment builder for travis ci builds, picked up by pytest."""


import os
import json
import pytest


@pytest.fixture
def tweet():
    """Returns the json loaded example tweet from test/data."""

    return json.load(open(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "test",
        "data",
        "tweet.json",
    )))


@pytest.fixture(autouse=True, scope="session")
def session_setup():
    """Install the environment variable for the API credentials."""

    env_key = "TWIT_OAUTH"
    if env_key in os.environ:
        with open(os.path.expanduser("~/.pyweet"), "w") as api_file:
            api_file.write("{0}\n{1}".format(*os.environ[env_key].split("|")))

    assert os.path.exists(os.path.expanduser("~/.pyweet")), "no user auth key"
