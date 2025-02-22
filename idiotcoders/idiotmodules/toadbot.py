# meta pic: https://static.whypodg.me/mods!toadbot.png
# meta banner: https://mods.whypodg.me/badges/toadbot.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10


import asyncio
from .. import loader, utils
from telethon.tl.types import Message 


@loader.tds
class ToadBotMod(loader.Module):
    """Модуль для ухода за вашей жабой, когда вам лень или же когда у вас нет на это времени
    """
    """
    Module for @toadbot, use it, when you have no time to take care of your frog or you are lazy
    """

    strings = {
        "name": "ToadBot",
        "jobs": "Choose a job where your toad will work.",
        "eats": "Enable toad auto-feeding?"
    }

    strings = {
        "name": "ToadBot",
        "_cls_doc": "Модуль для @toadbot, используйте его, когда у вас нет времени, чтобы ухаживать за жабой или вам лень",
        "jobs": "Выберите работу на которую будет ходить ваша жаба.",
        "eats": "Включить авто кормёжку жабы?"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "jobs",
                "Поход в столовую",
                lambda: self.strings("jobs"),
                validator=loader.validators.Choice(["Поход в столовую", "Работа грабитель", "Работа крупье"]),
                ))        
    @loader.command()
    async def frogcmd(self, message):
        """Уход за жабой | чтобы остановить пиши 'Уход за жабой стоп'"""
        if message.is_private:
            await utils.answer(message, "❌| <b>Команда не может быть запущена в личных сообщениях.</b>")
            return

        elif self.get("job") is None or self.get("job") is False:
            self.set("job", True)   
            await utils.answer(message, "✅| <b>Авто-уход за жабой был успешно запущен.</b>")

            job = self.config["jobs"]
            if job == "Поход в столовую":
                while self.get("job"):
                    await message.respond("Поход в столовую")
                    await asyncio.sleep(7200)
                    await message.respond("Забрать жабу с работы")
                    await asyncio.sleep(21600)
                return
            elif job == "Работа грабитель":
                while self.get("job"):
                    await message.respond("Работа грабитель")
                    await asyncio.sleep(7200)
                    await message.respond("Забрать жабу с работы")
                    await asyncio.sleep(21600)
                return
            elif job == "Работа крупье":
                while self.get("job"):
                    await message.respond("Работа крупье")
                    await asyncio.sleep(7200)
                    await message.respond("Забрать жабу с работы")
                    await asyncio.sleep(21600)
                return

    @loader.command()
    async def eatcmd(self, message):
        """Кормёжка жабы | чтобы остановить используйте 'корм стоп'"""
        if message.is_private:
            await utils.answer(message, "❌| <b>Команда не может быть запущена в личных сообщениях.</b>")
            return

        elif self.get("eat") is None or self.get("eat") is True:
            self.set("eat", False)
            await utils.answer(message, "<b>Авто-кормежка была успешно остановлена.</b>")
            return
        elif self.get("eat") is None or self.get("eat") is False:
            self.set("eat", True)
            await utils.answer(message, "✅| <b>Авто-кормежка жабы запущена.</b>")

            eat = self.get("eat")
            if eat == True:
                while self.get("eat"):
                    await message.respond("Покормить жабу")
                    await asyncio.sleep(0.5)
                    await message.respond("Жаба успешно покормлена.\n\nСледующая команда будет произведена через 12 часов.")
                    await asyncio.sleep(43200)
                
    @loader.watcher()
    async def watcher(self, message):
        if not getattr(message, "out", False):
            return
        if message.out:
            if message.raw_text.lower() == "корм стоп":
                self.set("eat", False)
                await utils.answer(message, "✅| <b>Авто кормёжка жабы успешно остановлена.</b>")
            elif message.raw_text.lower() == "уход за жабой стоп":
                self.set("job", False)
                await utils.answer(message, "✅| <b>Авто уход за жабой успешно остановлен.</b>")
