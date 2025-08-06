# meta developer: @hikkagpt
import json
import logging
import aiohttp
import base64
import os
from math import ceil

from telethon.tl.types import PeerUser
from .. import loader, utils

# --- Глобальные переменные и константы ---
PERSONAS_FILE = "zetta_assistant_personas.json"
MODELS_PER_PAGE = 10
# ИСПРАВЛЕНО: Контекстное окно увеличено в 10 раз
MAX_HISTORY_LENGTH = 200  # 100 пар вопрос-ответ

available_models = {
    "1": "o3-PRO", "2": "o1-PRO", "3": "o3-Mini-High", "4": "Grok 3", "5": "GPT 4.1",
    "6": "qwen3-235b-a22b", "7": "qwen-max-latest", "8": "qwen-plus-2025-01-25",
    "9": "qwen-turbo-2025-02-11", "10": "qwen2.5-coder-32b-instruct",
    "11": "qwen2.5-72b-instruct", "12": "gpt-4.5", "13": "gpt-4o", "14": "gpt-4o-mini",
    "15": "gpt4-turbo", "16": "gpt-3.5-turbo", "17": "gpt-4", "18": "deepseek-v3",
    "19": "deepseek-r1", "20": "gemini-1.5 Pro", "21": "gemini-2.5-pro-exp-03-25",
    "22": "gemini-2.5-flash", "23": "gemini-2.0-flash", "24": "llama-4-maverick",
    "25": "llama-4-scout", "26": "llama-3.3-70b", "27": "llama-3.3-8b",
    "28": "llama-3.1", "29": "llama-2", "30": "claude-3.5-sonnet", "31": "claude-3-haiku",
    "32": "bard", "33": "qwen", "34": "t-pro", "35": "t-lite"
}

sorted_models = list(available_models.items())

def load_personas():
    try:
        with open(PERSONAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_personas(personas):
    with open(PERSONAS_FILE, "w", encoding="utf-8") as f:
        json.dump(personas, f, indent=4, ensure_ascii=False)

personas = load_personas()


@loader.tds
class ZettaAIAssistantMod(loader.Module):
    """
>> Часть экосистемы Zetta - AI models <<
🌒 Version: 1.2 (Group Fix & Context Fix)
📍Описание:
Универсальный AI автоответчик для ваших личных чатов в Telegram.
Этот модуль является частью экосистемы Zetta и дополняет основной модуль «Zetta - AI models».

🤖 Больше возможностей в нашем боте: @ZettaGPT4o_bot

🔀Режимы работы:
- Ответ всем: ИИ отвечает на сообщения от любого пользователя в ЛС.
- Ответ друзьям: ИИ отвечает только пользователям из вашего списка друзей.
- Всем кроме друзей: ИИ отвечает всем, кто НЕ в списке друзей.

⚙️ Ключевые возможности:
- Контекстная память в каждом чате (до 100 сообщений).
- Основные настройки через меню `.zcfg`.
- Управление плагинами через интерактивное меню `.zplugins`.
- Раздельная настройка ролей командами (`.zrole`).
- Выбор из 35 моделей ИИ.

🫶 Разработчик: @hikkagpt"""
    strings = {"name": "Zetta - AI Assistant"}

    def __init__(self):
        self.is_active = False
        self.response_mode = "all"
        self.friends = []
        self.default_model = "gpt-4o"
        self.role_all = "Ты — вежливый и полезный AI ассистент Zetta. Ты автоответчик в личных чатах."
        self.role_friends = "Ты — AI ассистент по имени Zetta. Общайся неформально и дружелюбно. Ты просто автоответчик."
        self.human_mode = False
        self.provider = "OnlySq-Zetta"
        self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        self.history = {}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.is_active = self.db.get(self.strings["name"], "is_active", False)
        self.response_mode = self.db.get(self.strings["name"], "response_mode", "all")
        self.friends = self.db.get(self.strings["name"], "friends", [])
        self.default_model = self.db.get(self.strings["name"], "default_model", "gpt-4o-mini")
        self.role_all = self.db.get(self.strings["name"], "role_all", self.role_all)
        self.role_friends = self.db.get(self.strings["name"], "role_friends", self.role_friends)
        self.human_mode = self.db.get(self.strings["name"], "human_mode", False)
        self.provider = self.db.get(self.strings["name"], "provider", "OnlySq-Zetta")
        logging.info("Zetta - AI Assistant модуль загружен.")

    @loader.watcher(no_commands=True)
    async def watcher(self, message):
        # ИСПРАВЛЕНО: Железная защита от ответов в группах.
        if not message.is_private:
            return

        if not self.is_active or message.out:
            return

        chat_id = message.chat_id
        is_friend = message.sender_id in [f['id'] for f in self.friends]

        if self.response_mode == "friends" and not is_friend:
            return
        if self.response_mode == "except_friends" and is_friend:
            return
            
        request_text = message.text
        if not request_text:
            return

        self.history.setdefault(chat_id, [])
        role_to_use = self.role_friends if is_friend else self.role_all

        messages_to_send = [{"role": "system", "content": role_to_use}]
        messages_to_send.extend(self.history[chat_id])
        messages_to_send.append({"role": "user", "content": request_text})

        try:
            answer = await self.send_request_to_api(messages_to_send, self.default_model)
            if answer:
                self.history[chat_id].append({"role": "user", "content": request_text})
                self.history[chat_id].append({"role": "assistant", "content": answer})

                if len(self.history[chat_id]) > MAX_HISTORY_LENGTH:
                    self.history[chat_id] = self.history[chat_id][-MAX_HISTORY_LENGTH:]

                if self.human_mode:
                    await message.reply(answer)
                else:
                    await message.reply(f"<b>Ответ модели {self.default_model}:</b>\n{answer}")
        except Exception as e:
            logging.error(f"[ZettaAssistant] Ошибка при обработке сообщения: {e}")

    # --- КОМАНДЫ УПРАВЛЕНИЯ ПАМЯТЬЮ ---

    @loader.unrestricted
    async def zclearcmd(self, message):
        """Очистить историю диалога в текущем чате."""
        chat_id = message.chat_id
        if chat_id in self.history and self.history[chat_id]:
            self.history[chat_id] = []
            await utils.answer(message, "🟣 <b>История этого диалога очищена.</b>")
        else:
            await utils.answer(message, "🤷 <b>В этом чате и так нет истории.</b>")

    @loader.unrestricted
    async def zallclearcmd(self, message):
        """Очистить историю всех диалогов."""
        self.history = {}
        await utils.answer(message, "🟣 <b>История всех диалогов была полностью очищена.</b>")
        
    # --- КОМАНДЫ, ТРЕБУЮЩИЕ ВВОДА ---

    @loader.unrestricted
    async def zrolecmd(self, message):
        """Установить роль для 'all' или 'friends'."""
        args = utils.get_args_raw(message)
        if not args:
            usage_html = utils.escape_html(".zrole all <текст> или .zrole friends <текст>")
            await utils.answer(message, (f"<b>Текущие роли:</b>\n\n" f"<b>Для всех:</b> <i>{self.role_all}</i>\n\n" f"<b>Для друзей:</b> <i>{self.role_friends}</i>\n\n" f"<b>Использование:</b> <code>{usage_html}</code>"))
            return
        try: target, text = args.split(" ", 1)
        except ValueError: return await utils.answer(message, "🤔 <b>Неверный формат.</b> Укажите 'all' или 'friends' и текст роли.")
        if target.lower() == "all":
            self.role_all = text; self.db.set(self.strings["name"], "role_all", text)
            await utils.answer(message, "🟣 <b>Роль для 'всех' обновлена.</b>")
        elif target.lower() == "friends":
            self.role_friends = text; self.db.set(self.strings["name"], "role_friends", text)
            await utils.answer(message, "🟣 <b>Роль для 'друзей' обновлена.</b>")
        else: await utils.answer(message, "🤔 <b>Цель не ясна.</b> Укажите 'all' или 'friends'.")

    @loader.unrestricted
    async def zallrolecmd(self, message):
        """Установить одну роль для всех и для друзей."""
        args = utils.get_args_raw(message)
        if not args: return await utils.answer(message, "🤔 <b>Укажите текст для общей роли.</b>")
        self.role_all = args; self.role_friends = args
        self.db.set(self.strings["name"], "role_all", args)
        self.db.set(self.strings["name"], "role_friends", args)
        await utils.answer(message, "🟣 <b>Общая роль для всех и друзей установлена.</b>")

    @loader.unrestricted
    async def zplugincmd(self, message):
        """Создать плагин."""
        args = utils.get_args_raw(message)
        try: name, role = args.split(" ", 1)
        except ValueError:
            usage_html = utils.escape_html(".zplugin <название> <инструкция>")
            return await utils.answer(message, f"🤔 <b>Формат:</b> <code>{usage_html}</code>")
        personas[name] = role; save_personas(personas)
        await utils.answer(message, f"🟣 <b>Плагин '{name}' создан.</b> Теперь им можно управлять через <code>.zplugins</code>.")

    @loader.unrestricted
    async def zswitchcmd(self, message):
        """Применить плагин."""
        args = utils.get_args_raw(message)
        try: target, plugin_name = args.split(" ", 1)
        except ValueError:
            usage_html = utils.escape_html(".zswitch <all/friends> <название_плагина>")
            return await utils.answer(message, f"🤔 <b>Формат:</b> <code>{usage_html}</code>")
        if plugin_name not in personas: return await utils.answer(message, "🚫 <b>Плагин не найден.</b>")
        role_text = personas[plugin_name]
        if target.lower() == "all":
            self.role_all = role_text; self.db.set(self.strings["name"], "role_all", role_text)
            await utils.answer(message, f"🟣 <b>Роль для 'всех' переключена на плагин:</b> {plugin_name}")
        elif target.lower() == "friends":
            self.role_friends = role_text; self.db.set(self.strings["name"], "role_friends", role_text)
            await utils.answer(message, f"🟣 <b>Роль для 'друзей' переключена на плагин:</b> {plugin_name}")
        else: await utils.answer(message, "🤔 <b>Цель не ясна.</b> Укажите 'all' или 'friends'.")
        
    @loader.unrestricted
    async def zfriendcmd(self, message):
        """Добавить пользователя в друзья."""
        args = utils.get_args_raw(message); reply = await message.get_reply_message(); user_to_add = None
        if args:
            try: user_to_add = await self.client.get_entity(args if not args.isdigit() else int(args))
            except Exception: pass
        elif reply: user_to_add = await reply.get_sender()
        else: return await utils.answer(message, "🤔 <b>Ответьте на сообщение или укажите @username/ID.</b>")
        if not user_to_add: return await utils.answer(message, "🚫 <b>Не удалось найти пользователя.</b>")
        if user_to_add.id in [f['id'] for f in self.friends]: return await utils.answer(message, f"🟣 <b>{user_to_add.first_name}</b> уже в списке друзей.")
        self.friends.append({"id": user_to_add.id, "name": user_to_add.first_name})
        self.db.set(self.strings["name"], "friends", self.friends)
        await utils.answer(message, f"🫂 <b>{user_to_add.first_name}</b> добавлен(а) в друзья!")

    @loader.unrestricted
    async def zunfriendcmd(self, message):
        """Удалить пользователя из друзей."""
        args = utils.get_args_raw(message); reply = await message.get_reply_message(); user_to_remove_id, user_name = None, "Пользователь"
        if args:
            try:
                user = await self.client.get_entity(args if not args.isdigit() else int(args))
                user_to_remove_id, user_name = user.id, user.first_name
            except Exception: pass
        elif reply:
            user = await reply.get_sender()
            user_to_remove_id, user_name = user.id, user.first_name
        else: return await utils.answer(message, "🤔 <b>Ответьте на сообщение или укажите @username/ID.</b>")
        if not user_to_remove_id: return await utils.answer(message, "🚫 <b>Не удалось найти пользователя.</b>")
        if user_to_remove_id not in [f['id'] for f in self.friends]: return await utils.answer(message, f"🤷 <b>{user_name}</b> не найден(а) в списке друзей.")
        self.friends = [f for f in self.friends if f['id'] != user_to_remove_id]
        self.db.set(self.strings["name"], "friends", self.friends)
        await utils.answer(message, f"💔 <b>{user_name}</b> удален(а) из друзей.")

    @loader.unrestricted
    async def zfriendscmd(self, message):
        """Показывает список друзей."""
        if not self.friends: return await utils.answer(message, "🤷 <b>У вас пока нет друзей.</b>")
        friends_list = "\n".join([f"• <a href='tg://user?id={f['id']}'>{f['name']}</a>" for f in self.friends])
        await utils.answer(message, f"🫂 <b>Список друзей:</b>\n{friends_list}")

    # --- ГЛАВНОЕ ИНЛАЙН-МЕНЮ ---

    @loader.unrestricted
    async def zcfgcmd(self, message):
        """Показывает основное меню настроек."""
        await self._menu_main(message)
    
    # --- КОЛБЭКИ ДЛЯ ГЛАВНОГО МЕНЮ ---
    
    async def _toggle_active_callback(self, call):
        self.is_active = not self.is_active; self.db.set(self.strings["name"], "is_active", self.is_active)
        await self._menu_main(call=call)

    async def _set_mode_callback(self, call, mode):
        self.response_mode = mode; self.db.set(self.strings["name"], "response_mode", self.response_mode)
        await self._menu_response_mode(call=call)

    async def _set_model_callback(self, call, model_key):
        self.default_model = available_models[model_key]; self.db.set(self.strings["name"], "default_model", self.default_model)
        await self._menu_main(call=call)

    async def _toggle_human_callback(self, call):
        self.human_mode = not self.human_mode; self.db.set(self.strings["name"], "human_mode", self.human_mode)
        await self._menu_other(call=call)

    async def _toggle_provider_callback(self, call):
        self.provider = "Devj" if self.provider == "OnlySq-Zetta" else "OnlySq-Zetta"
        self.db.set(self.strings["name"], "provider", self.provider)
        await self._menu_other(call=call)
        
    async def _nav_callback(self, call, page, page_num=0):
        menus = {"main": self._menu_main, "modes": self._menu_response_mode, "models": self._menu_model_select, "other": self._menu_other}
        target_menu = menus.get(page)
        if not target_menu: return
        if page == "models": await target_menu(call=call, page=int(page_num))
        else: await target_menu(call=call)
            
    # --- ФУНКЦИИ ГЕНЕРАЦИИ ГЛАВНОГО МЕНЮ ---
    
    async def _menu_main(self, source=None, call=None):
        status = "<b>Активен</b> 🟣" if self.is_active else "<b>Выключен</b> ⚫️"
        mode_map = {"all": "Всем", "friends": "Только друзьям", "except_friends": "Всем кроме друзей"}
        text = (f"🟣 <b>Zetta Assistant</b>\n\n<b>Статус:</b> {status}\n<b>Режим ответа:</b> {mode_map.get(self.response_mode)}\n<b>Текущая модель:</b> {self.default_model}")
        buttons = [[{"text": "Вкл/Выкл", "callback": self._toggle_active_callback}], [{"text": "⚙️ Режим ответа", "callback": self._nav_callback, "args": ("modes", 0)}], [{"text": "🤖 Выбор модели", "callback": self._nav_callback, "args": ("models", 0)}], [{"text": "🔧 Прочие настройки", "callback": self._nav_callback, "args": ("other", 0)}]]
        message_to_use = call or source
        if call: await call.edit(text, reply_markup=buttons)
        else: await self.inline.form(text, message=message_to_use, reply_markup=buttons)

    async def _menu_response_mode(self, call):
        text = "🤔 <b>Выберите, кому должен отвечать ассистент:</b>"
        buttons = [[{"text": f"{'✅ ' if self.response_mode == 'all' else ''}Всем", "callback": self._set_mode_callback, "args": ("all",)}, {"text": f"{'✅ ' if self.response_mode == 'friends' else ''}Только друзьям", "callback": self._set_mode_callback, "args": ("friends",)}], [{"text": f"{'✅ ' if self.response_mode == 'except_friends' else ''}Всем, кроме друзей", "callback": self._set_mode_callback, "args": ("except_friends",)}], [{"text": "‹ Назад", "callback": self._nav_callback, "args": ("main", 0)}]]
        await call.edit(text, reply_markup=buttons)
        
    async def _menu_model_select(self, call, page=0):
        text = f"🤖 <b>Выберите модель для автоответчика (Стр. {page + 1}):</b>"
        start_index, end_index = page * MODELS_PER_PAGE, (page + 1) * MODELS_PER_PAGE
        page_models = sorted_models[start_index:end_index]
        buttons = [[{"text": f"{'✅ ' if self.default_model == v else ''}{k}. {v}", "callback": self._set_model_callback, "args": (k,)}] for k, v in page_models]
        nav = []
        if page > 0: nav.append({"text": "‹ Пред.", "callback": self._nav_callback, "args": ("models", page - 1)})
        if end_index < len(sorted_models): nav.append({"text": "След. ›", "callback": self._nav_callback, "args": ("models", page + 1)})
        buttons.append(nav)
        buttons.append([{"text": "‹ Назад в меню", "callback": self._nav_callback, "args": ("main", 0)}])
        await call.edit(text, reply_markup=buttons)

    async def _menu_other(self, call):
        human_status = "🟣 Включен" if self.human_mode else "⚫️ Выключен"
        text = (f"🔧 <b>Прочие настройки</b>\n\n<b>Режим 'Человека':</b> {human_status}\n<i>(Ответы приходят без подписи модели)</i>\n\n<b>API Провайдер:</b> {self.provider}")
        buttons = [[{"text": "👤 Вкл/Выкл 'Режим Человека'", "callback": self._toggle_human_callback}], [{"text": "🔄 Сменить провайдера", "callback": self._toggle_provider_callback}], [{"text": "‹ Назад", "callback": self._nav_callback, "args": ("main", 0)}]]
        await call.edit(text, reply_markup=buttons)

    # --- ИНЛАЙН-МЕНЮ УПРАВЛЕНИЯ ПЛАГИНАМИ ---
    
    @loader.unrestricted
    async def zpluginscmd(self, message):
        """Показывает меню управления плагинами."""
        await self._menu_plugins_list(message)

    async def _menu_plugins_list(self, source=None, call=None):
        if not personas:
            usage_html = utils.escape_html(".zplugincmd <имя> <инструкция>")
            text = f"🧩 <b>Плагины не найдены.</b>\n\nВы можете создать их командой <code>{usage_html}</code>."
            buttons = [[{"text": "Закрыть", "action": "close"}]]
        else:
            text = "🧩 <b>Управление плагинами</b>\n\nВыберите плагин для просмотра или удаления."
            buttons = []
            for name in sorted(personas.keys()):
                buttons.append([{"text": f"👁️ {name}", "callback": self._plugin_view_callback, "args": (name,)}, {"text": f"❌ Удалить", "callback": self._plugin_delete_prompt_callback, "args": (name,)}])
            buttons.append([{"text": "Закрыть", "action": "close"}])
        message_to_use = call or source
        if call: await call.edit(text, reply_markup=buttons)
        else: await self.inline.form(text, message=message_to_use, reply_markup=buttons)

    async def _plugin_view_callback(self, call, name):
        content = personas.get(name, "🚫 Плагин не найден.")
        text = f"<b>Содержимое плагина «{name}»:</b>\n\n<i>{utils.escape_html(content)}</i>"
        buttons = [[{"text": "‹ Назад к списку", "callback": self._menu_plugins_list, "args": (None,)}]]
        await call.edit(text, reply_markup=buttons)

    async def _plugin_delete_prompt_callback(self, call, name):
        text = f"Вы уверены, что хотите удалить плагин <b>«{name}»</b>?\n\n<b>Это действие необратимо.</b>"
        buttons = [[{"text": "Да, удалить", "callback": self._plugin_delete_confirm_callback, "args": (name,)}, {"text": "Нет, отмена", "callback": self._menu_plugins_list, "args": (None,)}]]
        await call.edit(text, reply_markup=buttons)

    async def _plugin_delete_confirm_callback(self, call, name):
        if name in personas: del personas[name]; save_personas(personas)
        await self._menu_plugins_list(call=call)

    # --- API ---

    async def send_request_to_api(self, messages, model):
        api_url = "http://109.172.94.236:5001/OnlySq-Zetta/v1/models" if self.provider == "OnlySq-Zetta" else "https://api.vysssotsky.ru/"
        if self.provider == 'Devj': payload = {"model": "gpt-4", "messages": messages, "max_tokens": 4096}
        else: payload = {"model": model, "request": {"messages": messages}}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(api_url, json=payload, headers={"Authorization": f"Bearer {self.api_key}"}) as response:
                    response.raise_for_status(); data = await response.json()
                    if self.provider == 'Devj': answer = data.get("choices", [{}])[0].get("message", {}).get("content", "🚫 Ответ не получен.")
                    else: answer = base64.b64decode(data.get("answer", "🚫 Ответ не получен.").strip()).decode('utf-8')
                    return answer.strip()
        except aiohttp.ClientError as e:
            logging.error(f"Ошибка при запросе к API ({self.provider}): {e}"); return f"🚫 Ошибка API: {e}"
        except Exception as e:
            logging.error(f"Непредвиденная ошибка при отправке запроса: {e}"); return f"🚫 Непредвиденная ошибка: {e}"
