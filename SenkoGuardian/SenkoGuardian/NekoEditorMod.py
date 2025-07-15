
#  This file is part of SenkoGuardianModules
#  Copyright (c) 2025 Senko
#  This software is released under the MIT License.
#  https://opensource.org/licenses/MIT

from hikkatl.types import Message
from .. import loader, utils
import random

@loader.tds
class NekoEditorMod(loader.Module):
    """Neko-редактор сообщений | Владелец: @SstAngelStar"""
    strings = {
        "name": "NekoEditor",
        "owner": "@SstAngelStar"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled",
                False,
                "Автоматическое редактирование",
                validator=loader.validators.Boolean()
            )
        )

    async def nekoedcmd(self, message: Message):
        """Управление Neko-режимом | .nekoed [on/off]"""
        args = utils.get_args_raw(message)
        me = await message.client.get_me()
        is_premium = getattr(me, 'premium', False)
        if not args:
            status = "включён" if self.config["enabled"] else "выключен"
            return await utils.answer(message, f"🐱 NekoEditor: {status}")
        if args.lower() in ["on", "вкл", "1"]:
            self.config["enabled"] = True
            if is_premium:
                await utils.answer(message, '<emoji document_id="5335044582218412321">☺️</emoji> Режим включён! Nya~')
            else:
                await utils.answer(message, "🐾 Режим включён! Nya~")
        elif args.lower() in ["off", "выкл", "0"]:
            self.config["enabled"] = False
            if is_premium:
                await utils.answer(message, '<emoji document_id="5377309873614627829">👌</emoji> Режим выключен... &gt;_&lt;')
            else:
                await utils.answer(message, "🌀 Режим выключен... &gt;_&lt;")
        self.db.set("NekoEditor", "enabled", self.config["enabled"])


    async def watcher(self, message: Message):
        """Автоматическое Neko-редактирование (без упоминания владельца)"""
        if (
            not self.config["enabled"]
            or not getattr(message, "out", False)
            or getattr(message, "fwd_from", None)
            or getattr(message, "forward", None)
            or not message.text
            or "nekoed" in message.raw_text.lower() 
        ):
            return
        neko_words = ["Nya~", "UwU", "OwO", ">_<", "^^", "(≧▽≦)"]
        modified_text = message.raw_text
        neko_word = random.choice(neko_words)
        modified_text = f"{neko_word} {modified_text}" if random.random() < 0.5 else f"{modified_text} {neko_word}"
        replacements = {
            "р": "w",
            "л": "w",
            "но": "ня",
            "на": "ня"
        }
        
        for old, new in replacements.items():
            modified_text = modified_text.replace(old, new)
        modified_text = utils.escape_html(modified_text).replace("&amp;gt;_&amp;lt;", "&gt;_&lt;")
        try:
            await message.edit(modified_text)
        except Exception:
            pass
