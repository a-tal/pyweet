"""Test the tweet formatting capabilities."""


import os
import sys
import json
import unittest

if sys.version_info.major >= 3:
    from io import StringIO
else:
    from StringIO import StringIO

import pyweet
from pyweet import AntiSpam


class FormattingTests(unittest.TestCase):
    def setUp(self):
        """Capture stdout."""

        self._stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        """Replace captured stdout, reset argv, clear the AntiSpam."""

        sys.stdout = self._stdout
        while len(sys.argv) > 1:
            sys.argv.pop(-1)
        AntiSpam.tweet_store = {}

    def test_basic_tweet_parsing(self):
        """Simple use case."""

        tweet = json.load(open(os.path.join(os.curdir, "data/tweet.json")))
        settings = pyweet.parse_args()
        pyweet._print_tweet(tweet, settings)
        self.assertEqual(
            "@StephenAtHome: The FDA wants to put new labels on our food - "
            "just when I'd grown accustomed to the taste of our current "
            "labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_parsing_with_time(self):
        """Test adding the timestamp to the tweet."""

        settings = pyweet.parse_args()
        settings.update({"time": True})

        tweet = json.load(open("data/tweet.json"))
        pyweet._print_tweet(tweet, settings)
        self.assertEqual(
            "04:45:30 @StephenAtHome: The FDA wants to put new labels on our "
            "food - just when I'd grown accustomed to the taste of our current"
            " labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_parsing_with_date(self):
        """Test adding the date to the tweet."""

        settings = pyweet.parse_args()
        settings.update({"date": True})

        tweet = json.load(open("data/tweet.json"))
        pyweet._print_tweet(tweet, settings)
        self.assertEqual(
            "Mar 6 @StephenAtHome: The FDA wants to put new labels on our "
            "food - just when I'd grown accustomed to the taste of our current"
            " labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_parsing_with_time_and_date(self):
        """Test using both the time and date."""

        settings = pyweet.parse_args()
        settings.update({"date": True, "time": True})

        tweet = json.load(open("data/tweet.json"))
        pyweet._print_tweet(tweet, settings)
        self.assertEqual(
            "Mar 6 04:45:30 @StephenAtHome: The FDA wants to put new labels on"
            " our food - just when I'd grown accustomed to the taste of our "
            "current labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_second_parse_is_anti_spammed(self):
        """The second identical tweet should be caught and not printed."""

        tweet = json.load(open("data/tweet.json"))
        settings = pyweet.parse_args()
        pyweet._print_tweet(tweet, settings)
        self.assertEqual(
            "@StephenAtHome: The FDA wants to put new labels on our food - "
            "just when I'd grown accustomed to the taste of our current "
            "labels!",
            sys.stdout.getvalue().strip(),
        )
        sys.stdout = StringIO()
        self.assertFalse(pyweet._print_tweet(tweet, settings))
        self.assertEqual("", sys.stdout.getvalue().strip())

    def test_date_parsing(self):
        """Test basic use case for string -> datetime parsing."""

        date_str = "Thu Mar 06 04:45:30 +0000 2014"
        date_obj = pyweet._parse_date(date_str)
        self.assertEqual(date_obj.timetuple().tm_mon, 3)
        self.assertEqual(date_obj.timetuple().tm_yday, 65)
        self.assertEqual(date_obj.timetuple().tm_year, 2014)
        self.assertEqual(date_obj.timetuple().tm_hour, 4)
        self.assertEqual(date_obj.timetuple().tm_min, 45)
        self.assertEqual(date_obj.timetuple().tm_sec, 30)


if __name__ == "__main__":
    unittest.main()
