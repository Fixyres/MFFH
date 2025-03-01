# meta developer: @YA_ManuI

from telethon.tl.types import Message, Channel
import random
from .. import loader, utils

@loader.tds
class QuotePickerMod(loader.Module):
    """Генератор случайных цитат из канала (с настройкой по умолчанию)"""
    strings = {
        "name": "QuotePicker",
        "no_channel": "❌ Канал по умолчанию не задан! Используй .setdefchannel",
        "no_access": "❌ Нет доступа к каналу!",
        "set_ok": "✅ Канал по умолчанию установлен: {}"
    }

    def __init__(self):
        self.default_channel_id = None  # ID канала по умолчанию

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        # Загрузка сохраненного ID при старте
        self.default_channel_id = self.db.get("QuotePicker", "default_channel")

    @loader.command()
    async def rquote(self, message: Message):
        """[username канала] - Получить случайную цитату"""
        args = utils.get_args_raw(message)
        channel_entity = None

        try:
            # Если аргумент передан - используем его, иначе берем по умолчанию
            if args:
                channel_entity = await self.client.get_entity(args)
            else:
                if not self.default_channel_id:
                    return await utils.answer(message, self.strings("no_channel"))
                channel_entity = await self.client.get_entity(self.default_channel_id)

            if not isinstance(channel_entity, Channel):
                return await utils.answer(message, "❌ Это не канал!")

            messages = await self.client.get_messages(channel_entity, limit=2000)
            text_messages = [m for m in messages if m.text]

            if not text_messages:
                return await utils.answer(message, "📭 Нет текстовых сообщений")

            quote = random.choice(text_messages)
            result = f"📖 Случайная цитата из {channel_entity.title}:\n\n{quote.text}"
            await utils.answer(message, result)

        except ValueError:
            await utils.answer(message, "❌ Канал не найден!")
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {str(e)}")

    @loader.command()
    async def setdefchannel(self, message: Message):
        """<username/id канала> - Установить канал по умолчанию"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, "❌ Укажите канал!")

        try:
            channel = await self.client.get_entity(args)
            if not isinstance(channel, Channel):
                return await utils.answer(message, "❌ Это не канал!")

            self.default_channel_id = channel.id
            self.db.set("QuotePicker", "default_channel", channel.id)
            await utils.answer(message, self.strings("set_ok").format(channel.title))

        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {str(e)}")