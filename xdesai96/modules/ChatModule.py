# meta developer: @xdesai

from datetime import timedelta, datetime, timezone
import os
from .. import loader, utils
from telethon.tl.functions.channels import (
    GetParticipantRequest,
    LeaveChannelRequest,
    DeleteChannelRequest,
    EditTitleRequest,
)
from telethon.errors import (
    UserNotParticipantError,
    UserIdInvalidError,
    MessageTooLongError,
)
from telethon.tl.types import (
    Channel,
    Chat,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
    ChatBannedRights,
)
from telethon.tl.functions.messages import (
    DeleteChatRequest,
    EditChatDefaultBannedRightsRequest,
    EditChatTitleRequest,
)


@loader.tds
class ChatModuleMod(loader.Module):
    strings = {
        "name": "ChatModule",
        "my_id": "<emoji document_id=5208454037531280484>💜</emoji> <b>My ID:</b> <code>{my_id}</code>",
        "chat_id": "<emoji document_id=5886436057091673541>💬</emoji> <b>Chat ID:</b> <code>{chat_id}</code>",
        "user_id": "<emoji document_id=6035084557378654059>👤</emoji> <b>User's ID:</b> <code>{user_id}</code>",
        "user_not_found": "<emoji document_id=5019523782004441717>❌</emoji> <b>User not found.</b>",
        "user_not_participant": "<emoji document_id=5019523782004441717>❌</emoji> <b>User is not in this group.</b>",
        "rights_header": '<b><a href="tg://user?id={id}">{name}</a>\'s rights in this chat\n\n',
        "not_an_admin": "<emoji document_id=5019523782004441717>❌</emoji> {user} is not an admin.",
        "no_rights": "<emoji document_id=5019523782004441717>❌</emoji> <b>I don't have enough rights :(</b>",
        "no_user": "<emoji document_id=5019523782004441717>❌</emoji> <b>User not found.</b>",
        "change_info": "Change Info",
        "delete_messages": "Delete Messages",
        "ban_users": "Ban users",
        "invite_users": "Invite Users",
        "pin_messages": "Pin Messages",
        "add_admins": "Add Admins",
        "manage_call": "Manage Call",
        "post_stories": "Post Stories",
        "edit_stories": "Edit Stories",
        "delete_stories": "Delete Stories",
        "anonymous": "Anonymous",
        "manage_topics": "Manage Topics",
        "post_messages": "Post messages",
        "edit_messages": "Edit messages",
        "invalid_args": "<emoji document_id=5019523782004441717>❌</emoji> <b>Invalid args.</b>",
        "error": "<b>Error:</b> <code>{error}</code>",
        "of_chat": "Chat",
        "of_channel": "Channel",
        "loading": "<emoji document_id=5021712394259268143>🟡</emoji> <b>Loading data ...</b>",
        "own_list": "<b>My possessions ({count}):</b>\n\n{msg}",
        "no_ownerships": "<emoji document_id=5019523782004441717>❌</emoji> <b>No possessions.</b>",
        "not_a_chat": "<emoji document_id=5276240711795107620>⚠️</emoji> <b>It works only in groups!</b>",
        "successful_delete": "<emoji document_id=5021905410089550576>✅</emoji> {chat_type} successfully deleted",
        "search_deleted_accounts": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching for deleted accounts</b>",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>No deleted accounts found here</b>",
        "kicked_deleted_accounts": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Removed {count} deleted accounts</b>",
        "admins_in_chat": "<emoji document_id=5276229330131772747>👑</emoji> <b>Admins in <code>{title}</code> ({count}):</b>\n\n",
        "admins_in_chat_caption": '<b>Admins in "{}":</b>',
        "too_many_admins": "Damn, too many admins here. Loading the list of admins into a file...",
        "no_admins_in_chat": "<b>No admins in this chat.</b>",
        "bots_in_chat": "<emoji document_id=5276127848644503161>🤖</emoji> <b>Bots in <code>{title}</code> ({count}):</b>\n\n",
        "bots_in_chat_caption": "<b>Bots in <code>{}</code>:</b>",
        "too_many_bots": "Damn, too many bots here. Loading the list of bots into a file...",
        "no_bots_in_chat": "<b>No bots in this chat.</b>",
        "users_in_chat": "<emoji document_id=5275979556308674886>👤</emoji> <b>Users in <code>{title}</code> ({count}):</b>\n\n",
        "users_in_chat_caption": "<b>Users in <code>{}</code>:</b>",
        "no_user_in_chat": "<b>No users in this chat.</b>",
        "user_is_banned": "⛔️ <b>{name} [<code>{id}</code>] has been banned for {time_info}.</b>",
        "user_is_banned_with_reason": "⛔️ <b>{name} [<code>{id}</code>] has been banned for {time_info}.</b>\n<i>Reason: {reason}</i>",
        "user_is_banned_forever": "⛔️ <b>{name} [<code>{id}</code>] has been banned forever.</b>",
        "user_is_banned_forever_with_reason": "⛔️ <b>{name} [<code>{id}</code>] has been banned forever.</b>\n<i>Reason: {reason}</i>",
        "minutes": "{time} minutes",
        "hours": "{time} hours",
        "days": "{time} days",
        "user_is_unbanned": "👋🏻 <b>{name} [<code>{id}</code>] has been unbanned.</b>",
        "user_is_kicked": "🍃 <b><code>{name}</code> [<code>{id}</code>] has been kicked.</b>",
        "user_is_kicked_with_reason": "🍃 <b><code>{name}</code> [<code>{id}</code>] has been kicked.</b>\n<i>Reason: {reason}</i>",
        "user_is_muted_with_reason": "🔇 <b>{name} [<code>{id}</code>] has been muted for {time_info}.</b>\n<i>Reason: {reason}</i>",
        "user_is_muted": "🔇 <b>{name} [<code>{id}</code>] has been muted for {time_info}.</b>",
        "user_is_muted_with_reason_forever": "🔇 <b>{name} [<code>{id}</code>] has been muted forever.</b>\n<i>Reason: {reason}</i>",
        "user_is_muted_forever": "🔇 <b>{name} [<code>{id}</code>] has been muted forever.</b>",
        "user_is_unmuted": "🔊 <b>{name} [<code>{id}</code>] has been unmuted.</b>",
        "chat_muted": "🔇 <b>The chat is now muted for participants.</b>",
        "chat_unmuted": "✅ <b>The chat is now open to all participants.</b>",
        "title_changed": "<b>The {type_of} title was successfully changed from <code>{old_title}</code> to <code>{new_title}</code>.</b>",
    }

    @loader.command(ru_doc="[reply] - Узнать ID")
    async def id(self, message):
        """[reply] - Get the ID"""
        my_id = (await self._client.get_me()).id
        chat = await message.get_chat()
        chat_id = chat.id
        reply = await message.get_reply_message()
        user_id = None
        if reply and not message.is_private:
            user_id = reply.sender_id
        output = f"{self.strings('my_id').format(my_id=my_id)}\n{self.strings('chat_id').format(chat_id=chat_id)}"
        if user_id:
            output += f"\n{self.strings('user_id').format(user_id=user_id)}"
        return await utils.answer(message, output)

    @loader.command(
        ru_doc="[reply/username/id] - Посмотреть права администратора пользователя"
    )
    async def rights(self, message):
        """[reply/username/id] - Check user's admin rights"""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if message.is_group and message.is_channel:
            rights = [
                "change_info",
                "delete_messages",
                "ban_users",
                "invite_users",
                "pin_messages",
                "add_admins",
                "manage_call",
                "post_stories",
                "edit_stories",
                "delete_stories",
                "anonymous",
                "manage_topics",
                "post_messages",
                "edit_messages",
            ]
            if reply:
                participant_id = reply.sender_id
            else:
                if args:
                    participant_id = (
                        args[0] if not args[0].strip().isdigit() else int(args[0])
                    )
                else:
                    return await utils.answer(message, self.strings("user_not_found"))
            try:
                result = await self._client(
                    GetParticipantRequest(channel=chat, participant=participant_id)
                )
            except UserNotParticipantError:
                return await utils.answer(
                    message,
                    self.strings("user_not_participant").format(user=participant_id),
                )
            except (UserIdInvalidError, ValueError):
                return await utils.answer(
                    message, self.strings("no_user").format(user=participant_id)
                )
            user = await self._client.get_entity(participant_id)
            participant = result.participant
            output = f"{self.strings('not_an_admin').format(user=user.first_name)}"
            if hasattr(participant, "admin_rights") and participant.admin_rights:
                output = self.strings("rights_header").format(
                    name=user.first_name, id=user.id
                )
                can_do = ""
                for right in rights:
                    if getattr(participant.admin_rights, right):
                        can_do += f"<emoji document_id=6296367896398399651>✅</emoji> {self.strings(right)}\n"
                if not can_do:
                    can_do += "No rights"
                output += can_do

            return await utils.answer(
                message, f"<blockquote expandable><b>{output}</b></blockquote>"
            )

    @loader.command(ru_doc="Покинуть чат")
    async def leave(self, message):
        """Leave chat"""
        await message.delete()
        await self._client(LeaveChannelRequest((await message.get_chat()).id))

    @loader.command(ru_doc="[a[1-100] b[1-100]] | [reply] Удалить сообщения")
    async def d(self, message):
        """[a[1-100] b[1-100]] | [reply] - Delete messages"""
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        await message.delete()
        if args:
            direction = args[0][0]
            try:
                count = int(args[0][1:])
                if count < 1 or count > 99:
                    return await utils.answer(message, self.strings("invalid_args"))
            except:
                count = 99
            if reply:
                ids = [reply.id]
                if direction == "a":
                    messages = await self._client.get_messages(
                        reply.chat_id, min_id=reply.id, limit=count, reverse=True
                    )
                    ids.extend([msg.id for msg in messages])
                elif direction == "b":
                    messages = await self._client.get_messages(
                        reply.chat_id, max_id=reply.id, limit=count - 1
                    )
                    ids.extend([msg.id for msg in messages])
                else:
                    return await utils.answer(message, self.strings("invalid_args"))
                try:
                    await self._client.delete_messages(reply.chat_id, ids)
                except Exception as e:
                    await utils.answer(message, self.strings("error").format(error=e))
        else:
            if reply:
                try:
                    await reply.delete()
                except:
                    return
            else:
                return

    @loader.command(
        ru_doc="Показывает список чатов, каналов и групп где вы админ/владелец"
    )
    async def own(self, message):
        """Shows the list of chats, channels and groups where you are an admin/owner"""
        count = 0
        msg = ""
        async for dialog in self._client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                chat = await self._client.get_entity(dialog.id)
                if chat.admin_rights or chat.creator:
                    count += 1
                    chat_type = (
                        self.strings("of_chat")
                        if dialog.is_group
                        else self.strings("of_channel")
                    )
                    msg += f"• {chat.title} <b>({chat_type})</b> | <code>{chat.id}</code>\n"

        if msg:
            await utils.answer(
                message,
                f"<blockquote expandable><b>{self.strings('own_list').format(count=count, msg=msg)}</b></blockquote>",
                parse_mode="html",
            )
        else:
            await utils.answer(message, self.strings("no_ownerships", message))

    @loader.command(ru_doc="[link/id] Удаляет группу/канал")
    async def dgc(self, message):
        """[link/id] Delete chat/channel"""
        args = utils.get_args(message)
        if not args:
            if message.is_private:
                return await utils.answer(message, self.strings("not_a_chat"))
            chat = await self._client.get_entity(message.chat_id)
            if message.is_channel:
                chat_type = self.strings("of_channel")
                await self._client(DeleteChannelRequest(chat.id))
            else:
                chat_type = self.strings("of_chat")
                await self._client(DeleteChatRequest(chat.id))
            return
        else:
            link = (
                await self._client.get_entity(int(args[0]))
                if args[0].isdigit()
                else await self._client.get_entity(args[0])
            )
            if isinstance(link, Channel):
                chat_type = self.strings("of_channel")
                await self._client(DeleteChannelRequest(link.id))
            elif isinstance(link, Chat):
                chat_type = self.strings("of_chat")
                await self._client(DeleteChatRequest(link.id))
            else:
                return await utils.answer(message, self.strings("invalid_args"))
        return await utils.answer(
            message, self.strings("successful_delete").format(chat_type=chat_type)
        )

    @loader.command(ru_doc="Очищает группу/канал от удаленных аккаунтов")
    async def flush(self, message):
        """Removes deleted accounts from the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))

        chat = await message.get_chat()

        if not chat.admin_rights and not chat.creator:
            return await utils.answer(message, self.strings("no_rights"))

        removed_count = 0

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except ChatAdminRequiredError:
                    return await utils.answer(message, self.strings("no_rights"))
                except Exception as e:
                    return await utils.answer(
                        message, self.strings("error").format(error=str(e))
                    )

        if removed_count == 0:
            await utils.answer(message, self.strings("no_deleted_accounts"))
        else:
            await utils.answer(
                message,
                self.strings("kicked_deleted_accounts").format(count=removed_count),
            )

    @loader.command(ru_doc="Показывает админов в группе/канале")
    async def admins(self, message):
        """Shows the admins in the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        title = chat.title
        admins = await self._client.get_participants(
            message.chat_id, filter=ChannelParticipantsAdmins()
        )
        real_members = [
            member for member in admins if not member.bot and not member.deleted
        ]
        admins_header = self.strings("admins_in_chat").format(
            title=title, count=len(real_members)
        )
        if len(real_members) == 0:
            return await utils.answer(message, "no_admins_in_chat")
        for user in real_members:
            if not user.deleted:
                admins_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
            try:
                await utils.answer(
                    message,
                    f"<blockquote expandable><b>{admins_header}</b></blockquote>",
                )
            except MessageTooLongError:
                await utils.answer(message, self.strings("too_many_admins"))
                with open("adminlist.md", "w+") as file:
                    file.write(admins_header)
                await message.client.send_file(
                    message.chat_id,
                    "adminlist.md",
                    caption=self.strings("admins_in_chat_caption").format(title),
                    reply_to=message.id,
                )
                os.remove("adminlist.md")
                await message.delete()

    @loader.command(ru_doc="Показывает ботов в группе/канале")
    async def bots(self, message):
        """Shows the bots in the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        title = chat.title
        bots = await self._client.get_participants(
            message.chat_id, filter=ChannelParticipantsBots()
        )
        bots_header = self.strings("bots_in_chat").format(title=title, count=len(bots))
        if len(bots) == 0:
            return await utils.answer(message, self.strings("no_bots_in_chat"))
        for user in bots:
            if not user.deleted:
                bots_header += f'<emoji document_id=5316712579467321913>🔴</emoji> <a href="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
            try:
                await utils.answer(
                    message, f"<blockquote expandable><b>{bots_header}</b></blockquote>"
                )
            except MessageTooLongError:
                await utils.answer(message, self.strings("too_many_bots"))
                with open("botlist.md", "w+") as file:
                    file.write(bots_header)
                await message.client.send_file(
                    message.chat_id,
                    "adminlist.md",
                    caption=self.strings("bots_in_chat_caption").format(title),
                    reply_to=message.id,
                )
                os.remove("botlist.md")
                await message.delete()

    @loader.command(ru_doc="Показывает простых участников чата/канала")
    async def users(self, message):
        """Shows the users in the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        title = chat.title
        users = await self._client.get_participants(message.chat_id)
        real_users = [
            member for member in users if not member.bot and not member.deleted
        ]
        users_header = self.strings("users_in_chat").format(
            title=title, count=len(real_users)
        )
        if len(real_users) == 0:
            return await utils.answer(message, self.strings("no_user_in_chat"))
        for user in users:
            if not user.bot and not user.deleted:
                users_header += f'<emoji document_id=5314378500965145730>🔵</emoji> <a href ="tg://user?id={user.id}">{user.first_name}</a> | <code>{user.id}</code>\n'
        try:
            await utils.answer(
                message, f"<blockquote expandable><b>{users_header}</b></blockquote>"
            )
            return
        except MessageTooLongError:
            await utils.answer(message, self.strings("large_chat_loading"))
            file = open("userslist.md", "w+")
            file.write(users_header)
            file.close()
            await message.client.send_file(
                message.chat_id,
                "userslist.md",
                caption=self.strings("users_in_chat_caption").format(title),
                reply_to=message.id,
            )
            os.remove("userslist.md")
            await message.delete()
            return

    @loader.command(ru_doc="Забанить участника")
    async def ban(self, message):
        """Ban a participant"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        args = utils.get_args(message)
        reason = ""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        until = 0
        now = None
        if not reply and args:
            if args[0].startswith("@"):
                id = "".join(args[0][1:])
            elif args[1].startswith("@"):
                time = int(args[0][:-1])
                unit = args[0][-1]
                now = datetime.now(timezone.utc)
                id = "".join(args[1][1:])
                if unit == "m":
                    until = now + timedelta(minutes=time)
                    time_info = self.strings("minutes").format(time=time)
                elif unit == "h":
                    until = now + timedelta(hours=time)
                    time_info = self.strings("hours").format(time=time)
                elif unit == "d":
                    until = now + timedelta(days=time)
                    time_info = self.strings("days").format(time=time)
                else:
                    return utils.answer(message, self.strings("invalid_args"))
            user = await self._client.get_entity(id if not id.isdigit() else int(id))
        elif reply and args:
            if args[0][0].isdigit() and not args[0][-1].isdigit():
                time = int(args[0][:-1])
                unit = args[0][-1]
                now = datetime.now(timezone.utc)
                id = reply.sender_id
                if unit == "m":
                    until = now + timedelta(minutes=time)
                    time_info = self.strings("minutes").format(time=time)
                elif unit == "h":
                    until = now + timedelta(hours=time)
                    time_info = self.strings("hours").format(time=time)
                elif unit == "d":
                    until = now + timedelta(days=time)
                    time_info = self.strings("days").format(time=time)
                else:
                    return utils.answer(message, self.strings("invalid_args"))
            else:
                id = reply.sender_id
            user = await self._client.get_entity(id)
        elif reply and not args:
            user = await self._client.get_entity(reply.sender_id)
        elif not reply and not args:
            return await utils.answer(message, self.strings("invalid_args"))
        if "\n" in message.text:
            reason = message.text.split("\n", 1)[1]

        if until != 0:
            if reason:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_banned_with_reason").format(
                        id=user.id,
                        name=user.first_name,
                        reason=reason,
                        time_info=time_info,
                    ),
                )
            else:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_banned").format(
                        id=user.id, name=user.first_name, time_info=time_info
                    ),
                )
        else:
            if reason:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_banned_forever_with_reason").format(
                        id=user.id, name=user.first_name, reason=reason
                    ),
                )
            else:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_banned_forever").format(
                        id=user.id, name=user.first_name
                    ),
                )
        await self._client.edit_permissions(
            chat, user, until_date=until, view_messages=False
        )
        return ret

    @loader.command(ru_doc="Разбанить пользователя")
    async def unban(self, message):
        """Unban a user"""
        if message.is_private:
            return await utils.answer(self.strings("not_a_chat"))
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        user = None
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        elif args:
            user = await self._client.get_entity(
                args[0] if not args[0].isdigit() else int(args[0])
            )
        else:
            return await utils.answer(self.strings("no_user"))
        chat = await message.get_chat()
        await self._client.edit_permissions(chat, user, view_messages=True)
        return await utils.answer(
            message,
            self.strings("user_is_unbanned").format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Кикнуть участника")
    async def kick(self, message):
        """Kick a participant"""
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        reason = ""
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        elif args:
            user = await self._client.get_entity(
                args[0] if not args[0].isdigit() else int(args[0])
            )
        else:
            return await utils.answer(message, self.strings("no_user"))
        if "\n" in message.text:
            reason = message.text.split("\n", 1)[1]
        chat = await message.get_chat()
        await self._client.kick_participant(chat, user)
        return (
            await utils.answer(
                message,
                self.strings("user_is_kicked").format(id=user.id, name=user.first_name),
            )
            if not reason
            else await utils.answer(
                message,
                self.strings("user_is_kicked_with_reason").format(
                    id=user.id, name=user.first_name, reason=reason
                ),
            )
        )

    @loader.command(ru_doc="Замутить участника")
    async def mute(self, message):
        """Mute a participant"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        args = utils.get_args(message)
        reason = ""
        chat = await message.get_chat()
        reply = await message.get_reply_message()
        until = 0
        now = None
        if not reply and args:
            if args[0].startswith("@"):
                id = "".join(args[0][1:])
            elif args[1].startswith("@"):
                time = int(args[0][:-1])
                unit = args[0][-1]
                now = datetime.now(timezone.utc)
                id = "".join(args[1][1:])
                if unit == "m":
                    until = now + timedelta(minutes=time)
                    time_info = self.strings("minutes").format(time=time)
                elif unit == "h":
                    until = now + timedelta(hours=time)
                    time_info = self.strings("hours").format(time=time)
                elif unit == "d":
                    until = now + timedelta(days=time)
                    time_info = self.strings("days").format(time=time)
                else:
                    return utils.answer(message, self.strings("invalid_args"))
            user = await self._client.get_entity(id if not id.isdigit() else int(id))
        elif reply and args:
            if args[0][0].isdigit() and not args[0][-1].isdigit():
                time = int(args[0][:-1])
                unit = args[0][-1]
                now = datetime.now(timezone.utc)
                id = reply.sender_id
                if unit == "m":
                    until = now + timedelta(minutes=time)
                    time_info = self.strings("minutes").format(time=time)
                elif unit == "h":
                    until = now + timedelta(hours=time)
                    time_info = self.strings("hours").format(time=time)
                elif unit == "d":
                    until = now + timedelta(days=time)
                    time_info = self.strings("days").format(time=time)
                else:
                    return utils.answer(message, self.strings("invalid_args"))
            else:
                id = reply.sender_id
            user = await self._client.get_entity(id)
        elif reply and not args:
            user = await self._client.get_entity(reply.sender_id)
        elif not reply and not args:
            return await utils.answer(message, self.strings("invalid_args"))

        if "\n" in message.text:
            reason = message.text.split("\n", 1)[1]
        if until != 0:
            if reason:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_muted_with_reason").format(
                        id=user.id,
                        name=user.first_name,
                        time_info=time_info,
                        reason=reason,
                    ),
                )
            else:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_muted").format(
                        id=user.id,
                        name=user.first_name,
                        time_info=time_info,
                    ),
                )
        else:
            if reason:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_muted_with_reason_forever").format(
                        id=user.id, name=user.first_name, reason=reason
                    ),
                )
            else:
                ret = await utils.answer(
                    message,
                    self.strings("user_is_muted_forever").format(
                        id=user.id, name=user.first_name
                    ),
                )
        await self._client.edit_permissions(
            chat,
            user,
            until_date=until,
            send_messages=False,
            send_media=False,
            send_stickers=False,
            send_gifs=False,
            send_games=False,
            send_inline=False,
            send_polls=False,
        )
        return ret

    @loader.command(ru_doc="Размутить участника")
    async def unmute(self, message):
        """Unmute a participant"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        args = utils.get_args(message)
        reply = await message.get_reply_message()
        chat = await message.get_chat()
        if reply:
            user = await self._client.get_entity(reply.sender_id)
        elif args:
            user = await self._client.get_entity(
                args[0] if not args[0].isdigit() else int(args[0])
            )
        else:
            return await utils.answer(message, "no_user")

        await self._client.edit_permissions(
            chat,
            user,
            send_messages=True,
            send_media=True,
            send_stickers=True,
            send_gifs=True,
            send_games=True,
            send_inline=True,
            send_polls=True,
        )
        return await utils.answer(
            message,
            self.strings("user_is_unmuted").format(id=user.id, name=user.first_name),
        )

    @loader.command(ru_doc="Закрыть чат для всех кроме админов")
    async def mc(self, message):
        """Mute the chat for everyone except admins"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        current = chat.default_banned_rights
        is_muted = current.send_messages is True
        await self._client(
            EditChatDefaultBannedRightsRequest(
                chat,
                ChatBannedRights(
                    until_date=0,
                    send_messages=not is_muted,
                    send_media=not is_muted,
                    send_stickers=not is_muted,
                    send_gifs=not is_muted,
                    send_games=not is_muted,
                    send_inline=not is_muted,
                    send_polls=not is_muted,
                    send_photos=not is_muted,
                    send_videos=not is_muted,
                    send_roundvideos=not is_muted,
                    send_audios=not is_muted,
                    send_voices=not is_muted,
                    send_docs=not is_muted,
                    send_plain=not is_muted,
                ),
            )
        )
        if is_muted:
            return await utils.answer(message, self.strings("chat_unmuted"))
        else:
            return await utils.answer(message, self.strings("chat_muted"))

    @loader.command(ru_doc="Переименовать группу/канал")
    async def rename(self, message):
        """Rename the chat/channel"""
        if message.is_private:
            return await utils.answer(message, self.strings("not_a_chat"))
        chat = await message.get_chat()
        old_title = chat.title
        new_title = utils.get_args_raw(message)
        if message.is_channel:
            if message.is_group:
                type_of = self.strings("of_chat")
            else:
                type_of = self.strings("of_channel")
            await self._client(EditTitleRequest(channel=chat, title=new_title))
        else:
            type_of = self.strings("of_chat")
            await self._client(EditChatTitleRequest(chat_id=chat.id, title=new_title))
        return await utils.answer(
            message,
            self.strings("title_changed").format(
                old_title=old_title, new_title=new_title, type_of=type_of
            ),
        )
