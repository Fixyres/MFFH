"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

from .. import loader, utils
from telethon import functions, types

def register(cb):
	cb(ScrSpamMod())


class ScrSpamMod(loader.Module):
	"""Screenshot Spammer"""

	strings = {'name': 'ScrSpam'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def scrscmd(self, message):
		""".scrs <amount>"""
		a = 1
		r = utils.get_args(message)
		if r and r[0].isdigit():
			a = int(r[0])
		await message.edit("Screenshoting...")
		for _ in range(a):
			await message.client(functions.messages.SendScreenshotNotificationRequest(peer=await self.client.get_entity(message.chat_id), reply_to=types.InputReplyToMessage(reply_to_msg_id=message.id)))
		await message.delete()
		
