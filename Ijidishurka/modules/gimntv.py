# подпишись на тг канал @modwini
from .. import loader


@loader.tds
class bas(loader.Module):
    """Гимнт твича с Басбустом by @modwini"""

    strings = {"name": "bas"}

    async def b25cmd(self, message):
        """| 25%"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/286",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def b50cmd(self, message):
        """| 50%?"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/287",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def b75cmd(self, message):
        """| 75%"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/288",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
        return

    async def b100cmd(self, message):
        """| 100%"""

        reply = await message.get_reply_message()
        await message.delete()
        await message.client.send_file(
            message.to_id,
            "https://t.me/radiofmonline/289",
            voice_note=True,
            reply_to=reply.id if reply else None,
        )
