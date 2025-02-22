__version__ = (0, 0, 3)
# meta developer: @K0vaIskii

from hikkatl.tl.patched import Message
from .. import loader, utils
from telethon import functions, types
from asyncio import sleep



@loader.tds
class EmojiStatusModule(loader.Module):
    """Модуль для обновления Премиум-статуса"""

    strings = {
        "name": "KSEMModule",
        "status_updated": "<emoji document_id=5208964339775588373>✅</emoji> Премиум-статус обновлен!",
        "status_error": "<emoji document_id=5208868849767699176>⚠️</emoji> Не удалось обновить Премиум-статус",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "del_reply_emoji", True,
                "Удалять ответный эмодзи после обновления статуса?",
                validator=loader.validators.Boolean(),
            ),
        )

    @loader.command(ru_doc="<ответ> - Обновить Премиум-статус")
    async def sem(self, message: Message):
        """Set the emoji status"""

        doc = await message.get_reply_message()

        try:
            await self._client(functions.account.UpdateEmojiStatusRequest(
                emoji_status=types.EmojiStatus(document_id=int(doc.text.split()[1][12:31]))
            ))
            await utils.answer(message, self.strings("status_updated"))
            await sleep(2)
            await message.delete()
            if doc.from_id == message.from_id and self.config["del_reply_emoji"]:
                await doc.delete()
        except Exception as e:
            await utils.answer(message, self.strings("status_error"))
            await sleep(2)
            await message.delete()
            