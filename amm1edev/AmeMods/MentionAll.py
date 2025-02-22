#meta developer: @thisLyomi & @AmekaMods

from telethon import types
from .. import loader, utils

@loader.tds
class MentionAllMod(loader.Module):
    """Модуль для упоминания всех пользователей в чате."""
    strings = {"name": "MentionAll"}

    async def allcmd(self, message):
        """<text> - Для упоминания всех участников чата"""
        args = utils.get_args_raw(message)
        chat = await message.get_chat()

        if not isinstance(chat, (types.Chat, types.Channel)):
            await message.edit("<b>Команда доступна только в группах и супергруппах!</b>")
            return

        await message.edit("<b>Собираю список участников...</b>")
        participants = await message.client.get_participants(chat)

        mentions = []
        for user in participants:
            if user.bot:
                continue
            mentions.append(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>")

        if not mentions:
            await message.edit("<b>Не удалось найти участников для упоминания!</b>")
            return

        text = args + "\n\n" if args else ""
        text += "<tg-spoiler>" + " ".join(mentions) + "</tg-spoiler>"

        await message.respond(text, parse_mode="HTML")
        await message.delete()
