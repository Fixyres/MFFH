# чатгпт кормит, больные мозги тоже
#
# meta banner: https://files.catbox.moe/u91fwo.jpg (a gde femboy set 😔)
# meta developer: @HikkaZPM
#
# The module is made as a joke, all coincidences are random :P
# 
#       кот вахуи
#       /\_____/\
#      /  o   o  \
#     ( ==  ^  == )
#      )         (
#     (           )
#    ( (  )   (  ) )
#   (__(__)___(__)__)
# 
# 
#

from .. import loader, utils
import aiohttp
import logging

logger = logging.getLogger(__name__)

@loader.tds
class AurSearchMod(loader.Module):
    """Модуль для поиска пакетов в AUR (Arch User Repository)"""
    strings = {"name": "AURSearch"}

    async def client_ready(self, client, db):
        self._client = client

    @loader.unrestricted
    async def aurcmd(self, message):
        """Поиск пакетов в AUR. Использование: .aur <запрос>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите запрос для поиска в AUR\nПример: <code>.aur neofetch</code>")
            return

        url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={args}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await utils.answer(message, f"⚠️ Ошибка доступа к AUR (код {response.status})")
                        return
                    
                    data = await response.json()
                    
            if data["resultcount"] == 0:
                await utils.answer(message, f"🔍 По запросу <code>{args}</code> ничего не найдено")
                return
                
            packages = data["results"][:8]
            response_text = f"🔍 Результаты поиска в AUR для <code>{args}</code>:\n\n"
            
            for pkg in packages:
                pkg_url = f"https://aur.archlinux.org/packages/{pkg['Name']}"
                response_text += (
                    f"<blockquote expandable>📦 <b><a href='{pkg_url}'>{pkg['Name']}</a></b> ({pkg['Version']})\n"
                    f"└ {pkg.get('Description', 'Без описания')}\n\n"
                )
            
            if data["resultcount"] > 5:
                response_text += f"</blockquote>ℹ️ Показано 5 из {data['resultcount']} результатов"

        except aiohttp.ClientError:
            await utils.answer(message, "⚠️ Ошибка сети при подключении к AUR")
        except Exception as e:
            logger.exception("AUR search error")
            await utils.answer(message, f"🚫 Критическая ошибка: {str(e)}")

        await utils.answer(message, response_text)
