__version__ = (15, 0, 0)
# change-log: change api address + fix support for more country

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
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @kshmods
# meta banner: https://kappa.lol/nfF_A
# requires: requests aiofiles

import logging
import time
import io
import os
import inspect
import aiohttp
import json
import requests

from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class DevGPT(loader.Module):
	"""DevGPT - позволяет вам общаться с chatgpt и генерировать фото."""

	strings = {
		"name": "DevGPT",
		"wait": "<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>The server is processing the request, please wait...</b></blockquote>",
		"update_whats_new": "\n\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Change-log:</b><code>{whats_new}</code>\n\n</blockquote>",
		"quest": "\n\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Your request: {args}</blockquote>\n<blockquote><emoji document_id=5877260593903177342>⚙️</emoji> Model: <code>{model}</code></blockquote>\n<blockquote><emoji document_id=5199457120428249992>🕘</emoji> Response generation time: <i>{generation_time}s</i></b></blockquote>",
		"quest_img": "<blockquote><b><emoji document_id=5877465816030515018>😀</emoji> Link: <a href='{img_url}'>image</a></b></blockquote>\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Prompt:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Model:</b> <code>{mdl}</code></blockquote>\n\n<blockquote><emoji document_id=5199457120428249992>🕘</emoji> Response generation time: <i>{generation_time}s</i></blockquote>",
		"args_err": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Usage: {prefix}dgpt/dimg <model> <request></b></blockquote>",
		"query_err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>The request cannot be empty!</b></blockquote>",
		"server_err": "<blockquote><emoji document_id=5881702736843511327>⚠️</emoji> <b>Server error: {error}</b></blockquote>",
		"image_err": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Error generating image: {error}</b>",
		"models_list": "<blockquote><emoji document_id=5879841310902324730>😀</emoji><b>Text</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote><emoji document_id=5775949822993371030>🖼</emoji> <b>Images</b></blockquote>\n\n<blockquote>{img_models}</blockquote>",
		"model_not_found": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Model not found! List of available models: {prefix}dgmodels</b></blockquote>",
		"no_url": "No image URL received",
		"no_server_respond": "No response from the server",
		"fetch_failed": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> <b>Fetching data failed</b></blockquote>",
		"actual_version": "<blockquote> <emoji document_id=5208763618773978162>✅</emoji>You have actual DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote><emoji document_id=5875291072225087249>📊</emoji> You have old DevGPT ({ver}) </b></blockquote>\n\n<blockquote><emoji document_id=5879883461711367869>⬇️</emoji> <b>New version: {new_ver} <b></blockquote>",
		"update_command": "\n\n<blockquote><emoji document_id=5877410604225924969>🔄</emoji> To update type:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",
		"ban": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> You are banned! Reason: {reason}</blockquote>",
		"model_set": "<blockquote><emoji document_id=5823396554345549784>✔️</emoji> <b>Default model set.</b></blockquote>",
		"setmodel_help": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Usage: {prefix}setmodel</b> image/text model</blockquote>\n<blockquote><emoji document_id=5251243280577873996>✅</emoji> <b>Models: <code>{prefix}dgmodels</code></b></blockquote>"
	}

	strings_ua = {
		"wait": "<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Сервер обробляє запит, будь ласка, зачекайте...</b></blockquote>",
		"quest": "\n\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Ваш запит: {args}</blockquote>\n<blockquote><emoji document_id=5877260593903177342>⚙️</emoji> Модель: <code>{model}</code></blockquote>\n<blockquote><emoji document_id=5199457120428249992>🕘</emoji> Час генерації відповіді: <i>{generation_time}с</i></b></blockquote>",
		"update_whats_new": "\n\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Список изменений:</b><code>{whats_new}</code>\n\n</blockquote>",
		"quest_img": "<blockquote><b><emoji document_id=5877465816030515018>😀</emoji> Посилання: <a href='{img_url}'>зображення</a></b></blockquote>\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Запит:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Модель:</b> <code>{mdl}</code></blockquote>\n\n<blockquote><emoji document_id=5199457120428249992>🕘</emoji> Час генерації відповіді: <i>{generation_time}с</i></blockquote>",
		"args_err": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Використання {prefix}dgpt/dimg <модель> <запит></b></blockquote>",
		"query_err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Запит не може бути порожнім!</b></blockquote>",
		"server_err": "<blockquote><emoji document_id=5881702736843511327>⚠️</emoji> <b>Помилка сервера: {error}</b></blockquote>",
		"image_err": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Помилка при генерації зображення: {error}</b>",
		"models_list": "<blockquote><emoji document_id=5879841310902324730>😀</emoji><b>Текст</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote><emoji document_id=5775949822993371030>🖼</emoji> <b>Зображення</b></blockquote>\n\n<blockquote>{img_models}\n</blockquote>",
		"model_not_found": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Модель не знайдена! Список доступних моделей {prefix}dgmodels</b></blockquote>",
		"no_url": "Не отримано URL зображення",
		"no_server_respond": "Немає відповіді від сервера",
		"fetch_failed": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> <b>Не вдалося отримати дані</b></blockquote>",
		"actual_version": "<blockquote> <emoji document_id=5208763618773978162>✅</emoji>У вас актуальна версія DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote><emoji document_id=5875291072225087249>📊</emoji> У вас застаріла версія DevGPT ({ver}) </b></blockquote>\n\n<blockquote><emoji document_id=5879883461711367869>⬇️</emoji> <b>Нова версія: {new_ver} <b></blockquote>",
		"update_command": "\n\n<blockquote><emoji document_id=5877410604225924969>🔄</emoji> Для оновлення введіть:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",
		"ban": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> Вас забанено! З причини: {reason}</blockquote>",
		"model_set": "<blockquote><emoji document_id=5823396554345549784>✔️</emoji> <b>Набір моделей за замовчуванням.</b></blockquote>",
		"setmodel_help": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Використання: {prefix}setmodel</b> image/text model</blockquote>\n<blockquote><emoji document_id=5251243280577873996>✅</emoji> <b>Модель: <code>{prefix}dgmodels</code></b></blockquote>"
	}

	strings_ru = {
		"wait": "<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Сервер обрабатывает запрос, подождите...</b></blockquote>",
		"quest": "\n\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Ваш запрос: {args}</blockquote>\n<blockquote><emoji document_id=5877260593903177342>⚙️</emoji> Модель: <code>{model}</code></blockquote>\n<blockquote><emoji document_id=5199457120428249992>🕘</emoji> Время генерации ответа: <i>{generation_time}с</i></b></blockquote>",
		"update_whats_new": "\n\n<blockquote><emoji document_id=5879785854284599288>ℹ️</emoji> <b>Список изменений:</b><code>{whats_new}</code>\n\n</blockquote>",
		"quest_img": "<blockquote><b><emoji document_id=5877465816030515018>😀</emoji> Ссылка: <a href='{img_url}'>изображение</a></b></blockquote>\n\n<blockquote><emoji document_id=5465143921912846619>💭</emoji> <b>Запрос:</b> <code>{prmpt}</code></blockquote>\n\n<blockquote><emoji document_id=5994544674604322765>😀</emoji> <b>Модель:</b> <code>{mdl}</code></blockquote>\n\n<blockquote><emoji document_id=5199457120428249992>🕘</emoji> Время генерации ответа: <i>{generation_time}s</i></blockquote>",
		"args_err": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Использование {prefix}dgpt/dimg <модель> <запрос></b></blockquote>",
		"query_err": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Запрос не может быть пустым!</b></blockquote>",
		"server_err": "<blockquote><emoji document_id=5881702736843511327>⚠️</emoji> <b>Ошибка сервера: {error}</b></blockquote>",
		"image_err": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Ошибка при генерации изображения: {error}</b>",
		"models_list": "<blockquote><emoji document_id=5879841310902324730>😀</emoji><b>Текст</b></blockquote>\n\n<blockquote>{txt_models}</blockquote>\n\n<blockquote><emoji document_id=5775949822993371030>🖼</emoji> <b>Изображения</b></blockquote>\n\n<blockquote>{img_models}</blockquote>",
		"model_not_found": "<blockquote><emoji document_id=5208434048753484584>⛔</emoji> <b>Модель не найдена! Список доступных моделей {prefix}dgmodels</b></blockquote>",
		"no_url": "Не получен URL изображения",
		"no_server_respond": "Нет ответа от сервера",
		"fetch_failed": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> <b>Не удалось получить данные</b></blockquote>",
		"actual_version": "<blockquote> <emoji document_id=5208763618773978162>✅</emoji>У вас актуальная версия DevGPT ({ver})</b></blockquote>",
		"old_version": "<blockquote><emoji document_id=5875291072225087249>📊</emoji> У вас устаревшая версия DevGPT ({ver}) </b></blockquote>\n\n<blockquote><emoji document_id=5879883461711367869>⬇️</emoji> <b>Новая версия: {new_ver} <b></blockquote>",
		"update_command": "\n\n<blockquote><emoji document_id=5877410604225924969>🔄</emoji> Для обновления введите:</b> <code> {prefix}dlm {upd_file}</code></blockquote>",
		"ban": "<blockquote><emoji document_id=5208663713539704322>👎</emoji> Вы забанены! По причине: {reason}</blockquote>",
		"model_set": "<blockquote><emoji document_id=5823396554345549784>✔️</emoji> <b>Установлена модель по умолчанию.</b></blockquote>",
		"setmodel_help": "<blockquote><emoji document_id=5897846616966041652>❓</emoji> <b>Использование: {prefix}setmodel</b> image/text model</blockquote>\n<blockquote><emoji document_id=5251243280577873996>✅</emoji> <b>Модели: <code>{prefix}dgmodels</code></b></blockquote>"
	}

	def __init__(self):
		self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "default_image_model",
                "flux",
                lambda: "Default models for images",
                validator=loader.validators.Choice(
					[
                        "sdxl-turbo",
                        "sd-3.5",
                        "flux",
                        "flux-pro",
                        "flux-dev",
                        "flux-schnell",
                        "dall-e-3",
                        "midjourney"
                    ]
				),
            ),
			loader.ConfigValue(
                "default_text_model",
                "gpt-4",
                lambda: "Default models for text",
                validator=loader.validators.Choice(
					[
                        "evil",
                        "glm-4",
                        "gpt-4",
                        "gpt-4o",
                        "gpt-4o-mini",
                        "mixtral-8x7b",
                        "mistral-nemo",
                        "hermes-2-dpo",
                        "gemini-1.5-flash",
                        "gemini-2.0-flash",
                        "claude-3-haiku",
                        "blackboxai",
                        "blackboxai-pro",
                        "command-r",
                        "command-r-plus",
                        "command-r7b",
                        "qwen-2.5-coder-32b",
                        "qwq-32b",
                        "qvq-72b",
                        "deepseek-chat",
                        "deepseek-r1",
                        "dbrx-instruct"
                    ]
				),
            )
			)

	async def client_ready(self, client, _):
		# self.server_url = "https://api.kshteam.top"
		self.server_url = "https://api.kshteam.top"
		self.server_url_images = "https://api.kshteam.top/v1/images/generate"
		self.server_url_images_v2 = "https://v2.vysssotsky.ru/v1/generate"
		self.additional_server_url = "http://146.19.48.160:25701/generate_image"

		self.api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

		self._client = client
		self.prefix = self._client.loader.get_prefix()
		
		self.repo = "https://raw.githubusercontent.com/Plovchikdeval/dev_modules/main/"

		self.text_models = ["evil", "glm-4", "gpt-4", "gpt-4o", "gpt-4o-mini", "mixtral-8x7b", "mistral-nemo", "hermes-2-dpo", "gemini-1.5-flash", "gemini-2.0-flash", "claude-3-haiku", "blackboxai", "blackboxai-pro", "command-r", "command-r-plus", "command-r7b", "qwen-2.5-coder-32b", "qwq-32b", "qvq-72b", "deepseek-chat", "deepseek-r1", "dbrx-instruct"]
		self.image_models = ["sdxl-turbo", "sd-3.5", "flux", "flux-pro", "flux-dev", "flux-schnell", "dall-e-3", "midjourney"]

	async def generate_text(self, message):
		content = utils.get_args_raw(message)
		start_time = time.time()

		try:
			payload = {
				"model": self.config["default_text_model"],
				"messages": [{"role": "user", "content": content}],
				"max_tokens": 2048,
				"temperature": 0.7,
				"top_p": 1,
			}

			async with aiohttp.ClientSession() as session:
				async with session.post(f"{self.server_url}/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}",  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Content-Type": "application/json"}, json=payload) as response:
					response.raise_for_status()
					generation_time = round(time.time() - start_time, 2)
					if response.status == 200:
						data = await response.json()
						answer = data.get("choices", [{}])[0].get("message", {}).get("content", self.strings("no_server_respond"))
						answer = f"<blockquote>{answer}</blockquote>"

						await utils.answer(message, answer + self.strings("quest").format(args=content, generation_time=generation_time, model=self.config["default_text_model"]))
					else:
						await utils.answer(message, self.strings("server_err").format(error=f"HTTP {response.status}"))
		except Exception as e:
			await utils.answer(message, self.strings("server_err").format(error=str(e)))

	async def generate_image(self, message):
		prompt = utils.get_args_raw(message)
		start_time = time.time()

		try:
			payload = {
				"model": self.config["default_image_model"],
				"prompt": prompt,
				"response_format": "url"
			}

			async with aiohttp.ClientSession() as session:
				async with session.post(self.server_url_images.format(model_name=self.config["default_image_model"]), headers={"Authorization": f"Bearer {self.api_key}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Content-Type": "application/json"}, data=json.dumps(payload)) as response:
					generation_time = round(time.time() - start_time, 2)
					if response.status == 200:
						data = await response.json()
						image_url = data.get("data", [{}])[0].get("url", None)

						if image_url:
							try:
								async with session.get(image_url) as generated_image:
									file_name = "dgimage.png"
									with open(file_name,'wb') as file:
										file.write(await generated_image.read())

								await utils.answer_file(message, file_name, caption=(self.strings('quest_img').format(img_url=image_url, prmpt=prompt, mdl=self.config["default_image_model"], generation_time=generation_time)))
							finally:
								if os.path.exists(file_name):
									os.remove(file_name)
						else:
							await utils.answer(message, self.strings("image_err").format(error=self.strings("no_url")))
					elif self.config["default_image_model"] not in ["sd-3", "any-dark"]:
						logger.warning("v1 API down! Trying to use v2 instead", exc_info=True)
						payload_v2 = {
							"model": self.config["default_image_model"],
							"prompt": prompt
						}
						async with session.post(self.server_url_images_v2, headers={"Authorization": f"Bearer {self.api_key}", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Content-Type": "application/json"}, data=json.dumps(payload_v2)) as response_v2:
							generation_time = round(time.time() - start_time, 2)
							if response_v2.status == 200:
								
								image_v2 = await response_v2.text()

								try:
									image_v2 = json.loads(image_v2)
									image_v2_url = image_v2.get("url")
								except json.JSONDecodeError:
									image_v2_url = image_v2.strip()

								async with session.get(image_v2_url) as image_v2_response:
									image_v2_response.raise_for_status()
									image_v2_content = io.BytesIO(await image_v2_response.read())
								await utils.answer_file(message, image_v2_content, caption=(self.strings('quest_img').format(img_url=image_v2_url, prmpt=prompt, mdl=self.config["default_image_model"], generation_time=generation_time)))
							else:
								err_data = await response_v2.json()
								ban_reason = err_data.get("reason")
								await utils.answer(message, self.strings("ban").format(reason=ban_reason))
					elif response.status == 403:
						err_data = await response.json()
						ban_reason = err_data.get("reason")
						await utils.answer(message, self.strings("ban").format(reason=ban_reason))
					else:
						await utils.answer(message, self.strings("image_err").format(error=f"HTTP {response.status}"))

		except Exception as e:
			await utils.answer(message, self.strings("image_err").format(error=str(e)))
			
	@loader.command(en_doc="Ask gpt for something", ru_doc="Спросите gpt о чем-нибудь", ua_doc="Запитайте gpt про щось")
	async def dgpt(self, message: Message):
		"""Ask gpt for something"""
		args = utils.get_args_raw(message)
		if not args:
			await utils.answer(message, self.strings("args_err").format(prefix=self.prefix))
			return

		await utils.answer(message, self.strings("wait"))

		await self.generate_text(message)
	
	@loader.command(en_doc="Set default model", ru_doc="Установить модель по умолчанию", ua_doc="Встановити модель за замовчуванням")
	async def setmodel(self, message: Message):
		"""Set default model"""
		args = utils.get_args_raw(message)
		if not args or len(args.split()) != 2:
			await utils.answer(message, self.strings("setmodel_help").format(prefix=self.prefix))
			return
		prop = args.split(maxsplit=2)[0]
		model = args.split(maxsplit=2)[1]
		conf = "default_text_model" if prop == "text" else "default_image_model" if prop == "image" else None
		if conf == "default_text_model" and model not in self.text_models:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))
			return
		if conf == "default_image_model" and model not in self.image_models:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))
			return
		if conf is not None:
			self.config[conf] = model
			await utils.answer(message, self.strings("model_set"))
		else:
			await utils.answer(message, self.strings("model_not_found").format(prefix=self.prefix))
			return

	@loader.command(en_doc="Generate image", ru_doc="Сгенерировать изображение", ua_doc="Згенерувати зображення")
	async def dimg(self, message: Message):
		"""Generate image"""
		args = utils.get_args_raw(message)
		if not args:
			await utils.answer(message, self.strings("args_err").format(prefix=self.prefix))
			return

		await utils.answer(message, self.strings("wait"))

		await self.generate_image(message)

	@loader.command(en_doc="Display models list", ru_doc="Показать список моделей", ua_doc="Показати список моделей")
	async def dgmodels(self, message: Message):
		"""Display models list"""
		t_mdl = '\n'.join(self.text_models)
		i_mdl = '\n'.join(self.image_models)
		await utils.answer(message, self.strings("models_list").format(txt_models=t_mdl, img_models=i_mdl))

	@loader.command(en_doc="Check for updates", ru_doc="Проверить обновления", ua_doc="Перевірити оновлення")
	async def dgcheck(self, message: Message):
		"""Check for updates"""
		module_name = self.strings("name")
		module = self.lookup(module_name)
		sys_module = inspect.getmodule(module)

		local_file = io.BytesIO(sys_module.__loader__.data)
		local_file.name = f"{module_name}.py"
		local_file.seek(0)
		local_first_line = local_file.readline().strip().decode("utf-8")

		correct_version = sys_module.__version__
		correct_version_str = ".".join(map(str, correct_version))

		async with aiohttp.ClientSession() as session:
			async with session.get(f"{self.repo}/{local_file.name}") as response:
				if response.status == 200:
					remote_content = await response.text()
					remote_lines = remote_content.splitlines()
					what_new = remote_lines[1].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[1].startswith("# change-log:") else ""
					new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
					new_version_tuple = tuple(map(int, new_version.split(".")))
					if new_version_tuple <= __version__:
						await utils.answer(message, self.strings("actual_version").format(ver=correct_version_str))
						return
				else:
					await utils.answer(message, self.strings("fetch_failed"))
					return

		if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
			await utils.answer(message, self.strings("actual_version").format(ver=correct_version_str))
		else:
			update_message = self.strings("old_version").format(ver=correct_version_str, new_ver=new_version)
			update_message += self.strings("update_command").format(prefix=self.prefix, upd_file=f"{self.repo}/{local_file.name}")
			if what_new:
				update_message += self.strings("update_whats_new").format(whats_new=what_new)
			await utils.answer(message, update_message)