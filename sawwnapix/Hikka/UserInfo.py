# meta developer: @angellmodules

# thanks https://github.com/C0dwiz/H.Modules/blob/main/AccountData.py#L35-L49 for accdata

import requests
from .. import loader, utils


@loader.tds
class UserInfoAngellMod(loader.Module):
    """Модуль для получения информации о пользователе!"""
    strings = {"name": "AngelInfo"}

    async def client_ready(self, client, db):
        self.client = client
        self.config = loader.ModuleConfig(
            "banner_url", "https://0x0.st/s/d-on0hAQlsqVfdGs0DHC4g/X7kw.jpg",
            lambda: "Ссылка на баннер (URL изображения)"
        )

    async def uinfocmd(self, message):
        """<реплай> или <юзернейм>"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        user = None
        if args:
            try:
                user = await self.client.get_entity(args)
            except:
                await utils.answer(message, "Не удалось найти пользователя.")
                return
        elif reply:
            user = await self.client.get_entity(reply.sender_id)
        else:
            await utils.answer(message, "Укажите юзернейм или используйте команду на реплей.")
            return

        await message.edit("<emoji document_id=5341715473882955310>⚙️</emoji>Загружаю информацию...<emoji document_id=5341715473882955310>⚙️</emoji>")

        name = user.first_name or "Не указано"
        last_name = user.last_name or "Не указана"
        username = f"@{user.username}" if user.username else "Не указан"
        id_ = user.id
        avatar = "Есть" if user.photo else "Нет"
        premium = "Есть" if getattr(user, "premium", False) else "Нету"
        is_bot = "Да" if user.bot else "Нет"
        is_verified = "Да" if user.verified else "Нет"
        creation_date = await self.get_creation_date(id_)

        banner_url = self.config["banner_url"]

        text = (
            f"<emoji document_id=5424892643760937442>👁</emoji>Информация о {username}<emoji document_id=5424892643760937442>👁</emoji>\n\n"
            f"<emoji document_id=5334673106202010226>✏️</emoji>Имя: {name}\n"
            f"<emoji document_id=5334882760735598374>📝</emoji>Фамилия: {last_name}\n"
            f"<emoji document_id=5373012449597335010>👤</emoji>Юзернейм: {username}\n"
            f"<emoji document_id=5431897022456145283>📆</emoji>Дата аккаунта: {creation_date}\n"
            f"<emoji document_id=5422683699130933153>🪪</emoji>ID: {id_}\n"
            f"<emoji document_id=5375074927252621134>🖼</emoji>Аватар: {avatar}\n"
            f"<emoji document_id=5458799228719472718>⭐</emoji>Premium: {premium}\n"
            f"<emoji document_id=5427009714745517609>✅</emoji>Официальный аккаунт: {is_verified}\n"
            f"<emoji document_id=5372981976804366741>🤖</emoji>Бот: {is_bot}"
        )

        try:
            response = requests.get(banner_url)
            response.raise_for_status()
            banner_data = response.content

            await self.client.send_file(
                message.chat_id,
                file=banner_data,
                caption=text,
                reply_to=reply.id if reply else None
            )
            await message.delete()
        except Exception as e:
            await message.edit(f"Ошибка загрузки баннера: {e}")

    async def get_creation_date(self, tg_id: int) -> str:
   
        url = "https://restore-access.indream.app/regdate"
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
            "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
            "accept-language": "en-US,en;q=0.9",
        }
        data = {"telegramId": tg_id}
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()["data"]["date"]
            else:
                return "Ошибка получения данных"
        except Exception as e:
            return f"Ошибка: {str(e)}"

    @loader.sudo
    async def cfg(self, message):
       
        args = utils.get_args(message)
        if len(args) == 0:
            await message.edit("<b>Использование:</b> .cfg <параметр> <значение>\n\n"
                               "<b>Доступные параметры:</b>\n"
                               "banner_url — URL баннера")
            return

        param = args[0].lower()
        value = " ".join(args[1:])

        if param == "banner_url":
            self.config["banner_url"] = value
            await message.edit(f"<b>URL баннера обновлен:</b> {value}")
        else:
            await message.edit("<b>Неизвестный параметр.</b>")







#made by @sawwnapix
