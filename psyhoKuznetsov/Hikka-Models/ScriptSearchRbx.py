__version__ = (1, 0, 1)
# meta developer: @psyhomodules

import aiohttp
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class ScriptSearch(loader.Module):
    """Поиск скриптов для Roblox"""

    strings = {
        "name": "ScriptSearchRbx",
        "loading": "🔍 <b>Ищем скрипты для Roblox...</b>",
        "no_query": "❌ <b>Введите НАЗВАНИЕ ИГРЫ</b>",
        "no_results": "❌ <b>Нет скриптов для</b> <code>{}</code>",
        "error": "❌ <b>Ошибка:</b> <code>{}</code>",
        "results": "🎮 <b>РЕЗУЛЬТАТЫ ДЛЯ</b> <code>{}</code>:\n\n{}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "MAX_RESULTS", 5,
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
            
    
    async def format_script_info(self, script: dict) -> str:
        title = script.get("title", "Без названия")
        game = script.get("game", {}).get("name", "Неизвестная игра")
        script_code = script.get("script", "⚠️ <b>СКРИПТ НЕДОСТУПЕН</b>")[:1000]

        return (
            f"📝 <b>{title}</b>\n"
            f"🎮 <code>{game}</code>\n\n"
            f"<b>📜 СКРИПТ:</b>\n<code>{script_code}</code>\n"
        )

    @loader.command()
    async def search(self, message: Message):
        """Поиск скриптов для Roblox"""
        query = utils.get_args_raw(message)
        if not query:
            await utils.answer(message, self.strings["no_query"])
            return

        await utils.answer(message, self.strings["loading"])

        try:
            async with aiohttp.ClientSession() as session:
                url = f"https://scriptblox.com/api/script/search?q={query}&page=1"
                async with session.get(url) as response:
                    if response.status != 200:
                        await utils.answer(message, self.strings["error"].format("Ошибка сервера"))
                        return
                    data = await response.json()

                scripts = data.get("result", {}).get("scripts", [])
                if not scripts:
                    await utils.answer(message, self.strings["no_results"].format(query))
                    return

                results = []
                for script in scripts[:self.config["MAX_RESULTS"]]:
                    results.append(await self.format_script_info(script))

                response_text = self.strings["results"].format(query, "\n\n".join(results))
                await utils.answer(message, response_text)

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
