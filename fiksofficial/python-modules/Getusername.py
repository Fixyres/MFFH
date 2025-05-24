# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @PyModule
from .. import loader, utils

@loader.tds
class GetUserMod(loader.Module):
    """Получает username пользователя по его ID"""

    strings = {"name": "GetUser"}

    @loader.command()
    async def getuser(self, message):
        """[ID] - Найти username по ID."""
        args = utils.get_args_raw(message)

        if not args or not args.isdigit():
            return await message.edit("<emoji document_id=5774077015388852135>❌</emoji> <b>Укажите ID пользователя!</b>")

        user_id = int(args)

        try:
            user = await self.client.get_entity(user_id)
            if user.deleted or not user.first_name:
                return await message.edit(f"<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Пользователь не существует.</b></blockquote>\n\n<emoji document_id=6032850693348399258>🔎</emoji> <b>ID: {user_id}</b>")
            if user.username:
                if user.last_name is not None:
                    await message.edit(f"<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Username найден.</b></blockquote>\n\n<emoji document_id=6032850693348399258>🔎</emoji> <b>ID: {user_id}</b>\n<emoji document_id=5771887475421090729>👤</emoji> <b>Username: @{user.username}</b>\n<emoji document_id=6035084557378654059>👤</emoji> <b>First name: {user.first_name}</b>\n<emoji document_id=6035084557378654059>👤</emoji> <b>Last name: {user.last_name}</b>")
                else:
                    await message.edit(f"<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Username найден.</b></blockquote>\n\n<emoji document_id=6032850693348399258>🔎</emoji> <b>ID: {user_id}</b>\n<emoji document_id=5771887475421090729>👤</emoji> <b>Username: @{user.username}</b>\n<emoji document_id=6035084557378654059>👤</emoji> <b>First name: {user.first_name}</b>")
            else:
                if user.last_name is not None:
                    await message.edit(f"<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Username не найден.</b></blockquote>\n\n<emoji document_id=6032850693348399258>🔎</emoji> <b>ID: {user_id}</b>\n<emoji document_id=6035084557378654059>👤</emoji> <b>First name: {user.first_name}</b>\n<emoji document_id=6035084557378654059>👤</emoji> <b>Last name: {user.last_name}</b>")
                else:
                    await message.edit(f"<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Username не найден.</b></blockquote>\n\n<emoji document_id=6032850693348399258>🔎</emoji> <b>ID: {user_id}</b>\n<emoji document_id=6035084557378654059>👤</emoji> <b>First name: {user.first_name}</b>")
        except Exception:
            await message.edit(f"<blockquote><emoji document_id=5253959125838090076>👁</emoji> <b>Ошибка при поиске пользователя.</b></blockquote>\n\n<emoji document_id=6032850693348399258>🔎</emoji> <b>ID: {user_id}</b>")
