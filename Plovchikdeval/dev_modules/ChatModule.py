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

import asyncio, os
from .. import loader, security, utils
from datetime import timedelta, datetime
from ..inline.types import InlineCall # type: ignore
from telethon import functions
from telethon.tl.functions.messages import ExportChatInviteRequest, DeleteChatUserRequest, CreateChatRequest, DeleteChatRequest, GetHistoryRequest, AddChatUserRequest, ImportChatInviteRequest
from hikkatl.tl.types import Message
from telethon.tl.functions.channels import LeaveChannelRequest, GetFullChannelRequest, CreateChannelRequest, EditBannedRequest, EditTitleRequest, EditAdminRequest, JoinChannelRequest, DeleteChannelRequest, GetParticipantsRequest
from telethon.tl.types import *
from telethon.errors import *
from telethon.hints import EntityLike
from telethon.errors.rpcerrorlist import YouBlockedUserError, AdminRankInvalidError

@loader.tds
class ChatModule(loader.Module):
    strings_ru = {
        "name": "ChatModule",
        "loading": "🕐 <b>Обработка данных...</b>",
        "not_a_chat": "<emoji document_id=5312526098750252863>❌</emoji> <b>Команда не может быть запущена в личных сообщениях.</b>",
        "no_rights": "<emoji document_id=5318764049121420145>🫤</emoji> <b>У меня недостаточно прав.</b>",
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
        "adminrankerror" : "❌ Недопустимый префикс",
        "_cls_doc": "Управление правами администраторов в чатах.",
        "invalid_args": "❌ <b>Неверные аргументы.</b>",
        "spam_ban": "❌ Ваш аккаунт ограничен в создании новых групп/каналов.",
        "no_reply": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Вы не ответили на сообщение.</b>",
        "rpc_error": "Произошла ошибка: {error}",
        "invite_hash_expired": "Срок ссылки истек.",
        "title_changed": "Название группы/канала изменено на {new_name}",
        "chat_unavailable": "❌ Чат недоступен или приватный.",
        "of_chat": "Группа",
        "of_channel": "Канал",
        "own_list": "<b>Мои владения: {count}</b>\n{msg}",
        "no_ownerships": "Владений нет.",
        "no_user": "Пользователь не найден.",
        "unknown_user": "Неизвестный пользователь.",
        "unmuted": "🔈 {first_name} [<code>{user_id}</code>] был размучен.",
        "muted": "🔇 {first_name} [<code>{user_id}</code>] был замучен на {mute_time} {unit}.\n<i><b>Причина:</b> {reason}</i>",
        "users_too_much": "Лимит приглашения пользователей достигнут.",
        "kick_all": "{user_count} участников будут кикнуты.",
        "kicked": "🚷 {name} [<code>{id}</code>] был кикнут.\n<i><b>Причина:</b> {reason}</i>",
        "banned": "🚷 {name} [<code>{id}</code>] был забанен.\n<i><b>Причина:</b> {reason}</i>",
        "chat_type_error": "Не удалось определить тип чата.",
        "invite_success": "<b>Пользователь приглашён успешно!</b>",
        "privacy_settings_error": "<b>Настройки приватности пользователя не позволяют пригласить его.</b>",
        "deleted_account": "<b>Аккаунт пользователя удалён.</b>\n",
        "blocked_contact": "<b>Вы заблокировали этого пользователя.</b>\n",
        "search_deleted_accounts": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск удалённых аккаунтов</b>",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>Здесь нет ни одного удалённого аккаунта</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Удалено {count} удалённых аккаунтов</b>",
        "chat_info_header": "Информация о чате:\n",
        "group_title": "<b>Название группы:</b> {title}\n",
        "previous_title": "<b>Предыдущее название:</b> {title}\n",
        "group_type_public": "<b>Тип группы:</b> Публичный\n",
        "group_link": "<b>Ссылка:</b> {link}\n",
        "group_type_private": "<b>Тип группы:</b> Приватный\n",
        "group_creator_username": "<b>Создатель:</b> @{username}\n",
        "group_creator_link": "<b>Создатель:</b> <a href=\"tg://user?id={id}\">{firstname}</a>\n",
        "group_created": "<b>Создан:</b> {date} - {time}\n",
        "messages_viewable": "<b>Видимые сообщения:</b> {count}\n",
        "messages_sent": "<b>Всего сообщений:</b> {count}\n",
        "group_members": "<b>Участников:</b> {count}\n",
        "group_admins": "<b>Админов:</b> {count}\n",
        "group_bots": "<b>Ботов:</b> {count}\n",
        "group_online": "<b>Сейчас онлайн:</b> {count}\n",
        "group_restricted": "<b>Ограниченных пользователей:</b> {count}\n",
        "group_banned": "<b>Забаненных пользователей:</b> {count}\n",
        "group_stickers": "<b>Стикеры группы:</b> <a href=\"{stickers}\">Перейти</a>\n",
        "group_slowmode": "<b>Слоумод:</b> {slowmode}",
        "group_slowmode_time": ", {time} секунд\n",
        "group_restricted_status": "<b>Ограничен:</b> {restricted}\n",
        "group_restriction_details": "> Платформа: {platform}\n> Причина: {reason}\n> Текст: {text}\n\n",
        "group_scam": "<b>Скам:</b> да\n\n",
        "group_verified": "<b>Верифицирован:</b> {verified}\n",
        "group_description": "<b>Описание:</b> {description}\n",
        "no": "Нет",
        "yes": "Да",
        "no_title": "Нет названия",
        "join_success": "Успешно вступили в приватный чат по ссылке: {link}.",
        "successful_delete": "✅ ({chat_type}) успешно удалена.",
        "owner_info": "Владелец:\n<a href='tg://user?id={owner_id}'>{owner_name}</a>",
        "members_count": "Количество участников (без ботов) в чате: {count}",
        "bots_in_chat": "<b>Ботов в \"{title}\": {count}</b>\n",
        "deleted_bot": "\n• Удалённый бот <b>|</b> <code>{user_id}</code>",
        "too_many_bots": "Черт, слишком много ботов здесь. Загружаю список ботов в файл...",
        "no_one_unbanned": "Никто не разбанен",
        "no_one_banned": "Никто не забанен",
        "admins_in_chat": "<b>Админов в \"{title}\": {count}</b>\n",
        "too_many_admins": "Черт, слишком много админов здесь. Загружаю список админов в файл...",
        "users_not_found": "\n<b>Пользователи не найдены.</b>",
        "large_chat_loading": "<b>Черт, слишком большой чат. Загружаю список пользователей в файл...</b>",
        "admins_in_chat_caption": "<b>Админов в \"{}\":</b>",
        "bots_in_chat_caption": "<b>Ботов в \"{}\":</b>",
        "users_in_chat_caption": "<b>Пользователей в {}:</b>",
        "data_fetch_error": "Ошибка получения данных",
        "this_chat": "этом чате",
        "members_in_chat": "Участников в {title}:\n",
        "steal_complete": "({count}) Просто прикол)",
        "my_id": "<emoji document_id=5208454037531280484>💜</emoji> <b>Мой ID</b>: <code>{id}</code>",
        "users_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>ID пользователя</b>: <code>{id}</code>",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>ID чата</b>: <code>{id}</code>",
        "minutes": "минут",
        "hours": "часов",
        "days": "дней",
        "weeks": "недели",
        "get_rights_header": "<b>Права <a href='tg://user?id={id}'>{name}</a> в этом чате:</b>\n\n",
        "admin_rights": "🔹 <u>Права администратора:</u>\n",
        "not_admin": "🔹 <u>Права администратора:</u> ❌ <a href='tg://user?id={id}'>{name}</a> не администратор\n",
        "restricts": "\n🔹 <u>Ограничения:</u>\n",
        "no_restricts": "\n🔹 <u>Ограничения:</u> ✅ Нет ограничений\n",
        "invalid_number": "❗ Укажите корректное количество сообщений для удаления.",
        "no_reason": "Без причины",
        "deleted_messages": "✅ Удалено {count} сообщений.",
        "failed_get_rights": "<b>Ваши права не могут быть определены в этом чате.</b>",
    }

    strings = {
        "name": "ChatModule",
        "deleted_messages": "✅ {count} messages deleted.",
        "loading": "🕐 <b>Processing data...</b>",
        "invalid_number": "❗ Specify the correct number of messages to delete.",
        "no_reason": "No reason",
        "restricts": "\n🔹 <u>Restrictions:</u>\n",
        "no_restricts": "\n🔹 <u>Restrictions:</u> ✅ No restrictions\n",
        "admin_rights": "🔹 <u>Admin rights:</u>\n",
        "failed_get_rights": "<b>Your rights cannot be determined in this chat.</b>",
        "get_rights_header": "<b><a href='tg://user?id={id}'>{name}</a>'s rights in this chat:</b>\n\n",
        "not_admin": "🔹 <u>Admin rights:</u> ❌ <a href='tg://user?id={id}'>{name}</a> is not an admin\n",
        "not_a_chat": "<emoji document_id=5312526098750252863>❌</emoji> <b>The command cannot be run in private messages.</b>",
        "no_rights": "<emoji document_id=5318764049121420145>🫤</emoji> <b>I don't have enough rights.</b>",
        "no_user": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>You did not specify a user.</b>",
        "demoted": "<emoji document_id=5458403743835889060>😂</emoji> <b>{name} has been demoted from admin.</b>",
        "promoted_full": "<emoji document_id=5271557007009128936>👑</emoji> <b>{name} has been promoted to admin " \
                        "with full rights.</b>\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "promoted": "<emoji document_id=5451786809845491357>🫣</emoji> <b>{name} has been promoted to admin.</b>\n" \
                    "<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "choose_rights": "<emoji document_id=5271557007009128936>👑</emoji> <b>Select the rights you want to give " \
                         "{name}</b>\n<emoji document_id=5470060791883374114>✍️</emoji> <b>Rank:</b> {rank}",
        "right_change_info": "{emoji} Change profile {channel_or_chat}",
        "of_channel": "channel", "of_chat": "chat",
        "right_post_messages": "{emoji} Post messages",
        "right_edit_messages": "{emoji} Edit messages",
        "right_delete_messages": "{emoji} Delete messages",
        "right_ban_users": "{emoji} Restrict users",
        "right_invite_users": "{emoji} Invite users",
        "right_pin_messages": "{emoji} Pin messages",
        "right_add_admins": "{emoji} Add admins",
        "right_anonymous": "{emoji} Anonymous",
        "right_manage_call": "{emoji} Manage calls",
        "confirm": "✅ Confirm",
        "adminrankerror" : "❌ Invalid prefix",
        "_cls_doc": "Manage admin rights in chats.",
        "invalid_args": "❌ <b>Invalid arguments.</b>",
        "spam_ban": "❌ Your account is restricted from creating new groups/channels.",
        "no_reply": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>You did not reply to a message.</b>",
        "rpc_error": "Error occurred: {error}",
        "invite_hash_expired": "Link expired.",
        "title_changed": "Group/channel name changed to {new_name}",
        "chat_unavailable": "❌ Chat unavailable or private.",
        "of_chant": "Group",
        "of_channel": "Channel",
        "own_list": "<b>My possessions: {count}</b>\n{msg}",
        "no_ownerships": "No possessions.",
        "no_user": "User not found.",
        "unknown_user": "Unknown user.",
        "unmuted": "🔈 {first_name} [<code>{user_id}</code>] was unmuted.",
        "muted": "🔇 {first_name} [<code>{user_id}</code>] was muted for {mute_time} {unit}.\n<i><b>Reason:</b> {reason}</i>",
        "banned": "🚷 {name} [<code>{id}</code>] was banned.\n<i><b>Reason:</b> {reason}</i>",
        "users_too_much": "The user invitation limit has been reached.",
        "kick_all": "{user_count} participants will be kicked.",
        "kicked": "🚷 {name} [<code>{id}</code>] was kicked.\n<i><b>Reason:</b> {reason}</i>",
        "chat_type_error": "Failed to determine chat type.",
        "invite_success": "<b>User successfully invited!</b>",
        "privacy_settings_error": "<b>The user's privacy settings do not allow inviting them.</b>",
        "deleted_account": "<b>The user's account is deleted.</b>\n",
        "blocked_contact": "<b>You have blocked this user.</b>\n",
        "search_deleted_accounts": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching for deleted accounts</b>",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>No deleted accounts found here</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Removed {count} deleted accounts</b>",
        "chat_info_header": "Chat information:\n",
        "group_title": "<b>Group title:</b> {title}\n",
        "previous_title": "<b>Previous title:</b> {title}\n",
        "group_type_public": "<b>Group type:</b> Public\n",
        "group_link": "<b>Link:</b> {link}\n",
        "group_type_private": "<b>Group type:</b> Private\n",
        "group_creator_username": "<b>Creator:</b> @{username}\n",
        "group_creator_link": "<b>Creator:</b> <a href=\"tg://user?id={id}\">{firstname}</a>\n",
        "group_created": "<b>Created:</b> {date} - {time}\n",
        "messages_viewable": "<b>Viewable messages:</b> {count}\n",
        "messages_sent": "<b>Total messages:</b> {count}\n",
        "group_members": "<b>Members:</b> {count}\n",
        "group_admins": "<b>Admins:</b> {count}\n",
        "group_bots": "<b>Bots:</b> {count}\n",
        "group_online": "<b>Currently online:</b> {count}\n",
        "group_restricted": "<b>Restricted users:</b> {count}\n",
        "group_banned": "<b>Banned users:</b> {count}\n",
        "group_stickers": "<b>Group stickers:</b> <a href=\"{stickers}\">Go to</a>\n",
        "group_slowmode": "<b>Slow mode:</b> {slowmode}",
        "group_slowmode_time": ", {time} seconds\n",
        "group_restricted_status": "<b>Restricted:</b> {restricted}\n",
        "group_restriction_details": "> Platform: {platform}\n> Reason: {reason}\n> Text: {text}\n\n",
        "group_scam": "<b>Scam:</b> yes\n\n",
        "group_verified": "<b>Verified:</b> {verified}\n",
        "group_description": "<b>Description:</b> {description}\n",
        "no": "No",
        "yes": "Yes",
        "no_title": "No title",
        "join_success": "Successfully joined the private chat via the link: {link}.",
        "successful_delete": "✅ ({chat_type}) successfully deleted.",
        "owner_info": "Owner:\n<a href='tg://user?id={owner_id}'>{owner_name}</a>",
        "members_count": "Number of members (excluding bots) in the chat: {count}",
        "bots_in_chat": "<b>Bots in \"{title}\": {count}</b>\n",
        "deleted_bot": "\n• Deleted bot <b>|</b> <code>{user_id}</code>",
        "too_many_bots": "Damn, too many bots here. Loading the list of bots into a file...",
        "no_one_unbanned": "No one is unbanned",
        "no_one_banned": "No one is banned",
        "admins_in_chat": "<b>Admins in \"{title}\": {count}</b>\n",
        "too_many_admins": "Damn, too many admins here. Loading the list of admins into a file...",
        "users_not_found": "\n<b>No users found.</b>",
        "large_chat_loading": "<b>Damn, the chat is too large. Loading the list of users into a file...</b>",
        "admins_in_chat_caption": "<b>Admins in \"{}\":</b>",
        "bots_in_chat_caption": "<b>Bots in \"{}\":</b>",
        "users_in_chat_caption": "<b>Users in {}:</b>",
        "data_fetch_error": "Error fetching data",
        "this_chat": "this chat",
        "members_in_chat": "Members in {title}:\n",
        "steal_complete": "({count}) just for fun)",
        "my_id": "<emoji document_id=5208454037531280484>💜</emoji> <b>My ID</b>: <code>{id}</code>",
        "users_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>User's ID</b>: <code>{id}</code>",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>Chat ID</b>: <code>{id}</code>",
        "minutes": "minutes",
        "hours": "hours",
        "days": "days",
        "weeks": "weeks",
    }

    @loader.owner
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.muted = []

    @loader.command(
        ru_doc="| Покинуть чат"
    )
    async def leave(self, message: Message):
        """| Leave chat"""
        await message.delete()
        await message.client(LeaveChannelRequest((await message.get_chat()).id))

    @loader.command(
        ru_doc="<реплай> [роль] | Повышение пользователя до администратора с полными правами."
    )
    async def fullrights(self, message: Message):
        """<reply> [role] |  Upgrade the user to an administrator with full rights."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        rank, user_id = "", None
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
                EditAdminRequest(
                    message.chat_id, user.id,
                    ChatAdminRights(
                        other=True,
                        change_info=True,
                        post_messages=True if message.is_channel or chat else None,
                        edit_messages=True if message.is_channel or chat else None,
                        delete_messages=True,
                        ban_users=True,
                        invite_users=True,
                        add_admins=True,
                        anonymous=None,
                        pin_messages=True if not message.is_channel or chat else None,
                        manage_call=True if not message.is_channel or chat else None
                    ),
                    rank
                )
            )
        except ChatAdminRequiredError:
            return await utils.answer(message, self.strings("no_rights", message))

        await utils.answer(
            message,
            self.strings("promoted_full", message).format(
                name=user.first_name,
                rank=rank
            )
        )

    @loader.command(
        ru_doc="<reply/username/id> | Проверить права в текущем чате."
    )
    async def rights(self, message):
        """<reply/username/id> | Check rights in the current chat."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chat = await message.get_chat()
        chat_id = message.chat_id
        admin_rights = [
            "change_info",
            "delete_messages",
            "ban_users",
            "invite_users",
            "pin_messages",
            "manage_call",
            "add_admins",
            "anonymous",
            "edit_messages",
            "manage_topics",
            "post_messages",
        ]

        banned_rights = [
            "send_messages",
            "send_media",
            "send_photos",
            "send_videos",
            "send_roundvideos",
            "send_audios",
            "send_voices",
            "send_docs",
            "send_stickers",
            "send_gifs",
            "embed_links",
            "send_polls",
            "send_games",
            "send_inline",
        ]
        if not args:
            if not reply:
                if not chat or not chat_id:
                    return await utils.answer(message, self.strings("not_a_chat", message))

                if not hasattr(chat, "admin_rights") and not hasattr(chat, "banned_rights"):
                    return await utils.answer(message, self.strings('failed_get_rights', message))

                admin_rights = getattr(chat, "admin_rights", None)
                banned_rights = getattr(chat, "banned_rights", None)

                result = self.strings('get_rights_header').format(id=(await self.client.get_me()).id, name=f"{(await self.client.get_me()).first_name or ''} {(await self.client.get_me()).last_name or ''}")

                if admin_rights and isinstance(admin_rights, ChatAdminRights):
                    result += self.strings('admin_rights')
                    for right, value in admin_rights.to_dict().items():
                        result += f"  - {right}: {'✅' if value else '❌'}\n"
                else:
                    result += self.strings('not_admin').format(id=(await self.client.get_me()).id, name=f"{(await self.client.get_me()).first_name or ''} {(await self.client.get_me()).last_name or ''}")

                if banned_rights and isinstance(banned_rights, ChatBannedRights):
                    result += self.strings('restricts')
                    for right, value in banned_rights.to_dict().items():
                        result += f"  - {right}: {'❌' if value else '✅'}\n"
                else:
                    result += self.strings('no_restricts')

                await utils.answer(message, result)
            else:
                user = await reply.get_sender()
                if not chat or not chat_id:
                    return await utils.answer(message, self.strings("not_a_chat", message))
                permissions = await self.client.get_permissions(chat, user)

                result = self.strings('get_rights_header').format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")

                if permissions.has_default_permissions:
                    result += self.strings("not_admin").format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")
                else:
                    result += self.strings('admin_rights')
                    for right in admin_rights:
                        has_permission = getattr(permissions, right, False)
                        result += f"  - {right}: {'✅' if has_permission else '❌'}\n"
                restricts = ""
                for right in banned_rights:
                    has_permission = getattr(permissions, right, False)
                    if has_permission:
                        restricts += f"  - {right}: {'❌' if has_permission else '✅'}\n"
                if restricts == "":
                    result += self.strings("no_restricts")
                else:
                    result += self.strings("restricts")
                    result += restricts

                await utils.answer(message, result)
        else:
            args = utils.get_args_raw(message).split()
            user = await self.client.get_entity(int(args[0]) if args[0].isdigit() else args[0])
            if not chat or not chat_id:
                return await utils.answer(message, self.strings("not_a_chat", message))
            try:
                permissions = await self.client.get_permissions(chat, user)
            except UserNotParticipantError:
                return await utils.answer(message, self.strings("no_user", message))
            if permissions.has_left:
                return await utils.answer(message, self.strings("no_user", message))

            result = self.strings('get_rights_header').format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")

            if permissions.has_default_permissions:
                result += self.strings("not_admin").format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")
            else:
                result += self.strings('admin_rights')
                for right in admin_rights:
                    has_permission = getattr(permissions, right, False)
                    result += f"  - {right}: {'✅' if has_permission else '❌'}\n"
            restricts = ""
            for right in banned_rights:
                has_permission = getattr(permissions, right, False)
                if has_permission:
                    restricts += f"  - {right}: {'❌' if has_permission else '✅'}\n"
            if restricts == "":
                result += self.strings("no_restricts")
            else:
                result += self.strings("restricts")
                result += restricts

            await utils.answer(message, result)

    @loader.command(
        ru_doc="<reply> [role] | Повышение пользователя до администратора."
    )
    async def promote(self, message: Message):
        """<reply> [role] | Promote the user to administrator."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        rank, user_id = "", None
        chat = await message.get_chat()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
            if args:
                rank = args
        else:
            try:
                user_id = int(args.split()[0])
            except ValueError:
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

    async def _inline_promote(self, call: InlineCall, all_rights: dict, chat, rank: str, user):
        try:
            await self.client(
                EditAdminRequest(
                    chat.id, user.id,
                    ChatAdminRights(
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
        except ChatAdminRequiredError:
            return await call.edit(
                text=self.strings("no_rights")
            )
        except AdminRankInvalidError:
            return await call.edit(
                text=self.strings("adminrankerror")
            )

        await call.edit(
            text=self.strings("promoted").format(
                name=user.first_name,
                rank=rank
            )
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

    @loader.command(
        ru_doc="<реплай> | Снятие прав администратора с пользователя."
    )
    async def demote(self, message: Message):
        """<reply> | Demote the user."""
        if message.is_private:
            return await utils.answer(
                message, self.strings("not_a_chat", message)
            )

        user_id = None
        chat = await message.get_chat()
        rank = ""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if reply:
            if reply.sender_id != message._client.tg_id:
                user_id = reply.sender_id
        else:
            try:
                user_id = int(args.split()[0])
            except ValueError:
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
                EditAdminRequest(
                    message.chat_id, user.id,
                    ChatAdminRights(
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
                    rank
                )
            )
        except ChatAdminRequiredError:
            return await utils.answer(message, self.strings("no_rights", message))

        await utils.answer(
            message, self.strings("demoted", message).format(
                name=user.first_name
            )
        )

    @loader.command(
        ru_doc="<g|s|c> <название> <тег: OPTIONAL> | создать группу, супергруппу или канал."
    )
    async def create(self, message):
        """<g|s|c> <название> <tag: OPTIONAL> | create a group, supergroup, or channel."""
        args = utils.get_args_raw(message).split(" ")
        try:
            if args[-1].startswith("@"):
                title = " ".join(args[1:-1])
            else:
                title = " ".join(args[1:])
            if "g" in args[0]:
                r = await message.client(
                    CreateChatRequest(users=["missrose_bot"], title=title)
                )
                created_chat = r.chats[0].id
                await message.client(
                    DeleteChatUserRequest(chat_id=created_chat, user_id="@missrose_bot")
                )
                if args[-1].startswith("@"):
                    try:
                        await message.client(functions.channels.UpdateUsernameRequest(channel=r.chats[0], username=args[-1][1:]))
                    except UsernameOccupiedError:
                        return await utils.answer(message,f"Username {args[-1]} occupied")
                    except UsernameInvalidError:
                        return await utils.answer(message,"The username must match the pattern: [a-zA-Z][\\w\\d]{3,30}[a-zA-Z\\d]")
            elif "s" in args[0]:
                r = await message.client(
                    CreateChannelRequest(title=title, about="", megagroup=True)
                )
                if args[-1].startswith("@"):
                    try:
                        await message.client(functions.channels.UpdateUsernameRequest(channel=r.chats[0], username=args[-1][1:]))
                    except UsernameOccupiedError:
                        return await utils.answer(message,f"Username {args[-1]} occupied")
                    except UsernameInvalidError:
                        return await utils.answer(message,"The username must match the pattern: [a-zA-Z][\\w\\d]{3,30}[a-zA-Z\\d]")
            elif "c" in args[0]:
                r = await message.client(
                    CreateChannelRequest(title=title, about="", megagroup=False)
                )
                if args[-1].startswith("@"):
                    try:
                        await message.client(functions.channels.UpdateUsernameRequest(channel=r.chats[0], username=args[-1][1:]))
                    except UsernameOccupiedError:
                        return await utils.answer(message, f"Username {args[-1]} occupied")
                    except UsernameInvalidError:
                        return await utils.answer(message, "The username must match the pattern: [a-zA-Z][\\w\\d]{3,30}[a-zA-Z\\d]")
            created_chat = r.chats[0].id
            result = await message.client(ExportChatInviteRequest(peer=created_chat))
            await utils.answer(message,
                f'<b>Группа "{title}" создана.\nЛинк: {result.link}.</b>'
            )
        except IndexError:
            return await utils.answer(message, self.strings("invalid_args", message))
        except UnboundLocalError:
            return await utils.answer(message, self.strings("invalid_args", message))
        except UserRestrictedError:
            return await utils.answer(message, self.strings("spam_ban", message))

    @loader.command(
        ru_doc="<реплай> | Получить айди пользователя."
    )
    async def userid(self, message):
        """<reply> | Get user's id."""
        reply = await message.get_reply_message()
        if reply != None:
            await utils.answer(message, self.strings("users_id", message).format(id=reply.sender_id))
        else:
            await utils.answer(message, self.strings["Error_reply"])

    @loader.command(
        ru_doc="| Получить свой айди"
    )
    async def id(self, message):
        """| Get your id."""
        await utils.answer(message, self.strings("my_id", message).format(id=message.sender_id))

    @loader.command(
        ru_doc="| Получить айди чата."
    )
    async def chatid(self, message):
        """| Get chat id."""
        await utils.answer(message, self.strings("chat_id", message).format(id=utils.get_chat_id(message)))

    @loader.command(
        ru_doc="<реплай/кол-во> | Удаляет сообщения."
    )
    async def delcmd(self, message):
        """<reply/count> | Deletes messages."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if args:
            if not args.isdigit():
                return await utils.answer(message, self.strings("invalid_args", message))
            chat = message.chat
            purge_count = int(args)
            await message.delete()
            await self._purge_user_messages(chat, (await self.client.get_me()).id, purge_count)
        
        if not reply:
            return await utils.answer(message, self.strings("no_reply", message))

        try:
            await message.delete()
            await reply.delete()
        except Exception:
            pass
    
    async def _purge_user_messages(
        self,
        chat: EntityLike,
        user_id: int,
        purge_count: int,
    ) -> int:
        msgs = []
        msg_count = 0
        itermsg = self._client.iter_messages(entity=chat)
        i = 0
        async for msg in itermsg:
            if msg.sender_id == user_id:
                if i == purge_count:
                    break
                i += 1
                msgs += [msg.id]
                msg_count += 1
                if len(msgs) >= 99:
                    await self._client.delete_messages(chat, msgs)
                    msgs.clear()

        if msgs:
            await self._client.delete_messages(chat, msgs)

        return msg_count

    @loader.command(
        ru_doc="<ID или ссылка> | Удаляет группу/канал."
    )
    async def dgc(self, event):
        """<ID or link> | Deletes group/channel."""
        args = utils.get_args(event)
        if not args:
            await utils.answer(event, self.strings("invalid_args", event))
            return
        
        link = args[0] if isinstance(args, list) else args
        try:
            if link.isdigit():
                chat_id = int(link)
            elif "t.me" in link or "tg://" in link:
                chat_id = await event.client.get_entity(link)
                chat_id = chat_id.id
            else:
                await utils.answer(event, self.strings("invalid_args", event))
                return
            try:
                await event.client(DeleteChannelRequest(chat_id))
                chat_type = "Супергруппа/Канал"
            except Exception:
                try:
                    await event.client(DeleteChatRequest(chat_id))
                    chat_type = self.strings("of_chat", event)
                except Exception as e:
                    if "CHANNEL_PRIVATE" in str(e):
                        await utils.answer(event, "❌ Чат недоступен или приватный.")
                        return
                    elif "CHAT_ADMIN_REQUIRED" in str(e):
                        await utils.answer(event, self.strings("no_rights", event))
                        return
                    elif "Invalid object ID for a chat." in str(e):
                        await utils.answer(event, self.strings("invalid_args", event))
                        return
                    await utils.answer(event, self.strings("invalid_args", event).format(error=str(e)))
                    return
            await utils.answer(event, self.strings("successful_delete", event).format(chat_type=chat_type))

        except ChatAdminRequiredError:
            await utils.answer(event, self.strings("no_rights", event))
        except ChannelPrivateError:
            await utils.answer(event, self.strings("chat_unavailable", event))
        except RpcError as e:
            await utils.answer(event, self.strings("rpc_error", event).format(error=e))
        except Exception as e:
            await utils.answer(event, self.strings("rpc_error", event).format(error=e))

    @loader.command(
        ru_doc="<ссылка> | Вступает в группу или канал по ссылке."
    )
    async def join(self, event):
        """<link> | Join group or channel via link."""

        link = utils.get_args_raw(event)
        if not link:
            await utils.answer(event, self.strings("invalid_args", event))
            return

        link = link.strip()
        try:
            if "joinchat" in link or "+" in link:
                invite_hash = link.split("/")[-1].replace("joinchat/", "").replace("+", "")
                await self.client(ImportChatInviteRequest(invite_hash))
                await utils.answer(event, self.strings("join_success", event).format(link=link))
            else:
                entity = await self.client.get_entity(link)
                await self.client(JoinChannelRequest(entity))
                title = entity.title if hasattr(entity, 'title') else self.strings("no_title", event)
                await utils.answer(event, self.strings("join_success", event).format(link=link))
        except InviteHashExpiredError:
            await utils.answer(event, self.strings("invite_hash_expired", event))
        except ValueError:
            await utils.answer(event, self.strings("invalid_link", event))
        except Exception as e:
            await utils.answer(event, self.strings("rpc_error", event).format(error=str(e)))

    @loader.command(
        ru_doc="| Определяет владельца группы или канала."
    )
    async def whoisowner(self, event):
        """| Shows the owner of the group or channel."""
        chat = await event.get_input_chat()

        try:
            participants = await self.client.get_participants(chat, filter=ChannelParticipantsAdmins, aggressive=True)
            for admin in participants:
                if isinstance(admin.participant, ChannelParticipantCreator):
                    owner_name = f"{admin.first_name} {admin.last_name or ''}".strip()
                    owner_id = admin.id
                    await utils.answer(event, self.strings("owner_info").format(owner_id=owner_id, owner_name=owner_name))
                    return
            await utils.answer(event, "Владелец не найден.")
        except Exception as e:
            await utils.answer(event, self.strings("rpc_error", event).format(error=str(e)))

    @loader.command(
        ru_doc="<new_name> | Меняет название группы/канала на <new_name>"
    )
    async def rename(self, message):
        """<new_name> | Changes the group/channel name to <new_name>"""
        try:
            args = utils.get_args(message)
            if not args:
                await utils.answer(message, self.strings("invalid_args", message))
                return

            new_name = " ".join(args)
            
            chat = await message.get_chat()

            try:
                await self._client(EditTitleRequest(
                    channel=chat,
                    title=new_name
                ))
            except ChatAdminRequiredError:
                await utils.answer(message, self.strings("no_rights", message))
                return
            except Exception as e:
                await utils.answer(message, self.strings("rpc_error", message).format(error=e))
                return

            await utils.answer(message, self.strings("title_changed", message).format(new_name=new_name))
            await message.delete()
        except Exception as e:
            await utils.answer(message, self.strings("rpc_error", message).format(error=str(e)))

    @loader.command(
        ru_doc="| Показывает кол-во участников канала/группы"
    )
    async def members(self, event):
        """| Shows the number of members in the channel/group"""
        if not event.is_private:
            chat = await event.get_input_chat()
            try:
                members = await event.client.get_participants(chat)
                real_members = [member for member in members if not member.bot]
                count = len(real_members)
                await utils.answer(event, self.strings("members_count").format(count=count))
            except Exception as e:
                await utils.answer(event, self.strings("rpc_error", event).format(error=e))
        else:
            return await utils.answer(event, self.strings("not_a_chat", event))

    @loader.command(
        ru_doc="| Забанить всех участников в группе/канале"
    )
    async def banall(self, message):
        """| Ban all members in the group/channel"""
        await message.delete()
        chat = message.chat
        if chat:
            async for user in self.client.iter_participants(chat.id):
                try:
                    if user.id == (await self.client.get_me()).id:
                        continue
                    await self.client.edit_permissions(chat.id, user.id, view_messages=False)
                except Exception as e:
                    pass

    @loader.command(
        ru_doc="| Показывает информацию о чате."
    )
    async def chatinfo(self, chatinfo):
        """| Shows information about the chat."""
        if chatinfo.chat:
            await utils.answer(chatinfo, self.strings("loading", chatinfo))
            await chatinfo.delete()
            chat = await self.get_chatinfo(chatinfo)
            caption = await self.fetch_info(chat, chatinfo)
            try:
                await chatinfo.client.send_message(
                    chatinfo.to_id,
                    str(caption),
                    file=await chatinfo.client.download_profile_photo(
                        chat.full_chat.id, "chatphoto.jpg"
                    ),
                )
                os.remove("chatphoto.jpg")
            except Exception:
                await utils.answer(chatinfo, self.strings("rpc_error", chatinfo))
                await chatinfo.delete()
        else:
            await utils.answer(chatinfo, self.strings("not_a_chat", chatinfo))
            await chatinfo.delete()

    @loader.command(
        ru_doc="| Показывает список чатов, каналов и групп где вы админ/владелец."
    )
    async def own(self, message):
        """| Shows the list of chats, channels and groups where you are an admin/owner."""
        await utils.answer(message, self.strings("loading", message))
        
        count = 0
        msg = ""

        async for dialog in message.client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                chat = await message.client.get_entity(dialog.id)
                if chat.admin_rights or chat.creator:
                    count += 1
                    chat_type = self.strings("of_chat") if dialog.is_group else self.strings("of_channel")
                    msg += f'\n• {chat.title} <b>({chat_type})</b> | <code>{chat.id}</code>'

        if msg:
            await utils.answer(message, self.strings("own_list", message).format(count=count, msg=msg), parse_mode="html")
        else:
            await utils.answer(message, self.strings("no_ownerships", message))

    @loader.command(
        ru_doc="<id/username/reply> | Размучивает пользователя."
    )
    async def unmute(self, message):
        """<id/username/reply> | Unmutes the user."""
        if not message.is_reply:
            try:
                args = message.raw_text.split(maxsplit=1)
                if len(args) < 2:
                    await utils.answer(message, self.strings("no_user", message))
                    return
                
                user = int(args[1]) if args[1].isdigit() else args[1]
                user = await message.client.get_entity(user)
                first_name = user.first_name or self.strings("unknown_user", message)
                
                await message.client.edit_permissions(
                    entity=message.chat_id,
                    user=user.id,
                    send_messages=True,
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    send_polls=True
                )
                try:
                    self.muted.remove(user.id)
                except:
                    pass
                await utils.answer(message,
                    self.strings("unmuted", message).format(
                        user_id=user.id,
                        first_name=first_name
                    ),
                    parse_mode="html"
                )
                return
            except ValueError:
                await utils.answer(message, self.strings("no_user", message))
                return
            except Exception as e:
                await utils.answer(message, self.strings("rpc_error", message).format(error=e))
                return
        reply_message = await message.get_reply_message()
        user_id = reply_message.sender_id
        first_name = reply_message.sender.first_name
        try:
            await message.client.edit_permissions(
                entity = message.chat_id,
                user = user_id,
                send_messages = True,
                send_media = True,
                send_stickers = True,
                send_gifs = True,
                send_games = True,
                send_inline = True,
                send_polls = True
            )
            try:
                self.muted.remove(user_id)
            except:
                pass
            await utils.answer(message, self.strings("unmuted", message).format(user_id=user_id, first_name=first_name))
        except UserAdminInvalidError:
            await utils.answer(message, self.strings("no_rights", message))
        except ChatAdminRequiredError:
            await utils.answer(message, self.strings("no_rights", message))
        except Exception as e:
            await utils.answer(message, self.strings("rpc_error", message).format(error=e))

    @loader.command(
        ru_doc="<reply/ID/username> <time> | Мутит пользователя на определенное время."
    )
    async def mute(self, message):
        """<reply/ID/username> <time> | Mutes the user for a certain time."""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()

        if len(args) == 0:
            await utils.answer(message, self.strings("invalid_args", message))
            return

        if len(args) < 2 and not reply:
            await utils.answer(message, self.strings("invalid_args", message))
            return
        if not reply and len(args) > 2:
            reason = " ".join(args[2:])
        elif reply and len(args) > 1:
            reason = " ".join(args[1:])
        else:
            reason = self.strings("no_reason", message)
        try:
            unit = args[1][-1] if not reply else args[0][-1]
            mute_time = int(args[1][:-1]) if not reply else int(args[0][:-1])
            duration = timedelta(minutes=mute_time)
            if unit == "m":
                duration = timedelta(minutes=mute_time)
                unit = self.strings("minutes", message)
            elif unit == "h":
                duration = timedelta(hours=mute_time)
                unit = self.strings("hours", message)
            elif unit == "d":
                duration = timedelta(days=mute_time)
                unit = self.strings("days", message)
            elif unit == "w":
                duration = timedelta(weeks=mute_time)
                unit = self.strings("weeks", message)
            else:
                await utils.answer(message, self.strings("invalid_args", message))
                return
        except ValueError:
            await utils.answer(message, self.strings("invalid_args", message))
            return

        if message.is_reply:
            reply_message = await message.get_reply_message()
            user_id = reply_message.sender_id
            first_name = reply_message.sender.first_name
        else:
            user_identifier = int(args[0]) if args[0].isdigit() else args[0]
            try:
                user = await message.client.get_entity(user_identifier)
                user_id = user.id
                first_name = user.first_name
            except Exception:
                await utils.answer(message, self.strings("no_user", message))
                return

        try:
            self.muted.append(user_id)
            await message.client.edit_permissions(
                entity=message.chat_id,
                user=user_id,
                send_messages=False,
                send_media=False,
                send_stickers=False,
                send_gifs=False,
                send_games=False,
                send_inline=False,
                send_polls=False,
                until_date=duration
            )

            await utils.answer(message,
                self.strings("muted", message).format(
                    user_id=user_id,
                    first_name=first_name,
                    mute_time=mute_time,
                    unit=unit,
                    reason=reason
                ),
                parse_mode="html"
            )
            await asyncio.sleep(duration.total_seconds())
            if user_id in self.muted:
                await message.client.send_message(
                    message.chat_id,
                    self.strings("unmuted", message).format(
                        user_id=user_id,
                        first_name=first_name
                    ),
                    parse_mode="html"
                )
                try:
                    self.muted.remove(user_id)
                except:
                    pass

        except UserAdminInvalidError:
            await utils.answer(message, self.strings("no_rights", message))
        except ChatAdminRequiredError:
            await utils.answer(message, self.strings("no_rights", message))
        except Exception as e:
            await utils.answer(message, self.strings("rpc_error", message).format(error=e))

    @loader.command(
        ru_doc="| Кикает всех пользователей из чата."
    )
    async def kickall(self, event):
        """| Kicks all users from the chat."""
        user = [i async for i in event.client.iter_participants(event.to_id.channel_id)]
        await utils.answer(event, 
            self.strings("kick_all", event).format(
            user_count=len(user)
            )
        )
        for u in user:
            try:
                try:
                    if u.is_self != True:
                        await event.client.kick_participant(event.chat_id, u.id)
                        asyncio.sleep(1)
                except:
                    pass
            except FloodWaitError as e:
                await utils.answer(event, self.strings("flood_wait", event).format(seconds=e.seconds))

    @loader.command(
        ru_doc="<nobot: OPTIONAL> | Добавляет людей и ботов с чата в чат."
    )
    async def steal(self, event):
        """<nobot: OPTIONAL> | Adds people from the chat to the chat."""
        if len(event.text.split()) >= 2:
            idschannelgroup = int(event.text.split(" ", maxsplit=2)[1])
            arg = event.text.split(" ", maxsplit=2)[2] if len(event.text.split()) > 2 else None
            entity = await event.client.get_entity(idschannelgroup)
            participants = await event.client(GetParticipantsRequest(
                                        channel=idschannelgroup,
                                        filter=ChannelParticipantsSearch(''),
                                        offset=0,
                                        limit=0,
                                        hash=0
                                    ))
            existing_users = {p.id for p in participants.users}
            if arg and arg == "nobot":
                user = [
                    i async for i in event.client.iter_participants(event.to_id.channel_id)
                    if not i.bot
                ]
            else:
                user = [
                    i async for i in event.client.iter_participants(event.to_id.channel_id)
                ]
            await utils.answer(event, 
                self.strings("steal_complete", event).format(count=len(user))
            )
            await event.delete()
            try:
                if entity.broadcast or entity.megagroup:
                    for u in user:
                        try:
                            if isinstance(u, PeerUser):
                                u = await event.client.get_entity(u.user_id)
                            if u.id not in existing_users:
                                await event.client(functions.channels.InviteToChannelRequest(
                                    channel=idschannelgroup,
                                    users=[u.id]
                                ))
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds)
                        except Exception as e:
                            if "Too many requests" in str(e):
                                return
                            print(f"{str(e)}")
                        await asyncio.sleep(2)
                else:
                    for u in user:
                        try:
                            if isinstance(u, PeerUser):
                                u = await event.client.get_entity(u.user_id)
                            if u.id not in existing_users:
                                await event.client(functions.channels.AddChatUserRequest(
                                    chat_id=idschannelgroup, 
                                    users=[u.id],
                                    fwd_limit=0
                                ))
                        except FloodWaitError as e:
                            await asyncio.sleep(e.seconds)
                        except Exception as e:
                            if "Too many requests" in str(e):
                                return
                            print(f"{str(e)}")
                        await asyncio.sleep(2)
            except UsersTooMuchError:
                await utils.answer(event, self.strings("users_too_much", event))
                return
        else:
            await utils.answer(event, self.strings("invalid_args", event))

    @loader.command(
        ru_doc="| Выводит список участников в чате."
    )
    async def users(self, message):
        """| Shows the list of members in the chat."""
        if not message.is_private:
            await utils.answer(message, self.strings("loading", message))
            info = await message.client.get_entity(message.chat_id)
            title = info.title or self.strings("this_chat")
            users = await message.client.get_participants(message.chat_id)
            mentions = self.strings("members_in_chat").format(title=title)
            user_mentions = []
            for user in users:
                if not user.bot:
                    if not user.deleted:
                        user_mentions.append(f"\n• <a href =\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>")
                    else:
                        user_mentions.append(self.strings("deleted_account").format(user_id=user.id))

            if user_mentions:
                mentions += ''.join(user_mentions)
            else:
                mentions += self.strings("users_not_found")

            try:
                await utils.answer(message, mentions)
                return
            except MessageTooLongError:
                await utils.answer(message, self.strings("large_chat_loading"))
                file = open("userslist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                               "userslist.md",
                               caption=self.strings("users_in_chat_caption").format(title),
                               reply_to=message.id)
                os.remove("userslist.md")
                await message.delete()
                return
        else:
            return await utils.answer(message, self.strings("not_a_chat"), message)

    @loader.command(
        ru_doc="| Выводит список всех админов в чате (без учёта ботов)."
    )
    async def admins(self, message):
        """| Shows the list of all admins in the chat (excluding bots)."""
        if not message.is_private:
            await utils.answer(message, self.strings("loading", message))
            info = await message.client.get_entity(message.chat_id)
            title = info.title or "this chat"

            admins = await message.client.get_participants(message.chat_id, filter=ChannelParticipantsAdmins)
            real_members = [member for member in admins if not member.bot]
            mentions = self.strings("admins_in_chat").format(title=title, count=len(real_members))

            for user in real_members:
                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += self.strings("deleted_account").format(user_id=user.id)

            try:
                await utils.answer(message, mentions)
            except MessageTooLongError:
                await utils.answer(message, self.strings("too_many_admins"))
                with open("adminlist.md", "w+") as file:
                    file.write(mentions)
                await message.client.send_file(message.chat_id,
                               "adminlist.md",
                               caption=self.strings("admins_in_chat_caption").format(title),
                               reply_to=message.id)
                os.remove("adminlist.md")
                await message.delete()
        else:
            return await utils.answer(message, self.strings("not_a_chat"))

    @loader.command(
        ru_doc="| Выводит список всех ботов в чате."
    )
    async def bots(self, message):
        """| Shows the list of all bots in the chat."""
        if not message.is_private:
            await utils.answer(message, self.strings("loading", message))

            info = await message.client.get_entity(message.chat_id)
            title = info.title if info.title else "this chat"

            bots = await message.client.get_participants(message.to_id, filter=ChannelParticipantsBots)
            mentions = self.strings("bots_in_chat").format(title=title, count=len(bots))

            for user in bots:
                if not user.deleted:
                    mentions += f"\n• <a href=\"tg://user?id={user.id}\">{user.first_name}</a> | <code>{user.id}</code>"
                else:
                    mentions += self.strings("deleted_bot").format(user_id=user.id)

            try:
                await utils.answer(message, mentions, parse_mode="html")
            except MessageTooLongError:
                await utils.answer(message, self.strings("too_many_bots"))
                file = open("botlist.md", "w+")
                file.write(mentions)
                file.close()
                await message.client.send_file(message.chat_id,
                               "botlist.md",
                               caption=self.strings("bots_in_chat_caption").format(title),
                               reply_to=message.id)
                os.remove("botlist.md")
                await message.delete()
        else:
            return await utils.answer(message, self.strings("not_a_chat", message))

    @loader.command(
        ru_doc="<reply/ID/username> | Разбанивает участника."
    )
    async def unban(self, message):
        """<reply/ID/username> | Unbans the user."""
        if not isinstance(message.to_id, PeerChannel):
            return await utils.answer(message, self.strings("not_a_chat", message))
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("no_one_unbanned"))
            if args[0].isdigit():
                who = int(args[0])
            else:
                who = args[0]
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("no_user", message))
        try:
            await self.client(EditBannedRequest(message.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=False)))
            await message.delete()
            return
        except BadRequestError:
            await utils.answer(message, self.strings("no_rights", message))
            return

    @loader.command(
        ru_doc="<reply/ID/username> | Банит участника."
    )
    async def ban(self, message):
        """<reply/id/username> | Bans the user."""
        if not isinstance(message.to_id, PeerChannel):
            return await utils.answer(message, self.strings("not_a_chat", message))
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
            reason = utils.get_args_raw(message)
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("no_one_banned"))
            if args[0].isdigit():
                who = int(args[0])
                reason = " ".join(args[1:])
            else:
                who = args[0]
                reason = " ".join(args[1:])
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("no_user", message))
        try:
            await self.client(EditBannedRequest(message.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))
            if not reason:
                reason = self.strings("no_reason", message)
            await utils.answer(message, self.strings("banned", message).format(name=user.first_name, id=user.id), reason=reason)
            return
        except BadRequestError:
            await utils.answer(message, self.strings("no_rights", message))
            return

    @loader.command(
        ru_doc="<reply/ID/username> | Кикает участника."
    )
    async def kick(self, message):
        """<reply/id/username> | Kicks the user."""
        if isinstance(message.to_id, PeerUser):
            return await utils.answer(message, self.strings("not_a_chat", message))
        if message.is_reply:
            user = await utils.get_user(await message.get_reply_message())
            reason = utils.get_args_raw(message)
        else:
            args = utils.get_args(message)
            if len(args) == 0:
                return await utils.answer(message, self.strings("invalid_args", message))
            if args[0].isdigit():
                who = int(args[0])
                reason = " ".join(args[1:])
            else:
                who = args[0]
                reason = " ".join(args[1:])
            user = await self.client.get_entity(who)
        if not user:
            return await utils.answer(message, self.strings("no_user", message))
        if user.is_self:
            if not (await message.client.is_bot()
                    or await self.allmodules.check_security(message, security.OWNER | security.SUDO)):
                return
        try:
            await self.client.kick_participant(message.chat_id, user.id)
            if not reason:
                reason = self.strings("no_reason", message)
            await utils.answer(message, self.strings("kicked", message).format(name=user.first_name, id=user.id, reason=reason))
            return
        except BadRequestError:
            await utils.answer(message, self.strings("no_rights", message))
            return

    @loader.command(
        ru_doc="<reply/ID/username> | Приглашает участника/бота в чат."
    )
    async def invite(self, message):
        """<reply/id/username> | Invites the user/bot to the chat."""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat", message))

        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        
        if not args and not reply:
            await utils.answer(message, self.strings("invalid_args", message))
            return

        try:
            entity = await message.client.get_entity(message.chat_id)
            if args:
                user = args if not args.isdigit() else int(args)
            else:
                user = reply.sender_id
            
            user = await message.client.get_entity(user)

            if message.is_group and not entity.megagroup:
                await message.client(AddChatUserRequest(chat_id=message.chat_id,
                                                        user_id=user.id,
                                                        fwd_limit=1000000))
            elif entity.broadcast or entity.megagroup:
                await message.client(functions.channels.InviteToChannelRequest(
                                channel=message.chat_id,
                                users=[user.id]
                            ))
            else:
                await utils.answer(message, self.strings("chat_type_error", message))
            await utils.answer(message, self.strings("invite_success", message))
            return

        except ValueError:
            m = self.strings("no_user", message)
            await utils.answer(message, m)
        except UserIdInvalidError:
            m = self.strings("no_user", message)
            await utils.answer(message, m)
        except UserPrivacyRestrictedError:
            m = self.strings("privacy_settings_error", message)
            await utils.answer(message, m)
        except UserNotMutualContactError:
            m = self.strings("privacy_settings_error", message)
            await utils.answer(message, m)
        except ChatAdminRequiredError:
            m = self.strings("no_rights", message)
            await utils.answer(message, m)
        except UserBotError:
            group = await message.client.get_entity(message.chat_id)
            if args:
                user = args if not args.isdigit() else int(args)
            else:
                user = reply.sender_id
            user = await message.client.get_entity(user)
            admin_rights = ChatAdminRights(
                change_info=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                add_admins=False
            )
            await self.client(EditAdminRequest(
                channel=group,
                user_id=user,
                admin_rights=admin_rights,
                rank='admin'
            ))
        except ChatWriteForbiddenError:
            m = self.strings("no_rights", message)
            await utils.answer(message, m)
        except ChannelPrivateError:
            m = self.strings("no_rights", message)
            await utils.answer(message, m)
        except InputUserDeactivatedError:
            m = self.strings("deleted_account", message)
            await utils.answer(message, m)
        except YouBlockedUserError:
            m = self.strings("blocked_contact", message)
            await utils.answer(message, m)
        return

    @loader.command(
        ru_doc="| Удаляет удалённые аккаунты из чата."
    )
    async def flush(self, message: Message):
        """| Removes deleted accounts from the chat."""
        chat = await message.get_chat()

        if isinstance(chat, User):
            await utils.answer(message, self.strings("not_a_chat", message))
            return

        if not chat.admin_rights and not chat.creator:
            await utils.answer(message, self.strings("no_rights", message))
            await message.delete()
            return

        removed_count = 0
        
        edit_message = await utils.answer(message, self.strings("search_deleted_accounts", message))
        if not edit_message:
            edit_message = message

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except ChatAdminRequiredError:
                    await utils.answer(message, self.strings("no_rights", message))
                    return
                except Exception as e:
                    await utils.answer(message, self.strings("rpc_error").format(error=str(e)))
                    return

        if removed_count == 0:
            await utils.answer(message, self.strings("no_deleted_accounts", message))
        else:
            await utils.answer(message, self.strings("kicked_deleted_accounts", message).format(count=removed_count))

    @loader.command(
        ru_doc="| Удаляет все сообщения от тебя."
    )
    async def wipe(self, message):
        """| Deletes all your messages."""
        chat = message.chat
        if chat:
            async for msg in message.client.iter_messages(chat, from_user="me"):
                await msg.delete()
        else:
            await utils.answer(message, self.strings("not_a_chat", message))

    @loader.owner
    async def _is_owner(self, chat_id):
        """Проверяет, является ли пользователь владельцем группы."""
        permissions = await self.client.get_permissions(chat_id, 'me')
        return permissions.is_creator

    async def get_chatinfo(self, event):
        chat = utils.get_args_raw(event)
        chat_info = None
        if chat:
            try:
                chat = int(chat)
            except ValueError:
                pass
        if not chat:
            if event.reply_to_msg_id:
                replied_msg = await event.get_reply_message()
                if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                    chat = replied_msg.fwd_from.channel_id
            else:
                chat = event.chat_id
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except:
            try:
                chat_info = await event.client(GetFullChannelRequest(chat))
            except ChannelInvalidError:
                return None
            except ChannelPrivateError:
                return None
            except ChannelPublicGroupNaError:
                return None
            except:
                chat = event.input_chat
                chat_info = await event.client(GetFullChannelRequest(chat))
                return chat_info
        return chat_info


    async def fetch_info(self, chat, event):
        chat_obj_info = await event.client.get_entity(chat.full_chat.id)
        chat_title = chat_obj_info.title
        try:
            msg_info = await event.client(
                GetHistoryRequest(
                    peer=chat_obj_info.id,
                    offset_id=0,
                    offset_date=datetime(2010, 1, 1),
                    add_offset=-1,
                    limit=1,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
        except Exception:
            msg_info = None
            await utils.answer(event, self.strings("rpc_error", event))
        first_msg_valid = (
            True
            if msg_info and msg_info.messages and msg_info.messages[0].id == 1
            else False
        )
        creator_valid = True if first_msg_valid and msg_info.users else False
        creator_id = msg_info.users[0].id if creator_valid else None
        creator_firstname = (
            msg_info.users[0].first_name
            if creator_valid and msg_info.users[0].first_name is not None
            else self.strings("deleted_account", event)
        )
        creator_username = (
            msg_info.users[0].username
            if creator_valid and msg_info.users[0].username is not None
            else None
        )
        created = msg_info.messages[0].date if first_msg_valid else None
        former_title = (
            msg_info.messages[0].action.title
            if first_msg_valid
            and type(msg_info.messages[0].action) is MessageActionChannelMigrateFrom
            and msg_info.messages[0].action.title != chat_title
            else None
        )
        description = chat.full_chat.about
        members = (
            chat.full_chat.participants_count
            if hasattr(chat.full_chat, "participants_count")
            else chat_obj_info.participants_count
        )
        admins = (
            chat.full_chat.admins_count if hasattr(chat.full_chat, "admins_count") else None
        )
        banned_users = (
            chat.full_chat.kicked_count if hasattr(chat.full_chat, "kicked_count") else None
        )
        restrcited_users = (
            chat.full_chat.banned_count if hasattr(chat.full_chat, "banned_count") else None
        )
        users_online = 0
        async for i in event.client.iter_participants(event.chat_id):
            if isinstance(i.status, UserStatusOnline):
                users_online = users_online + 1
        group_stickers = (
            chat.full_chat.stickerset.title
            if hasattr(chat.full_chat, "stickerset") and chat.full_chat.stickerset
            else None
        )
        messages_viewable = msg_info.count if msg_info else None
        messages_sent = (
            chat.full_chat.read_inbox_max_id
            if hasattr(chat.full_chat, "read_inbox_max_id")
            else None
        )
        messages_sent_alt = (
            chat.full_chat.read_outbox_max_id
            if hasattr(chat.full_chat, "read_outbox_max_id")
            else None
        )
        username = chat_obj_info.username if hasattr(chat_obj_info, "username") else None
        bots_list = chat.full_chat.bot_info
        bots = 0
        slowmode = (
            self.strings("yes", event)
            if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
            else self.strings("no", event)
        )
        slowmode_time = (
            chat.full_chat.slowmode_seconds
            if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled
            else None
        )
        restricted = (
            self.strings("yes", event)
            if hasattr(chat_obj_info, "restricted") and chat_obj_info.restricted
            else self.strings("no", event)
        )
        verified = (
            self.strings("Yes", event) if hasattr(chat_obj_info, "verified") and chat_obj_info.verified else self.strings("no", event)
        )
        username = "@{}".format(username) if username else None
        creator_username = "@{}".format(creator_username) if creator_username else None

        if admins is None:
            try:
                participants_admins = await event.client(
                    GetParticipantsRequest(
                        channel=chat.full_chat.id,
                        filter=ChannelParticipantsAdmins(),
                        offset=0,
                        limit=0,
                        hash=0,
                    )
                )
                admins = participants_admins.count if participants_admins else None
            except Exception:
                await utils.answer(event, self.strings("rpc_error", event))
        if bots_list:
            for bot in bots_list:
                bots += 1

        caption = self.strings("chat_info_header", event)
        caption += f"<b>ID:</b> {chat_obj_info.id}\n"
        if chat_title is not None:
            caption += self.strings("group_title", event).format(title=chat_title)
        if former_title is not None:
            caption += self.strings("previous_title", event).format(title=former_title)
        if username is not None:
            caption += self.strings("group_type_public", event)
            caption += self.strings("group_link", event).format(link=username)
        else:
            caption += self.strings("group_type_private", event)
        if creator_username is not None:
            caption += self.strings("group_creator_username", event).format(username=creator_username)
        elif creator_valid:
            caption += self.strings("group_creator_link", event).format(
                id=creator_id, firstname=creator_firstname
            )
        if created is not None:
            caption += self.strings("group_created", event).format(
                date=created.date().strftime('%b %d, %Y'), time=created.time()
            )
        else:
            caption += self.strings("group_created", event).format(
                date=chat_obj_info.date.date().strftime('%b %d, %Y'),
                time=chat_obj_info.date.time()
            )
        if messages_viewable is not None:
            caption += self.strings("messages_viewable", event).format(count=messages_viewable)
        if messages_sent:
            caption += self.strings("messages_sent", event).format(count=messages_sent)
        elif messages_sent_alt:
            caption += self.strings("messages_sent", event).format(count=messages_sent_alt)
        if members is not None:
            caption += self.strings("group_members", event).format(count=members)
        if admins is not None:
            caption += self.strings("group_admins", event).format(count=admins)
        if bots_list:
            caption += self.strings("group_bots", event).format(count=bots)
        if users_online:
            caption += self.strings("group_online", event).format(count=users_online)
        if restrcited_users is not None:
            caption += self.strings("group_restricted", event).format(count=restrcited_users)
        if banned_users is not None:
            caption += self.strings("group_banned", event).format(count=banned_users)
        if group_stickers is not None:
            caption += self.strings("group_stickers", event).format(
                stickers=f"t.me/addstickers/{chat.full_chat.stickerset.short_name}"
            )
        caption += "\n"
        caption += self.strings("group_slowmode", event).format(slowmode=slowmode)
        if hasattr(chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled:
            caption += self.strings("group_slowmode_time", event).format(time=slowmode_time)
        else:
            caption += "\n"
        caption += self.strings("group_restricted_status", event).format(restricted=restricted)
        if chat_obj_info.restricted:
            caption += self.strings("group_restriction_details", event).format(
                platform=chat_obj_info.restriction_reason[0].platform,
                reason=chat_obj_info.restriction_reason[0].reason,
                text=chat_obj_info.restriction_reason[0].text
            )
        else:
            caption += ""
        if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
            caption += self.strings("group_scam", event)
        if hasattr(chat_obj_info, "verified"):
            caption += self.strings("group_verified", event).format(verified=verified)
        if description:
            caption += self.strings("group_description", event).format(description=description)
        return caption