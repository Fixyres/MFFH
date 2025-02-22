"""
           _
 ___  __ _| |_ __ ___   ___ _ __ _ __
/ __|/ _` | | '_ ` _ \ / _ \ '__| '__|
\__ \ (_| | | | | | | |  __/ |  | |
|___/\__, |_|_| |_| |_|\___|_|  |_|
        |_|

🔒 Licensed under the GNU GPLv3
🌐 https://www.gnu.org/licenses/gpl-3.0.htmla
"""

# meta banner: https://github.com/sqlmerr/hikka_mods/blob/main/assets/banners/triggers.png?raw=true
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/triggers.png?raw=true
# meta developer: @sqlmerr_m
# requires: cachetools

import ast
import logging
import asyncio
import json
from contextlib import suppress
from typing import Dict, List, TypedDict, Any, Callable, Optional, Tuple, TypeVar, Union
from meval import meval

from .. import loader, utils
from hikkatl.tl.patched import Message

from cachetools import TTLCache

from ..inline.types import InlineCall
from ..types import HikkaReplyMarkup, JSONSerializable


logger = logging.getLogger(__name__)


class Action(TypedDict):
    type: str
    data: Dict[str, str]


ACTION_TYPES = ["callback", "invoke", "answer", "delete"]


class Filters(TypedDict, total=False):
    from_users: List[int]
    chats: List[int]
    is_admin: bool
    contains: bool
    ignorecase: bool


class Trigger(TypedDict):
    id: int
    m: str
    action: Action
    filters: Filters
    delay: float


def dict_updater(obj: Dict[str, Union[dict, Any]], query: str, value: Any) -> None:
    keys = query.split(".")
    current = obj
    for key in keys[:-1]:
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"key {key} not found")
        current = current[key]

    if not isinstance(current, dict) or keys[-1] not in current:
        raise ValueError(f"key {keys[-1]} not found")
    if not isinstance(current[keys[-1]], type(value)):
        raise ValueError(f"value in dict must be the same type as value")
    current[keys[-1]] = value


def dict_getter(obj: Dict[str, Union[dict, Any]], query: str) -> Any:
    keys = query.split(".")
    current = obj
    for key in keys[:-1]:
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"key {key} not found")
        current = current[key]

    return current.get(keys[-1])


class TriggerManager:
    def __init__(
        self,
        getter_func: Callable[[str, Optional[JSONSerializable]], JSONSerializable],
        setter_func: Callable[[str, JSONSerializable], bool],
    ) -> None:
        self.getter = getter_func
        self.setter = setter_func

    def get_triggers(self) -> List[Trigger]:
        return self.getter("triggers", [])

    def get_trigger(self, t_id: int) -> Optional[Trigger]:
        triggers = self.get_triggers()
        for t in triggers:
            if t["id"] == t_id:
                return t

    def get_trigger_with_index(self, t_id: int) -> Optional[Tuple[int, Trigger]]:
        triggers = self.get_triggers()
        for i, t in enumerate(triggers):
            if t["id"] == t_id:
                return i, t

    def set_triggers(self, value: List[Trigger]) -> bool:
        return self.setter("triggers", value)

    def add_trigger(self, value: Trigger) -> bool:
        triggers = self.get_triggers()
        triggers.append(value)
        return self.set_triggers(triggers)

    def set_trigger(self, trigger: Trigger) -> bool:
        response = self.get_trigger_with_index(trigger["id"])
        if not response:
            return self.add_trigger(trigger)
        i, t = response
        triggers = self.get_triggers()
        triggers[i] = trigger
        return self.set_triggers(triggers)


class Configuration:
    def __init__(self, manager: TriggerManager) -> None:
        self.manager = manager

    def _triggers_menu_markup(self, triggers: List[Trigger]) -> HikkaReplyMarkup:
        if len(triggers) > 96:
            triggers = triggers[:95]
        return [
            {
                "text": f"ID-{t['id']}",
                "callback": self._open_trigger_config,
                "kwargs": {"trigger": t},
            }
            for t in triggers
        ]

    def _main_menu_markup(self) -> HikkaReplyMarkup:
        return [
            [{"text": "🔀 Triggers", "callback": self._open_triggers_menu}],
            [{"text": "❌ Close", "action": "close"}],
        ]

    def _trigger_config_markup(self, trigger: Trigger) -> HikkaReplyMarkup:
        buttons = [
            self._input_button(trigger, "m", "message"),
            self._input_button(trigger, "delay", "delay"),
            {
                "text": "🛡 Filters",
                "callback": self._open_filters_config_menu,
                "kwargs": {"trigger": trigger},
            },
            {
                "text": "💊 Action",
                "callback": self._open_action_config_menu,
                "kwargs": {"trigger": trigger},
            },
            {
                "text": "⬅️ Back",
                "callback": self._open_triggers_menu,
            },
        ]
        return utils.chunks(buttons, 2)

    def _trigger_filters_markup(self, trigger: Trigger) -> HikkaReplyMarkup:
        types = Filters.__annotations__.items()
        f = []
        for k, v in types:
            if v == bool:
                f.append(self._bool_filter_config(trigger, k))
            elif v == List[int]:
                f.append(self._list_int_filter_config(trigger, k))

        f.append(
            [
                {
                    "text": "⬅️ Back",
                    "callback": self._open_trigger_config,
                    "kwargs": {"trigger": trigger},
                }
            ]
        )

        return f

    def _bool_filter_config(self, trigger: Trigger, key: str) -> HikkaReplyMarkup:
        async def callback(call: InlineCall) -> None:
            val: Optional[bool] = trigger["filters"].get(key)
            if val is None:
                await call.answer("error: filter not found")
                return
            trigger["filters"][key] = not val
            self.manager.set_trigger(trigger)
            await call.answer("✅")
            await self._open_filters_config_menu(call, trigger)

        v: Optional[bool] = trigger["filters"].get(key)
        if v is None:
            trigger["filters"][key] = False

        return [
            {
                "text": f"{'❌' if not v else '✅'} {key}",
                "callback": callback,
            }
        ]

    def _list_int_filter_config(self, trigger: Trigger, key: str) -> HikkaReplyMarkup:
        async def callback(call: InlineCall, query: str, action: str) -> None:
            val: List[int] = trigger["filters"].get(key)
            if val is None:
                await call.answer("filter not found")
                return
            if action == "append":
                if not query.isdigit():
                    logger.error("input value to append must be an integer")
                    return
                val.append(int(query))
            elif action == "set":
                try:
                    query = ast.literal_eval(query)
                    if isinstance(query, int):
                        val = [query]
                    elif iter(query) and isinstance(query[0], int):
                        val = list(query)
                    else:
                        raise ValueError(
                            "input value must be list of integers or integers. For example: [-123, 456, 678]; 123"
                        )

                except (ValueError, TypeError) as e:
                    logger.warning(f"{query}, {type(query)}")
                    logger.error(e)
                    return

            elif action == "delete":
                try:
                    query = ast.literal_eval(query)
                    if not isinstance(query, int):
                        raise ValueError("input value must be an integer")

                    with suppress(ValueError):
                        val.remove(query)

                except ValueError as e:
                    logger.error(e)
                    return

            trigger["filters"][key] = val
            self.manager.set_trigger(trigger)
            await open_configuration(call)

        async def open_configuration(call: InlineCall) -> None:
            val: Optional[List[int]] = trigger["filters"].get(key)
            if val is None:
                val = []
                trigger["filters"][key] = val

            await call.edit(
                text=f"<b>Configuring </b><code>{key}</code><b> of trigger </b><code>{trigger['id']}</code>: \n<code>{val}</code>",
                reply_markup=[
                    [
                        {
                            "text": f"➕ Add value",
                            "input": "✍️ Enter value to append",
                            "handler": callback,
                            "kwargs": {"action": "append"},
                        },
                    ],
                    [
                        {
                            "text": f"➖ Delete value",
                            "input": "✍️ Enter value to delete",
                            "handler": callback,
                            "kwargs": {"action": "delete"},
                        },
                    ],
                    [
                        {
                            "text": f"✍️ Set",
                            "input": "✍️ Enter list to replace",
                            "handler": callback,
                            "kwargs": {"action": "set"},
                        }
                    ],
                    [
                        {
                            "text": "⬅️ Back",
                            "callback": self._open_filters_config_menu,
                            "kwargs": {"trigger": trigger},
                        }
                    ],
                ],
            )

        return [
            {
                "text": f"{key} - list[int]",
                "callback": open_configuration,
            }
        ]

    def _input_button(
        self, trigger: Trigger, path: str, title: str
    ) -> HikkaReplyMarkup:
        return {
            "text": f"✍️ {title.capitalize()}",
            "input": f"✍️ Enter new value for '{title}'",
            "handler": self._update_trigger_input_handler,
            "kwargs": {
                "path": path,
                "trigger": trigger,
            },
        }

    def _trigger_config_text(self, trigger: Trigger) -> str:
        return f"🛠 <b>Editing trigger with id {trigger['id']}</b>\n\n<code>{utils.escape_html(str(trigger))}</code>"

    async def _update_trigger_input_handler(
        self, call: InlineCall, query: str, path: str, trigger: Trigger
    ) -> None:
        try:
            val = dict_getter(trigger, path)
        except ValueError:
            await call.answer("error")
            return

        if val is None:
            with suppress(Exception):
                value = ast.literal_eval(query)
        else:
            if not isinstance(val, str):
                value = ast.literal_eval(query)
            else:
                value = query

        try:
            dict_updater(trigger, path, value)
            self.manager.set_trigger(trigger)
        except ValueError:
            return

        await call.edit(
            text=self._trigger_config_text(trigger),
            reply_markup=self._trigger_config_markup(trigger),
        )

    async def _open_filters_config_menu(
        self, call: InlineCall, trigger: Trigger
    ) -> None:
        markup = self._trigger_filters_markup(trigger)
        await call.edit(text="⚙️ <b>Filter configuration</b>", reply_markup=markup)

    async def __change_action_type(
        self, call: InlineCall, val: str, trigger: Trigger
    ) -> None:
        if val not in ACTION_TYPES:
            await call.answer("error")
            return
        trigger["action"]["type"] = val
        self.manager.set_trigger(trigger)
        await call.answer("✅")
        await self._open_action_type_config_menu(call, trigger)

    async def _open_action_type_config_menu(
        self, call: InlineCall, trigger: Trigger
    ) -> None:
        markup = utils.chunks(
            [
                {
                    "text": f"{'⚫️' if trigger['action']['type'] == t else '⚪️'} {t}",
                    "callback": self.__change_action_type,
                    "kwargs": {"val": t, "trigger": trigger},
                }
                for t in ACTION_TYPES
            ],
            2,
        )
        markup.append(
            [
                {
                    "text": "⬅️ Back",
                    "callback": self._open_action_config_menu,
                    "kwargs": {"trigger": trigger},
                }
            ]
        )

        await call.edit("⚙️ <b>Select action type:</b>", reply_markup=markup)

    async def _open_action_config_menu(
        self, call: InlineCall, trigger: Trigger
    ) -> None:
        markup = [
            [
                {
                    "text": "♦️ Type",
                    "callback": self._open_action_type_config_menu,
                    "kwargs": {"trigger": trigger},
                }
            ],
            [self._input_button(trigger, "action.data", "data")],
            [
                {
                    "text": "⬅️ Back",
                    "callback": self._open_trigger_config,
                    "kwargs": {"trigger": trigger},
                }
            ],
        ]
        await call.edit(
            text=f"⚙️ <b>Action configuration</b>\n<code>{utils.escape_html(str(trigger['action']))}</code>",
            reply_markup=markup,
        )

    async def _open_triggers_menu(self, call: InlineCall) -> None:
        triggers = self.manager.get_triggers()
        markup = self._triggers_menu_markup(triggers)

        await call.edit(
            text="☰ <b>Select trigger to configure:</b>", reply_markup=markup
        )

    async def _open_trigger_config(self, call: InlineCall, trigger: Trigger):
        markup = self._trigger_config_markup(trigger)
        await call.edit(text=self._trigger_config_text(trigger), reply_markup=markup)

    async def render(self, form: Any, message: Message) -> None:
        await form(
            text="⚙️ <b>Triggers Configuration Menu</b>",
            message=message,
            reply_markup=self._main_menu_markup(),
        )


@loader.tds
class Triggers(loader.Module):
    """Triggers watch chat messages and can do anything, reply to a message with a given text, delete a message, execute any userbot command. Overall, a very cool module"""

    strings = {
        "name": "Triggers",
        "_cfg_status": "module working or not",
        "_cfg_allow_invoke": "can triggers run ANY userbot commands?",
        "_cfg_allow_callback": "can triggers run ANY python code?",
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
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Unexpected error: {e}</b>",
    }

    strings_ru = {
        "_cfg_status": "Модуль работает или нет",
        "_cfg_allow_invoke": "могут ли триггеры запускать ЛЮБЫЕ команды юзербота?",
        "_cfg_allow_callback": "могут ли триггеры запускать АБСОЛЮТНО любой код на python?",
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
        "_cls_doc": "Триггеры следят за сообщениями в чате и могут сделать что угодно, ответить на сообщение заданным текстом, удалить сообщение, выполнить любую команду юзербота. В общем очень крутой модуль",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: self.strings("_cfg_status"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "allow_invoke",
                False,
                lambda: self.strings("_cfg_allow_invoke"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "allow_callback",
                True,
                lambda: self.strings("_cfg_allow_callback"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "throttle_time",
                1.0,
                lambda: self.strings("_cfg_throttle_time"),
                validator=loader.validators.Float(minimum=0),
            ),
        )

        self.cache = TTLCache(maxsize=10_000, ttl=float(self.config["throttle_time"]))
        self.manager = TriggerManager(self.get, self.set)

    def increment_trigger_id(self) -> int:
        triggers: List[Trigger] = self.get("triggers", [])
        if triggers:
            return triggers[-1]["id"] + 1

        return 0

    async def _execute_callback(
        self, callback_id: str, message: Message, trigger: Trigger
    ) -> None:
        callbacks: Dict[str, int] = self.get("callbacks", {})
        if not (asset_id := callbacks.get(callback_id)):
            logger.error("callback with id %s not found", callback_id)
            return
        asset: Optional[Message] = await self.db.fetch_asset(asset_id)
        if not asset:
            logger.error("callback code not found", asset_id)
            return

        code = asset.text
        reply = await message.get_reply_message()
        kwargs = {
            "client": self.client,
            "c": self.client,
            "message": message,
            "m": message,
            "reply": reply,
            "r": reply,
            "trigger": trigger,
            "t": trigger,
            "utils": utils,
        }

        try:
            await meval(code, globals(), **kwargs)
        except Exception as e:
            logger.exception("callback code error: %s", e)

    @loader.command(
        ru_doc="[текст, на который будет тригеррится модуль] <реплай на текст ответа> - Добавить базовый триггер",
        alias="taddbase",
    )
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

        trigger = Trigger(
            m=args,
            id=self.increment_trigger_id(),
            action=Action(type="answer", data={"text": reply.text}),
            delay=0,
            filters=Filters(),
        )
        triggers.append(trigger)
        logger.info(triggers)
        self.set("triggers", triggers)

        text = self.strings("text_add").format(id=trigger["id"])

        await utils.answer(message, text)

    @loader.command(ru_doc="[триггер] - Добавить триггер из сырых данных", alias="tadd")
    async def triggeradd(self, message: Message):
        """[trigger] - Add a trigger from raw data"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        trigger = json.loads(args)
        if (
            not isinstance(trigger, dict)
            or not trigger.get("m")
            or not trigger.get("action")
            or not trigger.get("filters")
        ):
            return

        trigger["id"] = self.increment_trigger_id()
        if not trigger.get("delay") or trigger["delay"] < 0:
            trigger["delay"] = 0
        self.manager.add_trigger(trigger)

        text = self.strings("text_add").format(id=trigger["id"])

        await utils.answer(message, text)

    @loader.command(ru_doc="Посмотреть все триггеры")
    async def triggers(self, message: Message):
        """View all triggers"""

        triggers = self.manager.get_triggers()
        t = ""

        if not triggers:
            t = self.strings("empty")
        else:
            for trigger in triggers:
                t += f"  • {trigger['m']} {trigger['id']} action={trigger['action']['type'].lower()};\n"

        text = self.strings("text_all").format(
            triggers=t, chats=len(self.get("chats", []))
        )

        await utils.answer(message, text)

    @loader.command(ru_doc="Добавить чат, где будут работать триггеры", alias="tchat")
    async def triggerchat(self, message: Message):
        """Add chat, where triggers will work"""
        chats = self.get("chats", [])
        chat_id = utils.get_chat_id(message)
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
        configurator = Configuration(self.manager)
        await configurator.render(self.inline.form, message)

    @loader.command(ru_doc="[айди триггера] - Удалить триггер", alias="tdel")
    async def triggerdel(self, message: Message):
        """[trigger's id] - Delete trigger"""
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        if not args[0].isdigit():
            await utils.answer(
                message, self.strings("error").format("Input id must be an integer")
            )
            return

        triggers = self.manager.get_triggers()
        for trigger in triggers:
            if trigger["id"] == int(args[0]):
                triggers.remove(trigger)
                self.manager.set_triggers(triggers)
                await utils.answer(message, self.strings("success"))
                return

        await utils.answer(message, self.strings("not_found"))

    @loader.command(ru_doc="[айди колбека: str] <реплай на пайтон код> - Добавить колбек, который триггер сможет выполнить")
    async def tcallback(self, message: Message):
        """[callback_id: str] <reply to python code> - Add a callback that trigger can execute"""
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        callback_id = args[0]

        reply = await message.get_reply_message()
        if not reply or not reply.raw_text:
            await utils.answer(message, self.strings("no_reply"))
            return

        asset_id = await self.db.store_asset(reply)
        callbacks = self.get("callbacks", {})
        callbacks[callback_id] = asset_id
        self.set("callbacks", callbacks)

        await utils.answer(message, self.strings("success"))

    @loader.command(ru_doc="[айди триггера] - Получить триггер", alias="tget")
    async def triggerget(self, message: Message):
        """[trigger's id] - Get trigger"""
        args = utils.get_args_raw(message).split()
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        if not args[0].isdigit():
            await utils.answer(
                message, self.strings("error").format("Input id must be an integer")
            )
            return

        trigger = self.manager.get_trigger(int(args[0]))
        if trigger:
            await utils.answer(message, f"<code>{trigger}</code>")
            return

        await utils.answer(message, self.strings("not_found"))

    @loader.command(
        ru_doc="[айди триггера] [измененный триггер] - Изменить триггер", alias="tset"
    )
    async def triggerset(self, message: Message):
        """[trigger's id] [edited trigger] - Edit trigger"""
        args = utils.get_args_raw(message).split(maxsplit=1)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return
        if len(args) < 2:
            await utils.answer(message, self.strings("no_args"))
            return

        if not args[0].isdigit():
            await utils.answer(
                message, self.strings("error").format("Input id must be an integer")
            )
            return
        trigger_id = int(args[0])
        trigger = self.manager.get_trigger(trigger_id)
        if not trigger:
            await utils.answer(message, self.strings("not_found"))
            return

        try:
            new_trigger = json.loads(args[1])
            keys = new_trigger.keys()
            if not isinstance(new_trigger, dict) or not any(k in keys for k in keys):
                raise ValueError(
                    "trigger must be in JSON format and must have 'm' and 'action'"
                )

            new_trigger["id"] = trigger["id"]
            if not new_trigger.get("delay") or new_trigger["delay"] < 0:
                new_trigger["delay"] = 0

            self.manager.set_trigger(new_trigger)
        except Exception as e:
            await utils.answer(message, self.strings("error").format(e=e))
            return

        await utils.answer(message, self.strings("success"))

    @loader.command(
        ru_doc="[айди триггера] [путь] [значение] - Изменить одно значение триггера",
        alias="tupd",
    )
    async def triggerupdate(self, message: Message):
        """[trigger's id] [path] [value] - Edit trigger"""
        args = utils.get_args_raw(message).split(maxsplit=2)
        if not args or len(args) < 3:
            await utils.answer(message, self.strings("no_args"))
            return
        if not args[0].isdigit():
            await utils.answer(
                message, self.strings("error").format("Input id must be an integer")
            )
            return

        trigger = self.manager.get_trigger(int(args[0]))
        if not trigger:
            await utils.answer(message, self.strings("not_found"))
            return

        path = args[1]
        value = args[2]
        try:
            tvalue = dict_getter(trigger, "value")
        except Exception as e:
            await utils.answer(message, self.strings("error").format(e=e))
            return
        if tvalue is None:
            with suppress(Exception):
                value = ast.literal_eval(value)
        else:
            if not isinstance(tvalue, str):
                value = ast.literal_eval(tvalue)

        try:
            dict_updater(trigger, path, value)
            self.manager.set_trigger(trigger)
        except Exception as e:
            await utils.answer(message, self.strings("error").format(e=e))
            return

        await utils.answer(message, self.strings("success"))

    @loader.watcher()
    async def triggers_handler(self, message: Message):
        if not self.config["status"]:
            return

        if not message.text:
            return

        chats = self.get("chats", [])
        chat_id = utils.get_chat_id(message)
        if chat_id not in chats:
            return

        triggers = self.manager.get_triggers()
        if not triggers:
            return

        t = []
        for trigger in triggers:
            if (
                trigger["filters"].get("chats") is not None
                and chat_id not in trigger["filters"]["chats"]
            ):
                continue
            if (
                trigger["filters"].get("from_users") is not None
                and message.from_id not in trigger["filters"]["from_users"]
            ):
                continue

            if trigger["filters"].get("ignorecase"):
                message.text = message.text.lower()
                trigger["m"] = trigger["m"].lower()

            if message.text == trigger["m"]:
                t.append(trigger)
                continue

            if trigger["filters"].get("contains") and trigger["m"] in message.text:
                t.append(trigger)

            logger.info(trigger)

        for trigger in t:
            if trigger["id"] in self.cache:
                continue
            else:
                self.cache[trigger["id"]] = None

            action_type = trigger["action"]["type"]
            if trigger["delay"] != 0:
                await asyncio.sleep(trigger["delay"])

            if action_type == "answer":
                await message.reply(
                    trigger["action"]["data"]["text"].format(text=message.text)
                )
            elif action_type == "delete":
                await message.delete()
            elif action_type == "invoke":
                if self.config["allow_invoke"]:
                    await self.invoke(
                        trigger["action"]["data"].get("command"),
                        trigger["action"]["data"].get("args", ""),
                        message=message,
                    )
            elif action_type == "callback":
                if self.config["allow_callback"]:
                    callback_id = trigger["action"].get("data", {}).get("callback_id")
                    if not callback_id:
                        logger.warning(
                            "callback_id not set in trigger %s", trigger["id"]
                        )
                        continue
                    await self._execute_callback(callback_id, message, trigger)
            else:
                logger.error(
                    f"unknown action type {action_type} of trigger {trigger['id']}"
                )
