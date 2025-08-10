# meta developer: @wifitldev

import random
import asyncio
from .. import loader, utils

@loader.tds
class UserChecker(loader.Module):
    """Поиск 5 свободных юзернеймов через Telegram API"""

    strings = {
        "name": "UserChecker",
        "searching": "🔍 Ищу 5 свободных юзернеймов...",
        "found": "🎉 Найдены свободные юзернеймы:\n\n{}",
        "not_found": "😕 Не удалось найти 5 свободных юзернеймов за 100 попыток",
        "error": "⚠️ Ошибка: {}",
    }

    async def generate_username(self):
        """Генерация случайного юзернейма (5 букв)"""
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))

    async def check_username(self, username):
        """Проверка через client.get_entity()"""
        try:
            await self.client.get_entity(username)
            return False  
        except ValueError:
            return True   
        except Exception:
            return False  

    @loader.command(
        ru_doc="Найти 5 свободных юзернеймов",
        en_doc="Find 5 available usernames"
    )
    async def uccmd(self, message):
        """Поиск свободных юзернеймов через Telegram API"""
        await utils.answer(message, self.strings["searching"])
        
        try:
            usernames = []
            attempts = 0
            max_attempts = 100
            
            while len(usernames) < 5 and attempts < max_attempts:
                username = await self.generate_username()
                if await self.check_username(username):
                    usernames.append(f"• @{username} - t.me/{username}")
                attempts += 1
                await asyncio.sleep(0.3)  

            if usernames:
                result = self.strings["found"].format("\n".join(usernames[:5]))  # Берем первые 5
            else:
                result = self.strings["not_found"]
                
            await utils.answer(message, result)
                
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
