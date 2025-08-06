from .. import loader, utils
#Удаляет все сообщения
#Удаляет все сообщения
# dhdhrj
#ncjjcjf

# dhxjdnd
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
        else:
            await message.edit("<b>В лс не чищу!</b>")
