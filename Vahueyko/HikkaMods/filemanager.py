# meta developer: @VahueykoMod
# /*
# * +-----------------------------------------+
# * |
# * |              V A H U E Y K O
# * |
# * |              © 2024 Vahueyko
# * |
# * +-----------------------------------------+
# */
import os
from telethon import types
from .. import loader, utils


@loader.tds
class FileManagerMod(loader.Module):
    """Универсальный файловый менеджер"""

    strings = {
        "name": "File Manager",
        "no_file": "Ответь на файл",
        "upload_success": "Файл загружен: {}",
        "download_success": "Файл скачан: {}",
        "file_not_found": "Такого файла в директории нет",
        "no_filename": "Ты не указал имя файла",
        "no_path": "Укажи путь для сохранения файлов!",
        "path_set": "Путь для файлов установлен: {}",
        "file_deleted": "Файл {} успешно удалён! ",
        "file_delete_error": "Не удалось удалить файл: {} ",
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._db_name = "FileManager"
        self._path = self._db.get(self._db_name, "path", "/tmp")

    @loader.owner
    async def setpathcmd(self, message):
        """Установка пути, для работы с файлами."""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings["no_path"])

        self._path = args
        self._db.set(self._db_name, "path", args)
        await utils.answer(message, self.strings["path_set"].format(args))

    @loader.owner
    async def upcmd(self, message):
        """Загрузить файл на сервер (реплеем на файл)"""
        reply = await message.get_reply_message()
        if not reply or not reply.file:
            return await utils.answer(message, self.strings["no_file"])

        file = await reply.download_media(bytes)
        filename = reply.file.name
        file_path = os.path.join(self._path, filename)

        with open(file_path, 'wb') as f:
            f.write(file)

        await utils.answer(message, self.strings["upload_success"].format(filename))

    @loader.owner
    async def dlcmd(self, message):
        """Скачать файл с сервера. Указывать имя файла точно, с учётом расширения"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings["no_filename"])

        file_path = os.path.join(self._path, args)
        if not os.path.exists(file_path):
            return await utils.answer(message, self.strings["file_not_found"])

        try:
            if file_path.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
                await message.client.send_file(
                    message.chat_id,
                    file=file_path,
                    caption=self.strings["download_success"].format(args),
                    reply_to=message.id,
                    attributes=[types.DocumentAttributeAudio(
                        duration=0,
                        title=os.path.splitext(args)[0],performer=""
                    )]
                )
            else:
                await message.client.send_file(
                    message.chat_id,
                    file=file_path,
                    caption=self.strings["download_success"].format(args),
                    reply_to=message.id,
                    force_document=True
                )
        except Exception as e:
            await utils.answer(message, f"Ошибка при отправке файла: {str(e)}")

        await message.delete()

    @loader.owner
    async def lscmd(self, message):
        """Показать список файлов в текущей директории."""
        files = os.listdir(self._path)
        file_list = "\n".join(files)
        await utils.answer(message, f"Файлы в {self._path}: <blockquote> {file_list} </blockquote>")

    @loader.owner
    async def rmfcmd(self, message):
        """Удалить файл с сервера. Указывать имя файла точно, с учётом расширения"""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings["no_filename"])

        file_path = os.path.join(self._path, args)
        if not os.path.exists(file_path):
            return await utils.answer(message, self.strings["file_not_found"])

        try:
            os.remove(file_path)
            await utils.answer(message, self.strings["file_deleted"].format(args))
        except Exception as e:
            await utils.answer(message, self.strings["file_delete_error"].format(str(e)))

# DeleteAccountRequest
# edit_2fa
# log_out
# get_me
