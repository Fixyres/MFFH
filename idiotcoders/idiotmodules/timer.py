# meta pic: https://static.whypodg.me/mods!timer.png
# meta banner: https://mods.whypodg.me/badges/timer.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

import re
import datetime

from hikkatl.types import Message
from .. import loader, utils


@loader.tds
class TimerMod(loader.Module):
	"""Module that shows the time before an event"""
	strings = {
		"name": "Timer",
		"_cfg_msg": "Custom message for command .time\nMay contain {date} — your custom date",
		"_cfg_date": "Custom date",
		"_lang": "en",
		"wrong_date": "<emoji document_id=5321493651161881544>❗</emoji> <b>You pass the wrong date in config!</b> Change it on <code>.cfg Timer</code>\n\nThe reason may be that this date has already passed",
		"default_msg": "<emoji document_id=6327819143043090120>🎄</emoji> <b>Until New Year's, there are {date}</b>\n<emoji document_id=5269693399224557532>🥰</emoji> <i>Waiting for the New Year surrounded by friends</i>"
	}

	strings_ru = {
		"_cls_doc": "Модуль, показывающий время до какого-либо события",
		"_cfg_msg": "Кастомное сообщение для команды .time\nМожет содержать ключевое слово {date} — твою кастомную дату",
		"_cfg_date": "Кастомная дата",
		"_lang": "ru",
		"wrong_date": "<emoji document_id=5321493651161881544>❗</emoji> <b>Неправильно указана дата в конфиге!</b> Измени её в <code>.cfg Timer</code>\n\nПричиной может быть то, что эта дата уже прошла",
		"default_msg": "<emoji document_id=6327819143043090120>🎄</emoji> <b>До нового года осталось {date}</b>\n<emoji document_id=5269693399224557532>🥰</emoji> <i>Жду НГ в окружении друзей</i>"
	}

	def __init__(self):
		self.config = loader.ModuleConfig(
			loader.ConfigValue(
				"date",
				"31.12.2023",
				lambda: self.strings("_cfg_date"),
				validator=loader.validators.RegExp(
					regex=r"^\d{1,2}\.\d{1,2}\.\d{4}$"
				)
			),
			loader.ConfigValue(
				"msg",
				self.strings["default_msg"],
				lambda: self.strings("_cfg_msg"),
				validator=loader.validators.String()
			)
		)


	async def pluralForm(self, c, vs):
		c = abs(c)
		if c % 10 == 1 and c % 100 != 11:
			var = 0
		elif 2 <= c % 10 <= 4 and (c % 100 < 10 or c % 100 >= 20):
			var = 1
		else:
			var = 2
		return f"{c} {vs[var]}"


	@loader.command(
		ru_doc="— показать, сколько осталось до <чего-либо>"
	)
	async def timecmd(self, message: Message):
		"""— show how much time is left before the event"""
		d = str(self.config["date"]).split(".")
		msg = str(self.config["msg"])

		date = datetime.datetime(int(d[2]), int(d[1]), int(d[0]))
		now = datetime.datetime.now()

		if date < now:
			await utils.answer(message, self.strings["wrong_date"])
			return

		t = abs(date-now)

		if self.strings("_lang") == "ru":
			d = await self.pluralForm(t.days, ["день", "дня", "дней"])
			h = await self.pluralForm(t.seconds//3600, ["час", "часа", "часов"])
			m = await self.pluralForm(t.seconds//60%60, ["минута", "минуты", "минут"]) 
			s = await self.pluralForm(t.seconds%60, ["секунда", "секунды", "секунд"])
		else:
			d = str(t.days) + (" day" if t.days == 1 else " days")
			h = str(t.seconds//3600) + (" hour" if t.seconds//3600 == 1 else " hours")
			m = str(t.seconds//60%60) + (" minute" if t.seconds//60%60 == 1 else " minutes")
			s = str(t.seconds%60) + (" second" if t.seconds%60 == 1 else " seconds")

		time = f"{d}, {h}, {m}, {s}"
		await utils.answer(
			message,
			self.config["msg"].format(date=time)
		)
