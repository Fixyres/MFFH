#           __..--''``---....___   _..._    __
# /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
#///_.-' _..--.'_    \                    `( ) ) // //
#/ (_..-' // (< _     ;_..__               ; `' / ///
# / // // //  `-._,_)' // / ``--...____..-' /// / //
# 🐈 Module writed @ScreamDev 
# 👌 Channel @ScreamModules

import logging
import re

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class AutoCommentMod(loader.Module):
    """Automatically comments under any channels you want"""

    strings = {
        "name": "AutoFheta",
        "disabled": "❌ Disabled",
        "enabled": "✅ Enabled",
        "status_now": "👌 AutoComment was <b>{}</b>!",
        "config_status": "Are we ready to comment?",
        "config_channels": "Under which channels I should comment? (ids)",
    }

    strings_ru = {
        "disabled": "❌ Выключен",
        "enabled": "✅ Включён",
        "status_now": "👌 AutoComment теперь <b>{}</b>!",
        "config_status": "Комментим ли мы?",
        "config_channels": "Под каким каналами я должен комментировать (айди)",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                True,
                lambda: self.strings("config_status"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "channels",
                [],
                lambda: self.strings("config_channels"),
                validator=loader.validators.Series(
                    loader.validators.Union(
                        loader.validators.Integer(),
                    )
                ),
            ),
        )

    @loader.watcher(only_messages=True, only_channels=True)
    async def watcher(self, message):
        # Проверка включения функции автокомментариев
        if not self.config["status"]:
            return
            
        chat = utils.get_chat_id(message)

        # Проверка, находится ли чат в заданных каналах
        if chat not in self.config["channels"]:
            return

        # Извлекаем название из сообщения, если оно в моноширинном шрифте
        match = re.search(r'`([^`]+)`', message.text)
        if match:
            title = match.group(1).strip()
            # Формируем сообщение для комментария
            auto_comment = f".fheta {title}"

            # Отправляем комментарий
            await self.client.send_message(
                entity=chat, message=auto_comment, comment_to=message
            )
            logger.debug(f"commented on {message.id} in {chat}")

    async def commentcmd(self, message):
        """Toggle Module <on/off>"""

        self.config["status"] = not self.config["status"]
        status = (
            self.strings("enabled")
            if self.config["status"]
            else self.strings("disabled")
        )

        await utils.answer(message, self.strings("status_now").format(status))
