__version__ = (9, 1, 5, 6)
from .. import loader, utils
# алалкл
# ,ллалал
# dhfhrh

# dhxhrjfj


# fhfhhrhfjr

# dhxjrjdjfjjfjc
# jdhdjd
# hdhdj




# fhhdjr
class DelmeMod(loader.Module):
    """Удаляет все сообщения"""
    strings = {'name': 'DelMe'}
    
    @loader.sudo
    async def delmecmd(self, message):
        chat = message.chat
        if chat:
            args = utils.get_args_raw(message)
            if args != str(message.chat.id+message.sender_id):
                await message.edit(f"<b>Если ты точно хочешь это сделать, то напиши:</b>\n<code>.delme {message.chat.id+message.sender_id}</code>")
                return
            await delete(chat, message, True)
            
    @loader.sudo
    async def delmecmd(self, message):
        """Sasoon..."""
        chat = message.chat
        if chat:
            args = utils.get_args_raw(message)
            if args != str(message.chat.id+message.sender_id):
                await message.edit(f"<b>Если ты точно хочешь это сделать, то напиши:</b>\n<code>.delme {message.chat.id+message.sender_id}</code>")
                return
            await delete(chat, message, True)

# ZZZZZZZ
