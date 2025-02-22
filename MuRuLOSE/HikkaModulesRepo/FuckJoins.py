from hikkatl.types import Message
from .. import loader, utils
import tempfile
import requests
import re
import string
import random
import logging

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    FuckJoins
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: link
# meta desc: Tired of entering channels without your knowledge via JoinChannelRequest?\nThen use this module! You can remove all such requests with one command from the module (file or raw).

# meta developer: @BruhHikkaModules

logger = logging.getLogger(__name__)


@loader.tds
class FuckJoins(loader.Module):
    """Tired of entering channels without your knowledge via JoinChannelRequest?
    Then use this module! You can remove all such requests with one command from the module (file or raw).
    """

    strings = {
        "name": "FuckJoins",
        "wait": "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Wait, there is a cleanup of JoinChannelRequest requests in progress</b>",
    }
    strings_ru = {
        "_cls_doc": (
            "Надоели входы в каналы без вашего ведома с помощью JoinChannelRequest?\n"
            "Тогда используйте этот модуль! Вы можете одной командой из модуля (файла, либо raw) удалить все подобные запросы."
        ),
        "wait": "<emoji document_id=5451646226975955576>⌛️</emoji> <b>Ожидай, идёт очистка от запросов JoinChannelRequest</b>",
        "no-args-reply": "<emoji document_id=5447644880824181073>⚠️</emoji> <b>Вы не ответили на файл, не указали аргументов</b>",
    }

    async def client_ready(self, client, db):
        self._common = await self.import_lib(
            "https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/libaries/common.py",
            suspend_on_error=True
        )

    def get_username(self, string):
        pattern = "(.*)"
        match = re.search(pattern, string, re.DOTALL)
        if match:
            return match.group(1)
        else:
            logging.info("No match")


    @loader.command(
        ru_doc="[Ответ на файл / ссылка на сырой код (не работает)] - Заменить JoinChannelRequest на self.request_join",
    )
    async def rjoinsrjoin(self, message: Message):
        """ [Reply to file / link to raw code (not work)] - Replace JoinChannelRequest to self.request_join"""
        pattern = r'(await\s+client|self\.client|self\._client)\(JoinChannelRequest\([^)]*\)\)'

        args = utils.get_args_raw(message)

        await utils.answer(message, self.strings("wait"))

        if not args:
            reply = await message.get_reply_message()

            if not reply:
                return await utils.answer(self.strings["no-args-reply"])
            else:
                username = ""
                with tempfile.TemporaryDirectory() as tmpdir:
                    characters = string.ascii_letters + string.digits
                    filename = "".join(random.choice(characters) for _ in range(32))
                    path = tmpdir + "/" + filename
                    await reply.download_media(path)
                    with open(path + ".py", "r") as f:
                        code = f.read()
                        match = re.search("JoinChannelRequest\((.*?)\)", code)
                        if match:
                            jcr_str = match.group(1)
                            username = self.get_username(jcr_str)
                            new_code = re.sub(pattern, f"await self.request_join({username}, 'The city can sleep easy, because the FuckJoins module has destroyed the nasty JoinChannelRequest.')", code)
                    with open(path + ".py", "w") as f:
                        f.write(new_code)
                    await self.client.send_file(
                        message.chat_id,
                        file=path + ".py",
                        caption=f"Вот ваш измененный модуль {(reply).media.document.attributes[0].file_name}!",
                        reply_to=await self._common._topic_resolver(message) or None
                    )

        else:
            code = (await utils.run_sync(requests.get, args)).content.decode()

            match = re.search("JoinChannelRequest\((.*?)\)", code)
            if match:
                jcr_str = match.group(1)
                username = self.get_username(jcr_str)
                new_code = re.sub(pattern, f"await self.request_join({username}, 'The city can sleep easy, because the FuckJoins module has destroyed the nasty JoinChannelRequest.')", code)

            with tempfile.TemporaryDirectory() as tmpdir:
                characters = string.ascii_letters + string.digits
                filename = "".join(random.choice(characters) for _ in range(32))
                path = tmpdir + "/" + filename + ".py"
                with open(path, "x") as f:
                    f.write(new_code)
                return await self.client.send_file(
                    message.chat_id,
                    file=path,
                    caption=f"Вот ваш измененный модуль {args}!",
                    reply_to=await self._common._topic_resolver(message) or None
                )

    @loader.command(
        ru_doc="[Ответ на файл / ссылка на сырой код] - Удалить JoinChannelRequest",
    )
    async def removejoins(self, message: Message):
        """[Reply to file / link to raw code] - Remove JoinChannelRequest"""
        pattern = r'(await\s+client|self\.client|self\._client)\(JoinChannelRequest\([^)]*\)\)'

        args = utils.get_args_raw(message)

        await utils.answer(message, self.strings("wait"))

        if not args:
            reply = await message.get_reply_message()

            if not reply:
                return await utils.answer(self.strings["no-args-reply"])
            else:
                with tempfile.TemporaryDirectory() as tmpdir:
                    characters = string.ascii_letters + string.digits
                    filename = "".join(random.choice(characters) for _ in range(32))
                    path = tmpdir + "/" + filename
                    await reply.download_media(path)
                    with open(path + ".py", "r") as f:
                        code = f.read()
                    new_code = re.sub(pattern, "", code)
                    with open(path + ".py", "w") as f:
                        f.write(new_code)
                    await self.client.send_file(
                        message.chat_id,
                        file=path + ".py",
                        caption=f"Вот ваш измененный модуль {(reply).media.document.attributes[0].file_name}!",
                        reply_to=await self._common._topic_resolver(message) or None
                    )

        else:
            code = (await utils.run_sync(requests.get, args)).content.decode()

            new_code = re.sub(pattern, "", code)

            with tempfile.TemporaryDirectory() as tmpdir:
                characters = string.ascii_letters + string.digits
                filename = "".join(random.choice(characters) for _ in range(32))
                path = tmpdir + "/" + filename + ".py"
                with open(path, "x") as f:
                    f.write(new_code)
                return await self.client.send_file(
                    message.chat_id,
                    file=path,
                    caption=f"Вот ваш измененный модуль {args}!",
                    reply_to=await self._common._topic_resolver(message) or None
                )
