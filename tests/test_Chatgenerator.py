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
import sys

sys.path.append("..")
import pytest
from ptbtest import UserGenerator
from ptbtest import ChatGenerator
from telegram.chat import Chat


cg = ChatGenerator()


@pytest.mark.chat
def test_without_parameter():
    c = cg.get_chat()

    assert isinstance(c.id, int)
    assert c.id > 0
    assert c.username == c.first_name + c.last_name
    assert c.type == "private"


@pytest.mark.chat
def test_group_chat():
    c = cg.get_chat(type="group")
    assert c.id < 0
    assert c.type == "group"
    assert c.all_members_are_administrators == False
    assert isinstance(c.title, str)


@pytest.mark.chat
def test_group_all_members_are_administrators():
    c = cg.get_chat(type="group", all_members_are_administrators=True)
    assert c.type == "group"
    assert c.all_members_are_administrators == True


@pytest.mark.chat
def test_group_chat_with_group_name():
    c = cg.get_chat(type="group", title="My Group")

    assert c.title == "My Group"


@pytest.mark.chat
def test_private_from_user():
    u = UserGenerator().get_user()
    c = cg.get_chat(user=u)

    assert u.id == c.id
    assert c.username == c.first_name + c.last_name
    assert u.username == c.username
    assert c.type == "private"


@pytest.mark.chat
def test_supergroup():
    c = cg.get_chat(type="supergroup")

    assert c.id < 0
    assert c.type == "supergroup"
    assert isinstance(c.title, str)
    assert c.username == "".join(c.title.split())


@pytest.mark.chat
def test_supergroup_with_title():
    c = cg.get_chat(type="supergroup", title="Awesome Group")

    assert c.title == "Awesome Group"
    assert c.username == "AwesomeGroup"


@pytest.mark.chat
def test_supergroup_with_username():
    c = cg.get_chat(type="supergroup", username="mygroup")

    assert c.username == "mygroup"


@pytest.mark.chat
def test_supergroup_with_username_title():
    c = cg.get_chat(type="supergroup", username="mygroup", title="Awesome Group")

    assert c.title == "Awesome Group"
    assert c.username == "mygroup"


@pytest.mark.chat
def test_channel():
    c = cg.get_chat(type="channel")

    assert isinstance(c.title, str)
    assert c.type == "channel"
    assert c.username == "".join(c.title.split())


@pytest.mark.chat
def test_channel_with_title():
    c = cg.get_chat(type="channel", title="Awesome Group")
    assert c.title == "Awesome Group"
    assert c.username == "AwesomeGroup"


@pytest.mark.chat
def test_channel_with_username():
    c = cg.get_chat(type="channel", username="mygroup")

    assert c.username == "mygroup"


@pytest.mark.chat
def test_channel_with_username_title():
    c = cg.get_chat(type="channel", username="mygroup", title="Awesome Channel")

    assert c.title == "Awesome Channel"
    assert c.username == "mygroup"
