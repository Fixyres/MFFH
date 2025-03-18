"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P" 
                                                           
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

import json
import os
from .. import loader, utils

@loader.tds
class AliasManagerMod(loader.Module):
    strings = {
        "name": "AliasManager",
        "no_reply": "<blockquote>❌ <b>Reply to the file</b></blockquote>",
        "restored": "<blockquote>✅ Aliases restored successfully!</blockquote>",
        "cleared": "<blockquote>✅ All aliases cleared successfully!</blockquote>",
        "backed_up": "<blockquote>✅ Aliases backed up successfully!</blockquote>"
    }

    strings_ru = {
        "no_reply": "<blockquote>❌ <b>Ответьте на файл</b></blockquote>",
        "restored": "<blockquote>✅ Алиасы успешно восстановлены!</blockquote>",
        "cleared": "<blockquote>✅ Все алиасы успешно очищены!</blockquote>",
        "backed_up": "<blockquote>✅ Алиасы успешно сохранены!</blockquote>"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    def overwrite_aliases(self, aliases: dict):
        """Перезаписывает алиасы, заменяя старые значения"""
        self.client.loader.aliases.clear()
        for alias, cmd in aliases.items():
            if cmd in self.client.loader.commands:
                self.client.loader.add_alias(alias, cmd)

    @loader.command(
        ru_doc="Ресторнуть алиасы из конфига"
    )
    async def restorealiases(self, message):
        """Restore aliases from config"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            return await utils.answer(message, self.strings("no_reply"))

        file = await reply.download_media()
        with open(file, "r", encoding="utf-8") as f:
            loaded_result = json.load(f)

            aliases = loaded_result.get("aliases", {})

            if not aliases:
                return await utils.answer(message, "❌ No aliases found in the file.")

            self.overwrite_aliases(aliases)
        os.remove(file)
        return await utils.answer(message, self.strings("restored"))

    @loader.command(
        ru_doc="Очистить все алиасы"
    )
    async def clearaliases(self, message):
        """Clear aliases"""
        self.client.loader.aliases.clear()
        return await utils.answer(message, self.strings("cleared"))

    @loader.command(
        ru_doc="Резервное копирование алиасов"
    )
    async def backupaliases(self, message):
        """Backup aliases"""
        backup_file = f"aliases-{(await self.client.get_me()).id}.json"

        backup_data = {
            "aliases": self.client.loader.aliases
        }

        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=4)
        await utils.answer_file(message, f"{os.getcwd()}/{backup_file}")
        os.remove(f"{backup_file}")
        return await utils.answer(message, self.strings("backed_up"))
