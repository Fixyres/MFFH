from .. import loader, utils
from telethon.types import Message, MessageService
import asyncio

import logging

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    ControlSpam
    📜 Licensed under the GNU AGPLv3	
"""

# meta desc: desc
# meta developer: @BruhHikkaModules


logger = logging.getLogger(__name__)

@loader.tds
class ControlSpam(loader.Module):
    """Не просто спамь, а контролируй"""

    strings = {"name": "ControlSpam", "hello": "Hello world!"}
    strings_ru = {"hello": "Привет мир!"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                True,
                lambda: "Просто статус спама",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "ids",
                [],
                lambda: "Список айди сообщений",
                validator=loader.validators.Series()
            )
        )


    async def client_ready(self, client, db):
        self._common = await self.import_lib(
            "https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/libaries/common.py",
            suspend_on_error=True
        )
        self.client = client

    @loader.command()
    async def spam(self, message: Message):
        """[количество спама] [текст / реплай]  - Начать спам"""
        args = utils.get_args_raw(message).split(maxsplit=1)  # Разделяем на количество и текст
        reply = await message.get_reply_message()
        text = "Something went wrong"
        topic_id = None

        spam_id = len(self.config["ids"])
        new_spam_id = spam_id + 1

        self.config["ids"].append(
            {
                "data": {
                    "id": new_spam_id,
                    "message": text,
                    "count": 0,
                    "status": True
                }
            }
        )

        try:
            count = int(args[0]) if args else 0  # Количество сообщений
            if reply:
                text = reply.text
                topic_id = await self._common._topic_resolver(message)
            elif len(args) > 1:
                text = args[1]  # Берем текст после количества
            else:
                await message.edit("Укажите текст или сделайте реплай")
                return
        except (ValueError, IndexError):
            await message.edit("Укажите корректное количество и текст")
            return
        
        sent = 0

        self.config["ids"][spam_id]["data"]["text"] = text

        await utils.answer(message, f"Я начал спамить с сообщением айди: {new_spam_id}")
        
        while sent < count:
            self.config["ids"][spam_id]["data"]["count"] += 1
            status = self.config["ids"][spam_id]["data"]["status"]
            text = self.config["ids"][spam_id]["data"]["text"]
            if topic_id:
                await self.client.send_message(message.chat_id, text, reply_to=topic_id)
            else:
                await self.client.send_message(message.chat_id, text)
            if status is False:
                break
            sent += 1

        

    @loader.command()
    async def delayspam(self, message: Message):
        """[количество спама] [Задержка в секундах] [текст / реплай]  - Начать спам"""
        args = utils.get_args_raw(message).split(maxsplit=2)  # Разделяем на количество и текст
        reply = await message.get_reply_message()
        text = "Something went wrong"
        topic_id = None

        spam_id = len(self.config["ids"])
        new_spam_id = spam_id

        self.config["ids"].append(
            {
                "data": {
                    "id": new_spam_id,
                    "message": text,
                    "count": 0,
                    "status": True
                }
            }
        )

        try:
            count = int(args[0]) if args else 0  # Количество сообщений
            if reply:
                text = reply.text
                topic_id = await self._common._topic_resolver(message)
            elif len(args) > 1:
                text = args[2]  # Берем текст после количества
            else:
                await message.edit("Укажите текст или сделайте реплай")
                return
        except (ValueError, IndexError):
            await message.edit("Укажите корректное количество и текст")
            return
        
        sent = 0

        self.config["ids"][spam_id]["data"]["text"] = text

        await utils.answer(message, f"Я начал спамить с сообщением айди: {new_spam_id}")
        
        while sent < count:
            self.config["ids"][spam_id]["data"]["count"] += 1
            status = self.config["ids"][spam_id]["data"]["status"]
            text = self.config["ids"][spam_id]["data"]["text"]
            await asyncio.sleep(int(args[1]))
            if topic_id:
                await self.client.send_message(message.chat_id, text, reply_to=topic_id)
            else:
                await self.client.send_message(message.chat_id, text)
            if status is False:
                break
            sent += 1

    @loader.command()
    async def spam_stop(self, message: Message):
        """- [id] Закончить спам"""
        args = utils.get_args_raw(message)
        self.config["ids"][int(args)-1]["data"]["status"] = False
        await utils.answer(message, "Я закончил спамить")
