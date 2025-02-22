# meta developer: @Enceth
#да нету тут вирусов
import random
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class Gresti(loader.Module):
    """Дает возможность грести эти гребаные деньги лопатой"""

    strings = {
        "name": "Gresti",
        "enabled": "Начинаем грести эти гребаные деньги лопатой",
        "disabled": "Нот бизнес.",
        "invalid_prob": "Укажите вероятность от 0 до 100",
        "prob_set": "Вероятность установлена на {prob}%",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.enabled_chats = {}
        self.reply_probability = 10

    @loader.command()
    async def gresti(self, message: Message):
        """Включить/выключить модуль в чате."""
        chat_id = message.chat_id
        if chat_id in self.enabled_chats:
            self.enabled_chats.pop(chat_id, None)
            await utils.answer(message, self.strings["disabled"])
        else:
            self.enabled_chats[chat_id] = True
            await utils.answer(message, self.strings["enabled"])

    @loader.command()
    async def grest(self, message: Message):
        """Установить вероятность ответа (от 0 до 100)."""
        args = utils.get_args_raw(message)
        if args.isdigit() and 0 <= int(args) <= 100:
            self.reply_probability = int(args)
            await utils.answer(message, self.strings["prob_set"].format(prob=self.reply_probability))
        else:
            await utils.answer(message, self.strings["invalid_prob"])

    async def watcher(self, message: Message):
        chat_id = message.chat_id
        if chat_id not in self.enabled_chats:
            return
        if message.sender_id == (await self.client.get_me()).id:
            return
        if random.randint(1, 100) > self.reply_probability:
            return
        text = message.raw_text.split()
        if len(text) < 2:
            return
        start = random.randint(1, len(text) - 1)
        end = min(start + random.choice([1, 2]), len(text))
        target_phrase = " ".join(text[start:end])
        response = f'А теперь замени слово "{target_phrase}" на "грести эти гребаные деньги лопатой".'
        await message.reply(response)
