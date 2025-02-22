# meta developer: @angellmodules
from .. import loader, utils
from telethon import events
import asyncio

@loader.tds
class SpamBanmod(loader.Module):
    """Check account status"""
    strings = {"name": "SpamBan"}

    async def client_ready(self, client, db):
        self.client = client

    async def checkbancmd(self, message):
        """Check account status."""
        await message.edit("Checking the ban...")

        await asyncio.sleep(1)

        try:
           
            spambot = await self.client.get_entity("SpamBot")
            await self.client.send_message(spambot, "/start")

           

            @self.client.on(events.NewMessage(from_users=spambot.id))
            async def handler(event):
                


                await message.edit(event.message.message)
               

                self.client.remove_event_handler(handler)

        except Exception as e:
            await message.edit(f"<b>ошибка.: {str(e)}</b>")


#made by @sawwnapix
