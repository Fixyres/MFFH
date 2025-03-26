# meta developer: @xdesai

import asyncio
from .. import loader, utils
from telethon import errors

@loader.tds
class AccstatMod(loader.Module):
    """Gets information about user from funstat.\nBefore using unblock @Accstat_bot"""
    strings = {
        "name": "Accstat",
        "no_user": "<blockquote>❌ <b>User not specified</b></blockquote>",
        "error": "<blockquote><b>Error:</b> {err}</blockquote>",
        "timeout": "<blockquote>⏲ <b>Bot did not answer ...</b></blockquote>"
    }

    strings_ru = {
        "name": "Accstat",
        "no_user": "<blockquote>❌ <b>Пользователь не указан</b></blockquote>",
        "error": "<blockquote><b>Ошибка:</b> {err}</blockquote>",
        "timeout": "<blockquote>⏲ <b>Бот не ответил ...</b></blockquote>"
    }

    _bot = "@Accstat_bot"

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
    
    @loader.command(
        ru_doc="<user> | Получить информацию."
    )
    async def fstat(self, message):
        """<user> | Get info."""
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        if not reply:
            if not args:
                return await utils.answer(message, self.strings("no_user"))
            else:
                if args[0].isdigit():
                    user_id = int(args[0])
                    await utils.answer(message, f"⏳ Вычисляю...[id{user_id}]")
                    async with self._client.conversation(self._bot) as conv:
                        await conv.send_message(f"{user_id}")
                        try:
                            r = await conv.get_edit(timeout=4)
                            return await utils.answer(message, r.message)
                        except asyncio.exceptions.TimeoutError:
                            r = await conv.get_reply()
                            try:
                                return await utils.answer(message, r.message)
                            except errors.rpcerrorlist.MessageEmptyError:
                                return await utils.answer(message, self.strings("timeout"))
                else:
                    try:
                        user_id = (await self.client.get_entity(args[0])).id
                        await utils.answer(message, f"⏳ Вычисляю...[id{user_id}]")
                        async with self._client.conversation(self._bot) as conv:
                            await conv.send_message(f"{user_id}")
                            try:
                                r = await conv.get_edit(timeout=4)
                                return await utils.answer(message, r.message)
                            except asyncio.exceptions.TimeoutError:
                                r = await conv.get_reply()
                                try:
                                    return await utils.answer(message, r.message)
                                except errors.rpcerrorlist.MessageEmptyError:
                                    return await utils.answer(message, self.strings("timeout"))
                    except Exception as e:
                        return utils.answer(message, self.strings('error').format(err=e))
        else:
            user_id = reply.sender_id
            await utils.answer(message, f"⏳ Вычисляю...[id{user_id}]")
            async with self._client.conversation(self._bot) as conv:
                await conv.send_message(f"{user_id}")
                try:
                    r = await conv.get_edit(timeout=4)
                    return await utils.answer(message, r.message)
                except asyncio.exceptions.TimeoutError:
                    r = await conv.get_reply()
                    try:
                        return await utils.answer(message, r.message)
                    except errors.rpcerrorlist.MessageEmptyError:
                        return await utils.answer(message, self.strings("timeout"))
