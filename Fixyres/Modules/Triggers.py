"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""


# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_triggers.png?raw=true
# meta developer: @sqlmerr_m
# requires: cachetools

import uuid
import asyncio
import logging
import json

from .. import loader, utils
from hikkatl.tl.types import Message

from cachetools import TTLCache


@loader.tds
class Triggers(loader.Module):
    """Triggers watches chat messages and can do anything, reply to a message with a given text, delete a message, execute any userbot command. Overall, a very cool module"""
    
    strings = {
        "name": "Triggers",
        "_cfg_status": "module working or not",
        "_cfg_allow_invoke": "can triggers run ANY userbot commands?",
        "_cfg_throttle_time": "cooldown between trigger executions",
        "no_reply": "<emoji document_id=5210952531676504517>❌</emoji> No reply!",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> No args!",
        "text_add": (
            "<emoji document_id=5427009714745517609>✅</emoji> <b>Trigger successfully added</b>\n"
            "<i>id:</i> <code>{id}</code>"
        ),
        "empty": "  <emoji document_id=5411324253662356461>🫗</emoji> Empty\n",
        "text_all": (
            "<emoji document_id=5443038326535759644>💬</emoji> <b>Your triggers:</b>\n"
            "{triggers}\n"
            "<i>in {chats} chats</i>"
        ),
        "chat_added": "<emoji document_id=5456140674028019486>⚡️</emoji> <b>Chat {chat} successfully added</b>",
        "chat_removed": "<emoji document_id=5440660757194744323>‼️</emoji> <b>Chat {chat} successfully removed</b>",
        "success": "<emoji document_id=5427009714745517609>✅</emoji> <b>Success</b>",
        "not_found": "<emoji document_id=5210952531676504517>❌</emoji> <b>Trigger not found!</b>",
        "not_valid": "<emoji document_id=5210952531676504517>❌</emoji> <b>Trigger is not valid!</b>",
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Unexpected error: {e}</b>"
    }
    
    strings_ru = {
        "_cfg_status": "Модуль работает или нет",
        "_cfg_allow_invoke": "могут ли триггеры запускать ЛЮБЫЕ команды юзербота?",
        "_cfg_throttle_time": "Кд между выполнением триггеров. Для применения изменений требуется перезагрузить модуль/юзербота",
        "no_reply": "<emoji document_id=5210952531676504517>❌</emoji> Нет реплая!",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> Нет аргументов!",
        "text_add": (
            "<emoji document_id=5427009714745517609>✅</emoji> <b>Триггер успешно добавлен</b>\n"
            "<i>id:</i> <code>{id}</code>"
        ),
        "empty": "  <emoji document_id=5411324253662356461>🫗</emoji> Пусто\n",
        "text_all": (
            "<emoji document_id=5443038326535759644>💬</emoji> <b>Ваши триггеры:</b>\n"
            "{triggers}\n"
            "<i>в {chats} чатах</i>"
        ),
        "chat_added": "<emoji document_id=5456140674028019486>⚡️</emoji> <b>Чат {chat} успешно добавлен</b>",
        "chat_removed": "<emoji document_id=5440660757194744323>‼️</emoji> <b>Чат {chat} успешно убран</b>",
        "success": "<emoji document_id=5427009714745517609>✅</emoji> <b>Успешно</b>",
        "not_found": "<emoji document_id=5210952531676504517>❌</emoji> <b>Триггер не найден!</b>",
        "not_valid": "<emoji document_id=5210952531676504517>❌</emoji> <b>Триггер не валиден!</b>",
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Неожиданная ошибка. Обратитесь к разработчику модуля или попробуйте изменить данные: {e}</b>",
        "_cls_doc": "Триггеры следят за сообщениями в чате и могут сделать что угодно, ответить на сообщение заданным текстом, удалить сообщение, выполнить любую команду юзербота. В общем очень крутой модуль"
    }

    
    def __init__(self):
        self.config = loader.ModuleConfig(
			loader.ConfigValue(
				"status",
				False,
				lambda: self.strings("_cfg_status"),
				validator=loader.validators.Boolean()
			),
			loader.ConfigValue(
				"allow_invoke",
				False,
				lambda: self.strings("_cfg_allow_invoke"),
				validator=loader.validators.Boolean()
			),
			loader.ConfigValue(
				"throttle_time",
				1.0,
				lambda: self.strings("_cfg_throttle_time"),
				validator=loader.validators.Float(minimum=0)
			),
		)
        
        self.cache = TTLCache(maxsize=10_000, ttl=float(self.config["throttle_time"]))
    
    
    @loader.command(ru_doc="[текст, на который будет тригеррится модуль] <реплай на текст ответа> - Добавить базовый триггер", alias="tbaseadd")
    async def triggeraddbase(self, message: Message):
        """[text that the module will trigger on] <reply on the response text> - Add base trigger"""
        triggers = self.get("triggers", [])
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        
        reply = await message.get_reply_message()
        if not reply or not reply.text:
            await utils.answer(message, self.strings("no_reply"))
            return
        
        trigger = {
            "m": args,
            "id": str(uuid.uuid4())[:5],
            "action": {
                "type": "answer",
                "text": reply.text
            },
            "delay": 0
        }
        triggers.append(trigger)
        self.set("triggers", triggers)
        
        text = self.strings("text_add").format(id=trigger["id"])
        
        await utils.answer(message, text)
        

    @loader.command(ru_doc="[триггер] - Добавить триггер из сырых данных", alias="tadd")
    async def triggeradd(self, message: Message):
        """[trigger] - Add a trigger from raw data"""
        triggers = self.get("triggers", [])
        
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        
        trigger = json.loads(args)
        if not isinstance(trigger, dict) or not trigger["m"] \
            or not trigger["action"]:
                return
        
        trigger["id"] = str(uuid.uuid4())[:5]
        if not trigger.get("delay") or trigger["delay"] < 0:
            trigger["delay"] = 0
        
        
        triggers.append(trigger)
        self.set("triggers", triggers)
        
        text = self.strings("text_add").format(id=trigger["id"])
        
        await utils.answer(message, text)
    

    @loader.command(ru_doc="Посмотреть все триггеры")
    async def triggers(self, message: Message):
        """View all triggers"""
        
        triggers = self.get("triggers", [])
        t = ""
        
        if not triggers:
            t = self.strings("empty")
        else:
            for trigger in triggers:
                t += f"  • {trigger['m']} {trigger['id']} action={trigger['action']['type']};\n"
        
        
        text = self.strings("text_all").format(
            triggers=t,
            chats=len(self.get("chats", []))
        )
        
        await utils.answer(message, text)


    @loader.command(ru_doc="Добавить чат, где будут работать триггеры")
    async def triggerchat(self, message: Message):
        """Add chat, where triggers will work"""
        chats = self.get("chats", [])
        chat_id = message.chat.id
        flag = False
        
        if chat_id not in chats:
            chats.append(chat_id)
            flag = True
        else:
            chats.remove(chat_id)
        
        self.set("chats", chats)
        
        text = (
            self.strings("chat_added").format(chat=chat_id)
            if flag
            else self.strings("chat_removed").format(chat=chat_id)
        )
        
        await utils.answer(message, text)
        
    
    @loader.command(ru_doc="Конфиг модуля")
    async def tconfig(self, message: Message):
        """Config for the module."""
        name = self.strings("name")
        await self.allmodules.commands["config"](
            await utils.answer(message, f"{self.get_prefix()}config {name}")
        )
    
    @loader.command(ru_doc="[айди триггера] - Удалить триггер")
    async def triggerdel(self, message: Message):
        """[trigger's id] - Delete trigger"""
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        
        triggers = self.get("triggers", [])
        for trigger in triggers:
            if trigger["id"] == args[0]:
                triggers.remove(trigger)
                self.set("triggers", triggers)
                await utils.answer(message, self.strings("success"))
                return
            
        await utils.answer(message, self.strings("not_found"))
    
    
    @loader.command(ru_doc="[айди триггера] - Получить триггер", alias="tget")
    async def triggerget(self, message: Message):
        """[trigger's id] - Get trigger"""
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        
        triggers = self.get("triggers", [])
        for trigger in triggers:
            if trigger["id"] == args[0]:
                await utils.answer(message, json.dumps(trigger))
                return
            
        await utils.answer(message, self.strings("not_found"))


    @loader.command(ru_doc="[айди триггера] [измененный триггер] - Изменить триггер", alias="tget")
    async def triggerset(self, message: Message):
        """[trigger's id] [edited trigger] - Edit trigger"""
        args = utils.get_args_raw(message).split(maxsplit=1)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        
        triggers = self.get("triggers", [])
        for index, trigger in enumerate(triggers):
            if trigger["id"] == args[0]:
                try:
                    new_trigger = json.loads(args[1])
                    triggers[index] = new_trigger
                    if not isinstance(new_trigger, dict) or not new_trigger["m"] \
                        or not new_trigger["action"]:
                            raise ValueError("новый триггер должен быть словарем, и обязательно иметь ключ action")
                    
                    new_trigger["id"] = trigger["id"]
                    if not new_trigger.get("delay") or new_trigger["delay"] < 0:
                        new_trigger["delay"] = 0
                except Exception as e:
                    await utils.answer(message, self.string("error").format(e=e))
                
                await utils.answer(message, self.strings("success"))
                return
            
        await utils.answer(message, self.strings("not_found"))
    
    @loader.watcher()
    async def triggers_watcher(self, message: Message):
        if not self.config["status"]:
            return
        
        if not message.text:
            return
        
        if not getattr(message, "chat") or (getattr(message, "chat") and message.chat.id not in self.get("chats", [])):
            return
        
        
        triggers = self.get("triggers", [])
        if not triggers:
            return
        
        t = []
        for trigger in triggers:
            if trigger.get("filters") and trigger["filters"].get("chats", []) != [] and message.chat.id not in trigger["filters"].get("chats", []):
                continue
            if trigger.get("filters") and trigger["filters"].get("from_users", []) != [] and message.from_id not in trigger["filters"].get("from_users", []):
                continue
            
            if trigger.get("filters") and trigger["filters"].get("ignorecase") is True:
                message.text = message.text.lower()
                
            if message.text == trigger["m"]:
                t.append(trigger)
                continue
                
            if trigger.get("filters") and trigger["filters"].get("contains", False) is True and trigger["m"] in message.text:
                t.append(trigger)
        
        for trigger in t:
            if trigger["id"] in self.cache:
                continue
            else:
                self.cache[trigger["id"]] = None

            
            action_type = trigger["action"]["type"]
            if trigger["delay"] != 0:
                await asyncio.sleep(trigger["delay"]) 
            
            if action_type == "answer":
                await message.reply(trigger["action"]["text"].format(text=message.text))
            elif action_type == "delete":
                await message.delete()
            elif action_type == "invoke":
                if self.config["allow_invoke"]:
                    await self.invoke(
                        trigger["action"].get("command"),
                        trigger["action"].get("args", ""),
                        message=message
                    )