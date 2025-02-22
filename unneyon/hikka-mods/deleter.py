__version__ = (1, 0, 0)
#          █  █ █▄ █ █▄ █ █▀▀ ▀▄▀ █▀█ █▄ █
#          ▀▄▄▀ █ ▀█ █ ▀█ ██▄  █  █▄█ █ ▀█ ▄
#                © Copyright 2025
#            ✈ https://t.me/unneyon

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit, distribute or redistribute this file without direct permission from the author.

# meta banner: https://mods.unneyon.ru/banners/deleter.png
# meta pic: https://static.unneyon.ru/mods/deleter_icon.png
# meta developer: @unneyon_hmods
# scope: hikka_only
# scope: hikka_min 1.6.3

import logging

from telethon import types

from .. import loader, utils


logger = logging.getLogger(__name__)


@loader.tds
class DeleterMod(loader.Module):
	"""Module for delete your messages"""

	strings = {
		"name": "Deleter",
		"_cfg_trigger": "Trigger for delete messages",
		"_cfg_edit_msgs": "Is need to edit messages before delete them?",
		"_cfg_edit_text": "Text for edit messages"
	} 

	strings_ru = {
		"_cfg_trigger": "Триггер-команда для удаления сообщений",
		"_cfg_edit_msgs": "Нужно ли редактировать сообщения перед удалением?",
		"_cfg_edit_text": "Текст для редактирования сообщений",
		"_cls_doc": "Модуль для удаления своих сообщений"
	}

	def __init__(self):
		self.config = loader.ModuleConfig(
			loader.ConfigValue(
				"trigger",
				"дд",
				lambda: self.strings["_cfg_trigger"]
			),
			loader.ConfigValue(
				"edit_msgs",
				True,
				lambda: self.strings["_cfg_edit_msgs"],
				validator=loader.validators.Boolean()
			),
			loader.ConfigValue(
				"edit_text",
				"\xad",
				lambda: self.strings["_cfg_edit_text"]
			)
		)


	@loader.command(
		ru_doc="[число] — Удалить сообщения (можно использовать значение из конфига: «{значение}{число}», без пробела!)"
	)
	async def delmsgcmd(self, message: types.Message):
		"""[count] — Delete messages (you can use your trigger from config: «{value}{count}» and write them only together!)"""

		args = utils.get_args(message)
		count = 1
		if args:
			count = int(args[0]) if args[0].isnumeric() else 1

		dmsgs = []
		msgs = await self._client.get_messages(
			message.chat_id, limit=50+count
		)
		for i in msgs:
			if i.id == message.id:
				continue
			if i.sender_id == self._client.tg_id:
				dmsgs.append(i)

		if self.config["edit_msgs"]:
			await message.edit(self.config["edit_text"])
		await message.delete()

		for i in dmsgs:
			if count == 0:
				break
			if self.config["edit_msgs"]:
				try:
					await i.edit(self.config["edit_text"])
				except:
					pass
			await i.delete()
			count -= 1


	@loader.tag(
		only_messages=True, no_media=True, no_inline=True,
		out=True
	)
	async def watcher(self, message: types.Message):
		if not message.raw_text.startswith(self.config['trigger']):
			return

		p = message.raw_text.partition(self.config['trigger'])[2]
		count = int(p) if p.isdigit() else 1

		dmsgs = []
		msgs = await self._client.get_messages(
			message.chat_id, limit=50+count
		)
		for i in msgs:
			if i.id == message.id:
				continue
			if i.sender_id == self._client.tg_id:
				dmsgs.append(i)

		if self.config["edit_msgs"]:
			await message.edit(self.config["edit_text"])
		await message.delete()

		for i in dmsgs:
			if count == 0:
				break
			if self.config["edit_msgs"]:
				try:
					await i.edit(self.config["edit_text"])
				except:
					pass
			await i.delete()
			count -= 1