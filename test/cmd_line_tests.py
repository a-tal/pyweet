"""Tests for command line argument parsing."""


import sys
import unittest

try:
    from pyweet import pyweet
except ImportError:
    sys.path.insert(1, "..")
    from src import pyweet


class CmdLineTests(unittest.TestCase):
    def tearDown(self):
        """Returns sys.argv to its original state."""

        while len(sys.argv) > 1:
            sys.argv.pop(-1)

    def test_max_tweets(self):
        """Tests the -integer max tweet option."""

        sys.argv.append("-14")
        settings = pyweet.parse_args()
        self.assertEqual(settings.get("max"), 14)

    def test_search_phrase_with_hyphen(self):
        """Allow `-non-int` as a search phrase."""

        # NB: doing this will return a 403 from Twitter, you need at least one
        #     positive search phrase.
        sys.argv.append("-7e4")
        settings = pyweet.parse_args()
        self.assertEqual(settings.get("max"), 3)
        self.assertEqual(settings.get("search"), ["-7e4"])

    def test_search_tweets(self):
        """Tests search phrases."""

        sys.argv.append("ponies")
        settings = pyweet.parse_args()
        self.assertEqual(settings.get("search"), ["ponies"])

    def test_multiple_phrases(self):
        """Tests using more than one search keyword."""

        sys.argv.extend(["rainbows", "unicorns"])
        settings = pyweet.parse_args()
        self.assertEqual(settings.get("search"), ["rainbows", "unicorns"])

    def test_user_tweets(self):
        """Test specifiying tweets from a particular user."""

        sys.argv.extend(["-u", "billy"])
        settings = pyweet.parse_args()
        self.assertEqual(settings.get("user"), "billy")

    def test_stream(self):
        """Test using the stream flag."""

        sys.argv.append("-s")
        settings = pyweet.parse_args()
        self.assertTrue(settings.get("stream"))


if __name__ == "__main__":
    unittest.main()
