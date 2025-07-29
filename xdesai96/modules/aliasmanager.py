# meta developer: @xdesai

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
        "backed_up": "<blockquote>✅ Aliases backed up successfully!</blockquote>",
    }

    strings_ru = {
        "no_reply": "<blockquote>❌ <b>Ответьте на файл</b></blockquote>",
        "restored": "<blockquote>✅ Псевдонимы успешно восстановлены!</blockquote>",
        "cleared": "<blockquote>✅ Все псевдонимы успешно очищены!</blockquote>",
        "backed_up": "<blockquote>✅ Псевдонимы успешно сохранены!</blockquote>",
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

    @loader.command(ru_doc="Ресторнуть алиасы из конфига")
    async def restorealiases(self, message):
        """Restore aliases from config"""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            return await utils.answer(message, self.strings["no_reply"])

        file = await reply.download_media()
        with open(file, "r", encoding="utf-8") as f:
            loaded_result = json.load(f)

            aliases = loaded_result.get("aliases", {})

            if not aliases:
                return await utils.answer(message, "❌ No aliases found in the file.")

            self.overwrite_aliases(aliases)
        os.remove(file)
        return await utils.answer(message, self.strings["restored"])

    @loader.command(ru_doc="Очистить все алиасы")
    async def clearaliases(self, message):
        """Clear aliases"""
        self.client.loader.aliases.clear()
        return await utils.answer(message, self.strings["cleared"])

    @loader.command(ru_doc="Резервное копирование алиасов")
    async def backupaliases(self, message):
        """Backup aliases"""
        backup_file = f"aliases-{(await self.client.get_me()).id}.json"

        backup_data = {"aliases": self.client.loader.aliases}

        with open(backup_file, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=4)
        await utils.answer_file(message, f"{os.getcwd()}/{backup_file}")
        os.remove(f"{backup_file}")
        return await utils.answer(message, self.strings["backed_up"])
