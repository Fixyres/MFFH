#meta developer: @thisLyomi & @AmekaMods

# Если тебе код смотреть не лень, то и на тгк подпишись

from .. import loader, utils

@loader.tds
class AmeAutoReplyMod(loader.Module):
    """Модуль автоответчик."""
    
    strings = {
        "name": "AmeAutoReply",
        "module_enabled": "<emoji document_id=5264971795647184318>✅</emoji> <b>Автоответчик включен.</b>",
        "module_disabled": "<emoji document_id=5262642849630926308>❌</emoji> <b>Автоответчик выключен.</b>",
        "reset": "<emoji document_id=5345794417208861153>🔄</emoji> <b>Список пользователей с сработавшим автоответчиком сброшен.</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "reply_message", "Привет! Это автоответчик. Я свяжусь с вами позже.", 
            "Сообщение для автоответчика."
        )
        self.is_active = True
        self.replied_users = set()

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.replied_users = set(self.db.get("AutoReply", "replied_users", []))
        self.is_active = self.db.get("AutoReply", "is_active", True)

    async def watcher(self, message):
        if not self.is_active:
            return
        if not message.is_private or message.out or message.sender_id in self.replied_users:
            return
        await message.reply(self.config["reply_message"])
        self.replied_users.add(message.sender_id)
        self.db.set("AutoReply", "replied_users", list(self.replied_users))

    async def enablecmd(self, message):
        """Включить автоответчик."""
        self.is_active = True
        self.db.set("AutoReply", "is_active", True)
        await message.edit(self.strings["module_enabled"])

    async def disablecmd(self, message):
        """Выключить автоответчик."""
        self.is_active = False
        self.db.set("AutoReply", "is_active", False)
        await message.edit(self.strings["module_disabled"])

    async def resetcmd(self, message):
        """Сбросить список пользователей с сработавшим автоответчиком."""
        self.replied_users.clear()
        self.db.set("AutoReply", "replied_users", [])
        await message.edit(self.strings["reset"])
