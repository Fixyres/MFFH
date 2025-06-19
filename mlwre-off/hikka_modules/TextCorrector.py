# Name: TextCorrector
# Description: Автоматическое исправление ошибок в тексте с помощью ИИ
# Commands: correcttext, autocorrector, correctstatus, model
# meta developer: @YahooMods
# requires: g4f

from .. import loader, utils
from g4f.client import Client
import logging

logger = logging.getLogger(__name__)

@loader.tds
class TextCorrectorMod(loader.Module):
    """Модуль для исправления ошибок в тексте с помощью ИИ"""
    
    strings = {
        "name": "TextCorrector",
        "autocorrector_enabled": "🟢 Автокорректор включен",
        "autocorrector_disabled": "🔴 Автокорректор выключен", 
        "correcting": "🔄 Исправляю ошибки...",
        "correction_error": "❌ Ошибка при исправлении текста: {}",
        "no_text": "❌ Нет текста для исправления",
        "corrected": "✅ Исправлено:\n\n{}",
        "status_on": "🟢 Автокорректор: включен",
        "status_off": "🔴 Автокорректор: выключен",
        "model_set": "✅ Модель ИИ установлена: {}",
        "current_model": "🤖 Текущая модель: {}"
    }
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "auto_correct",
                False,
                lambda: "Автоматически исправлять ошибки в сообщениях",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "model",
                "gpt-4o-mini",
                lambda: "Модель ИИ для исправления текста"
            )
        )
        self.ai_client = None
        self.tg_client = None
    
    async def client_ready(self, client, db):
        """Инициализация после готовности клиента"""
        self.ai_client = Client()
        self.tg_client = client
        
        # Правильное получение информации о пользователе
        try:
            me = await client.get_me()
            logger.info(f"TextCorrector загружен для пользователя: {me.first_name}")
        except Exception as e:
            logger.error(f"Ошибка при получении информации о пользователе: {e}")
    
    async def correct_text(self, text: str) -> str:
        """Исправляет ошибки в тексте с помощью ИИ"""
        try:
            prompt = f"""Исправь только орфографические и грамматические ошибки в словах в этом тексте. 
НЕ добавляй запятые, точки или другие знаки препинания. 
НЕ меняй структуру предложений. 
НЕ переформулируй текст.
Просто исправь ошибки в словах, сохранив все остальное как есть:

{text}"""
            
            model_name = self.config["model"]
            response = self.ai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                web_search=False
            )
            
            corrected_text = response.choices[0].message.content.strip()
            return corrected_text
            
        except Exception as e:
            logger.error(f"Ошибка при исправлении текста: {e}")
            return text
    
    @loader.command()
    async def correcttext(self, message):
        """Исправить ошибки в тексте"""
        args = utils.get_args_raw(message)
        
        if not args:
            reply = await message.get_reply_message()
            if reply and reply.text:
                text = reply.text
            else:
                await utils.answer(message, self.strings("no_text"))
                return
        else:
            text = args
        
        await utils.answer(message, self.strings("correcting"))
        
        try:
            corrected = await self.correct_text(text)
            await utils.answer(message, self.strings("corrected").format(corrected))
        except Exception as e:
            await utils.answer(message, self.strings("correction_error").format(str(e)))
    
    @loader.command()
    async def autocorrector(self, message):
        """Включить/выключить автокорректор"""
        current = self.config["auto_correct"]
        self.config["auto_correct"] = not current
        
        if self.config["auto_correct"]:
            await utils.answer(message, self.strings("autocorrector_enabled"))
        else:
            await utils.answer(message, self.strings("autocorrector_disabled"))
    
    @loader.command()
    async def correctstatus(self, message):
        """Показать статус автокорректора"""
        if self.config["auto_correct"]:
            await utils.answer(message, self.strings("status_on"))
        else:
            await utils.answer(message, self.strings("status_off"))
    
    @loader.command()
    async def model(self, message):
        """Установить модель ИИ для исправления текста"""
        args = utils.get_args_raw(message)
        
        if not args:
            current_model = self.config["model"]
            await utils.answer(message, self.strings("current_model").format(current_model))
            return
            
        new_model = args.strip()
        self.config["model"] = new_model
        await utils.answer(message, self.strings("model_set").format(new_model))
    
    @loader.watcher("out")
    async def watcher(self, message):
        """Автоматически исправляет ошибки в исходящих сообщениях"""
        if not self.config["auto_correct"] or not self.ai_client:
            return
            
        if not hasattr(message, 'text') or not message.text or message.text.startswith("."):
            return
            
        if not hasattr(message, 'out') or not message.out:
            return
            
        try:
            corrected = await self.correct_text(message.text)
            
            if corrected != message.text and corrected.strip():
                await message.edit(corrected)
                
        except Exception as e:
            logger.error(f"Ошибка в автокорректоре: {e}")
            
