# @Sekai_Yoneya

import os
from .. import loader, utils
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.users import GetFullUserRequest


@loader.tds
class WhoIsMod(loader.Module):
    """Получает информацию о пользователе."""
    strings = {'name': 'Whois'}

    async def whoiscmd(self, message):
        """Используй .whois <@ или реплай>; ничего"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        await message.edit("<b>Получаю информацию о пользователе...</b>")

        try:
            if args:
                user = await message.client.get_entity(args if not args.isdigit() else int(args))
            else:
                user = await message.client.get_entity(reply.sender_id)
        except:
            user = await message.client.get_me()
        
        user = await message.client(GetFullUserRequest(user.id))
        photo, caption = await get_info(user, message)

        await message.client.send_file(message.chat_id, photo if photo else None, caption=caption,
                                       link_preview=False, reply_to=reply.id if reply else None)
        os.remove(photo)
        await message.delete()


async def get_info(user, message):
    """Подробная информация о пользователе."""
    uuser = user.user

    user_photos = await message.client(GetUserPhotosRequest(user_id=uuser.id,
                                                           offset=42, max_id=0, limit=100))
    user_photos_count = "У пользователя нет аватарки."
    try:
        user_photos_count = user_photos.count
    except:
        pass

    user_id = uuser.id
    first_name = uuser.first_name or "Пользователь не указал имя."
    last_name = uuser.last_name or "Пользователь не указал фамилию."
    username = uuser.username or "У пользователя нет юзернейма."
    user_bio = user.about or "У пользователя нет информации о себе."
    common_chat = user.common_chats_count
    is_bot = "Да" if uuser.bot else "Нет"
    restricted = "Да" if uuser.restricted else "Нет"
    verified = "Да" if uuser.verified else "Нет"

    photo = await message.client.download_profile_photo(user_id, str(user_id) + ".jpg", download_big=True)
    caption = (f"<b>ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:</b>\n\n"
               f"<b>Имя:</b> {first_name}\n"
               f"<b>Фамилия:</b> {last_name}\n"
               f"<b>Юзернейм:</b> @{username}\n"
               f"<b>ID:</b> <code>{user_id}</code>\n"
               f"<b>Бот:</b> {is_bot}\n"
               f"<b>Ограничен:</b> {restricted}\n"
               f"<b>Верифицирован:</b> {verified}\n\n"
               f"<b>О себе:</b> \n<code>{user_bio}</code>\n\n"
               f"<b>Кол-во аватарок в профиле:</b> {user_photos_count}\n"
               f"<b>Общие чаты:</b> {common_chat}\n"
               f"<b>Пермалинк:</b> <a href=\"tg://user?id={user_id}\">клик</a>")

    return photo, caption
