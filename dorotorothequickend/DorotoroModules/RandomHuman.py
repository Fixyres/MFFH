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
# ---------------------------------------------------------------------------------
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/DorotoroGenerateHuman.png
# meta developer: @DorotoroMods

from .. import loader, utils
from telethon.tl.types import Message
from ..utils import answer

@loader.tds
class RandomHuman(loader.Module): 
	"""Отправляет рандомное имя, фамилию, дату рождения, email, пароль и телефон.""" 
	strings = {'name': 'GenerateHuman'} 
	
	@loader.command()
	async def generatehumancmd(self, message: Message):
		"- сгенерировать человека."
		msg = await answer(message, '<b><i>Подбираю человека...</i></b>')
		async with self._client.conversation("@randomdatatools_bot") as conv:
			popo4ka = await conv.send_message("👤 Пользователь")
			r = await conv.get_response()
			await popo4ka.delete() 
			await r.delete()
		dsopthx = r.text.split('\n')
		dsopthx.remove('👤 Пользователь')
		dsopthx.remove('<i>(Нажмите на значение, чтобы скопировать его)</i>')
		chel = '\n'.join(dsopthx)
		text = f"<b>Человек сгенерирован. Кое-что про него:\n\n{chel}\n\n<tg-spoiler><i>RandomHuman</i></tg-spoiler></b>"
		await answer(msg, text)

	@loader.command()
	async def generatepasscmd(self, message: Message):
		"- сгенерировать паспорт."
		msg = await answer(message, "<b><i>Ищу паспорта...</i></b>")
		async with self._client.conversation("@randomdatatools_bot") as conv:
			jdun = await conv.send_message("🛂 Паспорт")
			r = await conv.get_response()
			await jdun.delete()
			await r.delete()
		udalit = r.text.split('\n')
		udalit.remove("🛂 Паспорт")
		udalit.remove("<i>(Нажмите на значение, чтобы скопировать его)</i>")
		papa = '\n'.join(udalit)
		text = f"<b>Паспорт сгенерирован. Вот что я нарыл:\n\n{papa}\n\n<tg-spoiler><i>RandomHuman</i></tg-spoiler></b>"
		await answer(msg, text)

	@loader.command()
	async def generateschlcmd(self, message: Message):
		"- сгенерировать инф-цию об образовании."
		msg = await answer(message, "<b><i>Пробиваю документы...</i></b>")
		async with self._client.conversation("@randomdatatools_bot") as conv:
			jdun = await conv.send_message("🏫 Образование")
			r = await conv.get_response()
			await jdun.delete()
			await r.delete()
		udalit = r.text.split('\n')
		udalit.remove("🏫 Образование")
		udalit.remove("<i>(Нажмите на значение, чтобы скопировать его)</i>")
		papa = '\n'.join(udalit)
		text = f"<b>Образование сгенерировано. Вот что я нарыл:\n\n{papa}\n\n<tg-spoiler><i>RandomHuman</i></tg-spoiler></b>"
		await answer(msg, text)

	@loader.command()
	async def generatedocscmd(self, message: Message):
		"- сгенерировать документы."
		msg = await answer(message, "<b><i>Пробиваю документы...</i></b>")
		async with self._client.conversation("@randomdatatools_bot") as conv:
			jdun = await conv.send_message("📄 Документы")
			r = await conv.get_response()
			await jdun.delete()
			await r.delete()
		udalit = r.text.split('\n')
		udalit.remove("📄 Документы")
		udalit.remove("<i>(Нажмите на значение, чтобы скопировать его)</i>")
		papa = '\n'.join(udalit)
		text = f"<b>Документы сгенерированы. Вот что я нарыл:\n\n{papa}\n\n<tg-spoiler><i>RandomHuman</i></tg-spoiler></b>"
		await answer(msg, text)

	@loader.command()
	async def generateauto(self, message: Message):
		"- сгенерировать инф-цию об авто."
		msg = await answer(message, "<b><i>Пробиваю номера авто...</i></b>")
		async with self._client.conversation("@randomdatatools_bot") as conv:
			jdun = await conv.send_message("🚙 Автомобиль")
			r = await conv.get_response()
			await jdun.delete()
			await r.delete()
		udalit = r.text.split('\n')
		udalit.remove("🚙 Автомобиль")
		udalit.remove("<i>(Нажмите на значение, чтобы скопировать его)</i>")
		papa = '\n'.join(udalit)
		text = f"<b>Автомобиль сгенерирован. Вот что я нарыл:\n\n{papa}\n\n<tg-spoiler><i>RandomHuman</i></tg-spoiler></b>"
		await answer(msg, text)

	@loader.command()
	async def generatebank(self, message: Message):
		"- сгенерировать платежную инф-цию."
		msg = await answer(message, "<b><i>Пробиваю банковские карты...</i></b>")
		async with self._client.conversation("@randomdatatools_bot") as conv:
			jdun = await conv.send_message("🏦 Банк")
			r = await conv.get_response()
			await jdun.delete()
			await r.delete()
		udalit = r.text.split('\n')
		udalit.remove("🏦 Платежная информация")
		udalit.remove("<i>(Нажмите на значение, чтобы скопировать его)</i>")
		papa = '\n'.join(udalit)
		text = f"<b>Платежная инф-ция сгенерирована. Вот что я нарыл:\n\n{papa}\n\n<tg-spoiler><i>RandomHuman</i></tg-spoiler></b>"
		await answer(msg, text)
