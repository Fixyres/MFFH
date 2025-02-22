"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""

# meta developer: @sqlmerr_m
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/fakedata.png?raw=true
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_fakedata.png?raw=true

import aiohttp

from typing import Dict, Any

from .. import utils, loader
from hikkatl.types import Message


@loader.tds
class FakeData(loader.Module):
    """Just fake data of persons and credit cards"""

    strings = {
        "name": "FakeData",
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Error in api!</b>",
        "person_text": (
            "<b>{emoji} Person:</b>\n"
            "  name - {name}\n"
            "  email - {email}\n"
            "  phone - {phone}\n"
            "  birthday - {birthday}\n"
            "  gender - {gender}\n"
            "  ip - {ip}\n"
            "  address - {address}\n\n"
        ),
        "credit_card_text": (
            "<b>💳 Credit card:</b>\n"
            "  type - {type}\n"
            "  number - {number}\n"
            "  expiration - {expiration}"
        ),
    }
    strings_ru = {
        "error": "<emoji document_id=5210952531676504517>❌</emoji> <b>Ошибка в апи!</b>",
        "person_text": (
            "<b>{emoji} Человек:</b>\n"
            "  имя - {name}\n"
            "  почта - {email}\n"
            "  номер телефона - {phone}\n"
            "  дата рождения - {birthday}\n"
            "  пол - {gender}\n"
            "  айпи - {ip}\n"
            "  адресс - {address}\n\n"
        ),
        "credit_card_text": (
            "<b>💳 Кредитная карта:</b>\n"
            "  тип - {type}\n"
            "  номер - {number}\n"
            "  истекает - {expiration}"
        ),
        "_cls_doc": "Просто фейковые данные о людях и их кредитных карт",
    }

    def get_formatted_person_text(self, data: Dict[str, Any]) -> str:
        address = data["address"]
        return self.strings("person_text").format(
            emoji="👨" if data["gender"] == "male" else "👩",
            name=f"{data['firstname']} {data['lastname']}",
            email=data["email"],
            phone=data["phone"],
            birthday=data["birthday"],
            gender=data["gender"],
            ip=data["ip"],
            address=f"{address['country']}, {address['city']}, {address['street']}",
        )

    def get_formatted_credit_card_text(self, data: Dict[str, Any]) -> str:
        return self.strings("credit_card_text").format(
            type=data["type"], number=data["number"], expiration=data["expiration"]
        )

    @loader.command(
        ru_doc='[язык (к примеру: "ru_RU" для Русского или "fr_FR" для французского и т.д.)] - Получить фейковые данные человека и его кредитной карты'
    )
    async def fakedata(self, message: Message):
        """[locale (for example: "ru_RU" for Russian or "fr_FR" for French)] - Get fake data about person and credit card"""
        args = utils.get_args_raw(message).split()
        params = {"_quantity": 1}
        if args:
            params["_locale"] = args[0]

        async with aiohttp.ClientSession("https://fakerapi.it") as session:
            async with session.get("/api/v1/persons", params=params) as response:
                if response.status != 200:
                    await utils.answer(message, self.strings("error"))
                data = await response.json()
                person = data["data"][0]
            async with session.get("/api/v2/creditCards", params=params) as response:
                if response.status != 200:
                    await utils.answer(message, self.strings("error"))
                data = await response.json()
                card = data["data"][0]
            async with session.get("/api/v1/users", params=params) as response:
                if response.status != 200:
                    await utils.answer(message, self.strings("error"))
                data = await response.json()
                person["ip"] = data["data"][0]["ip"]

        text = self.get_formatted_person_text(
            person
        ) + self.get_formatted_credit_card_text(card)
        await utils.answer(message, text)
