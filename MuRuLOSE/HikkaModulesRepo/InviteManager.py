from telethon.tl.functions.messages import ExportChatInviteRequest, EditExportedChatInviteRequest
from telethon.types import Message
from .. import loader, utils
from ..inline.types import InlineCall
import logging
import datetime

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    Module Name
"""

# scopes:

# 🔒      Licensed under the GNU AGPLv3

# meta banner: https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/assets/modbanners/inumber.png
# meta desc: Manage Telegram invite links
# meta developer: @BruhHikkaModules

logger = logging.getLogger(__name__)

@loader.tds
class InviteManager(loader.Module):
    """Manage Telegram invite links"""

    strings = {
        "name": "InviteManager",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> No arguments provided",
        "no_channel": "<emoji document_id=5210952531676504517>❌</emoji> Please specify a channel or use in a channel",
        "created": "<emoji document_id=5413334818047940135>✅</emoji> Invite link created: <code>{link}</code>",
        "select_action": "Select an action for the invite link: <code>{link}</code>",
        "revoked": "<emoji document_id=5413334818047940135>✅</emoji> Invite link revoked",
        "select_expiry": "Select expiration period for the invite link: <code>{link}</code>",
        "select_limit": "Select usage limit for the invite link: <code>{link}</code>",
        "updated_expiry": "<emoji document_id=5413334818047940135>✅</emoji> Expiry updated to {date}",
        "updated_limit": "<emoji document_id=5413334818047940135>✅</emoji> Usage limit updated to {limit}",
        "invalid_date": "<emoji document_id=5210952531676504517>❌</emoji> Invalid date format. Use YYYY-MM-DD HH:MM",
        "invalid_limit": "<emoji document_id=5210952531676504517>❌</emoji> Invalid number for usage limit",
        "invalid_link": "<emoji document_id=5210952531676504517>❌</emoji> Invalid invite link",
        "chat_required": "<emoji document_id=5210952531676504517>❌</emoji> Please use this command in the target channel or specify the channel",
    }

    strings_ru = {
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> Аргументы не указаны",
        "no_channel": "<emoji document_id=5210952531676504517>❌</emoji> Укажите канал или используйте в канале",
        "created": "<emoji document_id=5413334818047940135>✅</emoji> Ссылка-приглашение создана: <code>{link}</code>",
        "select_action": "Выберите действие для ссылки: <code>{link}</code>",
        "revoked": "<emoji document_id=5413334818047940135>✅</emoji> Ссылка отозвана",
        "select_expiry": "Выберите период действия для ссылки: <code>{link}</code>",
        "select_limit": "Выберите лимит использований для ссылки: <code>{link}</code>",
        "updated_expiry": "<emoji document_id=5413334818047940135>✅</emoji> Дата истечения обновлена: {date}",
        "updated_limit": "<emoji document_id=5413334818047940135>✅</emoji> Лимит использований обновлен: {limit}",
        "invalid_date": "<emoji document_id=5210952531676504517>❌</emoji> Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ",
        "invalid_limit": "<emoji document_id=5210952531676504517>❌</emoji> Неверное число для лимита",
        "invalid_link": "<emoji document_id=5210952531676504517>❌</emoji> Неверная ссылка-приглашение",
        "chat_required": "<emoji document_id=5210952531676504517>❌</emoji> Используйте команду в целевом канале или укажите канал",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(ru_doc="Создать ссылку-приглашение для канала")
    async def createinvite(self, message: Message):
        """Create an invite link for a channel"""
        args = utils.get_args_raw(message)
        chat = None

        if args:
            try:
                chat = await self.client.get_entity(args)
            except Exception as e:
                logger.error(f"Failed to get entity: {e}")
                await utils.answer(message, self.strings["no_channel"])
                return
        else:
            if message.is_channel or message.is_group:
                chat = message.peer_id
            else:
                await utils.answer(message, self.strings["no_channel"])
                return

        try:
            result = await self.client(
                ExportChatInviteRequest(
                    peer=chat,
                    legacy_revoke_permanent=False,
                    request_needed=False,
                    title="Invite Link"
                )
            )
            link = result.link
            await utils.answer(message, self.strings["created"].format(link=link))
        except Exception as e:
            logger.error(f"Error creating invite: {e}")
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> Failed to create invite link")

    @loader.command(ru_doc="[ссылка] [канал] - Редактировать ссылку-приглашение через инлайн-кнопки")
    async def editinvite(self, message: Message):
        """[link] [channel] - Edit an invite link with inline buttons"""
        args = utils.get_args_split_by(message, separator=" ")
        if len(args) < 2:
            if message.is_channel or message.is_group:
                chat = message.peer_id
                link = args[0] if args else None
            else:
                await utils.answer(message, self.strings["chat_required"])
                return
        else:
            link, chat_arg = args[0], args[1]
            try:
                chat = await self.client.get_entity(chat_arg)
            except Exception as e:
                logger.error(f"Failed to get entity: {e}")
                await utils.answer(message, self.strings["no_channel"])
                return

        if not link:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            if not link.startswith("https://t.me/"):
                raise ValueError("Invalid invite link")
            
            await self.inline.form(
                message=message,
                text=self.strings["select_action"].format(link=link),
                reply_markup=[
                    [
                        {"text": "Revoke", "callback": self._revoke_link, "args": (link, chat)},
                        {"text": "Set Expiry", "callback": self._prompt_expiry, "args": (link, chat)},
                    ],
                    [
                        {"text": "Set Usage Limit", "callback": self._prompt_limit, "args": (link, chat)},
                    ]
                ]
            )
        except Exception as e:
            logger.error(f"Error initiating edit: {e}")
            await utils.answer(message, self.strings["invalid_link"])

    async def _revoke_link(self, call: InlineCall, link: str, chat):
        try:
            await self.client(
                EditExportedChatInviteRequest(
                    peer=chat,
                    link=link,
                    revoked=True
                )
            )
            await call.edit(
                text=self.strings["revoked"],
                reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
            )
        except Exception as e:
            logger.error(f"Error revoking link: {e}")
            await call.edit(
                text="<emoji document_id=5210952531676504517>❌</emoji> Failed to revoke link",
                reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
            )

    async def _prompt_expiry(self, call: InlineCall, link: str, chat):
        await call.edit(
            text=self.strings["select_expiry"].format(link=link),
            reply_markup=[
                [
                    {"text": "1 Hour", "callback": self._set_expiry, "args": (link, chat, 1, "hours")},
                    {"text": "1 Day", "callback": self._set_expiry, "args": (link, chat, 1, "days")},
                ],
                [
                    {"text": "1 Week", "callback": self._set_expiry, "args": (link, chat, 1, "weeks")},
                    {"text": "1 Month", "callback": self._set_expiry, "args": (link, chat, 1, "months")},
                ],
                [
                    {"text": "No Expiry", "callback": self._set_expiry, "args": (link, chat, None, None)},
                    {"text": "Cancel", "callback": self._back_to_menu, "args": (link, chat)},
                ]
            ]
        )

    async def _set_expiry(self, call: InlineCall, link: str, chat, value: int, unit: str):
        expiry_date = None
        if value is not None and unit is not None:
            try:
                now = datetime.datetime.now()
                if unit == "hours":
                    expiry_date = now + datetime.timedelta(hours=value)
                elif unit == "days":
                    expiry_date = now + datetime.timedelta(days=value)
                elif unit == "weeks":
                    expiry_date = now + datetime.timedelta(weeks=value)
                elif unit == "months":
                    expiry_date = now + datetime.timedelta(days=value * 30)  # Approximate month
            except Exception as e:
                logger.error(f"Error calculating expiry: {e}")
                await call.edit(
                    text=self.strings["invalid_date"],
                    reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
                )
                return

        try:
            await self.client(
                EditExportedChatInviteRequest(
                    peer=chat,
                    link=link,
                    expire_date=expiry_date
                )
            )
            expiry_text = expiry_date.strftime("%Y-%m-%d %H:%M") if expiry_date else "no expiry"
            await call.edit(
                text=self.strings["updated_expiry"].format(date=expiry_text),
                reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
            )
        except Exception as e:
            logger.error(f"Error setting expiry: {e}")
            await call.edit(
                text="<emoji document_id=5210952531676504517>❌</emoji> Failed to update expiry",
                reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
            )

    async def _prompt_limit(self, call: InlineCall, link: str, chat):
        await call.edit(
            text=self.strings["select_limit"].format(link=link),
            reply_markup=[
                [
                    {"text": "1 Use", "callback": self._set_limit, "args": (link, chat, 1)},
                    {"text": "10 Uses", "callback": self._set_limit, "args": (link, chat, 10)},
                ],
                [
                    {"text": "50 Uses", "callback": self._set_limit, "args": (link, chat, 50)},
                    {"text": "100 Uses", "callback": self._set_limit, "args": (link, chat, 100)},
                ],
                [
                    {"text": "Unlimited", "callback": self._set_limit, "args": (link, chat, None)},
                    {"text": "Cancel", "callback": self._back_to_menu, "args": (link, chat)},
                ]
            ]
        )

    async def _set_limit(self, call: InlineCall, link: str, chat, usage_limit: int):
        try:
            await self.client(
                EditExportedChatInviteRequest(
                    peer=chat,
                    link=link,
                    usage_limit=usage_limit
                )
            )
            limit_text = str(usage_limit) if usage_limit is not None else "unlimited"
            await call.edit(
                text=self.strings["updated_limit"].format(limit=limit_text),
                reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
            )
        except Exception as e:
            logger.error(f"Error setting limit: {e}")
            await call.edit(
                text="<emoji document_id=5210952531676504517>❌</emoji> Failed to update limit",
                reply_markup=[[{"text": "Back", "callback": self._back_to_menu, "args": (link, chat)}]]
            )

    async def _back_to_menu(self, call: InlineCall, link: str, chat):
        await call.edit(
            text=self.strings["select_action"].format(link=link),
            reply_markup=[
                [
                    {"text": "Revoke", "callback": self._revoke_link, "args": (link, chat)},
                    {"text": "Set Expiry", "callback": self._prompt_expiry, "args": (link, chat)},
                ],
                [
                    {"text": "Set Usage Limit", "callback": self._prompt_limit, "args": (link, chat)},
                ]
            ]
        )