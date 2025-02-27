# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


import base64
import io

import requests
import telethon
from telethon.tl.types import *

from .. import loader, utils  # type: ignore


@loader.tds
class FDQuoteMod(loader.Module):
    strings = {
        "name": "FDQuote",
        "processing": "<b>[FDQ]</b> Processing...",
        "processing_api": "<b>[FDQ]</b> </code>API Processing...</code>",
        "photo": "Фото{}",
        "video": "Видео{}",
        "audio": "Аудио{}",
        "gif": "GIF{}",
        "voice": "Голосовое сообщение{}",
        "videonote": "Видеосообщение",
        "poll": "Опрос",
        "quiz": "Викторина",
        "sticker": "{}Стикер",
        "file": "Файл {}",
        "api_error": "<b>[FDQ]</b> API Error: <code>{}</code>",
        "error": "<b>[FDQ]</b> Err...",
        "deleted_acc": "Удалённый аккаунт",
        "need_reply": "<b>[FDQ]</b> Reply to message...",
    }

    def __init__(self):
        self.name = self.strings["name"]
        self.api_url = "https://api.d4n13l3k00.ru/quotes/generate"
        self.debug = False

    @loader.owner
    async def fdqcmd(self, m: Message):
        ".fdq <реплай на юзера и текст> или <@username и текст> или <реплай и @username> или <реплай> - Создать квотес"
        message = await m.get_reply_message()
        args = m.text.split(maxsplit=2)
        args.pop(0)
        catch_reply = reply = viabot = pic = None
        if message:
            if args:
                if args[0].startswith("@"):
                    user_id = args[0][1:]
                    text = message.text
                else:
                    user_id = message.from_id or message.fwd_from.channel_id
                    text = " ".join(args)
            else:
                user_id = message.from_id or message.fwd_from.channel_id
                text = message.text
                catch_reply = True
        elif len(args) == 2 and args[0].startswith("@"):
            user_id = args[0][1:]
            text = args[1]
        else:
            return await utils.answer(m, self.strings["need_reply"])
        try:
            user = await m.client.get_entity(user_id)
        except ValueError:
            return await utils.answer(m, self.strings["error"])
        await utils.answer(m, self.strings["processing"])
        name = (
            telethon.utils.get_display_name(user)
            if type(user) == Channel
            else (
                self.strings["deleted_acc"]
                if user and user.deleted
                else telethon.utils.get_display_name(user)
            )
        )
        id = user.id
        avatar = await m.client.download_profile_photo(user, bytes)
        reply = await message.get_reply_message()
        ### / Message / ###
        if message.file and "image" in message.file.mime_type:
            pic = await message.download_media(bytes)
        elif message.video or message.gif:
            pic = await message.download_media(bytes, thumb=-1)
        if message.via_bot_id:
            viabot = str((await m.client.get_entity(message.via_bot_id)).username)
        ### / Reply / ###
        if reply and catch_reply:
            r = await m.client.get_entity(reply.from_id or reply.fwd_from.channel_id)
            if reply.photo:
                replText = self.strings["photo"].format(
                    f", {reply.raw_text}" if reply.raw_text else ""
                )
            elif reply.gif:
                replText = self.strings["gif"].format(
                    f", {reply.raw_text}" if reply.raw_text else ""
                )
            elif reply.video:
                if reply.video.attributes[0].round_message:
                    replText = self.strings["videonote"]
                else:
                    replText = self.strings["video"].format(
                        f", {reply.raw_text}" if reply.raw_text else ""
                    )
            elif reply.audio:
                replText = self.strings["audio"].format(
                    f", {reply.raw_text}" if reply.raw_text else ""
                )
            elif reply.voice:
                replText = self.strings["voice"].format(
                    f", {reply.raw_text}" if reply.raw_text else ""
                )
            elif reply.poll:
                replText = (
                    self.strings["quiz"]
                    if reply.media.poll.quiz
                    else self.strings["poll"]
                )
            elif reply.sticker:
                replText = self.strings["sticker"].format(
                    reply.sticker.attributes[1].alt + " "
                )
            elif reply.file:
                replText = self.strings["file"].format(
                    f", {reply.raw_text}" if reply.caption else ""
                )
            elif reply.raw_text:
                replText = reply.raw_text or ""
            reply = {
                "name": telethon.utils.get_display_name(r)
                if type(r) == Channel
                else (
                    self.strings["deleted_acc"]
                    if r and r.deleted
                    else telethon.utils.get_display_name(r)
                ),
                "text": replText,
            }
        else:
            reply = None
        await utils.answer(m, self.strings["processing_api"])
        js = {
            "avatar": base64.b64encode(avatar).decode() if avatar else None,
            "name": name,
            "text": text,
            "id": id,
            "pic": base64.b64encode(pic).decode() if pic else None,
            "reply": reply,
            "viabot": viabot,
        }
        if self.debug:
            f = io.BytesIO(str(js).encode("utf-8"))
            f.name = "request.debug"
            await m.respond(file=f)
        r = requests.post(self.api_url, json=js)
        if r.status_code == 200:
            quote = io.BytesIO(r.content)
            quote.name = "q.webp"
            if message:
                await message.reply(file=quote)
            else:
                await m.respond(file=quote)
            await m.delete()
        else:
            await utils.answer(m, self.strings["api_error"].format(r.json()["err"]))
