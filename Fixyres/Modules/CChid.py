__version__ = (2, 0, 10)
          
#            ▀█▀  █ █ █▀█  █▀▄▀█  ▄▀█ █▀
#             █  █▀█ █▄█ █ ▀  █ █▀█ ▄█  
#            https://t.me/netuzb
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://te.legra.ph/file/029eb6160b704b826c34a.png
# meta banner: https://te.legra.ph/file/c8577322bd5ce031efdca.jpg
# meta developer: @wilsonmods
# scope: hikka_only
# scope: hikka_min 1.3.0

import asyncio
import io
from asyncio import sleep
from os import remove

from telethon import errors, functions
from telethon.errors import (
    BotGroupsBlockedError,
    ChannelPrivateError,
    ChatAdminRequiredError,
    ChatWriteForbiddenError,
    InputUserDeactivatedError,
    MessageTooLongError,
    UserAlreadyParticipantError,
    UserBlockedError,
    UserIdInvalidError,
    UserKickedError,
    UserNotMutualContactError,
    UserPrivacyRestrictedError,
    YouBlockedUserError,
)
from telethon.tl.functions.channels import InviteToChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, GetCommonChatsRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChannelParticipantCreator,
    ChannelParticipantsAdmins,
    ChannelParticipantsBots,
)

from .. import loader, utils


@loader.tds
class CChidMod(loader.Module):
    """Модуль идентификации пользователей

> Надеюсь вам понравятся...
> И другие модули: @wilsonmods"""

    strings = {"name": "🆔 CChid"}

    async def client_ready(self, client, db):
        self.db = db

    async def chidcmd(self, message):
        """> Введите идентификационный номер или имя пользователя"""
        text = utils.get_args_raw(message) 
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()        
        if not text and not reply:
        	await message.edit("<b>🚨 Пожалуйста, введите ID или имя пользователя</b>")
        try:
            if args:            	
                user = await message.client.get_entity(                
                args if not args.isdigit() else int(args))
        except ValueError:           
            user = await message.client.get_entity(GetFullUserRequest(message.sender_id))
        
        user_id = f"""<b>🔥 Информация о <b><u>{text}</u></b>:</b>

<b>👤 Имя:</b> <code>{user.first_name}</code>
<b>👤 Фамилия:</b> <code>{user.last_name}</code>
<b>🗄️ Имя пользователя:</b> <code>@{user.username}</code>
<b>🔢 Номер:</b> <code>{user.phone}</code>
<b>🆔 ID номер:</b> <code>{user.id}</code>

<b>🧹 Удаленный аккаунт:</b> <code>{user.deleted}</code>
<b>✔️ Подтвержденный аккаунт:</b> <code>{user.verified}</code>
<b>👥 Контакт доступен:</b> <code>{user.contact}</code>

<b>🚨 Не забудьте инструкцию:</b> <code>.chid username</code>"""

        await self.inline.form(
                    text = user_id,
                    reply_markup=[
                    [{
                        "text": "↗️ Пользователь здесь", 
                        "url": f"https://t.me/{text}"
                    }],
                    [{
                        "text": "🔻 Закрыть", 
                        "action": "close"
                    }]], 
                        **{"photo": "https://i.imgur.com/sbvNwt4.jpeg"},
                    message=message,
                )
    
    async def toidcmd(self, message):
        """> Найти человека по идентификационному номеру"""
        text = utils.get_args_raw(message)
        toid = f"🆔 <b>ID номер:</b> <code>{text}</code>\n👤 <b><u>пользователь</u></b>, которого вы ищете: <a href='tg://openmessage?user_id={text}'>здесь</a>"
        if not text:
            await message.edit(self.strings("no_text", message))
        else:
            await message.edit(toid)
            return

    async def tidcmd(self, message):
        """> Идентификация ID по имени пользователя"""
        text = utils.get_args_raw(message) 
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()        
        if not text and not reply:
        	await message.edit("<b>🚨 Пожалуйста, введите <code>«username»</code></b>")
        try:
            if args:            	
                user = await message.client.get_entity(                
                args if not args.isdigit() else int(args))
        except ValueError:           
            user = await message.client.get_entity(GetFullUserRequest(message.sender_id))
        
        user_name = f"<b>🗄️ Информация:</b> Идентификационный номер <code>{text}</code> был обнаружен</b>\n"
        user_id = f"""<b>🆔 ID номер: <code>{user.id}</code></b>"""

        await message.edit(user_name + user_id)
        return
