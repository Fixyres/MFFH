#     ___    __ __ ____
#    /   |  / //_//  _/
#   / /| | / ,<   / /  
#  / ___ |/ /| |_/ /   
# /_/  |_/_/ |_/___/   
#                      
#     __  _______  ____  _____
#    /  |/  / __ \/ __ \/ ___/
#   / /|_/ / / / / / / /\__ \ 
#  / /  / / /_/ / /_/ /___/ / 
# /_/  /_/\____/_____//____/
#
# meta developer: @aki_modules

from .. import loader, utils
import telethon

class WalletCheckMod(loader.Module):
    strings = {'name': 'WalletCheck'}

    async def walletcmd(self, message: telethon.tl.types.Message):
        """Отправляет ваш баланс в @send"""
        bot_username = "@send"

        async with message.client.conversation(bot_username) as conv:
            sent_message = await conv.send_message("/wallet")
            response = await conv.get_response()

            await sent_message.delete()
            await response.delete()

        await utils.answer(message, response.text)
