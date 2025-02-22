# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель модуля.
from .. import loader, utils

@loader.tds
class KOTStealGifModule(loader.Module):
    "модуль который крадет гифки"
    strings = {
        "name": "KOTStealGif",
        "no_reply": "❌ Пожалуйста, ответьте на сообщение с гифкой.",
        "not_gif": "❌ Это сообщение не содержит гифку.",
    }

    @loader.command()
    async def гcmd(self, message):
        " - украсть гифку"
        reply = await message.get_reply_message()
        if not reply or not reply.document:
            await utils.answer(message, self.strings("no_reply"))
            return

        if reply.document.mime_type != "video/mp4" or not any(
            isinstance(attr, type(reply.document.attributes[0])) and attr.round_message is False for attr in reply.document.attributes
        ):
            await utils.answer(message, self.strings("not_gif"))
            return

        await message.client.send_file(
            message.chat_id,
            reply.document,
            reply_to=reply.id
        )

        await message.delete()
