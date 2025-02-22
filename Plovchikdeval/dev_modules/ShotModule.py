__version__ = (0, 0, 4)

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
# requires: pygments

import os
import io
import logging

import pygments
from pygments.formatters import ImageFormatter
from pygments.lexers import Python3Lexer
from requests import get

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class ShotModuleMod(loader.Module):
	"""Module for making screenshots"""

	strings = {
		"name": "ShotModule",
		"in_progress": "<blockquote><emoji document_id=5255971360965930740>🕔</emoji> <b>Taking a screenshot...</b></blockquote>",
		"web_no_args": "<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Provide a link or reply to the message</b></blockquote>",
		"not_py": "<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Reply to example.py</b></blockquote>",
		"err": "<blockquote><emoji document_id=5415732509310735525>😕</emoji> <b>Something went wrong</b></blockquote>",
		"no_token": "<blockquote><emoji document_id=5402461597237004802>🧐</emoji> <b>Token not found! Check config</b></blockquote>",
		"_cfg_token": "Paste the token received from screenshotapi.net"
	}

	strings_ru = {
		"in_progress": "<blockquote><emoji document_id=5255971360965930740>🕔</emoji> <b>Делаю скриншот...</b></blockquote>",
		"web_no_args": "<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Укажите ссылку или ответьте на сообщение</b></blockquote>",
		"not_py": "<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Ответьте на сообщение с файлом</b></blockquote>",
		"err": "<blockquote><emoji document_id=5415732509310735525>😕</emoji> <b>Что-то пошло не так</b></blockquote>",
		"no_token": "<blockquote><emoji document_id=5402461597237004802>🧐</emoji> <b>Токен не найден! Проверьте конфиг</b></blockquote>",
		"_cfg_token": "Вставьте токен, полученный от screenshotapi.net"
	}

	def __init__(self):
		self.config = loader.ModuleConfig(
				loader.ConfigValue(
						"token",
						None,
						lambda: self.strings("_cfg_token"),
						validator=loader.validators.Hidden(),
					),
			)

	async def client_ready(self, client, db):
		self._client = client

	@loader.sudo
	@loader.command(en_doc="Takes screenshot of website", ru_doc="Делает скриншот сайта")
	async def webs(self, message: Message):
		if not self.config["token"]:
			await utils.answer(message, self.strings("no_token"))
			return

		reply = None
		args = utils.get_args_raw(message)

		if not args:
			reply = await message.get_reply_message()

			if not reply:
				await utils.answer(message, self.strings("web_no_args"))
				return

			args = reply.raw_text

		await utils.answer(message, self.strings("in_progress"))

		webshot_api_lnk = f'https://shot.screenshotapi.net/screenshot?token={self.config["token"]}&url={args}&width=1920&height=1080&full_page=true&output=image'
		output = get(webshot_api_lnk)

		if not output.ok:
			await utils.answer(message, self.strings("err"))
			return

		output = io.BytesIO(output.content)
		output.name = "webshot.png"
		output.seek(0)

		await utils.answer_file(message, output, reply_to=reply)

	@loader.sudo
	@loader.command(en_doc="Takes screenshot of website", ru_doc="Делает скриншот файла")
	async def files(self, message: Message):
		reply = await message.get_reply_message()

		if not reply:
			await utils.answer(message, self.strings("not_py"))
			return

		media = reply.media

		if not media:
			await utils.answer(message, self.strings("not_py"))
			return

		await utils.answer(message, self.strings("in_progress"))

		try:
			file = await self._client.download_file(media)
			text = file.decode("utf-8")
			pygments.highlight(
				text,
				Python3Lexer(),
				ImageFormatter(font_name="DejaVu Sans Mono", line_numbers=True),
				"fileshot.png",
			)

			await utils.answer_file(message, "fileshot.png", reply_to=reply)

			os.remove("fileshot.png")
		except Exception as e:
			logger.error(str(e), exc_info=True)
			await utils.answer(message, self.strings("err"))

