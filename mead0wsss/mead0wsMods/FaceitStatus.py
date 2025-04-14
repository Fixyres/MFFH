__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods
# meta banner: https://x0.at/tYLF.png

import requests
from .. import loader, utils
from aiohttp import ClientSession
import logging

@loader.tds
class FaceitStatus(loader.Module):
    """Модуль для установки статуса в зависимости от уровня FACEIT CS 2"""
    strings = {"name": "FaceitStatus"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "nickname",
                "",
                lambda: "Никнейм Faceit для получения информации",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "enabled",
                False,
                lambda: "Включить или выключить обновление статуса.",
                validator=loader.validators.Boolean()
            )
        )

        self.faceit_level_emojis = {
            1: 5472218969999941969,
            2: 5472420816282983721,
            3: 5474655053975396078,
            4: 5474457803307359926,
            5: 5474321889067276806,
            6: 5471974427447009199,
            7: 5474505554753756989,
            8: 5474586712455782018,
            9: 5474493773658462333,
            10: 5474608393450691188,
        }

    async def client_ready(self):
        if self.config["enabled"]:
            self.update_status_loop.start()

    @loader.loop(interval=60)
    async def update_status_loop(self):
        await self.update_status()

    async def update_status(self):
        nickname = self.config["nickname"]
        if not nickname:
            return

        async with ClientSession() as session:
            async with session.get(f"https://api.faceit.com/users/v1/nicknames/{nickname}") as response:
                if response.status == 200:
                    payload = await response.json()
                    faceit_lvl = payload.get("payload", {}).get("games", {}).get("cs2", {}).get("skill_level")

                    if faceit_lvl in self.faceit_level_emojis:
                        emoji_id = self.faceit_level_emojis[faceit_lvl]
                        await self._client.set_status(emoji_id)
                else:
                    logging.error("Ошибка при запросе к FACEIT API: %s", response.status)

    @loader.command()
    async def on_faccmd(self, event):
        """Включить обновление статуса."""
        self.config["enabled"] = True
        await self.update_status()
        self.update_status_loop.start()
        await event.edit("✅ Обновление статуса включено.")

    @loader.command()
    async def off_faccmd(self, event):
        """Выключить обновление статуса."""
        self.config["enabled"] = False
        self.update_status_loop.stop()
        await event.edit("❌ Обновление статуса выключено.")

