# ---------------------------------------------------------------------------------
# Author: @shiro_hikka
# Name: Channel Imitator
# Description: Imitates someone else's channel in yours
# Commands: imitate
# ---------------------------------------------------------------------------------
#              © Copyright 2025
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# ---------------------------------------------------------------------------------
# scope: hikka_only
# meta developer: @shiro_hikka
# meta banner: https://0x0.st/s/FIR0RnhUN5pZV5CZ6sNFEw/8KBz.jpg
# ---------------------------------------------------------------------------------

__version__ = (1, 1, 0)

from .. import loader, utils
from telethon.tl.functions.messages import EditChatAboutRequest
from telethon.tl.functions.channels import (
    ToggleSignaturesRequest,
    EditPhotoRequest,
    GetFullChannelRequest,
    EditTitleRequest
)
from telethon.tl.types import (
    Message,
    MessageMediaUnsupported,
    MessageMediaPoll,
    Channel,
    Chat,
    User
)
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio
import io

@loader.tds
class ChannelImitator(loader.Module):
    """
    Imitates someone else's channel in yours
    Make assured your channel doesn't include avatars before using otherwise stolen ones will be overlayed with them
    !!!If your account is experiencing a frequent floodwait limitations specify at least 150 in the Cooldown config!!!
    """

    strings = {
        "name": "ChannelImitator",
        "start": "<emoji document_id=5444965061749644170>👨‍💻</emoji> It will take a few minutes.... probably much more",
        "cfg_author": "Specify a text that will appear instead of an absencing real author name",
        "cfg_forwarded": "Specify a text that will will appear instead of an absecing real forwarder name",
        "cfg_cooldown": "Specify a cooldown time between every sending"
    }

    def __init__(self):
        self.me = await self.client.get_me()

        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Your channel",
                None,
                lambda: "Specify your channel ID",
                validator=loader.validators.TelegramID()
            ),
            loader.ConfigValue(
                "Another channel",
                None,
                lambda: "Specify an another channel ID",
                validator=loader.validators.TelegramID()
            ),
            loader.ConfigValue(
                "Author replacer",
                "<i>No author</i>",
                lambda: self.strings["cfg_author"],
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "Forwarded replacer",
                "<i>Unknown</i>",
                lambda: self.strings["cfg_forwarded"],
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "Cooldown",
                60,
                lambda: self.strings["cfg_cooldown"],
                validator=loader.validators.Integer()
            )
        )

    async def checkData(self, iterList, item):
        is_ignore = False
        is_noneCaption = False
        is_fwd = True if item.fwd_from else False
        is_media = True if item.media else False
        media = None
        name = None
        name_id = None
        author = item.post_author if item.post_author else self.config["Author replacer"]

        if is_media and (isinstance(item.media, (MessageMediaUnsupported, MessageMediaPoll)) or hasattr(item.media, "months")):
            is_ignore = True

        try:
            text = item.text
        except:
            text = "§"

        if is_media and text == "":
            is_noneCaption = True
            media = io.BytesIO(await item.download_media(bytes))

        if isinstance(media, MessageMediaUnsupported):
                media = None
            elif is_ignore:
                pass
            elif hasattr(item.media, "photo"):
                media.name = "photo.png"
            else:
                media.name = item.media.document.mime_type.replace("/", ".")

        if is_fwd:
            if item.fwd_from.from_id:
                name_id = item.fwd_from.from_id

                try:
                    entity = await self.client.get_entity(name_id)
                    if isinstance(entity, (Channel, Chat)):
                        name = entity.title

                    elif isinstance(entity, User):
                        if entity.first_name:
                            name = f"{entity.first_name} {entity.last_name if entity.lastname else ''}"
                        else:
                            name = "<i>Deleted</i>"

                except:
                    name = self.config["Forwarded replacer"]
            else:
                name = item.fwd_from.from_name if item.fwd_from.from_name else self.config["Forwarded replacer"]

        _dict = {
            "media": media,
            "text": text,
            "author": author,
            "name": name,
            "id": name_id,
            "is_media": is_media,
            "is_noneCaption": is_noneCaption
        }
        iterList.append(_dict)
        return iterList

    async def imitatecmd(self, message: Message):
        """ [limit: int] [-save] - save all the media and messages from specified channel
        -save - simply save without changing title, bio and/or avatars"""
        args = (utils.get_args_raw(message)).split()
        limit = None
        if args:
            limit = int(args[0]) if args[0].isdigit() else None
            
        yourChannel = self.config["Your channel"]
        anotherChannel = self.config["Another channel"]
        if not all(isinstance(i, Channel) for i in [
            (await self.client.get_entity(yourChannel)),
            (await self.client.get_entity(anotherChannel))
        ]):
            return await utils.answer(message, "Please specify a <i>channel</i> ID")

        initName = self.me.first_name
        iterList = []

        if not "-save" in args:
            _photos = []
            entity = await self.client(GetFullChannelRequest(anotherChannel))
            title = entity.chats[0].title
            bio = entity.full_chat.about

            photos = await self.client.get_profile_photos(anotherChannel)
            if photos:
                for photo in photos:
                    _photos.append(photo)
            _photos = _photos[::-1]

        await utils.answer(message, self.strings["start"])

        try:
            if "-save" in args:
                await self.client(EditChatAboutRequest(yourChannel, bio))
                await self.client(EditTitleRequest(yourChannel, title))
                if _photos:
                    for _photo in _photos:
                        await self.client(EditPhotoRequest(yourChannel, _photo))

            await self.client(ToggleSignaturesRequest(yourChannel, enabled=True))
        except:
            pass

        async for i in self.client.iter_messages(anotherChannel, limit=limit):
            await self.checkData(iterList, item=i)

        iterList = iterList[::-1]
        for i in iterList:
            media = i["media"]
            text = i["text"]
            author = i["author"]
            name = i["name"]
            name_id = i["id"]
            is_media = i["is_media"]
            is_noneCaption = i["is_noneCaption"]

            if not is_media and text == "§":
                continue

            if self.me.first_name != author:
                await self.client(UpdateProfileRequest(first_name=author))

            if is_media and media:
                if is_noneCaption:
                    try:
                        await message.client.send_file(yourChannel, media)
                    except:
                        await message.client.send_message(yourChannel, "<i>Just a poll</i>")

                    try:
                        await message.client.send_message(
                            yourChannel,
                            f"↑ <b>forwarded from <a href='tg://user?id={name_id}'>{name}</a></b>" if name_id else f"<b>forwarded from {name}</b>" if name else ""
                        )
                    except:
                        pass
                else:
                    await message.client.send_file(
                        yourChannel,
                        media,
                        caption="".join((
                            f"<b>forwarded from <a href='tg://user?id={name_id}'>{name}</a>:</b>\n\n" if name_id else f"forwarded from <b>{name}:</b>\n\n" if name else "",
                            text
                        ))
                    )
                await asyncio.sleep(self.config["Cooldown"])
            else:
                await message.client.send_message(
                    yourChannel,
                    "".join((
                        f"<b>forwarded from <a href='tg://user?id={name_id}'>{name}</a>:</b>\n\n" if name_id else f"<b>forwarded from {name}:</b>\n\n" if name else "",
                        text
                    ))
                )
                await asyncio.sleep(self.config["Cooldown"])

        await self.client(UpdateProfileRequest(first_name=initName))
        await utils.answer(message, "<emoji document_id=5275990731813559483>😎</emoji> Done")
