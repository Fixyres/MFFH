# meta developer: @K0vaIskii
__version__ = (0, 0, 1)

from hikkatl.types import Message
from .. import loader, utils

@loader.tds  
class DeleteOnReply(loader.Module):
    """Просто удаляет реплей"""
    
    strings = {
        "name": "Kodel",
    }

    @loader.command(ru_doc="<ответ> - удалить нахуй!")
    async def d(self, message: Message):
        try:
            if message.is_reply:
                rmessage = await message.get_reply_message()  
                await rmessage.delete() 
                await message.delete()
            else:
                await message.delete()
        except Exception:
            await message.delete()