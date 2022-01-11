#!/usr/bin/env python
# pylint: disable=E0611,E0213,E1102,C0103,E1101,W0613,R0913,R0904
#
# A library that provides a testing suite fot python-telegram-bot
# wich can be found on https://github.com/python-telegram-bot/python-telegram-bot
# Copyright (C) 2017
# Pieter Schutz - https://github.com/eldinnie
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
from __future__ import absolute_import
import pytest
import telegram
from telegram import ChatAction
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import InlineQueryResult
from telegram import TelegramError
from telegram import User, Message, Chat, Update
from telegram.ext import Updater, CommandHandler
import sys

sys.path.append("..")
from ptbtest import Mockbot


mockbot = Mockbot()


@pytest.mark.mockbot
def test_updater_works_with_mockbot():
    # handler method
    def start(bot, update):
        message = bot.sendMessage(update.message.chat_id, "this works")
        assert isinstance(message, Message)

    updater = Updater(workers=2, bot=mockbot)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    user = User(id=1, first_name="test", is_bot=False)
    chat = Chat(45, "group")
    message = Message(404, user, None, chat, text="/start", bot=mockbot)
    message2 = Message(404, user, None, chat, text="start", bot=mockbot)
    message3 = Message(
        404, user, None, chat, text="/start@MockBot", bot=mockbot
    )
    message4 = Message(
        404, user, None, chat, text="/start@OtherBot", bot=mockbot
    )
    mockbot.insertUpdate(Update(0, message=message))
    mockbot.insertUpdate(Update(1, message=message2))
    mockbot.insertUpdate(Update(1, message=message3))
    mockbot.insertUpdate(Update(1, message=message4))
    data = mockbot.sent_messages
    assert len(data) == 2
    data = data[0]
    assert data["method"] == "sendMessage"
    assert data["chat_id"] == chat.id
    updater.stop()

@pytest.mark.mockbot
def test_properties():
        assert mockbot.id == 0
        assert mockbot.first_name == "Mockbot"
        assert mockbot.last_name == "Bot"
        assert mockbot.name == "@MockBot"
        mb2 = Mockbot("OtherUsername")
        assert(mb2.name, "@OtherUsername")
        mockbot.sendMessage(1, "test 1")
        mockbot.sendMessage(2, "test 2")
        assert len(mockbot.sent_messages) == 2
        mockbot.reset()
        assert len(mockbot.sent_messages) == 0

@pytest.mark.mockbot
def test_dejson_and_to_dict():
        import json

        d = mockbot.to_dict()
        assert isinstance(d, dict)
        js = json.loads(json.dumps(d))
        b = Mockbot.de_json(js, None)
        assert isinstance(b, Mockbot)

@pytest.mark.mockbot
def test_answerCallbackQuery():
        mockbot.answerCallbackQuery(
            1, "done", show_alert=True, url="google.com", cache_time=2
        )

        data = mockbot.sent_messages[-1]
        assert data["method"] == "answerCallbackQuery"
        assert data["text"] == "done"

@pytest.mark.mockbot
def test_answerInlineQuery():
        r = [InlineQueryResult("string", "1"),
             InlineQueryResult("string", "2")]
        mockbot.answerInlineQuery(
            1,
            r,
            is_personal=True,
            next_offset=3,
            switch_pm_parameter="asd",
            switch_pm_text="pm",
        )

        data = mockbot.sent_messages[-1]
        assert data["method"] == "answerInlineQuery"
        assert data["results"][0]["id"] == "1"

@pytest.mark.mockbot
def test_editMessageCaption():
        mockbot.editMessageCaption(chat_id=12, message_id=23)

        data = mockbot.sent_messages[-1]
        assert data["method"] == "editMessageCaption"
        assert data["chat_id"] == 12
        mockbot.editMessageCaption(
            inline_message_id=23, caption="new cap", photo=True
        )
        data = mockbot.sent_messages[-1]
        assert data["method"] == "editMessageCaption"
        with pytest.raises(TelegramError):
            mockbot.editMessageCaption()
        with pytest.raises(TelegramError):
            mockbot.editMessageCaption(chat_id=12)
        with pytest.raises(TelegramError):
            mockbot.editMessageCaption(message_id=12)

@pytest.mark.mockbot
def test_editMessageReplyMarkup():
        mockbot.editMessageReplyMarkup(chat_id=1, message_id=1)
        data = mockbot.sent_messages[-1]
        assert data["method"] == "editMessageReplyMarkup"
        assert data["chat_id"] == 1
        mockbot.editMessageReplyMarkup(inline_message_id=1)
        data = mockbot.sent_messages[-1]
        assert data["method"] == "editMessageReplyMarkup"
        assert data["inline_message_id"] == 1
        with pytest.raises(TelegramError):
            mockbot.editMessageReplyMarkup()
        with pytest.raises(TelegramError):
            mockbot.editMessageReplyMarkup(chat_id=12)
        with pytest.raises(TelegramError):
            mockbot.editMessageReplyMarkup(message_id=12)

@pytest.mark.mockbot
def test_editMessageText():
        mockbot.editMessageText("test", chat_id=1, message_id=1)
        data = mockbot.sent_messages[-1]
        assert data["method"] == "editMessageText"
        assert data["chat_id"] == 1
        assert data["text"] == "test"
        mockbot.editMessageText(
            "test",
            inline_message_id=1,
            parse_mode="Markdown",
            disable_web_page_preview=True,
        )
        data = mockbot.sent_messages[-1]
        assert data["method"] == "editMessageText"
        assert data["inline_message_id"] == 1

@pytest.mark.mockbot
def test_forwardMessage():
        mockbot.forwardMessage(1, 2, 3)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "forwardMessage"
        assert data["chat_id"] == 1

@pytest.mark.mockbot
def test_getChat():
        mockbot.getChat(1)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getChat"
        assert data["chat_id"] == 1

@pytest.mark.mockbot
def test_getChatAdministrators():
        mockbot.getChatAdministrators(chat_id=2)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getChatAdministrators"
        assert data["chat_id"] == 2

@pytest.mark.mockbot
def test_getChatMember():
        mockbot.getChatMember(1, 3)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getChatMember"
        assert data["chat_id"] == 1
        assert data["user_id"] == 3

@pytest.mark.mockbot
def test_getChatMembersCount():
        mockbot.getChatMembersCount(1)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getChatMembersCount"
        assert data["chat_id"] == 1

@pytest.mark.mockbot
def test_getFile():
        mockbot.getFile("12345")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getFile"
        assert data["file_id"] == "12345"

@pytest.mark.mockbot
def test_getGameHighScores():
        mockbot.getGameHighScores(
            1, chat_id=2, message_id=3, inline_message_id=4)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getGameHighScores"
        assert data["user_id"] == 1

@pytest.mark.mockbot
def test_getMe():
        data = mockbot.getMe()

        assert isinstance(data, User)
        assert data.name == "@MockBot"

@pytest.mark.mockbot
def test_getUpdates():
        data = mockbot.getUpdates()
        assert data == []

@pytest.mark.mockbot
def test_getUserProfilePhotos():
        mockbot.getUserProfilePhotos(1, offset=2)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "getUserProfilePhotos"
        assert data["user_id"] == 1

@pytest.mark.mockbot
def test_kickChatMember():
        mockbot.kickChatMember(chat_id=1, user_id=2)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "kickChatMember"
        assert data["user_id"] == 2

@pytest.mark.mockbot
def test_leaveChat():
        mockbot.leaveChat(1)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "leaveChat"

@pytest.mark.mockbot
def test_sendAudio():
        import uuid

        mockbot.sendAudio(
            1, "123", duration=2, performer="singer", title="song", caption="this song"
        )
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendAudio"
        assert data["chat_id"] == 1
        assert data["duration"] == 2
        assert data["performer"] == "singer"
        assert data["title"] == "song"
        assert data["caption"] == "this song"

@pytest.mark.mockbot
def test_sendChatAction():
        mockbot.sendChatAction(1, ChatAction.TYPING)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendChatAction"
        assert data["chat_id"] == 1
        assert data["action"] == "typing"

@pytest.mark.mockbot
def test_sendContact():
        mockbot.sendContact(1, "123456", "test", last_name="me")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendContact"
        assert data["chat_id"] == 1
        assert data["phone_number"] == "123456"
        assert data["last_name"] == "me"

@pytest.mark.mockbot
def test_sendDocument():
        mockbot.sendDocument(
            chat_id=1, document="45", filename="jaja.docx", caption="good doc"
        )
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendDocument"
        assert data["chat_id"] == 1
        assert data["filename"] == "jaja.docx"
        assert data["caption"] == "good doc"

@pytest.mark.mockbot
def test_sendGame():
        mockbot.sendGame(1, "testgame")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendGame"
        assert data["chat_id"] == 1
        assert data["game_short_name"] == "testgame"

@pytest.mark.mockbot
def test_sendLocation():
        mockbot.sendLocation(1, 52.123, 4.23)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendLocation"
        assert data["chat_id"] == 1

@pytest.mark.mockbot
def test_sendMessage():
        keyb = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("test 1", callback_data="test1")],
                [InlineKeyboardButton("test 2", callback_data="test2")],
            ]
        )
        mockbot.sendMessage(
            1,
            "test",
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=keyb,
            disable_notification=True,
            reply_to_message_id=334,
            disable_web_page_preview=True,
        )
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendMessage"
        assert data["chat_id"] == 1
        assert data["text"] == "test"
        assert data["reply_markup"]["inline_keyboard"][1][0]["callback_data"] == "test2"

@pytest.mark.mockbot
def test_sendPhoto():
        mockbot.sendPhoto(1, "test.png", caption="photo")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendPhoto"
        assert data["chat_id"] == 1
        assert data["caption"] == "photo"

@pytest.mark.mockbot
def test_sendSticker():
        mockbot.sendSticker(-4231, "test")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendSticker"
        assert data["chat_id"] == -4231

@pytest.mark.mockbot
def test_sendVenue():
        mockbot.sendVenue(
            1, 4.2, 5.1, "nice place", "somewherestreet 2", foursquare_id=2
        )
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendVenue"
        assert data["chat_id"] == 1
        assert data["foursquare_id"] == 2

@pytest.mark.mockbot
def test_sendVideo():
        mockbot.sendVideo(1, "some file", duration=3, caption="video")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendVideo"
        assert data["chat_id"] == 1
        assert data["duration"] == 3
        assert data["caption"] == "video"

@pytest.mark.mockbot
def test_sendVoice():
        mockbot.sendVoice(1, "some file", duration=3, caption="voice")
        data = mockbot.sent_messages[-1]

        assert data["method"] == "sendVoice"
        assert data["chat_id"] == 1
        assert data["duration"] == 3
        assert data["caption"] == "voice"

@pytest.mark.mockbot
def test_setGameScore():
        mockbot.setGameScore(
            1,
            200,
            chat_id=2,
            message_id=3,
            inline_message_id=4,
            force=True,
            disable_edit_message=True,
        )
        data = mockbot.sent_messages[-1]

        assert data["method"] == "setGameScore"
        assert data["user_id"] == 1
        mockbot.setGameScore(1, 200, edit_message=True)

@pytest.mark.mockbot
def test_unbanChatMember():
        mockbot.unbanChatMember(1, 2)
        data = mockbot.sent_messages[-1]

        assert data["method"] == "unbanChatMember"
        assert data["chat_id"] == 1
