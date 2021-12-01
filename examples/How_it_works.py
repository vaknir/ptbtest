"""
"PTB" is "python-telegram-bot".

The logic of logic of ptbtests is maximally easy.
First, like in PTB code, we are creating a "bot" and "updater".
"""

from telegram.ext import Updater
from ptbtest import Mockbot


self.bot = Mockbot()
self.updater = Updater(bot=self.bot)


"""
As you can see, an "updater" is a regular PTB object.
And the "bot" is Mockbot instance (which mimicks a real PTB bot).
An Updater getting our mockbot as a bot parameter.
To get updates Updater is calling "bot.get_updates" method of bot.

This is presented on this line:
https://github.com/python-telegram-bot/python-telegram-bot/blob/2f6c4075c866e4e03dccb2b1f41c1fa550e00d93/telegram/ext/updater.py#L596

The key moment is that "bot.get_updates" method are overrided by our mockbot!
So this method just returns a list with updates which we are inserted (almost) manually!
We are doing it via "bot.insertUpdate" method.

So this is a key magic of ptbtest.
"""
