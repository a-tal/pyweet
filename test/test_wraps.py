"""Test the wrapper function used by pyweet."""


from pyweet.wraps import get_twit


def test_basic_use():
    """Basic use case, no previous twitter object provided."""

    @get_twit
    def _test_method(twit=None, settings=None):
        assert twit is not None
        assert settings is not None

    _test_method()


def test_repassed_object():
    """If passed a twitter object, we should still be using the same one."""

    @get_twit
    def _test_method(twit=None, settings=None):
        assert twit is not None
        assert settings is not None
        return twit

    twit = _test_method()
    assert id(twit) == id(_test_method(twit=twit))


def test_uid_lookup():
    """If settings has a "user" key, the uid should be in settings."""

    @get_twit
    def _test_method(twit=None, settings=None):
        assert "uid" in settings
        assert settings["uid"] == 63485337

    _test_method(settings={"user": "notch"})


def test_uid_lookup_with_stream():
    """Slightly different code path if we're streaming, lookup first."""

    @get_twit
    def _test_method(twit=None, settings=None):
        assert "uid" in settings
        assert settings["uid"] == 63485337

    _test_method(settings={"user": "notch", "stream": True})
