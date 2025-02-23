#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.hikari.gay/aniquotes_icon.png
# meta banner: https://mods.hikariatama.ru/badges/aniquotes.jpg
# meta developer: @hikarimods & @sngscamer
# scope: hikka_only
# scope: hikka_min 1.2.10

from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class AnimatedQuotesMod(loader.Module):
    """Simple module to create animated stickers via bot"""

    strings = {
        "name": "AnimatedQuotes",
        "no_text": "🚫 <b>Provide a text to create sticker with</b>",
        "processing": (
            "<emoji document_id='6318766236746384900'>🕔</emoji> <b>Processing...</b>"
        ),
    }

    strings_ru = {
        "no_text": "🚫 <b>Укажи текст для создания стикера</b>",
        "processing": (
            "<emoji document_id='6318766236746384900'>🕔</emoji> <b>Обработка...</b>"
        ),
        "_cmd_doc_aniq": "<text> - Создать анимированный стикер",
        "_cls_doc": "Простенький модуль, который создает анимированные стикеры",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "sticker",
                 1,
                doc=lambda: "choose sticker",
                validator=loader.validators.Choice([1, 2, 3, 4]),
            ),
        )


    @loader.command()   
    async def cfgani(self, message):
             """> Set up buttons for the module"""
             name = self.strings("name")
             await self.allmodules.commands["config"](
             await utils.answer(message, 
             f"{self.get_prefix()}config {name}")
             )


    @loader.command()
    async def aniq(self, message: Message):
        """<text> - Create animated quote"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_text"))
            return

        message = await utils.answer(message, self.strings("processing"))
        amore = self.config["sticker"]

        try:
            query = await self._client.inline_query("@QuotAfBot", args)
            await message.respond(file=query[amore].document)
        except Exception as e:
            await utils.answer(message, str(e))
            return

        if message.out:
            await message.delete()
