#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: CHmodsList
# Description: Список каналов с модулями (идея: @codrago)
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/chmodslist.png?raw=true
# ---------------------------------------------------------------------------------

import asyncio 
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CHmodsList(loader.Module):
    """Список каналов с модулями (идея: @codrago)"""

    strings = {
        "name": "CHmodsList",

        "opening_config": "<b><emoji document_id=5327902038720257153>🔄</emoji> Открываю настройки...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "header_text",
                "<emoji document_id=5188377234380954537>🌘</emoji> Список каналов с модулями",
                lambda: "Заголовок текста с каналами модулей",
            ),
            loader.ConfigValue(
                "channels",
                [
            "<emoji document_id=5370547013815376328>😶‍🌫️</emoji> @hikarimods",
            "<emoji document_id=5373141891321699086>😎</emoji> @famods",
            "<emoji document_id=5445096582238181549>🦋</emoji> @morisummermods",
            "<emoji document_id=5449380056201697322>💚</emoji> @nalinormods",
            "<emoji document_id=5373026167722876724>🤩</emoji> @AstroModules",
            "<emoji document_id=5366217837104872614>⭐️</emoji> @shadow_modules",
            "<emoji document_id=5249042457731024510>💪</emoji> @vsecoder_m",
            "<emoji document_id=5371037748188683677>☺️</emoji> @mm_mods",
            "<emoji document_id=5370856741086960948>😈</emoji> @apodiktum_modules",
            "<emoji document_id=5370947515220761242>😇</emoji> @wilsonmods",
            "<emoji document_id=5467406098367521267>👑</emoji> @DorotoroMods",
            "<emoji document_id=5469986291380657759>✌️</emoji> @HikkaFTGmods",
            "<emoji document_id=5413703918947413540>🐈‍⬛</emoji> @nercymods",
            "<emoji document_id=5472091323571903308>🎈</emoji> @hikka_mods",
            "<emoji document_id=5298799263013151249>😐</emoji> @sqlmerr_m",
            "<emoji document_id=5296274178725396201>🥰</emoji> @AuroraModules",
            "<emoji document_id=5429400349377051725>😄</emoji> @BHikkaMods",
            "<emoji document_id=5355149418620272518>🌟</emoji> @BchModules",
                ],
                lambda: "Список каналов с модулями",
                validator=loader.validators.Series()
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def chsettings(self, message):
        """Изменить список каналов с модулями"""

        await utils.answer(message, self.strings['opening_config'])

        await self.invoke("config", "chmodslist", message.peer_id)

        await message.delete()

    @loader.command()
    async def chmods(self, message):
        """Посмотреть список каналов с модулями"""

        await utils.answer(message, "<b>{}</b>\n\n<b>{}</b>".format(self.config['header_text'], '\n'.join(self.config['channels'])))