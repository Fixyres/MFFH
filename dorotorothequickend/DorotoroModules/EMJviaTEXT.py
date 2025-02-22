#                █████████████████████████████████████████
#                █────██────█────█────█───█────█────█────█
#                █─██──█─██─█─██─█─██─██─██─██─█─██─█─██─█
#                █─██──█─██─█────█─██─██─██─██─█────█─██─█
#                █─██──█─██─█─█─██─██─██─██─██─█─█─██─██─█
#                █────██────█─█─██────██─██────█─█─██────█
#                █████████████████████████████████████████
#
#
#                     Copyright 2022 t.me/Dorotoro
#             https://www.gnu.org/licenses/agpl-3.0.html
#
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/DorotoroEMJviaTEXT.png
# meta developer: @DorotoroMods

from .. import loader, utils

@loader.tds
class EMJviaTEXT(loader.Module):
	"""[ONLY FOR TG PREMIUM]\n Этот модуль создан чтобы не рыскать миллиарды стикерпаков. \n Пример использования:\n Привет BloodTrail"""
	strings = {'name': 'EMJviaTEXT'}
	
	@loader.watcher(out=True)
	async def watcher(self, message):
		if self.get('emjviatext') == True:
			if "RoflanEbalo" in message.text:
				await message.edit(message.text.replace('RoflanEbalo', '<emoji document_id=5253485476844676349>😄</emoji>'))
			if "roflanebalo" in message.text:
				await message.edit(message.text.replace('roflanebalo', '<emoji document_id=5253485476844676349>😄</emoji>'))
			if "Roflanebalo" in message.text:
				await message.edit(message.text.replace('Roflanebalo', '<emoji document_id=5253485476844676349>😄</emoji>'))
			elif "BloodTrail" in message.text:
				await message.edit(message.text.replace('BloodTrail', '<emoji document_id=5256142171815288333>👍</emoji>'))
			elif "bloodtrail" in message.text:
				await message.edit(message.text.replace('bloodtrail', '<emoji document_id=5256142171815288333>👍</emoji>'))
			elif "Jebaited" in message.text:
				await message.edit(message.text.replace('Jebaited', '<emoji document_id=5456325941737298180>😮</emoji>'))
			elif "jebaited" in message.text:
				await message.edit(message.text.replace('jebaited', '<emoji document_id=5456325941737298180>😮</emoji>'))
			elif "Keepo" in message.text:
				await message.edit(message.text.replace('Keepo', '<emoji document_id=5456150582517571782>😸</emoji>'))
			elif "keepo" in message.text:
				await message.edit(message.text.replace('keepo', '<emoji document_id=5456150582517571782>😸</emoji>'))
			elif "TakeNRG" in message.text:
				await message.edit(message.text.replace('TakeNRG', '<emoji document_id=5456326650406902886>🤗</emoji>'))
			elif "takenrg" in message.text:
				await message.edit(message.text.replace('takenrg', '<emoji document_id=5456326650406902886>🤗</emoji>'))
			elif "KappaPride" in message.text:
				await message.edit(message.text.replace('KappaPride', '<emoji document_id=5456318807796620241>🏳️‍🌈</emoji>'))
			elif "kappapride" in message.text:
				await message.edit(message.text.replace('kappapride', '<emoji document_id=5456318807796620241>🏳️‍🌈</emoji>'))
			elif "DendiFace" in message.text:
				await message.edit(message.text.replace('DendiFace', '<emoji document_id=5456456946829762778>😁</emoji>'))
			elif "dendiface" in message.text:
				await message.edit(message.text.replace('dendiface', '<emoji document_id=5456456946829762778>😁</emoji>'))
			elif "LUL" in message.text:
				await message.edit(message.text.replace('LUL', '<emoji document_id=5456372550722396281>🤣</emoji>'))
			elif "lul" in message.text:
				await message.edit(message.text.replace('lul', '<emoji document_id=5456372550722396281>🤣</emoji>'))
			elif "RoflanPominki" in message.text:
				await message.edit(message.text.replace('RoflanPominki', '<emoji document_id=5253542209067687944>🕯️</emoji>'))
			elif "roflanpominki" in message.text:
				await message.edit(message.text.replace('roflanpominki', '<emoji document_id=5253542209067687944>🕯️</emoji>'))
			elif "Gigachad" in message.text:
				await message.edit(message.text.replace('Gigachad', '<emoji document_id=5465178805637226937>😎</emoji>'))
			elif "gigachad" in message.text:
				await message.edit(message.text.replace('gigachad', '<emoji document_id=5465178805637226937>😎</emoji>'))
			elif "Amogus" in message.text:
				await message.edit(message.text.replace('Amogus', '<emoji document_id=5454327849936755071>🍑</emoji>'))
			elif "ZXCat" in message.text:
				await message.edit(message.text.replace('ZXCat', '<emoji document_id=5461098861583932040>💃</emoji>'))
			elif "zxcat" in message.text:
				await message.edit(message.text.replace('zxcat', '<emoji document_id=5461098861583932040>💃</emoji>'))
			elif "ZXCcat" in message.text:
				await message.edit(message.text.replace('ZXCcat', '<emoji document_id=5461098861583932040>💃</emoji>'))
			elif "TheIlluminati" in message.text:
				await message.edit(message.text.replace('TheIlluminati', '<emoji document_id=5456498719681681736>💵</emoji>'))
			elif "theilluminati" in message.text:
				await message.edit(message.text.replace('theilluminati', '<emoji document_id=5456498719681681736>💵</emoji>'))
			elif "DoritosChips" in message.text:
				await message.edit(message.text.replace('DoritosChips', '<emoji document_id=5456163643513120377>🔺</emoji>'))
			elif "doritoschips" in message.text:
				await message.edit(message.text.replace('doritoschips', '<emoji document_id=5456163643513120377>🔺</emoji>'))
			elif "Simp" in message.text:
				await message.edit(message.text.replace('Simp', '<emoji document_id=5240295030983237831>🤭</emoji>'))
			elif "simp" in message.text:
				await message.edit(message.text.replace('simp', '<emoji document_id=5240295030983237831>🤭</emoji>'))
			elif "Lox" in message.text:
				await message.edit(message.text.replace('Lox', '<emoji document_id=5238130663818797192>😁</emoji>'))
			elif "lox" in message.text:
				await message.edit(message.text.replace('lox', '<emoji document_id=5238130663818797192>😁</emoji>'))
			elif "Sarcasm" in message.text:
				await message.edit(message.text.replace('Sarcasm', '<emoji document_id=5463303025915338248>😅</emoji>'))
			elif "sarcasm" in message.text:
				await message.edit(message.text.replace('sarcasm', '<emoji document_id=5463303025915338248>😅</emoji>'))
			elif "WutFace" in message.text:
				await message.edit(message.text.replace('WutFace', '<emoji document_id=5456640543796764131>😧</emoji>'))
			elif "wutface" in message.text:
				await message.edit(message.text.replace('wutface', '<emoji document_id=5456640543796764131>😧</emoji>'))
			elif "MonkaS" in message.text:
				await message.edit(message.text.replace('MonkaS', '<emoji document_id=5235752982808632917>😰</emoji>'))
			elif "Monkas" in message.text:
				await message.edit(message.text.replace('Monkas', '<emoji document_id=5235752982808632917>😰</emoji>'))
			elif "monkas" in message.text:
				await message.edit(message.text.replace('monkas', '<emoji document_id=5235752982808632917>😰</emoji>'))
			elif "BatemanWalk" in message.text:
				await message.edit(message.text.replace('BatemanWalk', '<emoji document_id=5240476433221953356>😎</emoji>'))
			elif "batemanwalk" in message.text:
				await message.edit(message.text.replace('batemanwalk', '<emoji document_id=5240476433221953356>😎</emoji>'))
			elif "TheRock" in message.text:
				await message.edit(message.text.replace('TheRock', '<emoji document_id=5242427215957729698>🤨</emoji>'))
			elif "therock" in message.text:
				await message.edit(message.text.replace('therock', '<emoji document_id=5242427215957729698>🤨</emoji>'))
			elif "Gachigasm" in message.text:
				await message.edit(message.text.replace('gachigasm', '<emoji document_id=5195438749026100649>🤤</emoji>'))
			elif "gachigasm" in message.text:
				await message.edit(message.text.replace('gachigasm', '<emoji document_id=5195438749026100649>🤤</emoji>'))
			elif "SuperGood" in message.text:
				await message.edit(message.text.replace('SuperGood', '<emoji document_id=5242534504240783567>🪳</emoji>'))
			elif "supergood" in message.text:
				await message.edit(message.text.replace('supergood', '<emoji document_id=5242534504240783567>🪳</emoji>'))
			elif "RoflanDovolen" in message.text:
				await message.edit(message.text.replace('RoflanDovolen', '<emoji document_id=5256071064336735168>🙂</emoji>'))
			elif "roflandovolen" in message.text:
				await message.edit(message.text.replace('roflandovolen', '<emoji document_id=5256071064336735168>🙂</emoji>'))
			elif "Scam" in message.text:
				await message.edit(message.text.replace('Scam', '<emoji document_id=5235930206044167357>☹</emoji>'))
			elif "scam" in message.text:
				await message.edit(message.text.replace('scam', '<emoji document_id=5235930206044167357>☹</emoji>'))
			elif "Cristiano" in message.text:
				await message.edit(message.text.replace('Cristiano', '<emoji document_id=5465290869923912522>🍷</emoji>'))
			elif "cristiano" in message.text:
				await message.edit(message.text.replace('cristiano', '<emoji document_id=5465290869923912522>🍷</emoji>'))
			elif "CoolStoryBob" in message.text:
				await message.edit(message.text.replace('CoolStoryBob', '<emoji document_id=5456647072147053405>👨‍🎨</emoji>'))
			elif "coolstorybob" in message.text:
				await message.edit(message.text.replace('coolstorybob', '<emoji document_id=5456647072147053405>👨‍🎨</emoji>'))
			elif "Bateman" in message.text:
				await message.edit(message.text.replace('Bateman', '<emoji document_id=5244673458083734407>😘</emoji>'))
			elif "bateman" in message.text:
				await message.edit(message.text.replace('bateman', '<emoji document_id=5244673458083734407>😘</emoji>'))
			elif "cmonBruh" in message.text:
				await message.edit(message.text.replace('cmonBruh', '<emoji document_id=5456421616428784682>🤨</emoji>'))
			elif "cmonbruh" in message.text:
				await message.edit(message.text.replace('cmonbruh', '<emoji document_id=5456421616428784682>🤨</emoji>'))
			elif "OmegaLUL" in message.text:
				await message.edit(message.text.replace('OmegaLUL', '<emoji document_id=5235437375726821884>😂</emoji>'))
			elif "omegalul" in message.text:
				await message.edit(message.text.replace('omegalul', '<emoji document_id=5235437375726821884>😂</emoji>'))
			elif "Poggers" in message.text:
				await message.edit(message.text.replace('Poggers', '<emoji document_id=5235565997112433719>😮</emoji>'))
			elif "poggers" in message.text:
				await message.edit(message.text.replace('poggers', '<emoji document_id=5235565997112433719>😮</emoji>'))
			elif "PepeHands" in message.text:
				await message.edit(message.text.replace('PepeHands', '<emoji document_id=5235672194473794817>😭</emoji>'))
			elif "pepehands" in message.text:
				await message.edit(message.text.replace('pepehands', '<emoji document_id=5235672194473794817>😭</emoji>'))
			elif "Pog" in message.text:
				await message.edit(message.text.replace('Pog', '<emoji document_id=5456646114369349279>😱</emoji>'))
			elif "pog" in message.text:
				await message.edit(message.text.replace('pog', '<emoji document_id=5456646114369349279>😱</emoji>'))
			elif "SeemsGood" in message.text:
				await message.edit(message.text.replace('SeemsGood', '<emoji document_id=5453919011999849933>👍</emoji>'))
			elif "seemsgood" in message.text:
				await message.edit(message.text.replace('seemsgood', '<emoji document_id=5453919011999849933>👍</emoji>'))
			elif "PoroSad" in message.text:
				await message.edit(message.text.replace('PoroSad', '<emoji document_id=5456358961445871838>😢</emoji>'))
			elif "porosad" in message.text:
				await message.edit(message.text.replace('porosad', '<emoji document_id=5456358961445871838>😢</emoji>'))
			elif "BibleThump" in message.text:
				await message.edit(message.text.replace('BibleThump', '<emoji document_id=5325692913701626627>😭</emoji>'))
			elif "biblethump" in message.text:
				await message.edit(message.text.replace('biblethump', '<emoji document_id=5325692913701626627>😭</emoji>'))


	@loader.command()
	async def emjviatext(self, message):
		"- включить/выключить автозамену текста на эмодзи."
		if self.get('emjviatext') == True:
			self.set('emjviatext', False)
			await utils.answer(message, "<b>EMJviaTEXT off. <emoji document_id=5289735335830365517>😎</emoji></b>")
			return
		elif self.get('emjviatext') == False or self.get('emjviatext') is None:
			self.set('emjviatext', True)
			await utils.answer(message, "<b>EMJviaTEXT on. <emoji document_id=5271812579038075619>😎</emoji></b>")

	@loader.command()
	async def emjlist(self, m):
		"- список эмодзи."
		await utils.answer(m, "<emoji document_id=5253485476844676349>😄</emoji> - <code>RoflanEbalo</code>\n <emoji document_id=5256142171815288333>👍</emoji> - <code>BloodTrail</code>\n <emoji document_id=5456325941737298180>😮</emoji> - <code>Jebaited</code>\n <emoji document_id=5456150582517571782>😸</emoji> - <code>Keepo</code>\n <emoji document_id=5456326650406902886>🤗</emoji> - <code>TakeNRG</code>\n <emoji document_id=5456318807796620241>🏳️‍🌈</emoji> - <code>KappaPride</code>\n <emoji document_id=5456456946829762778>😁</emoji> - <code>DendiFace</code>\n <emoji document_id=5456372550722396281>🤣</emoji> - <code>LUL</code>\n <emoji document_id=5253542209067687944>🕯️</emoji> - <code>RoflanPominki</code>\n <emoji document_id=5465178805637226937>😎</emoji> - <code>Gigachad</code>\n <emoji document_id=5454327849936755071>🍑</emoji> - <code>Amogus</code>\n <emoji document_id=5461098861583932040>💃</emoji> - <code>ZXCat</code>\n <emoji document_id=5456498719681681736>💵</emoji> - <code>TheIlluminati</code>\n <emoji document_id=5456163643513120377>🔺</emoji> - <code>DoritosChips</code>\n <emoji document_id=5240295030983237831>🤭</emoji> - <code>Simp</code>\n <emoji document_id=5238130663818797192>😁</emoji> - <code>Lox</code>\n <emoji document_id=5463303025915338248>😅</emoji> - <code>Sarcasm</code>\n <emoji document_id=5456640543796764131>😧</emoji> - <code>WutFace</code>\n <emoji document_id=5235752982808632917>😰</emoji> - <code>MonkaS</code>\n <emoji document_id=5240476433221953356>😎</emoji> - <code>BatemanWalk</code>\n <emoji document_id=5242427215957729698>🤨</emoji> - <code>TheRock</code>\n <emoji document_id=5195438749026100649>🤤</emoji> - <code>Gashigasm</code>\n <emoji document_id=5242534504240783567>🪳</emoji> - <code>SuperGood</code>\n <emoji document_id=5256071064336735168>🙂</emoji> - <code>RoflanDovolen</code>\n <emoji document_id=5235930206044167357>☹</emoji> - <code>Scam</code>\n  <emoji document_id=5465290869923912522>🍷</emoji> - <code>Cristiano</code>\n <emoji document_id=5456647072147053405>👨‍🎨</emoji> - <code>CoolStoryBob</code>\n <emoji document_id=5244673458083734407>😘</emoji> - <code>Bateman</code>\n <emoji document_id=5456421616428784682>🤨</emoji> - <code>cmonBruh</code>\n <emoji document_id=5235437375726821884>😂</emoji> - <code>OmegaLUL</code>\n  <emoji document_id=5235565997112433719>😮</emoji> - <code>Poggers</code>\n <emoji document_id=5456646114369349279>😱</emoji> - <code>Pog</code>\n <emoji document_id=5453919011999849933>👍</emoji> - <code>SeemsGood</code>\n <emoji document_id=5456358961445871838>😢</emoji> - <code>PoroSad</code>\n <emoji document_id=5325692913701626627>😭</emoji> - <code>BibleThump</code>   ")
