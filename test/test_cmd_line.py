"""Tests for command line argument parsing."""


import sys
import pytest

from pyweet import base
from pyweet.base import parse_args


@pytest.fixture(autouse=True)
def setup_argv(request):
    """Register the finalizer to clean up sys.argv."""

    request.addfinalizer(reset_argv)


@pytest.fixture
def reset_argv():
    """Returns sys.argv to its original state."""

    while len(sys.argv) > 1:
        sys.argv.pop(-1)


def test_max_tweets():
    """Tests the -integer max tweet option."""

    sys.argv.append("-14")
    settings = parse_args()
    assert settings.get("max") == 14


def test_search_phrase_with_hyphen():
    """Allow `-non-int` as a search phrase."""

    # NB: doing this will return a 403 from Twitter, you need at least one
    #     positive search phrase.
    sys.argv.append("-7e4")
    settings = parse_args()
    assert settings.get("max") == 3
    assert settings.get("search") == ["-7e4"]


def test_search_tweets():
    """Tests search phrases."""

    sys.argv.append("ponies")
    settings = parse_args()
    assert settings.get("search") == ["ponies"]


def test_multiple_phrases():
    """Tests using more than one search keyword."""

    sys.argv.extend(["rainbows", "unicorns"])
    settings = parse_args()
    assert settings.get("search") == ["rainbows", "unicorns"]


def test_user_tweets():
    """Test specifiying tweets from a particular user."""

    sys.argv.extend(["-u", "billy"])
    settings = parse_args()
    assert settings.get("user") == "billy"


def test_stream():
    """Test that setting only the stream flag raises an error."""

    sys.argv.append("-s")
    with pytest.raises(SystemExit):
        parse_args()


def test_date_flag():
    """Test using the date flag."""

    sys.argv.append("-d")
    settings = parse_args()
    assert settings.get("date")


def test_time_flag():
    """Test using the time flag."""

    sys.argv.append("-t")
    settings = parse_args()
    assert settings.get("time")


def test_time_and_date_flags():
    """Test using the time and the date flags."""

    sys.argv.extend(["-t", "-d"])
    settings = parse_args()
    assert settings.get("date")
    assert settings.get("time")


def test_time_date_and_stream_flags():
    """Test using the time, date and stream flags."""

    sys.argv.extend(["-t", "-d", "-s", "some", "phrase"])
    settings = parse_args()
    assert settings.get("date")
    assert settings.get("time")
    assert settings.get("stream")
    assert settings.get("search", ["some", "phrase"])


def test_spam_flag():
    """Test using the disable anti-spam flag."""

    sys.argv.append("-n")
    settings = parse_args()
    assert settings.get("spam")


def test_json_flag():
    """Test using the -j flag to dump the tweet jsons."""

    sys.argv.append("-j")
    settings = parse_args()
    assert settings.get("json")


def test_negative_search():
    """We should be able to use a - at the start of a phrase to NOT it."""

    sys.argv.extend(["-something", "theotherthing"])
    settings = parse_args()
    assert settings.get("search") == ["-something", "theotherthing"]


def test_help():
    """The -h flag should raise SysExit with base.py's docstring."""

    # shouldn't matter the order the -h comes in
    sys.argv.extend(["-u", "someone", "-s", "-h", "wow", "much", "search"])
    with pytest.raises(SystemExit) as raises:
        parse_args()

    assert base.__doc__.strip() in raises.value.args


def test_max_with_negative_search():
    """Should be able to use -int with NOT search phrases."""

    sys.argv.extend(["-6", "-apples", "pears"])
    settings = parse_args()
    assert settings.get("max") == 6
    assert settings.get("search") == ["-apples", "pears"]
