#                █████████████████████████████████████████
#                █────██────█────█────█───█────█────█────█
#                █─██──█─██─█─██─█─██─██─██─██─█─██─█─██─█
#                █─██──█─██─█────█─██─██─██─██─█────█─██─█
#                █─██──█─██─█─█─██─██─██─██─██─█─█─██─██─█
#                █────██────█─█─██────██─██────█─█─██────█
#                █████████████████████████████████████████             
# 		 _             __  __           _       _                
#      /\       | |           |  \/  |         | |     | |               
#     /  \   ___| |_ _ __ ___ | \  / | ___   __| |_   _| | ___  ___      
#    / /\ \ / __| __| '__/ _ \| |\/| |/ _ \ / _` | | | | |/ _ \/ __|     
#   / ____ \\__ \ |_| | | (_) | |  | | (_) | (_| | |_| | |  __/\__ \     
#  /_/    \_\___/\__|_|  \___/|_|  |_|\___/ \__,_|\__,_|_|\___||___/     
#
#
#                     Copyright 2022 t.me/Dorotoro
#             https://www.gnu.org/licenses/agpl-3.0.html            
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/DorotoroCheckSpamBan.png
# meta developer: @DorotoroMods & @AstroModules

from .. import loader, utils
from ..utils import answer
from telethon.tl.types import Message

@loader.tds
class SpamBanCheckMod(loader.Module):
	"""Check spam ban for your account."""
	strings = {'name': 'CheckSpamBan'}
	
	@loader.command()
	async def spamban(self, message: Message):
		"- проверяет ваш аккаунт на наличие спам-бана через бота @SpamBot."
		async with self._client.conversation("@SpamBot") as conv:
			msg = await conv.send_message("/start")
			r = await conv.get_response()
			if r.text == 'Ваш аккаунт свободен от каких-либо ограничений.':
				text = "<b>Все прекрасно!\nУ вас нет спам бана.</b>"
			else:
				kk = r.text.split('\n')[2]
				ll = r.text.split('\n')[4]
				text = f"<b>К сожалению ваш аккаунт получил спам-бан...\n\n{kk}\n\n{ll}</b>"
			await msg.delete()
			await r.delete()
		await answer(message, text)
		
