#meta developer: @angellmodules

import asyncio
from telethon import events
from .. import loader, utils
from telethon.tl.types import MessageMediaDocument

@loader.tds
class SoundCloudMod(loader.Module):
    """Download music from SoundCloud🫀"""
    strings = {"name": "SoundCloud"}

    async def sclcmd(self, message):
        """<link from SoundCloud>"""
        link = utils.get_args_raw(message)
        
        if not link:
            await message.edit("<emoji document_id=5774077015388852135>❌</emoji> provide a SoundCloud link.")
            return
           
        chat_id = message.chat_id
        await self._client.send_message("@scload_bot", link)
        await asyncio.sleep(1)
        await message.delete()

        @self._client.on(events.NewMessage(from_users="@scload_bot"))
        async def handler(event):
            if event.media and isinstance(event.media, MessageMediaDocument):
                await self._client.send_file(chat_id, event.media, caption="")
                self._client.remove_event_handler(handler, events.NewMessage(from_users="@scload_bot"))


#made by @sawwnapix
