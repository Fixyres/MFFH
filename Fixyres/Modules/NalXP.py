import asyncio
import time
from telethon import functions, types
from .. import loader, utils

class Farm:
    async def _pay_taxes(self):
        async with self._client.conversation(self._bot) as conv:
            await asyncio.sleep(3)
            await conv.send_message('моя ферма')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(1)  # Предполагается, что кнопка оплаты налогов на позиции 1
            await asyncio.sleep(3)
            await conv.send_message('мой бизнес')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(1)  # Предполагается, что кнопка оплаты налогов на позиции 1
            await asyncio.sleep(3)
            await conv.send_message('мой генератор')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(1)  # Предполагается, что кнопка оплаты налогов на позиции 1
            await asyncio.sleep(3)
            await conv.send_message('мое дерево')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(1)  # Предполагается, что кнопка оплаты налогов на позиции 1
            await asyncio.sleep(3)
            await conv.send_message('мой карьер')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(1)  # Предполагается, что кнопка оплаты налогов на позиции 1
            await asyncio.sleep(3)
            await conv.send_message('мой сад')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(1)  # Предполагается, что кнопка оплаты налогов на позиции 1

    async def _water_garden(self):
        async with self._client.conversation(self._bot) as conv:
            await asyncio.sleep(3)
            await conv.send_message('мой сад')
            r = await conv.get_response()
            await asyncio.sleep(3)
            await r.click(3)  # Предполагается, что кнопка полива на позиции 4 (индекс 3)

class NalXPMod(loader.Module, Farm):
    """
    модуль созданный для плати налогов и полив сада. творец - @nik_xp
    """

    strings = {"name": "NalXP"}

    _bot = "@bfgproject"     
    
    def __init__(self):        
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "AutoTree",
                True,
                "Автоматически собирать и оплачивать налоги.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "AutoWater",
                False,
                "Автоматически поливать сад.",
                validator=loader.validators.Boolean(),
            ),
        )            
     
    @loader.loop(interval=1, autostart=True)
    async def main_loop(self):
        if self.config["AutoTree"] and (not self.get("Tree_time") or (time.time() - self.get("Tree_time")) >= 3600):
            await self._pay_taxes()
            self.set("Tree_time", int(time.time()))

        if self.config["AutoWater"] and (not self.get("Water_time") or (time.time() - self.get("Water_time")) >= 3600):
            await self._water_garden()
            self.set("Water_time", int(time.time()))
            
        await self._client(functions.messages.ReadMentionsRequest(self._bot))

    @loader.command()
    async def nal(self, message):
        """Начать автоматическую оплату налогов и полив сада."""
        self.config["AutoTree"] = True
        self.config["AutoWater"] = True
        self.main_loop.start()  # Запуск цикла
        await message.reply("Автоматическая оплата налогов и полив сада включены.")
        
    @loader.command()
    async def nalstop(self, message):
        """Остановить автоматическую оплату налогов и полив сада."""
        self.config["AutoTree"] = False
        self.config["AutoWater"] = False
        self.main_loop.stop()  # Остановка цикла
        await message.reply("Автоматическая оплата налогов и полив сада остановлены.")