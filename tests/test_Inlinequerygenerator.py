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
from re import match
from telegram import User
from telegram import Update
from telegram import Location
from telegram import InlineQuery
from telegram import ChosenInlineResult
from ptbtest import UserGenerator
from ptbtest import Mockbot
from ptbtest import InlineQueryGenerator
from ptbtest.errors import (BadBotException, BadUserException)
import pytest
import sys
sys.path.append("..")


iqg = InlineQueryGenerator()


@pytest.mark.inlinequery
def test_standard():
    u = iqg.get_inline_query()
    assert isinstance(u, Update)
    assert isinstance(u.inline_query, InlineQuery)
    assert isinstance(u.inline_query.from_user, User)

    bot = Mockbot(username="testbot")
    iqg2 = InlineQueryGenerator(bot=bot)
    assert bot.username == iqg2.bot.username

    with pytest.raises(BadBotException, match="Invalid ptbtest.Mockbot object"):
        iqg3 = InlineQueryGenerator(bot="bot")


@pytest.mark.inlinequery
def test_with_user():
    ug = UserGenerator()
    user = ug.get_user()
    u = iqg.get_inline_query(user=user)
    assert u.inline_query.from_user.id == user.id

    with pytest.raises(BadUserException, match="Invalid telegram.User object"):
        iqg.get_inline_query(user="user")


@pytest.mark.inlinequery
def test_query():
    u = iqg.get_inline_query(query="test")
    assert u.inline_query.query == "test"

    with pytest.raises(AttributeError, match="query"):
        iqg.get_inline_query(query=True)


@pytest.mark.inlinequery
def test_offset():
    u = iqg.get_inline_query(offset="44")
    assert u.inline_query.offset == "44"

    with pytest.raises(AttributeError, match="offset"):
        iqg.get_inline_query(offset=True)


@pytest.mark.inlinequery
def test_location():
    u = iqg.get_inline_query(location=True)
    assert isinstance(u.inline_query.location, Location)

    loc = Location(23.0, 90.0)
    u = iqg.get_inline_query(location=loc)
    assert u.inline_query.location.longitude == 23.0

    with pytest.raises(AttributeError, match="telegram.Location"):
        iqg.get_inline_query(location="location")


iqc = InlineQueryGenerator()


@pytest.mark.inlinequery
def test_chosen_inline_result():
    u = iqc.get_chosen_inline_result("testid")
    assert isinstance(u, Update)
    assert isinstance(u.chosen_inline_result, ChosenInlineResult)
    assert isinstance(u.chosen_inline_result.from_user, User)
    assert u.chosen_inline_result.result_id == "testid"

    with pytest.raises(AttributeError, match="chosen_inline_result"):
        iqc.get_chosen_inline_result()


@pytest.mark.inlinequery
def test_with_location():
    u = iqc.get_chosen_inline_result("testid", location=True)
    assert isinstance(u.chosen_inline_result.location, Location)
    loc = Location(23.0, 90.0)
    u = iqc.get_chosen_inline_result("testid", location=loc)
    assert u.chosen_inline_result.location.longitude == 23.0

    with pytest.raises(AttributeError, match="telegram.Location"):
        iqc.get_chosen_inline_result("test_id", location="loc")


@pytest.mark.inlinequery
def test_inline_message_id():
    u = iqc.get_chosen_inline_result("test")
    assert isinstance(u.chosen_inline_result.inline_message_id, str)

    u = iqc.get_chosen_inline_result(
        "test", inline_message_id="myidilike")
    assert u.chosen_inline_result.inline_message_id == "myidilike"


@pytest.mark.inlinequery
def test_user():
    ug = UserGenerator()
    user = ug.get_user()
    u = iqc.get_chosen_inline_result("test", user=user)
    assert u.chosen_inline_result.from_user.id == user.id

    with pytest.raises(BadUserException, match="Invalid telegram.User object"):
        iqc.get_chosen_inline_result("test", user="user")
