#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: FAmod
# Description: Управление вещами, связанными с @FAmods_Bot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/famod.png?raw=true
# ---------------------------------------------------------------------------------

import re
import shlex
import hikkatl
import aiohttp
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Famod(loader.Module):
    """Управление вещами, связанными с @FAmods_Bot"""

    strings = {
        "name": "Famod",

        "no_q": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно <code>{}{} [запрос]</code></b>",

        "searching_module": "<emoji document_id=5334904192622403796>🔄</emoji> <b>Поиск модуля...</b>",
        "getting_stats": "<emoji document_id=5328302454226298081>🔄</emoji> <b>Получение статистики...</b>",

        "no_found": "<emoji document_id=5440381017384822513>❌</emoji> <b>Не нашёл такой модуль</b>",
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def _install(self, call, text, url_name):
        link = f"https://raw.githubusercontent.com/FajoX1/FAmods/main/{url_name}.py"
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as response:
                code = await response.text()

        requires_comments = re.findall(r'#\s*requires:\s*(.*)', code)
        all_requires = ''.join(requires_comments).strip()

        if all_requires:
            requirements_list = shlex.split(all_requires)
            process = await asyncio.create_subprocess_exec('pip', 'install', *requirements_list)
            await process.wait()

        loader_m = self.lookup("loader")

        await loader_m.download_and_install(link, None)

        await call.edit(
            text,
            reply_markup={
                "text": (
                    "✅ Установлен"
                ),
                "data": "empty",
            }
        )

    async def _get_stats(self):
     while True:
      try:
        async with self._client.conversation("@FAmods_Bot") as conv:
            msg = await conv.send_message("/stats")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            text = r.text
            text = text.replace("📊", "<emoji document_id=5431577498364158238>📊</emoji>")
            text = text.replace("💻", "<emoji document_id=5431376038628171216>💻</emoji>")
            text = text.replace("🧑‍💻", "<emoji document_id=5190458330719461749>🧑‍💻</emoji>")
            return text
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    @loader.command()
    async def fmstats(self, message):
        """Просмотр статистики"""

        await utils.answer(message, self.strings['getting_stats'])

        stats = await self._get_stats()

        await utils.answer(message, stats)

    @loader.command()
    async def fmsearch(self, message):
        """Поиск модуля"""
        
        query = utils.get_args_raw(message)

        if not query:
            return await utils.answer(message, self.strings['no_q'].format(self.get_prefix(), 'fmsearch'))

        await utils.answer(message, self.strings['searching_module'])
        
        try:
            q = await self._client.inline_query("@FAmods_Bot", query)
            result = q.result.results[0]
            
            text = result.send_message.message
            
            url_name = str(result.send_message.reply_markup.rows[0].buttons[0].data).split(":")[1]

        except (IndexError, AttributeError):
            return await utils.answer(message, self.strings['no_found'])
        
        module_name = text.split(' ')[2]

        text = text.replace(text.split('\n')[0], '<b>' + text.split('\n')[0] + '</b>')
        text = text.replace("(source)", f"(<a href='https://raw.githubusercontent.com/FajoX1/FAmods/main/{url_name}.py'>source</a>)")
        text = text.replace(text.split('\n')[1], '<i>' + text.split('\n')[1] + '</i>')
        text = text.replace(module_name, '<code>' + module_name + '</code>')
        
        keyboard = [
            [
                {
                    "text": "⬇️ Установить",
                    "callback": self._install,
                    "args": (text, url_name),
                }
            ],
        ]
        
        await self.inline.form(
            text=text,
            message=message,
            reply_markup=keyboard,
            force_me=True,
        )

    @loader.inline_handler(thumb_url="https://cdn-0.emojis.wiki/emoji-pics/apple/magnifying-glass-tilted-right-apple.png")
    async def famods(self, query):
        """Поиск модулей"""

        if not query.args:
            return [
                {
                    "title": "Поиск модулей",
                    "description": "Введите запрос для поиска модулей",
                    "message": "🔎 Введи запрос к поиску",
                    "thumb": "https://cdn-0.emojis.wiki/emoji-pics/apple/magnifying-glass-tilted-right-apple.png",
                }
            ]

        q = await self._client.inline_query("@FAmods_Bot", query.args)
        mods = q.result.results

        modules = []

        for mod in mods:
            text = mod.send_message.message
            
            url_name = str(mod.send_message.reply_markup.rows[0].buttons[0].data).split(":")[1]
        
            module_name = text.split(' ')[2]
            module_description = text.split('ℹ️')[1].strip()

            text = text.replace(text.split('\n')[0], '<b>' + text.split('\n')[0] + '</b>')
            text = text.replace("(source)", f"(<a href='https://raw.githubusercontent.com/FajoX1/FAmods/main/{url_name}.py'>source</a>)")
            text = text.replace(text.split('\n')[1], '<i>' + text.split('\n')[1] + '</i>')
            text = text.replace(module_name, '<code>' + module_name + '</code>')

            modules.append({
                "name": module_name,
                "description": module_description,
                "url_name": url_name,
                "text": text,
            })

        return [
            {
                "title": module['name'],
                "description": module['description'],
                "message": self.inline.sanitise_text(
                    module['text']
                ),
                "thumb": "https://cdn-0.emojis.wiki/emoji-pics/apple/laptop-apple.png",
                "reply_markup": {
                    "text": "⬇️ Установить",
                    "callback": self._install,
                    "args": (module['text'], module['url_name']),
                }
            }
            for module in modules
        ]
