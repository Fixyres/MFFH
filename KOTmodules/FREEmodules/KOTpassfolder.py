# meta developer: @kotcheat

import random
import string
import asyncio
from .. import loader, utils
from telethon.tl.functions.messages import CreateChatRequest

@loader.tds
class KOTpassfolder(loader.Module):
    """Удобный инструмент для генерации и управления паролями и логинами, который поможет вам создавать безопасные пароли и логины, а также легко управлять ими. Так же можно регулировать длину желаемоего пароля и логина и писать примечание для чего он будет использоваться (by @kotcheat)"""

    strings = {
        "name": "KOTpassfolder",
        "generate_credentials": "<b>Сгенерированные  данные:</b>\n\n<b>Логин:</b> <code>{login}</code>\n<b>Пароль:</b> <span class='hidden-text'>{password}</span>\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "saved_credentials": "<b>Сохраненные  данные:</b>\n\n{credentials}\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "no_saved_credentials": "Нет сохраненных данных.\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "credentials_saved": "Данные сохранены.\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "credentials_cleared": "Все данные очищены.\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "note_added": "Примечание добавлено к данным.\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "credentials_deleted": "Данные удалены.\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "private_chat_created": "Приватный чат создан. ID чата: <code>{chat_id}</code>\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "private_chat_exists": "Приватный чат уже создан. ID чата: <code>{chat_id}</code>\n\n<i>Это сообщение будет автоматически удалено через 30 секунд.</i>",
        "error": "Произошла ошибка. Пожалуйста, попробуйте позже.",
        "usage": "Использование: .gen <длина пароля>\nПример: .gen 12"
    }

    def __init__(self):
        self.saved_credentials = []
        self.last_generated_password = None
        self.last_generated_login = None
        self.private_chat_id = None

    async def client_ready(self, client, db):
        self.db = db
        self.client = client
        self.saved_credentials = self.db.get("KOTpassfolder", "saved_credentials", [])
        self.private_chat_id = self.db.get("KOTpassfolder", "private_chat_id", None)

    @loader.command(ru_doc="Генерирует случайный пароль и логин")
    async def gen(self, message):
        """Генерирует случайный пароль и логин"""
        try:
            length = int(utils.get_args_raw(message))
            if length <= 0 or length > 20:
                await utils.answer(message, self.strings["error"])
                return
        except ValueError:
            length = 10  # Длина пароля по умолчанию

        characters = string.ascii_letters + string.digits + "@$"
        password = ''.join(random.choices(characters, k=length))
        login_characters = string.ascii_letters + string.digits
        login = ''.join(random.choices(login_characters, k=length))

        self.last_generated_password = password
        self.last_generated_login = login
        generated_message = await utils.answer(message, self.strings["generate_credentials"].format(login=login, password=password))
        await asyncio.sleep(30)
        await generated_message.delete()

    @loader.command(ru_doc="Сохраняет последние сгенерированные данные")
    async def save(self, message):
        """Сохраняет последние сгенерированные данные"""
        if self.last_generated_password is None or self.last_generated_login is None:
            await utils.answer(message, self.strings["error"])
            return

        self.saved_credentials.append((self.last_generated_login, self.last_generated_password, ""))
        self.db.set("KOTpassfolder", "saved_credentials", self.saved_credentials)
        saved_message = await utils.answer(message, self.strings["credentials_saved"])
        await asyncio.sleep(30)
        await saved_message.delete()

    @loader.command(ru_doc="Показывает сохраненные данные")
    async def show(self, message):
        """Показывает сохраненные данные"""
        if not self.saved_credentials:
            no_credentials_message = await utils.answer(message, self.strings["no_saved_credentials"])
            await asyncio.sleep(30)
            await no_credentials_message.delete()
            return

        credentials_list = "\n\n".join(
            f"<b>{index + 1}. Логин:</b> <code>{login}</code>\n<b>Пароль:</b> <span class='hidden-text'>{password}</span>\n<b>Примечание:</b> {note}"
            for index, (login, password, note) in enumerate(self.saved_credentials)
        )
        saved_credentials_message = await utils.answer(message, self.strings["saved_credentials"].format(credentials=credentials_list))
        await asyncio.sleep(30)
        await saved_credentials_message.delete()

    @loader.command(ru_doc="Генерирует новые данные и сохраняет их")
    async def gensave(self, message):
        """Генерирует новые  данные и сохраняет их"""
        try:
            length = int(utils.get_args_raw(message))
            if length <= 0 or length > 20:
                await utils.answer(message, self.strings["error"])
                return
        except ValueError:
            length = 10  # Длина пароля по умолчанию

        characters = string.ascii_letters + string.digits + "@$"
        password = ''.join(random.choices(characters, k=length))
        login_characters = string.ascii_letters + string.digits
        login = ''.join(random.choices(login_characters, k=length))

        self.saved_credentials.append((login, password, ""))
        self.db.set("KOTpassfolder", "saved_credentials", self.saved_credentials)
        generated_message = await utils.answer(message, self.strings["generate_credentials"].format(login=login, password=password))
        saved_message = await utils.answer(message, self.strings["credentials_saved"])
        await asyncio.sleep(30)
        await saved_message.delete()
        await asyncio.sleep(30)
        await generated_message.delete()

    @loader.command(ru_doc="Очищает все сохраненные данные")
    async def clear(self, message):
        """Очищает все сохраненные  данные"""
        if not self.saved_credentials:
            no_credentials_message = await utils.answer(message, self.strings["no_saved_credentials"])
            await asyncio.sleep(30)
            await no_credentials_message.delete()
            return

        self.saved_credentials.clear()
        self.db.set("KOTpassfolder", "saved_credentials", self.saved_credentials)
        cleared_message = await utils.answer(message, self.strings["credentials_cleared"])
        await asyncio.sleep(30)
        await cleared_message.delete()

    @loader.command(ru_doc="Добавляет примечание к сохраненным данным")
    async def note(self, message):
        """Добавляет примечание к сохраненным данным"""
        args = utils.get_args_raw(message).split(maxsplit=1)
        if len(args) < 2:
            await utils.answer(message, self.strings["error"])
            return

        try:
            index = int(args[0]) - 1
            note = args[1]
            if index < 0 or index >= len(self.saved_credentials):
                await utils.answer(message, self.strings["invalid_index"])
                return
        except ValueError:
            await utils.answer(message, self.strings["error"])
            return

        login, password, _ = self.saved_credentials[index]
        self.saved_credentials[index] = (login, password, note)
        self.db.set("KOTpassfolder", "saved_credentials", self.saved_credentials)
        note_added_message = await utils.answer(message, self.strings["note_added"])
        await asyncio.sleep(30)
        await note_added_message.delete()

    @loader.command(ru_doc="Удаляет сохраненные данные по номеру")
    async def delcred(self, message):
        """Удаляет сохраненные  данные по номеру"""
        try:
            index = int(utils.get_args_raw(message)) - 1
            if index < 0 or index >= len(self.saved_credentials):
                await utils.answer(message, self.strings["invalid_index"])
                return
        except ValueError:
            await utils.answer(message, self.strings["error"])
            return

        del self.saved_credentials[index]
        self.db.set("KOTpassfolder", "saved_credentials", self.saved_credentials)
        deleted_message = await utils.answer(message, self.strings["credentials_deleted"])
        await asyncio.sleep(30)
        await deleted_message.delete()

    @loader.command(ru_doc="Создает приватный чат")
    async def createprivatechat(self, message):
        """Создает приватный чат"""
        if self.private_chat_id is not None:
            await utils.answer(message, self.strings["private_chat_exists"].format(chat_id=self.private_chat_id))
            return

        result = await message.client(CreateChatRequest(
            users=["me"],
            title="Приватный чат для сохранения данных"
        ))
        self.private_chat_id = result.chats[0].id
        self.db.set("KOTpassfolder", "private_chat_id", self.private_chat_id)
        created_message = await utils.answer(message, self.strings["private_chat_created"].format(chat_id=self.private_chat_id))
        await asyncio.sleep(30)
        await created_message.delete()

    @loader.command(ru_doc="Сохраняет данные в приватный чат по номеру")
    async def saveprivatedata(self, message):
        """Сохраняет данные с примечанием в приватный чат по номеру"""
        if self.private_chat_id is None:
            await utils.answer(message, self.strings["error"])
            return

        args = utils.get_args_raw(message).split(maxsplit=1)
        if len(args) < 1:
            await utils.answer(message, self.strings["error"])
            return

        try:
            index = int(args[0]) - 1
            if index < 0 or index >= len(self.saved_credentials):
                await utils.answer(message, self.strings["invalid_index"])
                return
        except ValueError:
            await utils.answer(message, self.strings["error"])
            return

        login, password, note = self.saved_credentials[index]

        # Отправляем сообщение в приватный чат
        await message.client.send_message(
            self.private_chat_id,
            f"<b>Логин:</b> <code>{login}</code>\n<b>Пароль:</b> <span class='hidden-text'>{password}</span>\n<b>Примечание:</b> {note}"
        )

        note_added_message = await utils.answer(message, self.strings["note_added"])
        await asyncio.sleep(30)
        await note_added_message.delete()