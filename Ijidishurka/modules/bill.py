# канал @modwini
from .. import loader


@loader.tds
class billy(loader.Module):
    """Подпишись на канал @modwini"""

    strings = {"name": "Billy"}

    async def billycmd(self, message):
        """Отправляет видео сообщение"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://telesco.pe/kruglishik/31",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
