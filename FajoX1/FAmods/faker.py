#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Faker
# Description: Генерация фейк информации
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/faker.png?raw=true
# requires: faker
# ---------------------------------------------------------------------------------

import faker
import random
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Faker(loader.Module):
    """Генерация фейк информации"""

    strings = {
        "name": "Faker",

        "loading": "<b><emoji document_id=5332600281970517875>🔄</emoji> Генерирую информацию...</b>"
    }


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    async def _gen_fake(self):

        fake = faker.Faker()

        name = fake.first_name()
        surname = fake.last_name()
        age = random.randint(18, 63)

        country = fake.country()
        address = fake.address()
        post_code = fake.zipcode()

        email = fake.email()
        phone_number = fake.phone_number()

        return f"""<b>
🔰 Сгенерированная фейк информация:

📄 Имя: <code>{name}</code>
📄 Фамилия: <code>{surname}</code>
💈 Возраст: <code>{age}</code>

🗺 Страна: <code>{country}</code>
🏠 Адрес: <code>{address}</code>
📮 Пост-код: <code>{post_code}</code>

📧 Е-мейл: <code>{email}</code> 
☎ Номер телефона: <code>{phone_number}</code>
</b>"""

    @loader.command()
    async def gfake(self, message):
        """Сгенерировать фейк информацию"""

        await utils.answer(message, self.strings["loading"])

        await utils.answer(message, await self._gen_fake())