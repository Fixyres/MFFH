# meta developer: @wifitldev
# requires: requests

import random
import requests
import asyncio
from .. import loader, utils

@loader.tds
class UsernameChecker(loader.Module):
    """Поиск свободных юзернеймов в Telegram, не всегда точный"""

    strings = {
        "name": "UseChecker",
        "searching": "🔍 Ищу 5 свободных юзернеймов...",
        "found": "🎉 5 свободных юзернеймов:\n\n{}",
        "not_found": "😕 Не удалось найти 5 свободных юзернеймов за 50 попыток",
        "error": "⚠️ Ошибка: {}",
    }

    async def generate_username(self):
        """Генерация случайного юзернейма (5 букв)"""
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))

    async def check_username(self, username):
        """Проверка доступности юзернейма"""
        url = f"https://t.me/{username}"
        try:
            r = requests.get(url, timeout=5)
            return "If you have <strong>Telegram</strong>" in r.text
        except:
            return False

    @loader.command(
        ru_doc="Найти 5 свободных юзернеймов",
        en_doc="Find 5 available usernames"
    )
    async def uccmd(self, message):
        """Найти ровно 5 свободных юзернеймов"""
        await utils.answer(message, self.strings["searching"])
        
        try:
            usernames = []
            attempts = 0
            max_attempts = 100  # Максимум 100 попыток
            
            while len(usernames) < 5 and attempts < max_attempts:
                username = await self.generate_username()
                if await self.check_username(username):
                    usernames.append(f"• @{username} - t.me/{username}")
                attempts += 1
                await asyncio.sleep(0.5)  # Антифлуд

            if len(usernames) == 5:
                result = self.strings["found"].format("\n".join(usernames))
            else:
                result = self.strings["not_found"]
                
            await utils.answer(message, result)
                
        except Exception as e:
            error_msg = self.strings["error"].format(str(e))
            await utils.answer(message, error_msg)
