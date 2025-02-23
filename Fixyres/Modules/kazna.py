import asyncio

from telethon.types import Message

from .. import loader, utils


class BuyMod(loader.Module):
    """Модуль для пополнения казны"""    
    strings = {
        "name": "kazna"
    
    }
    async def client_ready(self, client, db) -> None:
        if hasattr(self, "hikka"):
            return
        self.db = db
        self.client = client

    async def kazcmd(self, msg: Message):
        """Пример ввода: .kaz 1e19"""
        try:
            args = utils.get_args(msg)
            if not args:
                self.db.set(self.strings["name"], "kazna", False)
                return await utils.answer(msg, "<emoji document_id=5276032951342088188>💥</emoji><b>Пополнение казны остановлено</b>")
            if len(args) != 1:
                return await utils.answer(msg, "<emoji document_id=5276032951342088188>💥</emoji><b>Хуета</b>")
            await utils.answer(msg, f"<emoji document_id=5224607267797606837>☄️</emoji><b>Пополнение казны запущено. Время сна {self.config['sleepTime']} (минут), пополнение по {args[0]}</b>")
            self.db.set(self.strings["name"], "kazna", True)
            while self.db.get(self.strings["name"], "kazna"):
                await self._client.send_message(--1002116157217, f"Клан казна {args[0]}")
                await asyncio.sleep(60*int(self.config["sleepTime"]))
        except Exception as e:
            await utils.answer(msg, (e))

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "sleepTime",
                30,
                "Время сна (в минутах)",
                validator=loader.validators.Integer(),
            ),
        )