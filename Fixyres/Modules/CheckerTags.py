#meta deleloper: @moduleslist
#meta banner: https://envs.sh/J6r.jpg

from .. import loader, utils
from telethon.tl.types import Message
from telethon.tl.functions.channels import CreateChannelRequest, UpdateUsernameRequest, JoinChannelRequest
from datetime import datetime
import asyncio
import pytz
import logging

logger = logging.getLogger(__name__)

@loader.tds
class CheckerUsernamesMod(loader.Module):
    """💡 Smart username checker with fast checking system"""

    strings = {
        "name": "CheckerUsernames",
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Username checker disabled</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Username checker enabled</b>", 
        "status": "<emoji document_id=5449687343931859785>🔄</emoji> <b>Checker status: {}\n</b><emoji document_id=5974081491901091242>⏰</emoji> <b>Check interval: {} seconds</b>",
        "set_interval": "<emoji document_id=5776375003280838798>✅</emoji> <b>New check interval set: {} seconds</b>",
        "invalid_interval": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Invalid interval! Use number ≥10 seconds</b>"
    }

    strings_ru = {
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Чекер юзернеймов выключен</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Чекер юзернеймов включен</b>",
        "status": "<emoji document_id=5449687343931859785>🔄</emoji> <b>Статус чекера: {}\n</b><emoji document_id=5974081491901091242>⏰</emoji> <b>Интервал проверки: {} секунд</b>",
        "set_interval": "<emoji document_id=5776375003280838798>✅</emoji> <b>Установлен новый интервал: {} секунд</b>",
        "invalid_interval": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Неверный интервал! Используйте число ≥10 секунд</b>"
    }

    strings_ua = {
        "off": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Чекер юзернеймів вимкнено</b>",
        "on": "<emoji document_id=5776375003280838798>✅</emoji> <b>Чекер юзернеймів увімкнено</b>",
        "status": "<emoji document_id=5449687343931859785>🔄</emoji> <b>Статус чекера: {}\n</b><emoji document_id=5974081491901091242>⏰</emoji> <b>Інтервал перевірки: {} секунд</b>",
        "set_interval": "<emoji document_id=5776375003280838798>✅</emoji> <b>Встановлено новий інтервал: {} секунд</b>",
        "invalid_interval": "<emoji document_id=5350311258220404874>❗️</emoji> <b>Невірний інтервал! Використовуйте число ≥10 секунд</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "usernames",
                ["example", "test"],
                "List of usernames to check",
                validator=loader.validators.Series(loader.validators.String())
            ),
            loader.ConfigValue(
                "check_interval",
                10,
                "Check interval in seconds (minimum 10)",
                validator=loader.validators.Integer(minimum=10)
            ),
            loader.ConfigValue(
                "channel_text",
                "🔒 This username is now occupied",
                "Text to send in created channel",
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "timezone",
                "UTC",
                "Your timezone (use .timezones to see list)",
                validator=loader.validators.String()
            )
        )
        self.checker_task = None

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        # Загружаем состояние из базы данных
        self.active = self.get("active", False)
        if self.checker_task:
            self.checker_task.cancel()
        self.checker_task = asyncio.create_task(self._checker())
        
        await client(JoinChannelRequest("@moduleslist"))

        # Если был активен при перезагрузке, отправляем уведомление
        if self.active:
            await self._client.send_message(
                "me",
                "🔄 Checker has been restored after restart"
            )

    async def _checker(self):
        while True:
            if not self.active:
                await asyncio.sleep(10)
                continue

            try:
                current_time = datetime.now(pytz.timezone(self.config["timezone"])).strftime("%H:%M:%S")

                for username in self.config["usernames"]:
                    try:
                        if len(username) < 5 or len(username) > 32:
                            logger.error(f"Invalid username length: {username}")
                            continue

                        try:
                            await self._client.get_entity(f"@{username}")
                        except ValueError:
                            await self._client.send_message(
                                "me",
                                f"🔄 Username @{username} is free! Creating channel..."
                            )

                            channel = await self._client(
                                CreateChannelRequest(
                                    title=f"Reserved @{username}",
                                    about=self.config["channel_text"]
                                )
                            )

                            await self._client(
                                UpdateUsernameRequest(
                                    channel.chats[0].id,
                                    username
                                )
                            )

                            await self._client.send_message(
                                channel.chats[0].id,
                                self.config["channel_text"]
                            )

                            await self._client.send_message(
                                "me",
                                f"🎯 Username caught!\n👤 @{username}\n⏰ Time: {current_time}\n⚡️ Channel: {channel.chats[0].id}"
                            )

                    except Exception as e:
                        await self._client.send_message(
                            "me",
                            f"❌ Error checking @{username}: {str(e)}"
                        )

            except Exception as e:
                await self._client.send_message(
                    "me",
                    f"❌ Main checker error: {str(e)}"
                )

            await asyncio.sleep(self.config["check_interval"])

    @loader.command(
        ru_doc="Включить/выключить чекер юзернеймов",
        ua_doc="Увімкнути/вимкнути чекер юзернеймів", 
        en_doc="Toggle username checker"
    )
    async def checker(self, message: Message):
        """Toggle username checker"""
        self.active = not self.active
        # Сохраняем состояние в базу данных
        self.set("active", self.active)

        if not self.active:
            # Очищаем логгер при выключении
            logger.handlers.clear()

        status = "✅ Enabled" if self.active else "❌ Disabled"
        await utils.answer(
            message,
            self.strings("status").format(
                status,
                self.config["check_interval"]
            )
        )

    @loader.command(
        ru_doc="<секунды> - Установить интервал проверки в секундах (≥10)",
        ua_doc="<секунди> - Встановити інтервал перевірки в секундах (≥10)",
        en_doc="<seconds> - Set check interval in seconds (≥10)"
    )
    async def interval(self, message: Message):
        """<seconds> - Set check interval in seconds (≥10)"""
        args = utils.get_args_raw(message)

        if not args or not args.isdigit() or int(args) < 10:
            await utils.answer(message, self.strings("invalid_interval"))
            return

        self.config["check_interval"] = int(args)
        await utils.answer(
            message,
            self.strings("set_interval").format(args)
        )

    @loader.command(
        ru_doc="Показать все доступные таймзоны",
        ua_doc="Показати всі доступні часові пояси",
        en_doc="Show all available timezones"
    )
    async def timezones(self, message: Message):
        """Show all available timezones"""
        await message.delete()
        await self.invoke(
            "e",
            "import pytz; print('\\n'.join(pytz.all_timezones))",
            message.peer_id
        )