"""Tests for the object class AntiSpam.

Uses the pyweet AntiSpam with a 1 second timeout instead of the usual 5 minutes
that you would experience if you actually ran the program.
"""


import time
import pytest

from pyweet.spam import AntiSpam


@pytest.fixture(autouse=True)
def set_test_timeout(request):
    request.addfinalizer(clear_store)
    AntiSpam.timeout = 1


@pytest.fixture
def clear_store():
    AntiSpam.tweet_store = {}
    AntiSpam.timeout = 600


def test_duplicates_are_spam():
    """Identical messages without the timout should be marked as spam."""

    message = "a generic message to test with"
    assert not AntiSpam.is_spam(message)
    assert AntiSpam.is_spam(message)
    assert AntiSpam.is_spam(message)
    assert AntiSpam.is_spam(message)


def test_timeouts():
    """"After the timeout period, a message should get through."""

    message = "another generic message to test with"
    assert not AntiSpam.is_spam(message)
    assert AntiSpam.is_spam(message)

    assert AntiSpam.timeout == 1, "pytest isn't picking up the fixture"
    time.sleep(2)  # wait a bit
    AntiSpam.clear()
    assert not AntiSpam.is_spam(message)
    assert AntiSpam.is_spam(message)
