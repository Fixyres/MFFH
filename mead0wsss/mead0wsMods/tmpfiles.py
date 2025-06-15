# -- version --
__version__ = (1, 0, 0)
# -- version --


# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods


# meta developer: @mead0wssMods



# -- main --
from .. import loader, utils
import io
import requests
import json 
# -- main --



@loader.tds
class tmpfilesMod(loader.Module): # initialization 
    """Модуль для загрузки файлов на tmpfiles.org"""

    strings = {
        "name": "tmpfiles",
        "uploading": "<emoji document_id=5307779382499090971>🫥</emoji> <b>Uploading file...</b>",
        "reply_to_file": "<emoji document_id=4958526153955476488>❌</emoji> <b>Reply to file!</b>",
        "uploaded": "<emoji document_id=5278611606756942667>❤️</emoji> <b>Successful! File uploaded!</b>\n\n<emoji document_id=5278305362703835500>🔗</emoji> <b>URL:</b> <code>{}</code>",
        "error": "<emoji document_id=4958526153955476488>❌</emoji> <b>Error while uploading: {}</b>"
    }
    # стринги (не мои)
    strings_ru = {
        "name": "tmpfiles", 
        "uploading": "<emoji document_id=5307779382499090971>🫥</emoji> <b>Загружаю файл...</b>",
        "reply_to_file": "<emoji document_id=4958526153955476488>❌</emoji> <b>Ответьте на файл!</b>", 
        "uploaded": "️<emoji document_id=5278611606756942667>❤️</emoji> <b>Файл успешно загружен!</b>\n\n<emoji document_id=5278305362703835500>🔗</emoji> <b>URL:</b> <code>{}</code>",
        "error": "<emoji document_id=4958526153955476488>❌</emoji> <b>Ошибка при загрузке: {}</b>"
    }

    async def _get_file(self, message): # helper
        """Helper to get file from message""" 
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["reply_to_file"])
            return None
            
        if reply.media:
            file = io.BytesIO(await self.client.download_media(reply.media, bytes))
            if hasattr(reply.media, "document"):
                file.name = reply.file.name or f"file_{reply.file.id}"
            else:
                file.name = f"file_{reply.id}.jpg"
        else:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "text.txt"
            
        return file
        
    @loader.command(
        ru_doc = "Загрузка ваших файлов на tmpfiles.org", #loader
        en_doc = "Uploading your files to tmpfiles.org"
    )
    async def tmpfilescmd(self, message): # upload files
        await utils.answer(message, self.strings["uploading"])
        file = await self._get_file(message)
        if not file:
            return

        try:
            response = requests.post(
                "https://tmpfiles.org/api/v1/upload", # requests 
                files={"file": file}
            )
            if response.ok:
                data = json.loads(response.text)
                url = data["data"]["url"]
                await utils.answer(message, self.strings["uploaded"].format(url))
            else:
                await utils.answer(message, self.strings["error"].format(response.status_code))
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
            
            
            
            
            
# Структура модуля (да и сама логика) взята с K:Uploader <3
