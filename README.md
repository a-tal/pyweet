pyweet [![Build Status](https://travis-ci.org/a-tal/pyweet.png?branch=master)](https://travis-ci.org/a-tal/pyweet) [![Coverage Status](https://coveralls.io/repos/a-tal/pyweet/badge.png?branch=master)](https://coveralls.io/r/a-tal/pyweet?branch=master) [![Stories in Backlog](https://badge.waffle.io/a-tal/pyweet.png?label=ready&title=Backlog)](https://waffle.io/a-tal/pyweet) [![Stories in Progress](https://badge.waffle.io/a-tal/pyweet.png?label=ready&title=in+progress)](https://waffle.io/a-tal/pyweet)
==============================

Python Twitter Command Line Interface


Installation
============

pyweet is available through pip or easyinstall. Alternatively clone this repo and use the setup.py to build and install the package.


Configuration
=============

The first time you run pyweet it will need permission from your twitter account. A web browser should pop open to a page on twitter.com with a confirmation number (after you login to twitter). Paste that verification number back into the shell and the initial configuration is done. If you want to transfer your config to another computer, just copy the ~/.pyweet file.


Usage
=====

Basic usage with no arguments will display the last 3 tweets from your home timeline. The command strucuture is like so:

  `pyweet [search terms] [options]`

Search terms can be as many as you like. Use a hyphen before a word to NOT it. If you are searching, at least one of the phrases must not be a NOT term.

You can use `-<int>` to display an amount of tweets other than 3. `pyweet -10` for instance will display the last 10 tweets to your home timeline.

The `-u <user>` flag can be used to find tweets from a particular screen name.

Use of the `-s` flag will stream tweets to the console. It can be used in conjunction with the `-u` flag and search phrases to stream tweets matching a set of search phrases or from a particular user.

You can search via AND or via ORs, use multiple arguments to OR phrases together, and quote multiple phrases (with a space to separate) to AND together certain keywords.

For example, `pyweet -s "apples bananas" oranges -grapes` will stream tweets to do with apples AND bananas, or oranages, but not grapes.


Computations
============

I did this because it was easy. There's really not much that pyweet does itself other than wrap the twitter python module (which I did not write). There is a bit of built in anti spam measures (use `-n` to override them), but that's about it. All handling of search phrases is handled by Twitter, including NOTing phrases.

All errors thrown by pyweet will be captured by a global `try:except` block. It will prompt you if you'd like to see the traceback that caused the error, usually these are errors returned from Twitter after passing your API call.


Extra Info
==========

If you'd like to see all the metadata about the tweets, you can use the `-j` option to have it spit out the complete tweet JSON structure to stdout instead.


Feature Requests and Bugs
=========================

Please direct feature requests or bugs to Github's [issue tracking service](https://github.com/a-tal/pyweet/issues).
