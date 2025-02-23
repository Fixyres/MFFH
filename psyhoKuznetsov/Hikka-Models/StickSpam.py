__version__ = (1, 0, 0)
# meta developer: @psyho_Kuznetsov

from hikkatl.types import Message
from .. import loader, utils
import asyncio

@loader.tds
class StickSpam(loader.Module):
    """🚀 Модуль для спама стикерами"""

    strings = {
        "name": "StickSpam",
        "spam_started": "✈️ <b>Спам стикерами начат!</b>\n🆔 <code>{}</code>",
        "spam_stopped": "🛑 <b>Спам был принудительно остановлен!</b>",
        "invalid_count": "⚠️ <b>Количество должно быть от 1 до 1000!</b>",
        "invalid_interval": "⚠️ <b>Интервал должен быть больше 0!</b>",
        "sticker_id": "🆔 <b>ID стикера:</b> <code>{}</code>",
        "help": "📌 <b>Использование:</b> <code>.stickspam <ID_стикера> <количество> <интервал></code>",
        "error": "❌ <b>Ошибка:</b> <code>{}</code>"
    }

    def __init__(self):
        self.spamming = False

    async def client_ready(self, client, db):
        self._client = client

    @loader.command(ru_doc="🚀 Начать спам стикерами")
    async def stickspam(self, message: Message):
        args = utils.get_args_raw(message).split()

        if len(args) != 3:
            return await utils.answer(message, self.strings["help"])

        try:
            sticker_id, count, interval = args[0], int(args[1]), float(args[2])

            if not 1 <= count <= 1000:
                return await utils.answer(message, self.strings["invalid_count"])

            if interval <= 0:
                return await utils.answer(message, self.strings["invalid_interval"])

            self.spamming = True
            await utils.answer(message, self.strings["spam_started"].format(sticker_id))

            for _ in range(count):
                if not self.spamming:
                    break
                await self._client.send_file(message.chat_id, sticker_id, silent=True)
                await asyncio.sleep(interval)

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
        finally:
            self.spamming = False

    @loader.command(ru_doc="🛑 Остановить спам принудительно")
    async def stopspam(self, message: Message):
        self.spamming = False
        await utils.answer(message, self.strings["spam_stopped"])

    @loader.command(ru_doc="🔍 Получить ID стикера")
    async def idstick(self, message: Message):
        reply = await message.get_reply_message()

        if not reply or not reply.sticker:
            return await utils.answer(message, "❌ <b>Ответьте на стикер!</b>")

        sticker_id = reply.file.id
        await utils.answer(message, self.strings["sticker_id"].format(sticker_id))
