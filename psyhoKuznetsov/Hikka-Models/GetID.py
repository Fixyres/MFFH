__version__ = (1, 0, 0)
# meta developer: @psyhomodules

from hikkatl.types import Message
from hikkatl.utils import get_display_name
from hikkatl.tl.functions.users import GetFullUserRequest
from hikkatl.tl.functions.channels import GetFullChannelRequest
from hikkatl.tl.functions.messages import GetFullChatRequest
from hikkatl.tl.functions.contacts import ResolveUsernameRequest
from hikka import loader  

@loader.tds
class GetID(loader.Module):
    """Модуль для получения ID и юзернейма пользователя, чата или канала."""

    strings = {
        "name": "GetID",
        "error": "❌ <b>Ошибка:</b> <code>{}</code>",
        "no_username": "❌ <b>У этого пользователя нет юзернейма.</b>",
        "user_not_found": "❌ <b>Пользователь не найден.</b>",
        "usage_getid": "<b>Используйте:</b> <code>.getid</code> или <code>.getid @username</code>",
        "usage_getusername": "<b>Используйте:</b> <code>.getusername [ID]</code>",
        "id_must_be_number": "❌ <b>ID должен быть числом.</b>",
        "chat_type_unknown": "❌ <b>Не удалось определить тип чата.</b>",
        "id_format": "🆔 <b>ID:</b> <code>{}</code>",
        "username_format": "👤 <b>Юзернейм:</b> <code>@{}</code>"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def getidcmd(self, message: Message):
        """Узнать ID пользователя, чата или канала."""
        try:
            args = message.text.split()
            
            if len(args) > 1 and "@" in args[1]:
                username = args[1].replace("@", "")
                try:
                    user = await self.client(ResolveUsernameRequest(username))
                    if user and user.users:
                        await message.edit(self.strings["id_format"].format(user.users[0].id))
                    else:
                        await message.edit(self.strings["user_not_found"])
                    return
                except Exception as e:
                    await message.edit(self.strings["error"].format(str(e)))
                    return
            
            reply = await message.get_reply_message()
            if reply:
                user_id = reply.sender_id
                await message.edit(self.strings["id_format"].format(user_id))
                return
            
            if message.is_private:
                user_id = message.peer_id.user_id
                await message.edit(self.strings["id_format"].format(user_id))
            elif message.is_group:
                chat_id = message.chat_id
                await message.edit(self.strings["id_format"].format(chat_id))
            elif message.is_channel:
                channel_id = message.chat_id
                await message.edit(self.strings["id_format"].format(channel_id))
            else:
                await message.edit(self.strings["chat_type_unknown"])
                
        except Exception as e:
            await message.edit(self.strings["error"].format(str(e)))

    async def getusernamecmd(self, message: Message):
        """Узнать юзернейм по ID."""
        args = message.text.split()
        if len(args) < 2:
            await message.edit(self.strings["usage_getusername"])
            return
        
        try:
            user_id = int(args[1])
            try:
                full = await self.client(GetFullUserRequest(user_id))
                if hasattr(full, 'users') and full.users and full.users[0].username:
                    await message.edit(self.strings["username_format"].format(full.users[0].username))
                elif hasattr(full, 'user') and full.user and full.user.username:
                    await message.edit(self.strings["username_format"].format(full.user.username))
                else:
                    user = await self.client.get_entity(user_id)
                    if hasattr(user, 'username') and user.username:
                        await message.edit(self.strings["username_format"].format(user.username))
                    else:
                        await message.edit(self.strings["no_username"])
            except ValueError:
                await message.edit(self.strings["user_not_found"])
            except Exception as e:
                await message.edit(self.strings["error"].format(str(e)))
        except ValueError:
            await message.edit(self.strings["id_must_be_number"])
