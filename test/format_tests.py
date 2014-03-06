#coding: utf-8


"""Test the tweet formatting capabilities."""


from __future__ import unicode_literals

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
    """Capturing standard out, ensuring the tweets display correctly."""

    def setUp(self):
        """Capture stdout."""

        self._stdout = sys.stdout
        sys.stdout = StringIO()
        self.tweet = json.load(open(os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "data",
            "tweet.json",
        )))
        self.settings = pyweet.parse_args()

    def tearDown(self):
        """Replace captured stdout, reset argv, clear the AntiSpam."""

        sys.stdout = self._stdout
        while len(sys.argv) > 1:
            sys.argv.pop(-1)
        AntiSpam.tweet_store = {}

    def test_basic_tweet_parsing(self):
        """Simple use case."""

        pyweet._print_tweet(self.tweet, self.settings)
        self.assertEqual(
            "@StephenAtHome: The FDA wants to put new labels on our food - "
            "just when I'd grown accustomed to the taste of our current "
            "labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_parsing_with_time(self):
        """Test adding the timestamp to the tweet."""

        self.settings.update({"time": True})
        pyweet._print_tweet(self.tweet, self.settings)
        self.assertEqual(
            "04:45:30 @StephenAtHome: The FDA wants to put new labels on our "
            "food - just when I'd grown accustomed to the taste of our current"
            " labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_parsing_with_date(self):
        """Test adding the date to the tweet."""

        self.settings.update({"date": True})
        pyweet._print_tweet(self.tweet, self.settings)
        self.assertEqual(
            "Mar 6 @StephenAtHome: The FDA wants to put new labels on our "
            "food - just when I'd grown accustomed to the taste of our current"
            " labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_parsing_with_time_and_date(self):
        """Test using both the time and date."""

        self.settings.update({"date": True, "time": True})
        pyweet._print_tweet(self.tweet, self.settings)
        self.assertEqual(
            "Mar 6 04:45:30 @StephenAtHome: The FDA wants to put new labels on"
            " our food - just when I'd grown accustomed to the taste of our "
            "current labels!",
            sys.stdout.getvalue().strip(),
        )

    def test_second_parse_is_anti_spammed(self):
        """The second identical tweet should be caught and not printed."""

        pyweet._print_tweet(self.tweet, self.settings)
        self.assertEqual(
            "@StephenAtHome: The FDA wants to put new labels on our food - "
            "just when I'd grown accustomed to the taste of our current "
            "labels!",
            sys.stdout.getvalue().strip(),
        )
        sys.stdout = StringIO()
        pyweet._print_tweet(self.tweet, self.settings)
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

    def test_cannot_decode_crazy_chars(self):
        """People can tweet unicode hamburgers, it shouldn't break pyweet."""

        self.tweet["text"] = "do you have any spare ⌛ for a 🍔?"
        if sys.version_info.major == 2:
            self.assertFalse(pyweet._print_tweet(self.tweet, self.settings))
        else:
            self.assertIn(self.tweet["text"], sys.stdout.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
