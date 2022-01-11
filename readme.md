[![Documentation Status](https://readthedocs.org/projects/ptbtestsuite/badge/?version=master)](http://ptbtestsuite.readthedocs.io/en/master/?badge=master) ![Python](https://img.shields.io/pypi/pyversions/python-telegram-bot)]![tests workflow](https://github.com/vaknir/ptbtest/actions/workflows/ptb-actions.yml/badge.svg)

# ptb Pytest
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
