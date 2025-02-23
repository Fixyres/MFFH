__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

import aiohttp
import logging
from hikkatl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ScriptSearchMod(loader.Module):
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

    async def format_script_info(self, script: dict) -> str:
        title = script.get("title", "Без названия")
        game = script.get("game", {}).get("name", "Неизвестная игра")
        script_code = script.get("script", "⚠️ <b>СКРИПТ НЕДОСТУПЕН</b>")[:1000]  

        info = (
            f"📝 <b>{title}</b>\n"
            f"🎮 <code>{game}</code>\n\n"
            f"<b>📜 СКРИПТ:</b>\n<code>{script_code}</code>\n"
        )

        return info

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
                    data = await response.json()

                scripts = data.get("result", {}).get("scripts", [])
                
                if not scripts:
                    await utils.answer(message, self.strings["no_results"].format(query))
                    return

                results = []
                for script in scripts[:self.config["MAX_RESULTS"]]:
                    formatted_info = await self.format_script_info(script)
                    results.append(formatted_info)

                response_text = self.strings["results"].format(query, "\n\n".join(results))
                
                await utils.answer(message, response_text)

        except Exception as e:
            logger.exception(e)
            await utils.answer(message, self.strings["error"].format(str(e)))