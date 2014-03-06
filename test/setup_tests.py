"""Test environment builder for travis ci builds."""


import os
import logging


def main():
    """Install the environment variable for the API credentials."""

    env_key = "TWIT_OAUTH"
    if env_key in os.environ:
        with open(os.path.expanduser("~/.pyweet"), "w") as api_file:
            api_file.write("{}\n{}".format(*os.environ[env_key].split("|")))
    else:
        logging.error("%s not found in environment vairables.", env_key)


if __name__ == "__main__":
    main()
