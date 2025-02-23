__version__ = (1, 0, 0)

#           ███████╗███████╗████████╗██╗░█████╗░░██████╗░█████╗░███████╗
#           ╚════██║██╔════╝╚══██╔══╝██║██╔══██╗██╔════╝██╔══██╗██╔════╝
#           ░░███╔═╝█████╗░░░░░██║░░░██║██║░░╚═╝╚█████╗░██║░░╚═╝█████╗░░
#           ██╔══╝░░██╔══╝░░░░░██║░░░██║██║░░██╗░╚═══██╗██║░░██╗██╔══╝░░
#           ███████╗███████╗░░░██║░░░██║╚█████╔╝██████╔╝╚█████╔╝███████╗
#           ╚══════╝╚══════╝░░░╚═╝░░░╚═╝░╚════╝░╚═════╝░░╚════╝░╚══════
#                                © Copyright 2023
#                             https://t.me/zet1csce
#
# meta developer: @zet1csce

from .. import loader, utils
import logging

import telethon

#logger = logging.getLogger(__name__)

@loader.tds
class повторMod(loader.Module):
    """какой-то модуль"""
    
    strings = {
        "name": "повтор",
    }
    
    async def сcmd(self, message):
        """
        отправляет сообщение с аргументами
        """
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args:
            return await message.respond("нет аргументов")
        
        await self.client.send_message(
            message.peer_id,
            args,
            reply_to=reply if reply else None
        ) 

    async def ссcmd(self, message):
        """
        {число (кнопка по счету слева направо)}
        нажимает кнопку по реплаю
        """
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            return await message.reply(
                'нужен реплай'
            )

        if not args:
            n = 0
        else:
            if not args.isdigit():
                return await message.reply(
                    'че за хуйня в аргументах'
                )
            n = int(args)-1

        try:
            await reply.click(n)
        except Exception as e:
            await message.reply(
                f'бля вот:\n<>'
            )