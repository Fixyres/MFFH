# meta developer: @moduleslist
# meta banner: https://envs.sh/Ult.jpg

from .. import loader, utils
import logging
import aiohttp
import asyncio

logger = logging.getLogger(__name__)

@loader.tds
class AutoTranslatorMod(loader.Module):
    """Faster version of auto-translator using Google Translate API"""

    strings = {
        "name": "AutoTranslator",
        "enabled": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Auto-translation enabled</b>\nTarget language: {} ({})",
        "disabled": "<emoji document_id=5465665476971471368>❌</emoji> <b>Auto-translation disabled for {}</b>",
        "invalid_lang": "<emoji document_id=5465665476971471368>❌</emoji> <b>Invalid language code! Use command .tr_langs to see available languages</b>",
        "no_lang": "<emoji document_id=5465665476971471368>❌</emoji> <b>Please specify target language code</b>",
        "translating": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Translating...</b>",
        "langs_list": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Available languages:</b>\n\n{}"
    }

    strings_ru = {
        "enabled": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Автоперевод включен</b>\nЯзык перевода: {} ({})",
        "disabled": "<emoji document_id=5465665476971471368>❌</emoji> <b>Автоперевод для {} выключен</b>",
        "invalid_lang": "<emoji document_id=5465665476971471368>❌</emoji> <b>Неверный код языка! Используйте команду .tr_langs чтобы увидеть доступные языки</b>",
        "no_lang": "<emoji document_id=5465665476971471368>❌</emoji> <b>Укажите код языка для перевода</b>",
        "translating": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Перевожу...</b>",
        "langs_list": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Доступные языки:</b>\n\n{}"
    }

    strings_ua = {
        "enabled": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Автопереклад увімкнено</b>\nМова перекладу: {} ({})",
        "disabled": "<emoji document_id=5465665476971471368>❌</emoji> <b>Автопереклад для {} вимкнено</b>",
        "invalid_lang": "<emoji document_id=5465665476971471368>❌</emoji> <b>Невірний код мови! Використовуйте команду .tr_langs щоб побачити доступні мови</b>",
        "no_lang": "<emoji document_id=5465665476971471368>❌</emoji> <b>Вкажіть код мови для перекладу</b>",
        "translating": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Перекладаю...</b>",
        "langs_list": "<emoji document_id=5334882760735598374>🔄</emoji> <b>Доступні мови:</b>\n\n{}"
    }

    SUPPORTED_LANGS = {
        "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic",
        "hy": "Armenian", "as": "Assamese", "ay": "Aymara", "az": "Azerbaijani",
        "bm": "Bambara", "eu": "Basque", "be": "Belarusian", "bn": "Bengali",
        "bho": "Bhojpuri", "bs": "Bosnian", "bg": "Bulgarian", "ca": "Catalan",
        "ceb": "Cebuano", "ny": "Chichewa", "zh-CN": "Chinese (Simplified)",
        "zh-TW": "Chinese (Traditional)", "co": "Corsican", "hr": "Croatian",
        "cs": "Czech", "da": "Danish", "dv": "Dhivehi", "doi": "Dogri",
        "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian",
        "ee": "Ewe", "tl": "Filipino", "fi": "Finnish", "fr": "French",
        "fy": "Frisian", "gl": "Galician", "ka": "Georgian", "de": "German",
        "el": "Greek", "gn": "Guarani", "gu": "Gujarati", "ht": "Haitian Creole",
        "ha": "Hausa", "haw": "Hawaiian", "iw": "Hebrew", "hi": "Hindi",
        "hmn": "Hmong", "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo",
        "ilo": "Ilocano", "id": "Indonesian", "ga": "Irish", "it": "Italian",
        "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh",
        "km": "Khmer", "rw": "Kinyarwanda", "gom": "Konkani", "ko": "Korean",
        "kri": "Krio", "ku": "Kurdish", "ckb": "Kurdish (Sorani)", "ky": "Kyrgyz",
        "lo": "Lao", "la": "Latin", "lv": "Latvian", "ln": "Lingala",
        "lt": "Lithuanian", "lg": "Luganda", "lb": "Luxembourgish",
        "mk": "Macedonian", "mai": "Maithili", "mg": "Malagasy", "ms": "Malay",
        "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi",
        "mni-Mtei": "Meiteilon", "lus": "Mizo", "mn": "Mongolian",
        "my": "Myanmar", "ne": "Nepali", "no": "Norwegian", "or": "Odia",
        "om": "Oromo", "ps": "Pashto", "fa": "Persian", "pl": "Polish",
        "pt": "Portuguese", "pa": "Punjabi", "qu": "Quechua", "ro": "Romanian",
        "ru": "Russian", "sm": "Samoan", "sa": "Sanskrit", "gd": "Scots Gaelic",
        "nso": "Sepedi", "sr": "Serbian", "st": "Sesotho", "sn": "Shona",
        "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak", "sl": "Slovenian",
        "so": "Somali", "es": "Spanish", "su": "Sundanese", "sw": "Swahili",
        "sv": "Swedish", "tg": "Tajik", "ta": "Tamil", "tt": "Tatar",
        "te": "Telugu", "th": "Thai", "ti": "Tigrinya", "ts": "Tsonga",
        "tr": "Turkish", "tk": "Turkmen", "ak": "Twi", "uk": "Ukrainian",
        "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese",
        "cy": "Welsh", "xh": "Xhosa", "yi": "Yiddish", "yo": "Yoruba",
        "zu": "Zulu"
    }

    def __init__(self):
        self.session = None

    async def client_ready(self, client, db):
        """Initialize module"""
        self.client = client
        self.db = db
        self._chats = self.db.get("AutoTranslator", "chats", {})
        self.session = aiohttp.ClientSession()

    async def on_unload(self):
        """Called when module is being unloaded"""
        if self.session:
            await self.session.close()

    async def google_translate(self, text: str, target_lang: str) -> str:
        """Translate text using Google Translate API"""
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": target_lang,
            "dt": "t",
            "q": text,
        }

        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data[0][0][0]
                return text
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text

    @loader.command(
        ru_doc="Показать список доступных языков",
        en_doc="Show list of available languages",
        ua_doc="Показати список доступних мов"
    )
    async def tr_langs(self, message):
        """Show list of available languages"""
        langs_text = "\n".join(
            f"<code>{code}</code> - {name}" 
            for code, name in self.SUPPORTED_LANGS.items()
        )
        await utils.answer(message, self.strings("langs_list").format(langs_text))

    @loader.command(
        ru_doc="[язык] - Включить/выключить автоперевод в чате",
        en_doc="[lang] - Enable/disable auto-translation in chat",
        ua_doc="[мова] - Увімкнути/вимкнути автопереклад у чаті"
    )
    async def autotr(self, message):
        """[language_code] - Toggle auto-translation in current chat"""
        chat_id = str(message.chat_id)
        args = utils.get_args_raw(message)

        if chat_id in self._chats:
            old_lang = self._chats[chat_id]
            del self._chats[chat_id]
            self.db.set("AutoTranslator", "chats", self._chats)
            if not args:
                await utils.answer(
                    message,
                    self.strings("disabled").format(f"{old_lang} ({self.SUPPORTED_LANGS[old_lang]})")
                )
                return

        if not args:
            await utils.answer(message, self.strings("no_lang"))
            return

        lang = args.lower()
        if lang not in self.SUPPORTED_LANGS:
            await utils.answer(message, self.strings("invalid_lang"))
            return

        self._chats[chat_id] = lang
        self.db.set("AutoTranslator", "chats", self._chats)
        await utils.answer(
            message, 
            self.strings("enabled").format(lang, self.SUPPORTED_LANGS[lang])
        )

    @loader.watcher()
    async def watcher(self, message):
        """Watcher to translate messages"""
        if not getattr(message, "out", False) or not getattr(message, "text", False):
            return

        chat_id = str(message.chat_id)

        if (
            chat_id not in self._chats
            or message.text.startswith((".", "/"))
            or len(message.text) < 2
        ):
            return

        target_lang = self._chats[chat_id]
        original_text = message.text

        try:
            translated = await self.google_translate(original_text, target_lang)
            if translated and translated != original_text:
                await message.edit(translated)

        except Exception as e:
            logger.error(f"Translation error: {e}")
