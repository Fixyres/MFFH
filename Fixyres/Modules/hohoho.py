from telethon.tl.types import Message
from .. import loader, utils
import re

class hohoho(loader.Module):
    """
    был huhuhu стал hohoho
    """

    strings = {"name": "hohoho"}
    _bot = "@bfgproject"

    def __init__(self):
        self.client = None

    @loader.command()
    async def профф(self, message: Message):
        """- проверить профиль игрока через реплей, ID или username"""
        args = utils.get_args(message)
        if not args:
            if message.is_reply:
                reply = await message.get_reply_message()
                user_id = reply.sender_id
            else:
                await message.reply("Пожалуйста, укажите ид.")
                return
        else:
            user = args[0]
            if user.isdigit():
                user_id = int(user)
            else:
                try:
                    user = await self.client.get_entity(user)
                    user_id = user.id
                except Exception as e:
                    await message.reply(f"Не удалось получить ответа от бота.")
                    return

        async with message.client.conversation(self._bot) as conv:
            try:
                await conv.send_message(f"/get_profile {user_id}")
                r = await self._safe_get_response(conv)
                if r:
                    await r.forward_to(message.to_id)
            except Exception as e:
                await message.reply(f"Ошибка при общении с ботом: {str(e)}")

    async def _safe_get_response(self, conv, timeout=10):
        try:
            response = await conv.get_response(timeout=timeout)
            return response
        except asyncio.TimeoutError:
            return None

    def extract_bfg_id(self, text):
        match = re.search(r'ID человека в боте - (\d+)', text)
        return match.group(1) if match else None