from .. import loader, utils
from telethon import functions, types
import asyncio
from telethon.tl.functions.channels import JoinChannelRequest

#meta developer: @moduleslist

@loader.tds
class OnlineModule(loader.Module):
    """🌐 Модуль для вечного онлайна"""
    
    strings = {"name": "OnlineStatus"}
        
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.online = self.get_state()
        
        if self.online:
            asyncio.create_task(self._keep_online())
            
            await client(JoinChannelRequest("@moduleslist"))
            
    def get_state(self):
        return self.db.get(self.strings["name"], "online", False)
        
    async def _keep_online(self):
        while self.online:
            try:
                await self.client(functions.account.UpdateStatusRequest(
                    offline=False
                ))
                await asyncio.sleep(30)
            except Exception:
                break
        
    @loader.command()
    async def onl(self, message):
        """🌐 Включить/выключить вечный онлайн"""
        self.online = not self.online
        self.db.set(self.strings["name"], "online", self.online)
        
        if self.online:
            await utils.answer(message, "<blockquote><emoji document_id=5237907553152672597>✅</emoji><b> Вечный онлайн включен</b></blockquote>")
            asyncio.create_task(self._keep_online())
        else:
            await utils.answer(message, "<blockquote><emoji document_id=5237993272109967450>❌</emoji><b> Вечный онлайн выключен</b></blockquote>")