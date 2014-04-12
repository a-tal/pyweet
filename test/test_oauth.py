"""Tests for pyweet's oauth handling."""


import os
import mock
import codecs
import shutil
import pytest
import twitter

from pyweet.oauth import get_oauth
from pyweet.settings import Settings


@pytest.fixture
def move_around_auth_file(request):
    """Moves the pyweet auth file out of the way for a test."""

    request.addfinalizer(move_auth_file_back)
    # this should exist by now, we're going to move it to test not having it
    assert os.path.exists(Settings.AUTH_FILE)
    # move the local auth file
    shutil.move(Settings.AUTH_FILE, "{0}-temp".format(Settings.AUTH_FILE))
    # make sure that move worked
    assert not os.path.exists(Settings.AUTH_FILE)


def move_auth_file_back():
    """Return the temp auth file to it's initial location."""

    shutil.move("{0}-temp".format(Settings.AUTH_FILE), Settings.AUTH_FILE)
    # ensure success
    assert os.path.exists(Settings.AUTH_FILE)


def test_first_time_setup(move_around_auth_file):
    """If the settings auth file doesn't exist, use twitter's oauth_dance."""

    patched_read_token_file = mock.patch.object(
        twitter,
        "read_token_file",
        return_value=(1, 1),
    )

    with mock.patch.object(twitter, "oauth_dance") as dancer:
        with patched_read_token_file as reader:
            get_oauth()

    dancer.assert_called_once_with(
        "pyweet",
        Settings.API,
        str(codecs.decode(Settings.API_SECRET, "rot-13")),
        Settings.AUTH_FILE,
    )

    reader.assert_called_once_with(Settings.AUTH_FILE)
