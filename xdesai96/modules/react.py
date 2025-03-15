# meta developer: @xdesai

import asyncio
from .. import loader, utils
from telethon import types, functions

@loader.tds
class ReactMod(loader.Module):
    strings = {"name": "React",
               "no_reply": "<b>No reply.</b>",
               "no_user": "<b>Failed to get user info.</b>",
               "no_premium": "<b>No premium.</b>",
               "reacted": "<b>Reaction added.</b>"}
    strings_ru = {"no_reply": "<b>Нет реплая.</b>",
                  "no_user": "<b>Не удалось получить информацию о пользователе.</b>",
                  "no_premium": "<b>Нет премиума.</b>",
                  "reacted": "<b>Реакция добавлена.</b>"}
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "love",
                "❤",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "like",
                "👍",
                validator=loader.validators.String(),
            )
        )

    async def likecmd(self, message):
        """<reply> | React like"""
        reply = await message.get_reply_message()
        me = await self.client.get_me()
        if not reply:
            return await utils.answer(message, self.strings("no_reply", message))
        if self.config['like'].isdigit() and me.premium:
            await self._client(functions.messages.SendReactionRequest(peer=message.chat_id, msg_id=reply.id, reaction=[types.ReactionCustomEmoji(document_id=int(self.config['like']))]))
        elif self.config['like'].isdigit() and not me.premium:
            await utils.answer(message, self.strings("no_premium", message))
        else:
            await self._client(functions.messages.SendReactionRequest(peer=message.chat_id, msg_id=reply.id, reaction=[types.ReactionEmoji(emoticon=self.config['like'])]))
        await asyncio.sleep(1)
        await message.delete()

    async def lovecmd(self, message):
        """<reply> | React love"""
        reply = await message.get_reply_message()
        me = await self.client.get_me()
        if not reply:
            return await utils.answer(message, self.strings("no_reply", message))
        if self.config['love'].isdigit() and me.premium:
            await self._client(functions.messages.SendReactionRequest(peer=message.chat_id, msg_id=reply.id, reaction=[types.ReactionCustomEmoji(document_id=int(self.config['love']))]))
        elif self.config['love'].isdigit() and not me.premium:
            await utils.answer(message, self.strings("no_premium", message))
        else:
            await self._client(functions.messages.SendReactionRequest(peer=message.chat_id, msg_id=reply.id, reaction=[types.ReactionEmoji(emoticon=self.config['love'])]))
        await asyncio.sleep(1)
        await message.delete()