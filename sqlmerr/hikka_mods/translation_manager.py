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

# meta banner: https://github.com/sqlmerr/hikka_mods/blob/main/assets/banners/translation_manager.png?raw=true
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/translation_manager.png?raw=true
# meta developer: @sqlmerr_m

import asyncio
import logging

from .. import loader, utils
from hikkatl.tl.patched import Message

log = logging.getLogger(__name__)


@loader.tds
class TranslationManager(loader.Module):
    """Module for managing external modules translations"""

    strings = {
        "name": "TranslationManager",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> No args!",
        "get_txt": "<code>`{}`</code> <b>Translation in </b><code>{}</code> <b>module of language </b><code>{}</code><b>:</b>\n<blockquote>{}</blockquote>\n{}",
        "custom": "<emoji document_id=5962952497197748583>🔧</emoji> <b>Translation is edited</b>",
        "default": "<emoji document_id=5962952497197748583>🔧</emoji> <b>Translation is default</b>",
        "404": "<emoji document_id=5210952531676504517>❌</emoji> <b>Module not found!</b>",
        "success": "<emoji document_id=5255813619702049821>✅</emoji> <b>Success</b>",
        "only_external": "<emoji document_id=5210952531676504517>❌</emoji> <i>You can manage translations in only external mods. To update them use custom language.</i>"
    }

    strings_ru = {
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> Вы не передали аргументы!",
        "get_txt": "<code>`{}`</code> <b>Перевод модуля </b><code>{}</code> <b>в языке </b><code>{}</code><b>:</b>\n<blockquote>{}</blockquote>\n{}",
        "custom": "<emoji document_id=5962952497197748583>🔧</emoji> <b>Перевод изменен</b>",
        "default": "<emoji document_id=5962952497197748583>🔧</emoji> <b>Перевод стандартный</b>",
        "404": "<emoji document_id=5210952531676504517>❌</emoji> <b>Модуль не найден!</b>",
        "success": "<emoji document_id=5255813619702049821>✅</emoji> <b>Успешно</b>",
        "only_external": "<emoji document_id=5210952531676504517>❌</emoji> <i>Ты можешь управлять переводами только в сторонних модулях. Чтобы изменить их, используй кастомный язык.</i>",
        "_cls_doc": "Модуль для управления переводами сторонних модулей"
    }

    async def client_ready(self):
        while not self.lookup("Loader").fully_loaded:
            await asyncio.sleep(0.5)

        mods = self.get("mods")
        if not mods:
            return
        for mod, tr in mods.items():
            module = self.lookup(mod)
            if not module:
                continue
            if module.__origin__.startswith("<core"):
                log.info(f"Can't load translations for core module")
                continue
            for lang, st in tr.items():
                for k, v in st.items():
                    if hasattr(module, f"strings_{lang}"):
                        strings = getattr(module, f"strings_{lang}")
                        strings[k] = v
                        setattr(module, f"strings_{lang}", strings)
                    else:
                        module.strings._base_strings[k] = v
        log.info("Custom translations loaded")

    def get_one(self, mod: str, lang: str, name: str):
        if not (strings := self.get("mods", {}).get(mod)) or not strings.get(lang):
            module = self.lookup(mod)
            if not module:
                raise ValueError("404")
            if module.__origin__.startswith("<core"):
                raise ValueError("only_external")
            if hasattr(module, f"strings_{lang}"):
                return getattr(module, f"strings_{lang}", {}).get(name)
            return module.strings._base_strings.get(name), False
        return strings.get(lang, {}).get(name), True

    def set_one(self, mod: str, lang: str, name: str, val: str):
        module = self.lookup(mod)
        if not module:
            raise ValueError("404")
        if module.__origin__.startswith("<core"):
            raise ValueError("only_external")
        if hasattr(module, f"strings_{lang}"):
            strings = getattr(module, f"strings_{lang}")
            strings[name] = val
            setattr(module, f"strings_{lang}", strings)
        else:
            module.strings._base_strings[name] = val

        mods = self.get("mods", {})
        db_strings = mods.get(mod, {})
        lang_strings = db_strings.get(lang, {})
        lang_strings[name] = val
        db_strings[lang] = lang_strings

        mods[mod] = db_strings
        self.set("mods", mods)

    def del_one(self, mod: str, lang: str, name: str):
        mods = self.get("mods", {})
        if not ((strings := mods.get(mod)) and strings.get(lang)):
            return

        lang_strings = strings.get(lang)
        if not lang_strings.get(name):
            return

        del lang_strings[name]
        strings[lang] = lang_strings
        mods[mod] = strings
        self.set("mods", mods)

    @loader.command(ru_doc="[модуль] [язык] [ключ] - Получить перевод")
    async def trget(self, message: Message):
        """[mod] [lang] [key] - Get current translation"""
        if not (args := utils.get_args_raw(message).split()) or len(args) < 3:
            await utils.answer(message, self.strings("no_args"))
            return

        mod, lang, key = args
        try:
            tr, is_custom = self.get_one(mod, lang, key)
        except ValueError as e:
            await utils.answer(message, self.strings(e.args[0]))
            return

        await utils.answer(message, self.strings("get_txt").format(key, mod, lang, utils.escape_html(tr), self.strings("custom") if is_custom else self.strings("default")))

    @loader.command(ru_doc="[модуль] [язык] [ключ] [значение] - Изменить перевод")
    async def trset(self, message: Message):
        """[mod] [lang] [key] [val] - Set translation"""
        if not (args := utils.get_args_raw(message).split(maxsplit=3)) or len(args) < 4:
            await utils.answer(message, self.strings("no_args"))
            return
        mod, lang, key, val = args
        try:
            self.set_one(mod, lang, key, val)
        except ValueError as e:
            await utils.answer(message, self.strings(e.args[0]))
            return
        await utils.answer(message, self.strings("success"))

    @loader.command(ru_doc="[модуль] [язык] [ключ] - Удалить кастомный перевод")
    async def trdel(self, message: Message):
        """[mod] [lang] [key] - Delete custom translation"""
        if not (args := utils.get_args_raw(message).split()) or len(args) < 3:
            await utils.answer(message, self.strings("no_args"))
            return

        mod, lang, key = args
        try:
            self.del_one(mod, lang, key)
        except ValueError as e:
            await utils.answer(message, self.strings(e.args[0]))
            return
        await utils.answer(message, self.strings("success"))
