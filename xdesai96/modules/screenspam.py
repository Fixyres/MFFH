# meta developer: @xdesai

from .. import loader, utils
from telethon import functions, types

class ScrSpamMod(loader.Module):
    """Screenshot Spammer"""
    strings = {
	    'name': 'ScrSpam',
	    'invalid_number': '❌ <b>Invalid number.</b>'
    }

    strings_ru = {
	    'invalid_number': '❌ <b>Неверное кол-во.</b>'
	    }

    @loader.command(ru_doc="<кол-во> | Спам скриншотами")
    async def scrs(self, message):
        """<amount> | Screenshot spam"""
        args = utils.get_args_raw(message)
        if args and args.isdigit():
            amount = int(args)
        else:
            return await utils.answer(message, self.strings('invalid_number', message))

        await utils.answer(message, ".")

        for _ in range(amount):
            await message.client(functions.messages.SendScreenshotNotificationRequest(
                peer=await self.client.get_entity(message.chat_id),
                reply_to=types.InputReplyToMessage(reply_to_msg_id=message.id)
            ))

        await message.delete()
