__version__ = (1, 0, 1)
# meta developer: @psyhomodules

from .. import loader, utils
import asyncio
from telethon import functions, types

@loader.tds
class NetStatusM(loader.Module):
    """🌐 Модуль для 24/7 статуса 'в сети'"""
    
    strings = {
        "name": "NetStatus",
        "on": "✅ <b>Статус 'постоянно в сети' включён!</b>",
        "off": "❌ <b>Статус 'постоянно в сети' выключён!</b>",
        "already_on": "⚠️ <i>Статус уже включён.</i>",
        "already_off": "⚠️ <i>Статус уже выключён.</i>",
        "running": "🔄 <b>Поддерживаю статус 'в сети'...</b>",
        "status": "📊 <b>Статус 'постоянно в сети':</b> {}"
    }

    strings_ru = {
        "name": "NetStatus",
        "on": "✅ <b>Статус 'постоянно в сети' включён!</b>",
        "off": "❌ <b>Статус 'постоянно в сети' выключён!</b>",
        "already_on": "⚠️ <i>Статус уже включён.</i>",
        "already_off": "⚠️ <i>Статус уже выключён.</i>",
        "running": "🔄 <b>Поддерживаю статус 'в сети'...</b>",
        "status": "📊 <b>Статус 'постоянно в сети':</b> {}",
        "_cmd_doc_neton": "🟢 Включить статус 'постоянно в сети'",
        "_cmd_doc_netoff": "🔴 Выключить статус 'постоянно в сети'",
        "_cmd_doc_netstatus": "ℹ️ Проверить текущее состояние статуса",
        "_cls_doc": "🌐 Управляет статусом 'в сети' в Telegram"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._db_name = "NetStatusMod"
        self.is_running = self.get("is_running", False)
        self._task = None
        
        if self.is_running:
            asyncio.ensure_future(self._keep_online())

    def get(self, key, default=None):
        return self.db.get(self._db_name, key, default)
    
    def set(self, key, value):
        self.db.set(self._db_name, key, value)
  

    async def netoncmd(self, message):
        """🟢 Включить статус 'постоянно в сети'"""
        if self.is_running:
            return await utils.answer(message, self.strings["already_on"])
        
        self.is_running = True
        self.set("is_running", True)
        
        try:
            await self.client(functions.account.UpdateStatusRequest(offline=False))
            asyncio.ensure_future(self._keep_online())
            return await utils.answer(message, self.strings["on"])
        except Exception as e:
            self.is_running = False
            self.set("is_running", False)
            return await utils.answer(message, f"❌ <b>Ошибка:</b> <code>{e}</code>")

    async def netoffcmd(self, message):
        """🔴 Выключить статус 'постоянно в сети'"""
        if not self.is_running:
            return await utils.answer(message, self.strings["already_off"])
        
        self.is_running = False
        self.set("is_running", False)
        
        try:
            if self._task and not self._task.done():
                self._task.cancel()
                
            await self.client(functions.account.UpdateStatusRequest(offline=True))
            return await utils.answer(message, self.strings["off"])
        except Exception as e:
            return await utils.answer(message, f"❌ <b>Ошибка:</b> <code>{e}</code>")

    async def netstatuscmd(self, message):
        """ℹ️ Проверить текущее состояние статуса"""
        status = "🟢 Включен" if self.is_running else "🔴 Выключен"
        await utils.answer(message, self.strings["status"].format(status))

    async def _keep_online(self):
        self._task = asyncio.current_task()
        
        try:
            while self.is_running:
                try:
                    await self.client(functions.account.UpdateStatusRequest(offline=False))
                except Exception as e:
                    pass
                
                await asyncio.sleep(5)  
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.is_running = False
            self.set("is_running", False)
