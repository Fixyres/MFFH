#meta developer: @thisLyomi & @AmekaMods

from .. import loader, utils
from telethon.tl.types import ChatBannedRights
from telethon.errors import RPCError
from telethon.tl.functions.channels import EditBannedRequest

@loader.tds
class DcToolMod(loader.Module):
    """Модуль для взаимодействия с dc_id."""
    strings = {"name": "DcTool"}

    async def dcbancmd(self, message):
        """{dc_id} -- Бан пользователей с определенным dc_id."""
        
        args = utils.get_args_raw(message)
        
        if not args.isdigit() or not (1 <= int(args) <= 5) or args == None:
            await utils.answer(message, "❌ <b>Ошибка:</b> <code>Пожалуйста, укажите число от 1 до 5.</code>")
            return

        dc_id = int(args)
        dc_users = ""
        
        async for user in message.client.iter_participants(message.to_id):
            if not user.deleted:
                user_dc_id = user.to_dict().get("photo", {}).get("dc_id", "none")

                if user_dc_id == dc_id:
                    dc_users += f"\n<code>{user.id}</code>"
                    try:
                        if user.bot:
                            dc_users += " <b>(🤖 Бот.)</b>"
                            continue
                        await message.client(EditBannedRequest(
                            message.chat_id,
                            user.id,
                            ChatBannedRights(until_date=None, view_messages=True)
                        ))
                        dc_users += " <b>(Забанен.)</b>" 
                    except RPCError as e:
                        dc_users += f" <b>(❌ Ошибка:</b> <code>{e}</code><b>)</b>"

        await message.respond(f"<b>✅ Пользователи с dc id {dc_id}:</b> \n{dc_users}")

    async def listdccmd(self, message):
        """-- Возвращает список участников и их dc_id"""
        all = message.client.iter_participants(message.to_id)
        user_list = '' 

        async for user in all:
            if not user.deleted:
                dc_id = user.to_dict().get("photo", {}).get("dc_id", "none")
                user_info = f"<code>{user.id}</code>: <code>{dc_id}</code>"  
                try:
                    if user.bot:
                        user_info += " <b>(🤖 Бот. )</b>"
                except:
                    pass
                user_list += f"\n{user_info}"
        
        await utils.answer(message, f"<b>✅ Список dc_id пользователей:</b> \n{user_list}")

    async def getdcidcmd(self, message):
        """[User_ID] -- Получить dc_id пользователя с помощью указанного в сообщении айди или репли. """
        
        reply = await message.get_reply_message()
        
        if reply:
            user = await message.client.get_entity(reply.sender_id) 
        else:
            args = utils.get_args(message)
            if args:
                try:
                    user = await message.client.get_entity(int(args[0]))
                except (ValueError, UserIdInvalidError):
                    await message.respond("<b>❌ Ошибка:</b><code> Недействительное ID пользователя.</code>")
                    return
            else:
                await message.respond("<b>❌ Ошибка:</b><code> Не найден реплай или ID в сообщении.</code>")
                return

        dc_id = user.to_dict().get("photo", {}).get("dc_id", "none")

        await utils.answer(message, f"<b>✅ DC ID пользователя:</b> <code>{dc_id}</code>")
