"""Tests for the base functionality of pyweet."""


import mock
import pytest
import twitter

from pyweet import base


@pytest.fixture
def twit(statuses):
    """TwitterStream mock object."""

    mock_twit = mock.MagicMock(spec=twitter.TwitterStream)
    mock_twit.statuses = statuses
    mock_twit.search = statuses
    return mock_twit


@pytest.fixture
def statuses(filter, search):
    """Streaming Twitter statuses mock. Contains filter attribute."""

    mock_statuses = mock.MagicMock()
    mock_statuses.filter = filter
    mock_statuses.tweets = search
    mock_statuses.user_timeline = filter
    return mock_statuses


@pytest.fixture
def filter(tweet):
    """Streaming Twitter filter mock method. Returns 1 json loaded tweet."""

    return mock.MagicMock(return_value=[tweet])


@pytest.fixture
def search(tweet):
    """Static search, non streaming. Returns a dict of 1 json loaded tweet."""

    return mock.MagicMock(return_value={"statuses": [tweet]})


def test_streamed_search(twit, capfd, tweet):
    settings = {"user": "notch", "uid": 63485337, "search": ["some", "words"]}

    with mock.patch.object(base, "print_tweet") as patched:
        base.streamed_search(twit, settings)
    twit.statuses.filter.assert_called_once_with(
        follow=63485337,
        track="some,words",
    )
    assert patched.call_count == 1


class TestPrintTweets(object):
    """Tests related to the print_tweets function."""
    def test_calls_stream(selt, twit):
        """stream AND search OR user should call streamed_search."""

        settings = [
            {"stream": True, "search": ["things"], "user": None},
            {"stream": True, "search": None, "user": "notch"},
        ]
        for setting in settings:
            with mock.patch.object(base, "streamed_search") as patched:
                base.print_tweets(twit=twit, settings=setting)
            patched.assert_called_once_with(twit, setting)

    def test_user_timeline_called(self, twit):
        """uid without stream should trigger statuses.user_timeline."""

        settings = {
            "stream": False,
            "search": None,
            "user": "notch",
            "uid": 63485337,
            "max": 1,
            "spam": False,
        }

        base.print_tweets(twit=twit, settings=settings)
        twit.statuses.user_timeline.assert_called_once_with(user_id=63485337)

    def test_search_called(self, twit):
        """search without stream should call search.tweets."""

        settings = {
            "stream": False,
            "search": ["words", "and", "phrases"],
            "user": None,
            "uid": None,
            "max": 1,
            "spam": False,
        }

        base.print_tweets(twit=twit, settings=settings)
        twit.search.tweets.assert_called_once_with(q="words,and,phrases")

    def test_home_timeline(self, twit):
        """with no options, we should call statuses.home_timeline."""

        settings = {
            "stream": False,
            "search": None,
            "user": None,
            "uid": None,
            "max": 1,
            "spam": False,
        }

        base.print_tweets(twit=twit, settings=settings)
        twit.statuses.home_timeline.assert_called_once()
