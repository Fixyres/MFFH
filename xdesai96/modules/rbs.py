# meta developer: @xdesai

import asyncio
from .. import loader, utils
from telethon import types, functions


@loader.tds
class RBSMod(loader.Module):
    strings = {
        "name": "ReactByStatus",
        "no_reply": "<b>No reply.</b>",
        "no_user": "<b>Failed to get user info.</b>",
        "no_premium": "<b>No premium.</b>",
        "reacted": "<b>Reaction added.</b>",
    }
    strings_ru = {
        "no_reply": "<b>Нет реплая.</b>",
        "no_user": "<b>Не удалось получить информацию о пользователе.</b>",
        "no_premium": "<b>Нет премиума.</b>",
        "reacted": "<b>Реакция добавлена.</b>",
    }

    async def rbscmd(self, message):
        """<reply> | React by status"""
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return
        user = await utils.get_user(reply)
        if not user:
            await utils.answer(message, self.strings["no_user"])
            return
        if not user.premium or not (await self._client.get_me()).premium:
            await utils.answer(message, self.strings["no_premium"])
            return
        await self._client(
            functions.messages.SendReactionRequest(
                peer=message.chat_id,
                msg_id=reply.id,
                reaction=[
                    types.ReactionCustomEmoji(document_id=user.emoji_status.document_id)
                ],
            )
        )
        await utils.answer(message, self.strings["reacted"])
        await asyncio.sleep(2)
        await message.delete()
