"""Test environment builder for travis ci builds, picked up by pytest."""


import os
import pytest


@pytest.fixture(autouse=True, scope="session")
def session_setup():
    """Install the environment variable for the API credentials."""

    env_key = "TWIT_OAUTH"
    if env_key in os.environ:
        with open(os.path.expanduser("~/.pyweet"), "w") as api_file:
            api_file.write("{0}\n{1}".format(*os.environ[env_key].split("|")))

    assert os.path.exists(os.path.expanduser("~/.pyweet")), "no user auth key"
