# meta developer: @xdesai

from .. import loader, utils
from telethon.errors import UserNotParticipantError

@loader.tds
class CheckAdminRightsMod(loader.Module):
    strings_ru = {
        "change_info": "Изменение профиля",
        "delete_messages": "Удаление сообщений",
        "ban_users": "Блокировка пользователей",
        "invite_users": "Добавление участников",
        "pin_messages": "Закрепление сообщений",
        "post_stories": "Публикация историй",
        "edit_stories": "Изменение историй",
        "delete_stories": "Удаление историй",
        "manage_call": "Управление трансляциями",
        "anonymous": "Анонимность",
        "add_admins": "Назначение админов",
        "manage_topics": "Управление темами",
        "post_messages": "Публиковать сообщения",
        "edit_messages": "Изменять сообщения",
        "loading": "<blockquote><emoji document_id=5355040476774815817>🕰</emoji> <b>Обработка данных...</b></blockquote>",
        "not_a_chat": "<blockquote><emoji document_id=5312526098750252863>❌</emoji> <b>Команда не может быть запущена в личных сообщениях.</b></blockquote>",
        "no_user": "<blockquote><emoji document_id=5312383351217201533>⚠️</emoji> <b>Вы не указали пользователя.</b></blockquote>",
        "get_rights_header": "Права <a href='tg://user?id={id}'>{name}</a> в этом чате:",
        "not_admin": "<blockquote>❌ <a href='tg://user?id={id}'>{name}</a> не администратор</blockquote>\n"
    }

    strings = {
        "name": "CheckAdminRights",
        "change_info": "Change info",
        "delete_messages": "Delete messages",
        "ban_users": "Ban users",
        "invite_users": "Add members",
        "pin_messages": "Pin messages",
        "post_stories": "Post stories",
        "edit_stories": "Edit stories",
        "delete_stories": "Delete stories",
        "manage_call": "Manage call",
        "anonymous": "Anonymous",
        "add_admins": "Add admins",
        "manage_topics": "Manage topics",
        "post_messages": "Post messages",
        "edit_messages": "Edit messages",
        "loading": "<blockquote><emoji document_id=5355040476774815817>🕰</emoji> <b>Processing data...</b></blockquote>",
        "admin_rights": "<emoji document_id=5818778798782420696>➡️</emoji> <u>Admin rights:</u>\n",
        "get_rights_header": "<a href='tg://user?id={id}'>{name}</a>'s rights in this chat:",
        "not_admin": "<blockquote>❌ <a href='tg://user?id={id}'>{name}</a> is not an admin</blockquote>\n",
        "not_a_chat": "<blockquote><emoji document_id=5312526098750252863>❌</emoji> <b>The command cannot be run in private messages.</b></blockquote>",
        "no_user": "<blockquote><emoji document_id=5312383351217201533>⚠️</emoji> <b>You did not specify a user.</b></blockquote>",
    }
    @loader.command(
        ru_doc="<reply/username/id> | Проверить права в текущем чате."
    )
    async def rights(self, message):
        """<reply/username/id> | Check rights in the current chat."""
        if message.is_private:
            return await utils.answer(message, self.strings('not_a_chat'))
        await utils.answer(message, self.strings("loading"))
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chat = await message.get_chat()
        chat_id = message.chat_id
        admin_rights_g = [
            "change_info",
            "delete_messages",
            "ban_users",
            "invite_users",
            "pin_messages",
            "post_stories",
            "edit_stories",
            "delete_stories",
            "manage_call",
            "anonymous",
            "add_admins",
            "manage_topics",
        ]
        admin_rights_c = [
            "change_info",
            "post_messages",
            "edit_messages",
            "delete_messages",
            "post_stories",
            "edit_stories",
            "delete_stories",
            "invite_users",
            "ban_users",
            "add_admins",
            "manage_call",
        ]
        if not args:
            if not reply:
                return await utils.answer(message, self.strings("no_user"))
            else:
                user = await reply.get_sender()
                permissions = await self.client.get_permissions(chat, user)
                if user is None:
                    return await utils.answer(message, self.strings("no_user"))
                header = self.strings('get_rights_header').format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")
                result = ""

                if permissions.has_default_permissions:
                    result += self.strings("not_admin").format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")
                else:
                    result += self.strings('admin_rights')
                    if message.is_channel and chat.broadcast:
                        for right in admin_rights_c:
                            has_permission = getattr(permissions, right, False)
                            result += f"{'<emoji document_id=5021905410089550576>✅</emoji>' if has_permission else '<emoji document_id=5019523782004441717>❌</emoji>'} {self.strings(right)}\n"
                    else:
                        for right in admin_rights_g:
                            has_permission = getattr(permissions, right, False)
                            result += f"{'<emoji document_id=5021905410089550576>✅</emoji>' if has_permission else '<emoji document_id=5019523782004441717>❌</emoji>'} {self.strings(right)}\n"

                await utils.answer(message, f"<blockquote><b>{header}</blockquote>\n\n<blockquote>{result}</b></blockquote>")
        else:
            args = utils.get_args_raw(message).split()
            user = await self.client.get_entity(int(args[0]) if args[0].isdigit() else args[0])
            try:
                permissions = await self.client.get_permissions(chat, user)
            except UserNotParticipantError:
                return await utils.answer(message, self.strings("no_user", message))
            if permissions.has_left:
                return await utils.answer(message, self.strings("no_user", message))

            header = self.strings('get_rights_header').format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")
            result = ""

            if permissions.has_default_permissions:
                result += self.strings("not_admin").format(id=user.id, name=f"{user.first_name or ''} {user.last_name or ''}")
            else:
                result += self.strings('admin_rights')
                if message.is_channel and chat.broadcast:
                    for right in admin_rights_c:
                        has_permission = getattr(permissions, right, False)
                        result += f"{'<emoji document_id=5021905410089550576>✅</emoji>' if has_permission else '<emoji document_id=5019523782004441717>❌</emoji>'} {self.strings(right)}\n"
                else:
                    for right in admin_rights_g:
                            has_permission = getattr(permissions, right, False)
                            result += f"{'<emoji document_id=5021905410089550576>✅</emoji>' if has_permission else '<emoji document_id=5019523782004441717>❌</emoji>'} {self.strings(right)}\n"

            await utils.answer(message, f"<blockquote><b>{header}</blockquote>\n\n<blockquote>{result}</b></blockquote>")
