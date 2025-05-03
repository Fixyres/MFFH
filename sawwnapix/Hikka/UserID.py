from telethon.errors import UserIdInvalidError
from .. import loader, utils

@loader.tds
class UserByID(loader.Module):
    """Выдаёт username и tg-ссылку по ID"""
    strings = {"name": "UserByID"}

    @loader.command()
    async def getuser(self, message):
        """<id> — Получить username и ссылку по ID"""
        args = utils.get_args(message)
        if not args:
            return await message.edit("Укажи ID пользователя.")

        try:
            user_id = int(args[0])
        except ValueError:
            return await message.edit("ID должен быть числом.")

        try:
            user = await message.client.get_entity(user_id)
            username = f"@{user.username}" if user.username else "None"
            forever_link = f"tg://openmessage?user_id={user_id}"

            result = (
                f"<blockquote>👤Вот информация о пользователе:</blockquote>\n"
                f"<blockquote>🪪ID: {user_id}</blockquote>\n"
                f"<blockquote>🌐Username: {username}</blockquote>\n"
                f"<blockquote>🔍Forever Link: <a href=\"{forever_link}\">Click</a></blockquote>"
            )

            await message.edit(result, parse_mode="html")
        except UserIdInvalidError:
            await message.edit("Неверный ID пользователя.")
        except Exception as e:
            await message.edit(f"Ошибка: {e}")
