[![Documentation Status](https://readthedocs.org/projects/ptbtestsuite/badge/?version=master)](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) 
[![PyPI](https://img.shields.io/pypi/v/ptb_unittest.svg)](https://pypi.python.org/pypi/ptb_unittest) [![PyPI](https://img.shields.io/pypi/pyversions/ptb_unittest.svg)](https://pypi.python.org/pypi/ptb_unittest) [![PyPI](https://img.shields.io/pypi/l/ptb_unittest.svg)](https://pypi.python.org/pypi/ptbtest)

# ptb unittest
## a testsuite for [Python telegram bot](https://github.com/python-telegram-bot/python-telegram-bot/)
**Note:** This is a derivative work of the original [ptbtest](https://pypi.python.org/pypi/ptbtest)

This library is for people wanting to write unittests for their `python-telegram-bot` driven bots.
The following things make this library attractive to create unittests
* `Mockbot` - A fake bot that does not contact telegram servers
* Works with the `Updater` from `telegram.ext`
* `Generator` classes to easily create `Users`, `Chats` and `Updates` objects.

Read the [documentation](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) for further reading and check out the examples.

### Disclaimer
Unstable package. Most files are not up-to-date with latest `python-telegram-bot`. Feel free to contribute.
#### Use at your own risk.