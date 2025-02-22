# канал @modwini
from .. import loader


@loader.tds
class hihihaha(loader.Module):
    """Громкий звук хихихаха👍
Подпишись на канал @modwini"""

    strings = {"name": "hihihaha"}

    async def hihicmd(self, message):
        """Отпровляет гс с громким звуком"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/194",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return
