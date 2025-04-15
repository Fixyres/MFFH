__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from .. import loader, utils
import telethon
from telethon.tl.types import Message
import re
import asyncio

@loader.tds
class BFGPromoMonitorMod(loader.Module):
    """Мониторит канал с промо на BFG если находит водить в бота"""

    strings = {
        "name": "BFGPromoMonitor",
        "enabled": "<b>✅ Авто-промо включено!</b>",
        "disabled": "<b>❌ Авто-промо выключено!</b>",
        "status_enabled": "<b>🔵 Статус: Авто-промо активно</b>",
        "status_disabled": "<b>🔴 Статус: Авто-промо неактивно</b>",
        "no_promo": "<b>🤔 Промо не найдено в сообщении</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "MONITOR_CHANNEL", "@bforgame_dev",
            "TARGET_BOT", "@bfgproject",
        )
        self.is_monitoring = False

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.is_monitoring = self.db.get("BFGPromoMonitor", "status", False)

    @loader.command()
    async def promocmd(self, message):
        """Включить/выключить авто-промо"""
        self.is_monitoring = not self.is_monitoring
        self.db.set("BFGPromoMonitor", "status", self.is_monitoring)
        await utils.answer(
            message,
            self.strings["enabled"] if self.is_monitoring else self.strings["disabled"]
        )

    @loader.command()
    async def promoscmd(self, message):
        """Проверить статус авто-промо"""
        status = self.db.get("BFGPromoMonitor", "status", False)
        await utils.answer(
            message,
            self.strings["status_enabled"] if status else self.strings["status_disabled"]
        )

    async def watcher(self, message):
        if not self.is_monitoring:
            return

        if not isinstance(message, Message):
            return

        if message.chat and message.chat.username == self.config["MONITOR_CHANNEL"][1:]:
            text = message.text or ""
            promo_pattern = r"(?i)(Промо|промо)\s*\[([^\]]*)\]"
            match = re.search(promo_pattern, text)

            if match:
                promo_type, promo_content = match.groups()
                promo_message = f"<b>{promo_type}</b> [<code>{promo_content}</code>]"
                try:
                    await self.client.send_message(
                        self.config["TARGET_BOT"], promo_message
                    )
                except Exception as e:
                    await self.client.send_message(
                        "me",
                        f"<b>❌ Ошибка отправки промо в {self.config['TARGET_BOT']}: {str(e)}</b>"
                    )
