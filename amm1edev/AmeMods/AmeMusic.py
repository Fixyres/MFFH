#meta developer: @thisLyomi & @AmekaMods

import asyncio
from telethon import events
from .. import loader, utils

@loader.tds
class LyaMusic(loader.Module):
    """Модуль для поиска музыки, основанный на боте @LyaDownbot"""
    
    strings = {
        "name": "LyaMusic",
        "searching": "<b>🔍 Ищу музыку...</b>",
        "no_results": "<b>❌ Произошла ошибка. Попробуйте указать точное название трека, либо трек невозможно найти.</b>",
        "loading": "<b>⏳ Загрузка трека...</b>",
        "enter_name": "<b>❌ Введите название трека </b>"
    }
    strings_en = {
        "name": "LyaMusic",
        "searching": "<b>🔍 Searching music...</b>",
        "no_results": "<b>❌ Could not find the track, try entering the correct track name or track author.</b>",
        "loading": "<b>⏳ Downloading track...</b>",
        "enter_name": "<b>❌ Enter track name </b>"
    }

    async def searchmcmd(self, message):
        """{Название трека} - Поиск трека."""
        args = "/search " + utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("enter_name"))
            return

        await utils.answer(message, self.strings("searching"))
        
        try:
            async with message.client.conversation("@LyaDownbot") as conv:
                await conv.send_message(args)
                while True:
                    response = await conv.get_response()
                    if "Не удалось найти трек" in response.text:
                        await utils.answer(message, self.strings("no_results"))
                        return
                    
                    if "Загрузка трека" in response.text:
                        await utils.answer(message, self.strings("loading"))

                    if response.media:
                        await message.client.send_file(message.chat_id, response.media)
                        await message.delete()
                        return

                    await asyncio.sleep(1)
                    updated_response = await message.client.get_messages(conv.chat_id, ids=response.id)
                    if updated_response.text != response.text and "Не удалось найти трек" in updated_response.text:
                        await utils.answer(message, self.strings("no_results"))
                        return

        except Exception as e:
            await utils.answer(message, self.strings("no_results"))
