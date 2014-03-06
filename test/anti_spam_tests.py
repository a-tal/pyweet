"""Tests for pyweet's anti spam measures."""


import time
import unittest

from pyweet import AntiSpam


class AntiSpamTests(unittest.TestCase):
    """Tests for the object class AntiSpam."""

    def setUp(self):
        """"Get the default timeout."""

        self.default_timeout = AntiSpam.timeout

    def tearDown(self):
        """Reset the default timeout and tweet store."""

        AntiSpam.tweet_store = {}
        AntiSpam(self.default_timeout)

    def test_timeout_is_variable(self):
        """If this doesn't work, the other tests wont either."""

        self.assertEqual(AntiSpam.timeout, 600)
        AntiSpam(1)
        self.assertEqual(AntiSpam.timeout, 1)

    def test_duplicates_are_spam(self):
        """Identical messages without the timout should be marked as spam."""

        message = "a generic message to test with"
        self.assertFalse(AntiSpam.is_spam(message))
        self.assertTrue(AntiSpam.is_spam(message))
        self.assertTrue(AntiSpam.is_spam(message))
        self.assertTrue(AntiSpam.is_spam(message))

    def test_timeouts(self):
        """"After the timeout period, a message should get through."""

        message = "a generic message to test with"
        AntiSpam(1)  # 1 second timeout
        self.assertFalse(AntiSpam.is_spam(message))
        self.assertTrue(AntiSpam.is_spam(message))

        time.sleep(2)  # wait a bit
        self.assertFalse(AntiSpam.is_spam(message))
        self.assertTrue(AntiSpam.is_spam(message))


if __name__ == "__main__":
    unittest.main()
