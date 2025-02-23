# meta developer: @ScreamDev
# Попросил сделать: @Carunocat
# Переписанный модуль @Foxy437

from .. import loader, utils

@loader.tds
class BoldMod(loader.Module):
    """Модуль для авто замены ПОТУЖНО на жирный только если сообщение содержит 'потужно'. Переписанный модуль @Foxy437"""
    strings = {"name": "PotuznoBold"}
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.db.set(self.strings["name"], "bold_enabled", False)

    async def on_boldcmd(self, message):
        """Включить авто замену ПОТУЖНО на жирный."""
        self.db.set(self.strings["name"], "bold_enabled", True)
        await utils.answer(message, "Авто замена включена!")

    async def off_boldcmd(self, message):
        """Выключить авто замену ПОТУЖНО на жирный."""
        self.db.set(self.strings["name"], "bold_enabled", False)
        await utils.answer(message, "Авто замена выключена!")

    async def watcher(self, message):
        if self.db.get(self.strings["name"], "bold_enabled") and "потужно" in message.text.lower():
            if message.out:
                bold_text = f"<b>{message.text}</b>"
                await message.edit(bold_text)
