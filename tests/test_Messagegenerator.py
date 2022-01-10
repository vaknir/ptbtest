from __future__ import absolute_import
from telegram import (
    Audio,
    Contact,
    Document,
    Location,
    Sticker,
    User,
    Update,
    Venue,
    Video,
    Voice,
    PhotoSize,
    Message,
)
from ptbtest import UserGenerator, MessageGenerator, ChatGenerator
from ptbtest import Mockbot
from ptbtest import (
    BadBotException,
    BadChatException,
    BadUserException,
    BadMarkupException,
    BadMessageException,
)
import pytest
import sys

sys.path.append("..")


mg = MessageGenerator()


@pytest.mark.message
def test_is_update():
    u = mg.get_message()
    assert isinstance(u, Update)
    assert isinstance(u.message, Message)


@pytest.mark.message
def test_bot():
    u = mg.get_message()
    assert isinstance(u.message.bot, Mockbot)
    assert u.message.bot.username == "MockBot"

    b = Mockbot(username="AnotherBot")
    mg2 = MessageGenerator(bot=b)
    u = mg2.get_message()
    assert u.message.bot.username == "AnotherBot"

    with pytest.raises(BadBotException):
        mg3 = MessageGenerator(bot="Yeah!")


@pytest.mark.message
def test_private_message():
    u = mg.get_message(private=True)
    assert u.message.from_user.id == u.message.chat.id


@pytest.mark.message
def test_not_private():
    u = mg.get_message(private=False)
    assert u.message.chat.type == "group"
    assert u.message.from_user.id != u.message.chat.id


@pytest.mark.message
def test_with_user():
    ug = UserGenerator()
    us = ug.get_user()
    u = mg.get_message(user=us, private=False)
    assert u.message.from_user.id == us.id
    assert u.message.from_user.id != u.message.chat.id

    u = mg.get_message(user=us)
    assert u.message.from_user == us
    assert u.message.from_user.id == u.message.chat.id

    with pytest.raises(BadUserException):
        us = "not a telegram.Usematch="
        u = mg.get_message(user=us)


@pytest.mark.message
def test_with_chat():
    cg = ChatGenerator()
    c = cg.get_chat()
    u = mg.get_message(chat=c)
    assert u.message.chat.id == u.message.from_user.id
    assert u.message.chat.id == c.id

    c = cg.get_chat(type="group")
    u = mg.get_message(chat=c)
    assert u.message.from_user.id == u.message.chat.id
    assert u.message.chat.id == c.id

    with pytest.raises(BadChatException, match="get_channel_post"):
        c = cg.get_chat(type="channel")
        mg.get_message(chat=c)

    with pytest.raises(BadChatException):
        c = "Not a telegram.Chat"
        mg.get_message(chat=c)


@pytest.mark.message
def test_with_chat_and_user():
    cg = ChatGenerator()
    ug = UserGenerator()
    us = ug.get_user()
    c = cg.get_chat()
    u = mg.get_message(user=us, chat=c)
    assert u.message.from_user.id != u.message.chat.id
    assert u.message.from_user.id == us.id
    assert u.message.chat.id == c.id

    us = "not a telegram.Usematch="
    with pytest.raises(BadUserException):
        u = mg.get_message(user=us)
    with pytest.raises(BadUserException):
        u = mg.get_message(chat=c, user="usematch=")

    c = "Not a telegram.Chat"
    with pytest.raises(BadChatException):
        mg.get_message(chat=c)
    with pytest.raises(BadChatException):
        mg.get_message(user=u, chat="chat")


mg = MessageGenerator()


@pytest.mark.message
def test_simple_text():
    u = mg.get_message(text="This is a test")
    assert u.message.text == "This is a test"


@pytest.mark.message
def test_text_with_markdown():
    teststr = (
        "we have *bold* `code` [google](www.google.com) @username #hashtag _italics_ ```pre block``` "
        "ftp://snt.utwente.nl /start"
    )
    u = mg.get_message(text=teststr)
    assert u.message.text == teststr

    u = mg.get_message(text=teststr, parse_mode="Markdown")
    assert len(u.message.entities) == 9
    for ent in u.message.entities:
        if ent.type == "bold":
            assert ent.offset == 8
            assert ent.length == 4
        elif ent.type == "code":
            assert ent.offset == 13
            assert ent.length == 4
        elif ent.type == "italic":
            assert ent.offset == 44
            assert ent.length == 7
        elif ent.type == "pre":
            assert ent.offset == 52
            assert ent.length == 9
        elif ent.type == "text_link":
            assert ent.offset == 18
            assert ent.length == 6
            assert ent.url == "www.google.com"
        elif ent.type == "mention":
            assert ent.offset == 25
            assert ent.length == 9
        elif ent.type == "hashtag":
            assert ent.offset == 35
            assert ent.length == 8
        elif ent.type == "url":
            assert ent.offset == 62
            assert ent.length == 20
        elif ent.type == "bot_command":
            assert ent.offset == 83
            assert ent.length == 6

    with pytest.raises(BadMarkupException):
        mg.get_message(text="bad *_double_* markdown",
                       parse_mode="Markdown")


@pytest.mark.message
def test_with_html():
    teststr = (
        "we have <b>bold</b> <code>code</code> <a href='www.google.com'>google</a> @username #hashtag "
        "<i>italics</i> <pre>pre block</pre> ftp://snt.utwente.nl /start"
    )
    u = mg.get_message(text=teststr)
    assert u.message.text == teststr

    u = mg.get_message(text=teststr, parse_mode="HTML")
    assert len(u.message.entities) == 9
    for ent in u.message.entities:
        if ent.type == "bold":
            assert ent.offset == 8
            assert ent.length == 4
        elif ent.type == "code":
            assert ent.offset == 13
            assert ent.length == 4
        elif ent.type == "italic":
            assert ent.offset == 44
            assert ent.length == 7
        elif ent.type == "pre":
            assert ent.offset == 52
            assert ent.length == 9
        elif ent.type == "text_link":
            assert ent.offset == 18
            assert ent.length == 6
            assert ent.url == "www.google.com"
        elif ent.type == "mention":
            assert ent.offset == 25
            assert ent.length == 9
        elif ent.type == "hashtag":
            assert ent.offset == 35
            assert ent.length == 8
        elif ent.type == "url":
            assert ent.offset == 62
            assert ent.length == 20
        elif ent.type == "bot_command":
            assert ent.offset == 83
            assert ent.length == 6

    with pytest.raises(BadMarkupException):
        mg.get_message(
            text="bad <b><i>double</i></b> markup", parse_mode="HTML"
        )


@pytest.mark.message
def test_wrong_markup():
    with pytest.raises(BadMarkupException):
        mg.get_message(text="text", parse_mode="htmarkdownl")


mg = MessageGenerator()


@pytest.mark.message
def test_reply():
    u1 = mg.get_message(text="this is the first")
    u2 = mg.get_message(text="This is the second",
                        reply_to_message=u1.message)
    assert u1.message.text == u2.message.reply_to_message.text

    with pytest.raises(BadMessageException):
        u = "This is not a Messages"
        mg.get_message(reply_to_message=u)


# mg = MessageGenerator()
ug = UserGenerator()
cg = ChatGenerator()


@pytest.mark.message
def test_forwarded_message():
    import datetime
    u1 = ug.get_user()
    u2 = ug.get_user()
    c = cg.get_chat(type="group")
    u = mg.get_message(user=u1, chat=c, forward_from=u2,
                       text="This is a test")
    assert u.message.from_user.id == u1.id
    assert u.message.forward_from.id == u2.id
    assert u.message.from_user.id != u.message.forward_from.id
    assert u.message.text == "This is a test"
    assert isinstance(u.message.forward_date, datetime.datetime)
    mg.get_message(forward_from=u2, forward_date=datetime.datetime.now())

    with pytest.raises(BadUserException):
        u3 = "This is not a Usematch="
        u = mg.get_message(
            user=u1, chat=c, forward_from=u3, text="This is a test"
        )


@pytest.mark.message
def test_forwarded_channel_message():
    import datetime

    c = cg.get_chat(type="channel")
    us = ug.get_user()
    u = mg.get_message(
        text="This is a test", forward_from=us, forward_from_chat=c
    )
    assert u.message.chat.id != c.id
    assert u.message.from_user.id != us.id
    assert u.message.forward_from.id == us.id
    assert u.message.text == "This is a test"
    assert isinstance(u.message.forward_from_message_id, int)
    assert isinstance(u.message.forward_date, datetime.datetime)

    u = mg.get_message(text="This is a test", forward_from_chat=c)
    assert u.message.from_user.id != u.message.forward_from.id
    assert isinstance(u.message.forward_from, User)
    assert isinstance(u.message.forward_from_message_id, int)
    assert isinstance(u.message.forward_date, datetime.datetime)

    with pytest.raises(BadChatException):
        c = "Not a Chat"
        u = mg.get_message(text="This is a test", forward_from_chat=c)

    with pytest.raises(BadChatException):
        c = cg.get_chat(type="group")
        u = mg.get_message(text="This is a test", forward_from_chat=c)


@pytest.mark.message
def test_new_chat_members():
    user = ug.get_user()
    chat = cg.get_chat(type="group")
    u = mg.get_message(chat=chat, new_chat_members=[user])
    assert u.message.new_chat_members[0].id == user.id

    with pytest.raises(BadChatException):
        mg.get_message(new_chat_members=[user])
    with pytest.raises(BadUserException):
        mg.get_message(chat=chat, new_chat_members=["usematch="])

@pytest.mark.message
def test_left_chat_member():
    user = ug.get_user()
    chat = cg.get_chat(type="group")
    u = mg.get_message(chat=chat, left_chat_member=user)
    assert u.message.left_chat_member.id == user.id

    with pytest.raises(BadChatException):
        mg.get_message(left_chat_member=user)
    with pytest.raises(BadUserException):
        mg.get_message(chat=chat, left_chat_member="usematch=")

@pytest.mark.message
def test_new_chat_title():
    chat = cg.get_chat(type="group")
    u = mg.get_message(chat=chat, new_chat_title="New title")
    assert u.message.chat.title == "New title"
    assert u.message.chat.title == chat.title

    with pytest.raises(BadChatException):
        mg.get_message(new_chat_title="New title")

@pytest.mark.message
def test_new_chat_photo():
    chat = cg.get_chat(type="group")
    u = mg.get_message(chat=chat, new_chat_photo=True)
    assert isinstance(u.message.new_chat_photo, list)
    assert isinstance(u.message.new_chat_photo[0], PhotoSize)
    photo = [PhotoSize("2", "unid", 1, 1, file_size=3)]
    u = mg.get_message(chat=chat, new_chat_photo=photo)
    assert len(u.message.new_chat_photo) == 1

    with pytest.raises(BadChatException):
        mg.get_message(new_chat_photo=True)

    photo = "foto's!"
    with pytest.raises(BadMessageException):
        mg.get_message(chat=chat, new_chat_photo=photo)
    with pytest.raises(BadMessageException):
        mg.get_message(chat=chat, new_chat_photo=[1, 2, 3])

@pytest.mark.message
def test_pinned_message():
    chat = cg.get_chat(type="supergroup")
    message = mg.get_message(chat=chat, text="this will be pinned").message
    u = mg.get_message(chat=chat, pinned_message=message)
    assert u.message.pinned_message.text == "this will be pinned"

    with pytest.raises(BadChatException):
        mg.get_message(pinned_message=message)
    with pytest.raises(BadMessageException):
        mg.get_message(chat=chat, pinned_message="message")

@pytest.mark.message
def test_multiple_statusmessages():
    with pytest.raises(BadMessageException):
        mg.get_message(
            private=False,
            new_chat_members=ug.get_user(),
            new_chat_title="New title",
        )


@pytest.mark.message
def test_caption_solo():
    with pytest.raises(BadMessageException, match="caption without"):
        mg.get_message(caption="my cap")

@pytest.mark.message
def test_more_than_one():
    with pytest.raises(BadMessageException, match="more than one"):
        mg.get_message(photo=True, video=True)

@pytest.mark.message
def test_location():
    loc = Location(50.012, -32.11)
    u = mg.get_message(location=loc)
    assert loc.longitude == u.message.location.longitude

    u = mg.get_message(location=True)
    assert isinstance(u.message.location, Location)

    with pytest.raises(BadMessageException, match="telegram\.Location"):
        mg.get_message(location="location")

@pytest.mark.message
def test_venue():
    ven = Venue(Location(1.0, 1.0), "some place", "somewhere")
    u = mg.get_message(venue=ven)
    assert u.message.venue.title == ven.title

    u = mg.get_message(venue=True)
    assert isinstance(u.message.venue, Venue)

    with pytest.raises(BadMessageException, match="telegram\.Venue"):
        mg.get_message(venue="Venue")

@pytest.mark.message
def test_contact():
    con = Contact("0612345", "testman")
    u = mg.get_message(contact=con)
    assert con.phone_number == u.message.contact.phone_number

    u = mg.get_message(contact=True)
    assert isinstance(u.message.contact, Contact)

    with pytest.raises(BadMessageException, match="telegram\.Contact"):
        mg.get_message(contact="contact")

@pytest.mark.message
def test_voice():
    voice = Voice("idyouknow", "uuid", 12, 30)
    u = mg.get_message(voice=voice)
    assert voice.file_id == u.message.voice.file_id

    assert voice.duration == u.message.voice.duration

    cap = "voice file"
    u = mg.get_message(voice=voice, caption=cap)
    assert u.message.caption == cap

    u = mg.get_message(voice=True)
    assert isinstance(u.message.voice, Voice)

    with pytest.raises(BadMessageException, match="telegram\.Voice"):
        mg.get_message(voice="voice")

@pytest.mark.message
def test_video():
    video = Video(
        file_id="idyouknow",
        file_unique_id="unid",
        width=200,
        height=200,
        duration=10,
    )
    u = mg.get_message(video=video)
    assert video.file_id == u.message.video.file_id

    assert video.file_unique_id == u.message.video.file_unique_id

    cap = "video file"
    u = mg.get_message(video=video, caption=cap)
    assert u.message.caption == cap

    u = mg.get_message(video=True)
    assert isinstance(u.message.video, Video)

    with pytest.raises(BadMessageException, match="telegram\.Video"):
        mg.get_message(video="video")

@pytest.mark.message
def test_sticker():
    sticker = Sticker("idyouknow", "unid", 30, 30, is_animated=False)
    u = mg.get_message(sticker=sticker)
    assert sticker.file_id == u.message.sticker.file_id

    cap = "sticker file"
    u = mg.get_message(sticker=sticker, caption=cap)
    assert u.message.caption, cap

    u = mg.get_message(sticker=True)
    assert isinstance(u.message.sticker, Sticker)

    with pytest.raises(BadMessageException, match="telegram.Sticker"):
        mg.get_message(sticker="stickematch=")

@pytest.mark.message
def test_document():
    document = Document(
        file_id="idyouknow", file_unique_id="unid", file_name="test.pdf"
    )
    u = mg.get_message(document=document)
    assert document.file_id == u.message.document.file_id

    cap = "document file"
    u = mg.get_message(document=document, caption=cap)
    assert u.message.caption == cap

    u = mg.get_message(document=True)
    assert isinstance(u.message.document, Document)

    with pytest.raises(BadMessageException, match="telegram\.Document"):
        mg.get_message(document="document")

@pytest.mark.message
def test_audio():
    audio = Audio("idyouknow", "unid", 23)
    u = mg.get_message(audio=audio)
    assert audio.file_id == u.message.audio.file_id

    cap = "audio file"
    u = mg.get_message(audio=audio, caption=cap)
    assert u.message.caption == cap

    u = mg.get_message(audio=True)
    assert isinstance(u.message.audio, Audio)

    with pytest.raises(BadMessageException, match="telegram\.Audio"):
        mg.get_message(audio="audio")

@pytest.mark.message
def test_photo():
    photo = [PhotoSize("2", "unid", 1, 1, file_size=3)]
    u = mg.get_message(photo=photo)
    assert photo[0].file_size == u.message.photo[0].file_size

    cap = "photo file"
    u = mg.get_message(photo=photo, caption=cap)
    assert u.message.caption == cap

    u = mg.get_message(photo=True)
    assert isinstance(u.message.photo, list)
    assert isinstance(u.message.photo[0], PhotoSize)

    with pytest.raises(BadMessageException, match="telegram\.Photo"):
        mg.get_message(photo="photo")
    with pytest.raises(BadMessageException, match="telegram\.Photo"):
        mg.get_message(photo=[1, 2, 3])



@pytest.mark.message
def test_edited_message():
    u = mg.get_edited_message()
    assert isinstance(u.edited_message, Message)
    assert isinstance(u, Update)

@pytest.mark.message
def test_with_parameters():
    u = mg.get_edited_message(text="New *text*", parse_mode="Markdown")
    assert u.edited_message.text == "New text"
    assert len(u.edited_message.entities) == 1

@pytest.mark.message
def test_with_message():
    m = mg.get_message(text="first").message
    u = mg.get_edited_message(message=m, text="second")
    assert m.message_id == u.edited_message.message_id
    assert m.chat.id == u.edited_message.chat.id
    assert m.from_user.id == u.edited_message.from_user.id
    assert u.edited_message.text == "second"

    with pytest.raises(BadMessageException):
        mg.get_edited_message(message="Message")



@pytest.mark.message
def test_channel_post():
    u = mg.get_channel_post()
    assert isinstance(u, Update)
    assert isinstance(u.channel_post, Message)
    assert u.channel_post.chat.type == "channel"
    assert u.channel_post.from_user == None

@pytest.mark.message
def test_with_chat():
    cg = ChatGenerator()
    group = cg.get_chat(type="group")
    channel = cg.get_chat(type="channel")
    u = mg.get_channel_post(chat=channel)
    assert channel.title == u.channel_post.chat.title

    with pytest.raises(BadChatException, match="telegram.Chat"):
        mg.get_channel_post(chat="chat")
    with pytest.raises(BadChatException, match="chat.type"):
        mg.get_channel_post(chat=group)


@pytest.mark.message
def test_with_user():
    # ug = UserGenerator()
    user = ug.get_user()
    u = mg.get_channel_post(user=user)
    assert u.channel_post.from_user.id == user.id


@pytest.mark.message
def test_with_content():
    u = mg.get_channel_post(
        text="this is *bold* _italic_", parse_mode="Markdown"
    )
    assert u.channel_post.text == "this is bold italic"
    assert len(u.channel_post.entities) == 2


@pytest.mark.message
def test_edited_channel_post():
    u = mg.get_edited_channel_post()
    assert isinstance(u.edited_channel_post, Message)
    assert isinstance(u, Update)


@pytest.mark.message
def test_with_parameters():
    u = mg.get_edited_channel_post(
        text="New *text*", parse_mode="Markdown")
    assert u.edited_channel_post.text == "New text"
    assert len(u.edited_channel_post.entities) == 1


@pytest.mark.message
def test_with_channel_post():
    m = mg.get_channel_post(text="first").channel_post
    u = mg.get_edited_channel_post(channel_post=m, text="second")
    assert m.message_id == u.edited_channel_post.message_id
    assert m.chat.id == u.edited_channel_post.chat.id
    assert u.edited_channel_post.text == "second"

    with pytest.raises(BadMessageException):
        mg.get_edited_channel_post(channel_post="Message")
