#coding: utf-8
"""Test the tweet formatting capabilities."""


from __future__ import unicode_literals

import sys
import json
import pytest

from pyweet.spam import AntiSpam
from pyweet.base import print_tweet, parse_date, parse_args


@pytest.fixture
def settings():
    _settings = parse_args()
    _settings.update({"spam": True})
    return _settings


@pytest.fixture(autouse=True)
def test_setup(request):
    """Register the finalizer."""

    AntiSpam.tweet_store = {}
    request.addfinalizer(test_teardown)


def test_teardown():
    """Reset argv and clear the AntiSpam."""

    while len(sys.argv) > 1:
        sys.argv.pop(-1)


def test_basic_tweet_parsing(tweet, settings, capfd):
    """Simple use case."""

    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert (
        "@StephenAtHome: The FDA wants to put new labels on our food - "
        "just when I'd grown accustomed to the taste of our current "
        "labels!"
    ) == out.strip()


def test_parsing_with_time(tweet, settings, capfd):
    """Test adding the timestamp to the tweet."""

    settings.update({"time": True})
    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert (
        "04:45:30 @StephenAtHome: The FDA wants to put new labels on our "
        "food - just when I'd grown accustomed to the taste of our current"
        " labels!"
    ) == out.strip()


def test_parsing_with_date(tweet, settings, capfd):
    """Test adding the date to the tweet."""

    settings.update({"date": True})
    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert (
        "Mar 6 @StephenAtHome: The FDA wants to put new labels on our "
        "food - just when I'd grown accustomed to the taste of our current"
        " labels!"
    ) == out.strip()


def test_parsing_with_time_and_date(tweet, settings, capfd):
    """Test using both the time and date."""

    settings.update({"date": True, "time": True})
    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert (
        "Mar 6 04:45:30 @StephenAtHome: The FDA wants to put new labels on"
        " our food - just when I'd grown accustomed to the taste of our "
        "current labels!"
    ) == out.strip()


def test_second_parse_is_spam(tweet, settings, capfd):
    """The second identical tweet should be caught and not printed."""

    settings.update({"spam": False})
    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert (
        "@StephenAtHome: The FDA wants to put new labels on our food - "
        "just when I'd grown accustomed to the taste of our current "
        "labels!"
    ) == out.strip()

    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert "" == out.strip()


def test_cannot_decode_crazy_chars(tweet, settings, capfd):
    """People can tweet unicode hamburgers, it shouldn't break pyweet."""

    tweet["text"] = "do you have any spare ⌛ for a 🍔?"
    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    if sys.version_info[0] == 2:
        assert not out
    else:
        assert tweet["text"] in out.strip()


def test_json_dumping(tweet, settings, capfd):
    """Verify the json dumped is the same as the test data input."""

    settings.update({"json": True})
    print_tweet(tweet, settings)
    out, _ = capfd.readouterr()
    assert json.loads(out.strip()) == tweet


def test_date_parsing():
    """Test basic use case for string -> datetime parsing."""

    date_str = "Thu Mar 06 04:45:30 +0000 2014"
    date_obj = parse_date(date_str)
    assert date_obj.timetuple().tm_mon == 3
    assert date_obj.timetuple().tm_yday == 65
    assert date_obj.timetuple().tm_year == 2014
    assert date_obj.timetuple().tm_hour == 4
    assert date_obj.timetuple().tm_min == 45
    assert date_obj.timetuple().tm_sec == 30
