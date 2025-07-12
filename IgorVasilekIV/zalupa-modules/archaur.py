"""
Some description:
Search pkgs on https://aur.archlinux.org (i dont know why)
"""

__version__ = (1, 2)

# meta banner: https://files.catbox.moe/u91fwo.jpg
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

from .. import loader, utils
import aiohttp
import logging

logger = logging.getLogger(__name__)

@loader.tds
class ArchAURMod(loader.Module):
    """Поиск aur пакетов в aur.archlinux.org"""
    
    strings = {"name": "ArchAUR"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "pkgs",
                10,
                lambda: "Количество пакетов для отображения",
                validator=loader.validators.Integer(minimum=1, maximum=35)
            )
        )
        
    async def client_ready(self, client, db):
        self._client = client

    @loader.unrestricted
    async def aurcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5210956306952758910>👀</emoji> Укажите запрос для поиска в AUR\nПример: <code>.aur neofetch</code>")
            return

        url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={args}"

        pkgs = self.config["pkgs"] # da
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await utils.answer(message, f"⚠️ Ошибка доступа к AUR (код {response.status})")
                        return
                    
                    data = await response.json()
                    
            if data["resultcount"] == 0:
                await utils.answer(message, f"<emoji document_id=5210956306952758910>👀</emoji> По запросу <code>{args}</code> ничего не найдено")
                return
                
            packages = data["results"][:pkgs]
            response_text = f"<emoji document_id=5397674675796985688>🔍</emoji> Результаты поиска в AUR для <code>{args}</code>:\n\n"
            
            for pkg in packages:
                pkg_url = f"https://aur.archlinux.org/packages/{pkg['Name']}"
                response_text += (
                    f"<blockquote expandable><emoji document_id=5433653135799228968>📦</emoji> <b><a href='{pkg_url}'>{pkg['Name']}</a></b> ({pkg['Version']})\n"
                    f"└ {pkg.get('Description', 'Без описания')}\n\n"
                )
            
            if data["resultcount"] > 0:
                response_text += f"</blockquote><emoji document_id=5210956306952758910>👀</emoji> Показано {self.config['pkgs']} из {data['resultcount']} результатов"

        except aiohttp.ClientError:
            await utils.answer(message, "⚠️ Ошибка сети при подключении к AUR")
        except Exception as e:
            logger.exception("AUR search error")
            await utils.answer(message, f"🚫 Критическая ошибка: {str(e)}")

        await utils.answer(message, response_text)
