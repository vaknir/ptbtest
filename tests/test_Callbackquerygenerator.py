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
from ptbtest import (BadBotException, BadCallbackQueryException,
                     BadUserException, BadMessageException)
from ptbtest import (CallbackQueryGenerator, MessageGenerator, Mockbot,
                     UserGenerator)
from telegram import (CallbackQuery, Message, Update, User)
import sys
sys.path.append("..")


cqg = CallbackQueryGenerator()


@pytest.mark.callback
def test_invalid_calls():
        with pytest.raises(BadCallbackQueryException,
                                     "message and inline_message_id"):
            cqg.get_callback_query()
        with pytest.raises(BadCallbackQueryException,
                                     "message and inline_message_id"):
            cqg.get_callback_query(message=True, inline_message_id=True)
        with pytest.raises(BadCallbackQueryException,
                                     "data and game_short_name"):
            cqg.get_callback_query(message=True)
        with pytest.raises(BadCallbackQueryException,
                                     "data and game_short_name"):
            cqg.get_callback_query(
                message=True, data="test-data", game_short_name="mygame")

@pytest.mark.callback
def test_required_auto_set():
        u = cqg.get_callback_query(
            inline_message_id=True, data="test-data")
        assert isinstance(u.callback_query.from_user, User)
        assert isinstance(u.callback_query.chat_instance, str)
        bot = Mockbot(username="testbot")
        cqg2 = CallbackQueryGenerator(bot=bot)
        assert bot.username == cqg2.bot.username

        with pytest.raises(BadBotException):
            cqg3 = CallbackQueryGenerator(bot="bot")
@pytest.mark.callback
def test_message():
    mg = MessageGenerator()
    message = mg.get_message().message
    u = cqg.get_callback_query(message=message, data="test-data")
    assert isinstance(u, Update)
    assert isinstance(u.callback_query, CallbackQuery)
    assert u.callback_query.message.message_id == message.message_id

    u = cqg.get_callback_query(message=True, data="test-data")

    assert isinstance(u.callback_query.message, Message)
    assert u.callback_query.message.from_user.username == cqg.bot.username
    with pytest.raises(BadMessageException):
        cqg.get_callback_query(message="message", data="test-data")

@pytest.mark.callback
def test_inline_message_id():
    u = cqg.get_callback_query(
            inline_message_id="myidilike", data="test-data")
    assert u.callback_query.inline_message_id == "myidilike"
    u = cqg.get_callback_query(
            inline_message_id=True, data="test-data")
    assert isinstance(u.callback_query.inline_message_id, str)

    with pytest.raises(BadCallbackQueryException,
                                     "string or True"):
        cqg.get_callback_query(
                inline_message_id=3.98, data="test-data")

@pytest.mark.callback
def test_user():
        ug = UserGenerator()
        user = ug.get_user()
        u = cqg.get_callback_query(
            user=user, message=True, data="test-data")
        assert user.id == u.callback_query.from_user.id
        assert user.id != u.callback_query.message.from_user.id

        with pytest.raises(BadUserException):
            u = cqg.get_callback_query(
                user="user", inline_message_id=True, data="test-data")
