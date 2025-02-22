# meta developer: @idiotcoders
# scope: hikka_min 1.6.3


import io
import logging

import telethon

from .. import loader, utils
from ..inline.types import InlineCall


@loader.tds
class PromoteMod(loader.Module):
    """Managing administrators rights in chats."""

    strings = {
        "name": "Promote",
        "not_a_chat": "<emoji document_id=5312526098750252863>❌</emoji> <b>The command cannot be run in private messages.</b>",
        "no_rights": "<emoji document_id=5318764049121420145>🫤</emoji> <b>I have no administrator rights or cannot promote" \
                     " and demote administrators.</b>",
        "no_user": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>You should specify an user.</b>",
        "demoted": "<emoji document_id=5458403743835889060>😂</emoji> <b>{name} was demoted to an regular user.</b>",
        "promoted_full": "<emoji document_id=5271557007009128936>👑</emoji> <b>{name} was promoted to an administrator" \
                        " with full rights.</b>\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "promoted": "<emoji document_id=5451786809845491357>🫣</emoji> <b>{name} was promoted to an administrator.</b>\n" \
                    "<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "choose_rights": "<emoji document_id=5271557007009128936>👑</emoji> <b>Choose administrator rights for {name}</b>" \
                         "\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank</b>: {rank}",
        "right_change_info": "{emoji} Change info {channel_or_chat}",
        "of_channel": "of channel", "of_chat": "of chat",
        "right_post_messages": "{emoji} Post messages",
        "right_edit_messages": "{emoji} Edit posts",
        "right_delete_messages": "{emoji} Delete messages",
        "right_ban_users": "{emoji} Restrict users",
        "right_invite_users": "{emoji} Invite users",
        "right_pin_messages": "{emoji} Pin messages",
        "right_add_admins": "{emoji} Promote administrators",
        "right_anonymous": "{emoji} Anonymous",
        "right_manage_call": "{emoji} Manage calls",
        "confirm": "✅ Confirm",
    }

    strings_ru = {
        "name": "Promote",
        "not_a_chat": "<emoji document_id=5312526098750252863>❌</emoji> <b>Команда не может быть запущена в личных сообщениях.</b>",
        "no_rights": "<emoji document_id=5318764049121420145>🫤</emoji> <b>У меня нет прав администратора в этом чате" \
                     " или я не могу изменять права администраторов.</b>",
        "no_user": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Вы не указали пользователя.</b>",
        "demoted": "<emoji document_id=5458403743835889060>😂</emoji> <b>С {name} сняты права администратора.</b>",
        "promoted_full": "<emoji document_id=5271557007009128936>👑</emoji> <b>{name} повышен до администратора " \
                        "с полными правами.</b>\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Должность:</b> {rank}",
        "promoted": "<emoji document_id=5451786809845491357>🫣</emoji> <b>{name} повышен до администратора.</b>\n" \
                    "<emoji document_id=5470060791883374114>✍️</emoji> <b>Должность:</b> {rank}",
        "choose_rights": "<emoji document_id=5271557007009128936>👑</emoji> <b>Выберите, какие права вы хотите дать " \
                         "{name}</b>\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Должность</b>: {rank}",
        "right_change_info": "{emoji} Изменение профиля {channel_or_chat}",
        "of_channel": "канала", "of_chat": "чата",
        "right_post_messages": "{emoji} Публиковать посты",
        "right_edit_messages": "{emoji} Изменять посты",
        "right_delete_messages": "{emoji} Удалять сообщения",
        "right_ban_users": "{emoji} Ограничивать пользователей",
        "right_invite_users": "{emoji} Добавлять пользователей",
        "right_pin_messages": "{emoji} Закреплять сообщения",
        "right_add_admins": "{emoji} Назначать администраторов",
        "right_anonymous": "{emoji} Анонимность",
        "right_manage_call": "{emoji} Управление звонками",
        "confirm": "✅ Подтвердить",
        "_cls_doc": "Управление правами администраторов в чатах."
    }


    async def client_ready(self, client, db):
        self.client = client
        self.logger = logging.getLogger(__name__)


    @loader.command(
        ru_doc="<пользователь> — Снятие прав администратора с пользователя."
    )
    async def demotecmd(self, message: telethon.types.Message):
        """<user> — Demote an administrator to a user."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        user_id = None
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
        else:
            user_id = await utils.get_target(message)

        if (not chat.admin_rights or not chat.admin_rights.add_admins) and not chat.creator:
            return await utils.answer(message, self.strings("no_rights", message))
        if not user_id:
            return await utils.answer(
                message, self.strings("no_user", message)
            )

        user = await message.client.get_entity(
            user_id
        )
        try:
            await message.client(
                telethon.tl.functions.channels.EditAdminRequest(
                    message.chat_id, user.id,
                    telethon.types.ChatAdminRights(
                        other=False,
                        change_info=None,
                        post_messages=None,
                        edit_messages=None,
                        delete_messages=None,
                        ban_users=None,
                        invite_users=None,
                        pin_messages=None,
                        add_admins=None,
                        anonymous=None,
                        manage_call=None,
                        manage_topics=None
                    ),
                    ""
                )
            )
        except telethon.errors.ChatAdminRequiredError:
            return await utils.answer(message, self.strings("no_rights", message))

        await utils.answer(
            message, self.strings("demoted", message).format(
                name=user.first_name
            )
        )


    @loader.command(
        ru_doc="<пользователь> [роль (aka префикс)] — Повышение пользователя до администратора с полными правами."
    )
    async def fullrightscmd(self, message: telethon.types.Message):
        """<user> [role (aka [prefix])] — Promote an user to administrator with full rights."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        rank, user_id = "Admin", None
        chat = await message.get_chat()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
            if args:
                rank = args
        else:
            user_id = await utils.get_target(message)
            if len(args.split()) > 1:
                rank = " ".join(args.split()[1:])

        if (not chat.admin_rights or not chat.admin_rights.add_admins) and not chat.creator:
            return await utils.answer(message, self.strings("no_rights", message))
        if not user_id:
            return await utils.answer(
                message, self.strings("no_user", message)
            )

        user = await message.client.get_entity(
            user_id
        )
        try:
            await message.client(
                telethon.tl.functions.channels.EditAdminRequest(
                    message.chat_id, user.id,
                    telethon.types.ChatAdminRights(
                        other=True,
                        change_info=True,
                        post_messages=True if chat.broadcast else None,
                        edit_messages=True if chat.broadcast else None,
                        delete_messages=True,
                        ban_users=True,
                        invite_users=True,
                        add_admins=True,
                        anonymous=None,
                        pin_messages=True if not chat.broadcast else None,
                        manage_call=True if not chat.broadcast else None
                    ),
                    rank
                )
            )
        except telethon.errors.ChatAdminRequiredError:
            return await utils.answer(message, self.strings("no_rights", message))

        await utils.answer(
            message,
            self.strings("promoted_full", message).format(
                name=user.first_name,
                rank=rank
            )
        )


    @loader.command(
        ru_doc="<пользователь> [роль (aka префикс)] — Повышение пользователя до администратора."
    )
    async def promotecmd(self, message: telethon.types.Message):
        """<user> [role (aka [prefix])] — Promote an user to administrator."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        rank, user_id = "Admin", None
        chat = await message.get_chat()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
            if args:
                rank = args
        else:
            user_id = await utils.get_target(message)
            if len(args.split()) > 1:
                rank = " ".join(args.split()[1:])

        if (not chat.admin_rights or not chat.admin_rights.add_admins) and not chat.creator:
            return await utils.answer(message, self.strings("no_rights", message))
        if not user_id:
            return await utils.answer(
                message, self.strings("no_user", message)
            )

        user = await message.client.get_entity(
            user_id
        )

        rights = {
            "change_info": False,
            "post_messages": False,
            "edit_messages": False,
            "delete_messages": False,
            "ban_users": False,
            "invite_users": False,
            "pin_messages": False,
            "add_admins": False,
            "anonymous": False,
            "manage_call": False,
            "": False
        }

        markup = []
        reply_markup = []

        markup.append(
            {
                "text": self.strings('right_change_info').format(
                    emoji='✏',
                    channel_or_chat=self.strings('of_channel') if chat.broadcast else self.strings('of_chat')
                ),
                "callback": self._ch_rights,
                "args": [["change_info", True], rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings('right_delete_messages').format(
                    emoji='🗑'
                ),
                "callback": self._ch_rights,
                "args": [["delete_messages", True], rights, chat, rank, user]
            },
        )
        if chat.broadcast:
            markup.append(
                {
                    "text": self.strings('right_post_messages').format(
                        emoji='✉',
                    ),
                    "callback": self._ch_rights,
                    "args": [["post_messages", True], rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings('right_edit_messages').format(
                        emoji='✏',
                    ),
                    "callback": self._ch_rights,
                    "args": [["edit_messages", True], rights, chat, rank, user]
                },
            )
        markup.append(
            {
                "text": self.strings('right_ban_users').format(
                    emoji='⛔',
                ),
                "callback": self._ch_rights,
                "args": [["ban_users", True], rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings('right_pin_messages').format(
                    emoji='📌',
                ),
                "callback": self._ch_rights,
                "args": [["pin_messages", True], rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings('right_add_admins').format(
                    emoji='👑',
                ),
                "callback": self._ch_rights,
                "args": [["add_admins", True], rights, chat, rank, user]
            },
        )
        if not chat.broadcast:
            markup.append(
                {
                    "text": self.strings('right_manage_call').format(
                        emoji='📞'
                    ),
                    "callback": self._ch_rights,
                    "args": [["manage_call", True], rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings('right_invite_users').format(
                        emoji='➕',
                    ),
                    "callback": self._ch_rights,
                    "args": [["invite_users", True], rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings('right_anonymous').format(
                        emoji='🎭',
                    ),
                    "callback": self._ch_rights,
                    "args": [["anonymous", True], rights, chat, rank, user]
                },
            )

        kb = []
        for i in markup:
            if len(kb) == 2:
                reply_markup.append(kb)
                kb = []
            kb.append(i)
        if kb != [] and kb not in reply_markup:
            reply_markup.append(kb)

        reply_markup.append([
            {
                "text": self.strings("confirm"),
                "callback": self._inline_promote,
                "args": [rights, chat, rank, user]
            }
        ])


        await self.inline.form(
            message=message,
            text=self.strings("choose_rights").format(
                name=user.first_name,
                rank=rank
            ),
            silent=True,
            reply_markup=reply_markup
        )


    async def _ch_rights(self, call: InlineCall, right: str, all_rights: dict, chat, rank: str, user):
        all_rights[right[0]] = right[1]

        markup = []
        reply_markup = []

        markup.append(
            {
                "text": self.strings("right_change_info").format(
                    emoji='✏' if not all_rights.get('change_info', False) else '✅',
                    channel_or_chat=self.strings('of_channel') if chat.broadcast else self.strings('of_chat')
                ),
                "callback": self._ch_rights,
                "args": [["change_info", not all_rights.get("change_info")], all_rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings("right_delete_messages").format(
                    emoji='🗑' if not all_rights.get('delete_messages', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["delete_messages", not all_rights.get("delete_messages", False)], all_rights, chat, rank, user]
            },
        )
        if chat.broadcast:
            markup.append(
                {
                    "text": self.strings("right_post_messages").format(
                        emoji='✉' if not all_rights.get('post_messages', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["post_messages", not all_rights.get("post_messages", False)], all_rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings("right_edit_messages").format(
                        emoji='✏' if not all_rights.get('edit_messages', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["edit_messages", not all_rights.get("edit_messages", False)], all_rights, chat, rank, user]
                },
            )
        markup.append(
            {
                "text": self.strings("right_ban_users").format(
                    emoji='⛔' if not all_rights.get('ban_users', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["ban_users", not all_rights.get("ban_users", False)], all_rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings("right_pin_messages").format(
                    emoji='📌' if not all_rights.get('pin_messages', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["pin_messages", not all_rights.get("pin_messages", False)], all_rights, chat, rank, user]
            },
        )
        markup.append(
            {
                "text": self.strings("right_add_admins").format(
                    emoji='👑' if not all_rights.get('add_admins', False) else '✅'
                ),
                "callback": self._ch_rights,
                "args": [["add_admins", not all_rights.get("add_admins", False)], all_rights, chat, rank, user]
            },
        )
        if not chat.broadcast:
            markup.append(
                {
                    "text": self.strings("right_manage_call").format(
                        emoji='📞' if not all_rights.get('manage_call', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["manage_call", not all_rights.get("manage_call", False)], all_rights, chat, rank, user]
                }
            )
            markup.append(
                {
                    "text": self.strings("right_invite_users").format(
                        emoji='➕' if not all_rights.get('invite_users', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["invite_users", not all_rights.get("invite_users", False)], all_rights, chat, rank, user]
                },
            )
            markup.append(
                {
                    "text": self.strings("right_anonymous").format(
                        emoji='🎭' if not all_rights.get('anonymous', False) else '✅'
                    ),
                    "callback": self._ch_rights,
                    "args": [["anonymous", not all_rights.get("anonymous", False)], all_rights, chat, rank, user]
                },
            )

        kb = []
        for i in markup:
            if len(kb) == 2:
                reply_markup.append(kb)
                kb = []
            kb.append(i)
        if kb != [] and kb not in reply_markup:
            reply_markup.append(kb)

        reply_markup.append([
            {
                "text": self.strings("confirm"),
                "callback": self._inline_promote,
                "args": [all_rights, chat, rank, user]
            }
        ])

        await call.edit(
            text=self.strings("choose_rights").format(
                name=user.first_name,
                rank=rank
            ),
            reply_markup=reply_markup
        )


    async def _inline_promote(self, call: InlineCall, all_rights: dict, chat, rank: str, user):
        try:
            await self.client(
                telethon.tl.functions.channels.EditAdminRequest(
                    chat.id, user.id,
                    telethon.types.ChatAdminRights(
                        other=True,
                        change_info=all_rights.get('change_info'),
                        post_messages=all_rights.get('post_messages') if chat.broadcast else None,
                        edit_messages=all_rights.get('edit_messages') if chat.broadcast else None,
                        delete_messages=all_rights.get('delete_messages'),
                        ban_users=all_rights.get('ban_users'),
                        invite_users=all_rights.get('invite_users'),
                        add_admins=all_rights.get('add_admins'),
                        anonymous=all_rights.get('anonymous'),
                        pin_messages=all_rights.get('pin_messages') if not chat.broadcast else None,
                        manage_call=all_rights.get('manage_call') if not chat.broadcast else None,
                        manage_topics=all_rights.get('manage_topics') if not chat.broadcast else None
                    ),
                    rank
                )
            )
        except telethon.errors.ChatAdminRequiredError:
            return await call.edit(
                text=self.strings("no_rights")
            )

        await call.edit(
            text=self.strings("promoted").format(
                name=user.first_name,
                rank=rank
            )
    )
