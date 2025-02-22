# meta developer: @RemoveWoman

from .. import loader, utils

@loader.tds
class EditMod(loader.Module):
    """Изменяет сообщения в ответе by @RemoveWoman"""
    strings = {"name": "Edit"}

    async def editcmd(self, message):
        """Сообщение в ответе отредактируется на написанное после .edit"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args or not reply:
            await message.edit("Нет аргументов или ответа")
            return
        await reply.edit(args)
        await message.delete()
