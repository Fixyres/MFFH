# meta developer: @ZSUtop_Ukraine 
from telethon.tl.functions.channels import JoinChannelRequest
from .. import loader

@loader.tds
class voiceGirls3(loader.Module):
    """Мемные гс для диалогов"""

    strings = {"name": "voiceMEMS1"}

    async def повезлоcmd(self, message):
        """| повезло повезло"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/15",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def нахяпcmd(self, message):
        """| Блять нахуй я сюда пришёл"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/14",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def ктототутcmd(self, message):
        """| Ай ай ай кто-то тут пиздабол"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/6",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def тыгенийcmd(self, message):
        """| Блин вот это ты умный"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/8",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def щазарежуcmd(self, message):
        """| Щас зарежу нахуй"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/11",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def япрощаюcmd(self, message):
        """| Я прощаю тебя"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/12",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def okurwacmd(self, message):
        """| О курва"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/16",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def отсталыйcmd(self, message):
        """| А я поняла ты уменствнно осталый, да?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/17",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def заебалинахcmd(self, message):
        """| Блять заебали нахуй написано же сначало сделать юзербота"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/18",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def отвинтаcmd(self, message):
        """| Всё зависит от винта"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/19",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def пошёлнахcmd(self, message):
        """| Пошёл нахуй"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/20",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def пиздаcmd(self, message):
        """| Да, пизда"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/21",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def  Крикcmd(self, message):
        """| Крик(пиздец громко)"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/22",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def  ohmycmd(self, message):
        """| Oh my gad"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/23",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def смехcmd(self, message):
        """| Стрёмный смех"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
        "https://t.me/zvuki12/24",
        voice_note=True,
        reply_to=reply.id if reply else None,
        )
        return

    async def почяcmd(self, message):
        """| Что, почему я черный?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/zvuki12/25",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return