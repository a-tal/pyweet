"""Test the wrapper function used by pyweet."""


import unittest

from pyweet import get_twit


class WrapperTests(unittest.TestCase):
    """Pyweet uses a wrap to provide the twitter object."""


    def test_basic_use(self):
        """Basic use case, no previous twitter object provided."""

        @get_twit
        def _test_method(twit=None, settings=None):
            self.assertIsNotNone(twit)
            self.assertIsNotNone(settings)

        _test_method()

    def test_repassed_object(self):
        """If passed in a twitter object, should stil be using the same one."""

        @get_twit
        def _test_method(twit=None, settings=None):
            self.assertIsNotNone(twit)
            self.assertIsNotNone(settings)
            return twit

        twit = _test_method()
        self.assertEqual(id(twit), id(_test_method(twit=twit)))

    def test_uid_lookup(self):
        """If settings has a "user" key, the uid should be in settings."""

        @get_twit
        def _test_method(twit=None, settings=None):
            self.assertIn("uid", settings)
            self.assertEqual(settings["uid"], 63485337)

        _test_method(settings={"user": "notch"})

    def test_uid_lookup_with_stream(self):
        """Slightly different code path if we're streaming, lookup first."""

        @get_twit
        def _test_method(twit=None, settings=None):
            self.assertIn("uid", settings)
            self.assertEqual(settings["uid"], 63485337)

        _test_method(settings={"user": "notch", "stream": True})


if __name__ == "__main__":
    unittest.main()
