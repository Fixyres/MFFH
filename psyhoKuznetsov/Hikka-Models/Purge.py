__version__ = (1, 0, 1)
# meta developer: @psyhomodules

import logging
import asyncio
from hikkatl.types import Message
from hikkatl.errors import FloodWaitError
from .. import loader, utils

@loader.tds
class TotalPurge(loader.Module):
    """Удаление всех сообщений чата/канала/лс"""
    strings = {"name": "Purge"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        
    @loader.unrestricted
    async def purgecmd(self, message: Message):
        """Удалить ВСЕ сообщения в текущем чате также работает и в каналах просто напиши ету команду"""
        chat = await message.get_chat()
        count = 0
        
        async for msg in self.client.iter_messages(chat):
            try:
                await msg.delete()
                count += 1
                if count % 500 == 0:
                    await message.edit(f"🚮 Удалено: {count}")
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds)
                continue
            except Exception:
                pass

        await message.delete()
        await self.client.send_message(chat, f"✅ Успешно удалено {count} сообщений")
