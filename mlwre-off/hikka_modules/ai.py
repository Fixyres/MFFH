# meta developer: @hmodule
# scope: hikka_only

import logging
import g4f
import asyncio
import functools
import html
from collections import defaultdict

from .. import loader, utils
from telethon.tl.types import Message, User

logger = logging.getLogger(__name__)

STATIC_EMOJIS = {
    "q": "❓",
    "brain": "🧠",
    "bulb": "💡",
    "cross": "❌",
    "tick": "✅",
    "broom": "🧹", 
}

ANIMATED_EMOJIS = {
    "q": "<emoji document_id=5319226943516725959>😘</emoji>",
    "brain": "<emoji document_id=5449876550126152994>😔</emoji>",
    "bulb": "<emoji document_id=5451907751829582151>🤔</emoji>",
    "cross": "<emoji document_id=5465665476971471368>❌</emoji>",
    "tick": "<emoji document_id=5427009714745517609>✅</emoji>",
    "broom": "<emoji document_id=5278491193053822590>🧹</emoji>",
}

@loader.tds
class G4fAskMod(loader.Module):
    """Модуль для взаимодействия с ИИ моделями через g4f с памятью"""
    strings = {
        "name": "G4fAsk",
        "no_args_ai": "{q} <b>Usage:</b> <code>.ai <model_alias></code>\n<b>Available:</b> <code>{available}</code>\n<b>Current:</b> <code>{current}</code>",
        "invalid_model": "{cross} <b>Invalid model alias</b> <code>{alias}</code>. Available: {available}",
        "model_set": "{tick} <b>AI model set to</b> <code>{model}</code>.",
        "no_args_ask": "{q} <b>Please provide a question.</b> Usage: <code>.ask <query></code>",
        "thinking": "{brain} <b>Thinking</b> with <code>{model}</code>...",
        "result": "<b>{q} Question:</b>\n{prompt}\n\n<b>{bulb} Answer ({model}):</b>\n{answer}",
        "missing_dep": "{cross} <b>Error:</b> Missing dependency. Please install required packages (<code>pip install -U g4f</code>).",
        "request_error": "{cross} <b>Error:</b> Failed to get response from <code>{model}</code>. ({error})",
        "unexpected_error": "{cross} <b>Error:</b> An unexpected error occurred while contacting <code>{model}</code>. Error: {error}",
        "chat_cleared": "{broom} <b>Chat memory cleared</b> for this chat.",
        "no_history": "{broom} No chat history found for this chat to clear.",
    }
    strings_ru = {
        "_cls_doc": "Модуль для взаимодействия с ИИ моделями через g4f с памятью",
        "no_args_ai": "{q} <b>Использование:</b> <code>.ai <модель></code>\n<b>Доступные:</b> <code>{available}</code>\n<b>Текущая:</b> <code>{current}</code>",
        "invalid_model": "{cross} <b>Неверное имя модели</b> <code>{alias}</code>. Доступные: {available}",
        "model_set": "{tick} <b>Модель ИИ установлена на</b> <code>{model}</code>.",
        "no_args_ask": "{q} <b>Укажите вопрос.</b> Использование: <code>.ask <запрос></code>",
        "thinking": "{brain} <b>Думаю</b> с помощью <code>{model}</code>...",
        "result": "<b>{q} Вопрос:</b>\n{prompt}\n\n<b>{bulb} Ответ ({model}):</b>\n{answer}",
        "missing_dep": "{cross} <b>Ошибка:</b> Отсутствует зависимость. Установите необходимые пакеты (<code>pip install -U g4f</code>).",
        "request_error": "{cross} <b>Ошибка:</b> Не удалось получить ответ от <code>{model}</code>. ({error})",
        "unexpected_error": "{cross} <b>Ошибка:</b> Произошла непредвиденная ошибка при обращении к <code>{model}</code>. Ошибка: {error}",
        "chat_cleared": "{broom} <b>Память диалога очищена</b> для этого чата.",
        "no_history": "{broom} История для этого чата не найдена (нечего очищать).",
        "_cmd_doc_ai": "<модель> - Установить модель ИИ (gemini, deepseek, claude)",
        "_cmd_doc_ask": "<запрос> - Задать вопрос выбранной модели ИИ (с учетом истории)",
        "_cmd_doc_clearchat": "Очистить память ИИ для текущего чата",
    }

    # Memory settings
    MEMORY_DEPTH = 10 # Number of user/assistant message pairs to remember

    def __init__(self):
        self.config = loader.ModuleConfig()
        self._chat_history = defaultdict(list) # Store history per chat_id

    async def client_ready(self, client, db):
        self.db = db
        try:
            import g4f
            self._client = g4f.Client()
        except ImportError:
            logger.critical("g4f library not found. Install it using 'pip install -U g4f'")
            self._client = None

        self._default_model = "gemini-2.0-flash"
        self._available_models = {
            "gemini": "gemini-2.0-flash",
            "deepseek": "deepseek-v3",
            "claude": "claude-3.7-sonnet",
        }
        if "G4fAskMod" not in self.db:
            self.db["G4fAskMod"] = {}
        if "g4f_model" not in self.db["G4fAskMod"]:
             self.db.set("G4fAskMod", "g4f_model", self._default_model)


    def _get_emojis(self, user: User) -> dict:
        """Returns the correct emoji dict based on user's premium status"""
        # Include all possible emojis needed by the module
        all_emojis = {**STATIC_EMOJIS, **ANIMATED_EMOJIS}
        base_emojis = ANIMATED_EMOJIS if getattr(user, 'premium', False) else STATIC_EMOJIS
        # Ensure all keys exist, falling back to static if animated isn't fully defined (safety)
        return {key: base_emojis.get(key, STATIC_EMOJIS.get(key)) for key in all_emojis.keys()}


    async def _answer(self, message: Message, text: str, **kwargs):
        """Helper to answer with HTML parse mode."""
        emojis = kwargs.pop("emojis", {})
        formatted_text = text.format(**kwargs, **emojis)
        await utils.answer(message, formatted_text, parse_mode='html')

    async def _answer_result(self, message: Message, text: str, prompt:str, answer:str, **kwargs):
        """Helper for the result message, escaping prompt and answer."""
        emojis = kwargs.pop("emojis", {})
        safe_prompt = html.escape(prompt)
        safe_answer = html.escape(answer)

        formatted_text = text.format(
            prompt=safe_prompt,
            answer=safe_answer,
            **kwargs,
            **emojis
        )
        await utils.answer(message, formatted_text, parse_mode='html')


    @loader.command(
        ru_doc="<модель> - Установить модель ИИ (gemini, deepseek, claude)",
        en_doc="<model_alias> - Set the AI model (gemini, deepseek, claude)",
        aliases=["setmodel"],
    )
    async def ai(self, message: Message):
        """Set the AI model"""
        sender = await message.get_sender()
        emojis = self._get_emojis(sender)

        if not self._client:
             await self._answer(message, self.strings("missing_dep"), emojis=emojis)
             return

        args = utils.get_args_raw(message)
        available_keys = ", ".join(f"<code>{key}</code>" for key in self._available_models.keys())

        if not args:
            current_model = self.db.get("G4fAskMod", "g4f_model", self._default_model)
            await self._answer(
                message,
                self.strings("no_args_ai"),
                available=available_keys,
                current=f"<code>{current_model}</code>",
                emojis=emojis
            )
            return

        model_alias = args.lower().strip()
        if model_alias not in self._available_models:
            await self._answer(
                message,
                self.strings("invalid_model"),
                alias=html.escape(model_alias),
                available=available_keys,
                emojis=emojis
            )
            return

        selected_model = self._available_models[model_alias]
        self.db.set("G4fAskMod", "g4f_model", selected_model)

        await self._answer(
            message,
            self.strings("model_set"),
            model=f"<code>{selected_model}</code>",
            emojis=emojis
        )

    @loader.command(
        ru_doc="<запрос> - Задать вопрос выбранной модели ИИ (с учетом истории)",
        en_doc="<query> - Ask a question to the configured AI model (with history)",
        aliases=["a"],
    )
    async def ask(self, message: Message):
        """Ask the AI a question, maintaining chat history"""
        chat_id = message.chat_id
        sender = await message.get_sender()
        emojis = self._get_emojis(sender)

        if not self._client:
             await self._answer(message, self.strings("missing_dep"), emojis=emojis)
             return

        prompt = utils.get_args_raw(message)

        if not prompt:
            msg_to_del = await self._answer(
                message,
                self.strings("no_args_ask"),
                emojis=emojis
            )
            await asyncio.sleep(3)
            if isinstance(msg_to_del, Message):
                try:
                    await msg_to_del.delete()
                except Exception: pass
            else:
                try:
                    await message.delete()
                except Exception: pass
            return

        model = self.db.get("G4fAskMod", "g4f_model", self._default_model)

        msg = await self._answer(
            message,
            self.strings("thinking"),
            model=f"<code>{model}</code>",
            emojis=emojis
        )
        if not isinstance(msg, Message):
            msg = message

        # Retrieve history for this chat
        current_history = self._chat_history[chat_id].copy()
        # Prepare message list for API
        messages_to_send = current_history + [{"role": "user", "content": prompt}]

        try:
            func_call = functools.partial(
                self._client.chat.completions.create,
                model=model,
                messages=messages_to_send # Send history + new prompt
            )
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                func_call
            )

            if not response or not response.choices:
                 logger.warning(f"Received empty or invalid response from API for model {model}. Response: {response}")
                 raise Exception("Empty or invalid response from API")

            answer = response.choices[0].message.content

            # Update history: Add user prompt and AI answer
            self._chat_history[chat_id].append({"role": "user", "content": prompt})
            self._chat_history[chat_id].append({"role": "assistant", "content": answer})

            # Trim history if it exceeds depth
            while len(self._chat_history[chat_id]) > self.MEMORY_DEPTH * 2:
                self._chat_history[chat_id].pop(0) # Remove oldest user message
                self._chat_history[chat_id].pop(0) # Remove oldest assistant message

            await self._answer_result(
                msg,
                self.strings("result"),
                prompt=prompt,
                answer=answer,
                model=f"<code>{model}</code>",
                emojis=emojis
            )

        except ImportError:
            logger.exception("Missing dependency for g4f")
            await self._answer(msg, self.strings("missing_dep"), emojis=emojis)
        except Exception as e:
            error_name = type(e).__name__
            logger.exception(f"Error during g4f request: {e}")
            error_str = str(e).lower()
            safe_error = html.escape(str(e))

            if "request" in error_name.lower() or "request" in error_str or "api" in error_str or "network" in error_str or "connection" in error_str or "empty or invalid response" in error_str:
                await self._answer(
                    msg,
                    self.strings("request_error"),
                    model=f"<code>{model}</code>",
                    error=safe_error,
                    emojis=emojis
                )
            else:
                await self._answer(
                    msg,
                    self.strings("unexpected_error"),
                    model=f"<code>{model}</code>",
                    error=safe_error,
                    emojis=emojis
                )

    @loader.command(
        ru_doc="Очистить память ИИ для текущего чата",
        en_doc="Clear the AI memory for the current chat",
    )
    async def clearchat(self, message: Message):
        """Clears the AI's conversation history for the current chat."""
        chat_id = message.chat_id
        sender = await message.get_sender()
        emojis = self._get_emojis(sender)

        if chat_id in self._chat_history:
            del self._chat_history[chat_id]
            await self._answer(message, self.strings("chat_cleared"), emojis=emojis)
        else:
            await self._answer(message, self.strings("no_history"), emojis=emojis)
