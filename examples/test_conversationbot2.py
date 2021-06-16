from __future__ import absolute_import
import unittest

from ptbtest import UserGenerator
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import RegexHandler
from telegram.ext import Updater

from ptbtest import ChatGenerator
from ptbtest import MessageGenerator
from ptbtest import Mockbot

"""
This is an example to show how the ptbtest suite can be used.
This example follows the conversationbot2 example at:
https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot2.py

"""


class TestConversationbot2(unittest.TestCase):
    def setUp(self):
        self.bot = Mockbot()
        self.cg = ChatGenerator()
        self.ug = UserGenerator()
        self.mg = MessageGenerator(self.bot)
        self.updater = Updater(bot=self.bot)  # type: ignore

    def test_conversation(self):
        CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

        reply_keyboard = [[KeyboardButton('Age'), KeyboardButton('Favourite colour')],
                          [KeyboardButton('Number of siblings'), KeyboardButton('Something else...')],
                          [KeyboardButton('Done')]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        def facts_to_str(user_data):
            facts = list()
            for key, value in user_data.items():
                facts.append('%s - %s' % (key, value))

            return "\n".join(facts).join(['\n', '\n'])

        def start(update, context):
            update.message.reply_text(
                "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
                "Why don't you tell me something about yourself?", reply_markup=markup)

            return CHOOSING

        def regular_choice(update, context):
            text = update.message.text
            context.user_data['choice'] = text
            update.message.reply_text('Your %s? Yes, I would love to hear about that!' % text.lower())

            return TYPING_REPLY

        def custom_choice(update, context):
            update.message.reply_text('Alright, please send me the category first, '
                                      'for example "Most impressive skill"')

            return TYPING_CHOICE

        def received_information(update, context):
            text = update.message.text
            category = context.user_data['choice']
            context.user_data[category] = text
            del context.user_data['choice']

            update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                                      "%s"
                                      "You can tell me more, or change your opinion on something."
                                      % facts_to_str(context.user_data), reply_markup=markup)

            return CHOOSING

        def done(update, context):
            if 'choice' in context.user_data:
                del context.user_data['choice']

            update.message.reply_text("I learned these facts about you:"
                                      "%s"
                                      "Until next time!" % facts_to_str(context.user_data))

            context.user_data.clear()
            return ConversationHandler.END

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                CHOOSING: [MessageHandler(Filters.regex('^(Age|Favourite colour|Number of siblings)$'),
                                        regular_choice),
                           MessageHandler(Filters.regex('^Something else...$'),
                                        custom_choice),
                           ],
                TYPING_CHOICE: [MessageHandler(Filters.text,
                                               regular_choice),
                                ],
                TYPING_REPLY: [MessageHandler(Filters.text,
                                              received_information),
                               ],
            },
            fallbacks=[MessageHandler(Filters.regex('^Done$'), done)]
        )
        dp = self.updater.dispatcher
        dp.add_handler(conv_handler)
        self.updater.start_polling()

        # We are going to test a conversationhandler. Since this is tied in with user and chat we need to
        # create both for consistancy
        user = self.ug.get_user()
        chat = self.cg.get_chat(type="group")
        user2 = self.ug.get_user()
        chat2 = self.cg.get_chat(user=user)

        # let's start the conversation
        u = self.mg.get_message(user=user, chat=chat, text="/start", parse_mode="HTML")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Doctor Botter\. I will")
        u = self.mg.get_message(user=user, chat=chat, text="Age")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Your age\? Yes")

        # now let's see what happens when another user in another chat starts conversating with the bot
        u = self.mg.get_message(user=user2, chat=chat2, text="/start", parse_mode="HTML")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Doctor Botter\. I will")
        self.assertEqual(data['chat_id'], chat2.id)
        self.assertNotEqual(data['chat_id'], chat.id)
        # and cancels his conv.
        u = self.mg.get_message(user=user2, chat=chat2, text="Done")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Until next time!")

        # cary on with first user
        u = self.mg.get_message(user=user, chat=chat, text="23")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Age - 23")
        u = self.mg.get_message(user=user, chat=chat, text="Something else...")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Most impressive skill")
        u = self.mg.get_message(user=user, chat=chat, text="programming skill")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"Your programming skill\? Yes")
        u = self.mg.get_message(user=user, chat=chat, text="High")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"programming skill - High")
        u = self.mg.get_message(user=user, chat=chat, text="Done")
        self.bot.insertUpdate(u)
        data = self.bot.sent_messages[-1]
        self.assertRegex(data['text'], r"programming skill - High")
        self.assertRegex(data['text'], r"Age - 23")

        self.updater.stop()


if __name__ == '__main__':
    unittest.main()
