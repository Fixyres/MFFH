from .. import loader, utils
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import time

def register(cb):
    cb(checker())


class checker(loader.Module):
    """Подпишись на канал @modwini"""
    strings = {'name': 'BfgB'}

    async def bcmd(self, message):
        """Показывает сколько у вас денег в @bforgame_bot"""
        chat = "@bforgame_bot"
        text = "б"
        reply = await message.get_reply_message()
        if not text and not reply:
            await message.edit("<b>Нет текста или реплая!</b>")
            return
        await message.edit("<b>💫Подпишись на канал @modwini</b>")
        async with message.client.conversation(chat) as conv:

            if text:
                try:
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1721358063))
                    await message.client.send_message(chat, text)
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>Разблокируй @bforgame_bot!</b>")
                    return
            else:
                try:
                    user = await utils.get_user(reply)
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1721358063))
                    await message.client.send_message(chat, f"{reply.raw_text} (с) {user.first_name}")
                    response = await response
                except YouBlockedUserError:
                    await message.edit("<b>Разблокируй @bforgame_bot!</b>")
                    return
        if response.text:
            await message.client.send_message(message.to_id, f"<b> {response.text} </b> ")
            #await message.client.send_message(message.to_id, f"<b>💫Подпишись на канал @modwini</b> ")
            await message.delete()
        if response.media:
            await message.client.send_file(message.to_id, response.media, reply_to=reply.id if reply else None)
            await message.delete()
