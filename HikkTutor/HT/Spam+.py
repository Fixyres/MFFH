__version__ = (1, 0, 3)

#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: Spam+

from .. import loader, utils
import random
import asyncio
from telethon.tl.types import Message

@loader.tds
class SpamPlusMod(loader.Module):
    """Модуль для спама"""

    strings = {"name": "Spam+"}

    emojis = [
        '😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉',
        '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😜', '🤪', '😝', '🤑',
        '🤗', '🤭', '🤫', '🤔', '🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬',
        '🤥', '😌', '😔', '😪', '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮', '🤧', '🥵',
        '🥶', '😵', '🤯', '🤠', '🥳', '😎', '🤓', '🧐', '😕', '😟', '🙁', '☹️', '😮',
        '😯', '😲', '😳', '🥺', '😦', '😧', '😨', '😰', '😥', '😢', '😭', '😱', '😖',
        '😣', '😞', '😓', '😩', '😫', '🥱', '😤', '😡', '😠', '🤬'
    ]

    def __init__(self):
        self.spam_active = False

    async def sicmd(self, message: Message):
        """Справка по модулю"""
        info = (
            "✨ <b>Модуль Spam+ - возможности:</b> 🌟\n\n"
            "<b>📋 Использование:</b>\n"
            "<code>.spam &lt;количество&gt; &lt;задержка&gt; &lt;аргумент&gt;</code>\n\n"
            "<b>📌 Пример:</b>\n"
            "<code>.spam 3 1 emojis</code> - отправляет 3 эмодзи с задержкой 1 секунда между каждым.\n"
            "<code>.spam 3 1 line</code> - отправляет 3 случайные строки из ответа или сообщения.\n\n"
            "<b>🔢 Доступные аргументы:</b>\n"
            "<code>emojis</code> - спам рандомными эмодзи.\n"
            "<code>[1-?]</code> - спам рандомными числами в указанном диапазоне.\n"
            "<code>usernames</code> - спам юзернеймами пользователей чата.\n"
            "<code>randomwords</code> - спам рандомными словами из текста.\n"
            "<code>increment</code> - спам с увеличением числа.\n"
            "<code>decrement</code> - спам с уменьшением числа.\n"
            "<code>line</code> - спам рандомной строкой из ответа или сообщения.\n\n"
            "<b>Автор не рекомендует использовать этот модуль и не несет ответственности за последствия.</b>"
        )
        await message.respond(info, parse_mode='html')

    async def spamcmd(self, message: Message):
        """Запуск спама"""
        if self.spam_active:
            await message.respond("🔄 Спам уже активен. Используйте <code>.stop</code> для остановки.", parse_mode='html')
            return

        args = utils.get_args_raw(message)
        if not args:
            await message.respond("❗ Пожалуйста, укажите параметры для спама.")
            return

        parts = args.split()
        if len(parts) < 2:
            await message.respond("⚠️ Неверные параметры. Используйте <code>.si</code> для справки.", parse_mode='html')
            return

        count = int(parts[0])
        delay = 0.3
        index = 1

        if index < len(parts) and self.is_float(parts[index]):
            delay = max(float(parts[index]), 0.3)
            index += 1

        content = " ".join(parts[index:])

        modes = ["[", "emojis", "usernames", "randomwords", "increment", "decrement", "line"]
        active_modes = [mode for mode in modes if mode in content]

        if len(active_modes) > 1:
            await message.respond("❌ Пожалуйста, используйте только один режим за раз.", parse_mode='html')
            return

        self.spam_active = True
        asyncio.create_task(self.run_spam(message, count, delay, content))

    def is_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    async def run_spam(self, message: Message, count: int, delay: float, content: str):
        try:
            if content.startswith("[") and "-" in content and content.endswith("]"):
                range_parts = content[1:-1].split("-")
                min_value, max_value = int(range_parts[0]), int(range_parts[1])
                await self.spam_random_numbers(message, count, delay, min_value, max_value)
            elif content.lower() == "emojis":
                await self.spam_random_emojis(message, count, delay)
            elif content.lower() == "usernames":
                await self.spam_usernames(message, count, delay)
            elif content.startswith("randomwords"):
                text = " ".join(content.split()[1:])
                await self.spam_random_words(message, count, delay, text)
            elif content.startswith("increment"):
                start_number = int(content.split()[1])
                await self.spam_increment(message, count, delay, start_number)
            elif content.startswith("decrement"):
                start_number = int(content.split()[1])
                await self.spam_decrement(message, count, delay, start_number)
            elif content.lower() == "line":
                await self.spam_random_line(message, count, delay)
            else:
                await self.spam_text(message, count, delay, content)
        finally:
            self.spam_active = False

    async def stopcmd(self, message: Message):
        """Остановка спама"""
        if not self.spam_active:
            await message.respond("⛔ Я чёт спама не вижу.", parse_mode='html')
        else:
            self.spam_active = False
            await message.respond("🛑 Спам остановлен.", parse_mode='html')

    async def spam_text(self, message: Message, count: int, delay: float, content: str):
        for _ in range(count):
            if not self.spam_active:
                break
            await message.respond(content)
            await asyncio.sleep(delay)

    async def spam_random_numbers(self, message: Message, count: int, delay: float, min_value: int, max_value: int):
        for _ in range(count):
            if not self.spam_active:
                break
            number = random.randint(min_value, max_value)
            await message.respond(str(number))
            await asyncio.sleep(delay)

    async def spam_random_emojis(self, message: Message, count: int, delay: float):
        for _ in range(count):
            if not self.spam_active:
                break
            emoji = random.choice(self.emojis)
            await message.respond(emoji)
            await asyncio.sleep(delay)

    async def spam_usernames(self, message: Message, count: int, delay: float):
        participants = await message.client.get_participants(message.to_id)
        usernames = [p.username for p in participants if p.username]

        if not usernames:
            await message.respond("❌ Нет доступных юзернеймов для спама.")
            return

        for _ in range(count):
            if not self.spam_active:
                break
            username = random.choice(usernames)
            await message.respond(f"@{username}")
            await asyncio.sleep(delay)

    async def spam_random_words(self, message: Message, count: int, delay: float, text: str):
        words = text.split()
        for _ in range(count):
            if not self.spam_active:
                break
            word = random.choice(words)
            await message.respond(word)
            await asyncio.sleep(delay)

    async def spam_increment(self, message: Message, count: int, delay: float, start_number: int):
        for i in range(count):
            if not self.spam_active:
                break
            await message.respond(str(start_number + i))
            await asyncio.sleep(delay)

    async def spam_decrement(self, message: Message, count: int, delay: float, start_number: int):
        for i in range(count):
            if not self.spam_active:
                break
            await message.respond(str(start_number - i))
            await asyncio.sleep(delay)

    async def spam_random_line(self, message: Message, count: int, delay: float):
        reply = await message.get_reply_message()
        if reply:
            lines = reply.text.split('\n')
        else:
            lines = message.text.split('\n')[1:]

        if not lines:
            await message.respond("❌ Нет доступных строк для спама.")
            return

        for _ in range(count):
            if not self.spam_active:
                break
            line = random.choice(lines)
            await message.respond(line)
            await asyncio.sleep(delay)