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
    return mock_twit


@pytest.fixture
def statuses(filter):
    """Streaming Twitter statuses mock. Contains filter attribute."""

    mock_statuses = mock.MagicMock()
    mock_statuses.filter = filter
    return mock_statuses


@pytest.fixture
def filter(tweet):
    """Streaming Twitter filter mock method. Returns 1 json loaded tweet."""

    return mock.MagicMock(return_value=[tweet])


def test_streamed_search(twit, capfd, tweet):
    settings = {"user": "notch", "uid": 63485337, "search": ["some", "words"]}

    with mock.patch.object(base, "print_tweet") as patched:
        base.streamed_search(twit, settings)
    twit.statuses.filter.assert_called_once_with(
        follow=63485337,
        track="some,words",
    )
    assert patched.call_count == 1


if __name__ == "__main__":
    pytest.main()
