#meta developer: @Daniel1236n & @thisLyomi & @AmekaMods
#----------------------------------------------------------------------------
from .. import loader, utils
from telethon import events

@loader.tds
class hzMod(loader.Module):
    """Модуль для ответа на сообщения 'хз' в определенном чате."""
    strings = {"name": "xzmodule"}

    
    async def client_ready(self, client, db):
        self.client = client

    @loader.command(
        ru_doc = "Вкл/Выкл модуль в этом чате"
    ) 
    async def xzcmd(self, message):
        """On/Off mod in current chat"""
        chat_id = message.chat_id
        if not message.chat_id:
            await message.edit("Эта команда должна быть использована в чате.")
            return

        active_chats = self.db.get(self.strings["name"], "active_chats", [])

        if chat_id in active_chats:
            active_chats.remove(chat_id)
            self.db.set(self.strings["name"], "active_chats", active_chats)
            await message.edit(f"Автоответ в чате {chat_id} отключен.")
        else:
            active_chats.append(chat_id)
            self.db.set(self.strings["name"], "active_chats", active_chats)
            await message.edit(f"Автоответ в чате {chat_id} активирован.")

    @loader.unrestricted
    async def watcher(self, message):
        """Следит за сообщениями и отвечает 'хз'"""
        chat_id = message.chat_id
        active_chats = self.db.get(self.strings["name"], "active_chats", [])

        if chat_id in active_chats and not message.out:
            await message.reply("хз")
