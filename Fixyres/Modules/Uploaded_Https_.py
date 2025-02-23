__version__ = (7, 7, 7)  # meta developer: @Yaukais, @Shadow_red1

import asyncio
from telethon.tl.types import Message
from telethon import events
from .. import loader, utils
from telethon import functions, types
from ..inline.types import InlineCall
from telethon.tl.types import ChatAdminRights

class Uploder_httpsMod(loader.Module):
    """Загрузшик https сылок на акаунты!"""
    strings = {"name": "Uploder_https"}

    @loader.command("up_https")
    async def up_httpscmd(self, message: Message):
        """Загружает пользователя и генерирует https ссылку на его аккаунт."""
        
        args = message.text.split()
        
        if len(args) < 2:
            await message.edit("❌ Пожалуйста, укажите пользователя.")
            return
        
        user = args[1]
        await message.edit("🚀 Загрузка...")

        try:
            # Получаем информацию о пользователе
            user_obj = await self.client.get_entity(user)
            username = user_obj.username
            
            if username:
                link = f"https://t.me/{username}"
                await message.edit(f"🎡 Файл загружен!\n\n<code>{link}</code>")
            else:
                await message.edit("❌ У пользователя нет юзернейма.")
        except Exception as e:
            await message.edit(f"❌ Ошибка: {str(e)}")