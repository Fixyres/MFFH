# meta developer: @angellmodules

import asyncio
from .. import loader, utils

@loader.tds
class AniverseCardBotMod(loader.Module):
    """Module for @aniversecard_bot"""
    strings = {"name": "AniverseCard"}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.auto_card_task = None
        self.auto_card_interval = 4 * 60 * 60 + 10 * 60
    
    async def autocardcmd(self, message):
        """Starts auto card collection every 4 hours and 10 minutes.
        For best results, start it when a card is available to collect."""
        chat_id = "@aniversecard_bot"
       
        if self.auto_card_task and not self.auto_card_task.cancelled():
            await message.edit("Auto card collection is already activated.<emoji document_id=5774022692642492953>✅</emoji>")
            return
        
        await message.edit("Auto card collection activated<emoji document_id=5774022692642492953>✅</emoji>")
        
        if self.auto_card_task:
            self.auto_card_task.cancel()

        async def auto_card():
            while True:
                await self.client.send_message(chat_id, "получить карту")
                await asyncio.sleep(self.auto_card_interval)
        
        self.auto_card_task = asyncio.ensure_future(auto_card())

    async def autocardoffcmd(self, message):
        """Stops auto card collection"""
        if self.auto_card_task and not self.auto_card_task.cancelled():
            self.auto_card_task.cancel()
            self.auto_card_task = None
            await message.edit("Auto card collection deactivated.<emoji document_id=5774077015388852135>❌</emoji>")
        else:
            await message.edit("Auto card collection is already deactivated.<emoji document_id=5774077015388852135>❌</emoji>")

    async def nickacmd(self, message):
        """Changes nickname with .nicka <nickname>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Please specify a nickname.<emoji document_id=6030563507299160824>❗</emoji>")
            return
        
        chat_id = "@aniversecard_bot"
        new_nick = args
        await self.client.send_message(chat_id, f"сменить ник {new_nick}")
        await message.edit(f"Nickname changed to {new_nick}<emoji document_id=6039614175917903752>✏️</emoji>.")

#made by @sawwnapix
