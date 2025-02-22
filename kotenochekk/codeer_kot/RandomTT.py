# meta developer: @codeer_kot, @angellmodules
from .. import loader
from telethon import events
from telethon.tl.functions.messages import DeleteHistoryRequest

@loader.tds
class RandomTT(loader.Module):
    """Отправляет случайное видео из Тиктока!"""
    strings = {"name": "RandomTT"}

    @loader.command()
    async def ttcmd(self, message):
        """Отправляет случайное видео"""
        chat = message.chat
        msg = await self.client.send_message("@AizenSoloBot", "/tt")

        async with self.client.conversation("@AizenSoloBot") as conv:
            response = await conv.wait_event(events.NewMessage(from_users="@AizenSoloBot"))
            await message.reply(response.message)

        await self.client(DeleteHistoryRequest(peer="@AizenSoloBot", max_id=0, just_clear=False, revoke=True))
        await message.delete()
