# meta pic: https://static.whypodg.me/mods!stablediffusion.png
# meta banner: https://mods.whypodg.me/badges/stablediffusion.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.6.2

import json
import re
import requests
import datetime

from hikkatl.types import Message
from .. import loader, utils


@loader.tds
class StableDiffusionMod(loader.Module):
	"""Some mod for work with StableDiffusion. API KEY required!"""
	strings = {
		"name": "StableDiffusion",
		"_cfg_api_key": "Insert the StableDiffusionApi.com API Key",
		"_cfg_model": "Pass the AI model",
		"_cfg_bad_prompt": "Pass the bad prompt — is that what you don't want to see in the pic",
		"_cfg_debug": "Debug mode",
		"_cfg_samples": "Default quantity of images to generate",
		"_cfg_steps": "Steps — The higher the number, the more the image will be detailed",
		"_cfg_upscale": "Using upscale",
		"error": "<emoji document_id=6325579261763651444>⚠</emoji> <b>Some error occured!</b>\n\n<code>{}</code>",
		"key_required": "<b>API Key required!</b> Insert it in <code>.cfg StableDiffusion</code>",
		"done": "<emoji document_id=5327958075158568158>✅</emoji> <b>Image is generated!</b>\n\n",
		"debug": "<b>Model:</b> <code>{model}</code>\n<b>Prompt:</b> <code>{prompt}</code>\n" \
				 "<b>Bad prompt:</b> <code>{negative}</code>\n<b>Steps:</b> <i>{steps}, {upsc}" \
				 "upscaled using external AI{time}</i>",
		"not": "not ",
		"drawing": "<emoji document_id=5431456208487716895>🎨</emoji> <b>Image is drawing...</b>",
		"help": "<emoji document_id=5325762745574891391>🥹</emoji> <b>Help for</b> <code>StableDiffusion</code> <b>module</b>\n\n\n" \
				"<emoji document_id=5409309265460471937>1️⃣</emoji> <b>Configuration:</b>\nAll configuration in the config" \
				" - <code>.cfg StableDiffusion</code>\n\n\n<emoji document_id=5408970203562255606>2️⃣</emoji> <b>" \
				"Parameters and their description:</b>\n  <code>api_key</code> is your personal access key to StableDiffusionAPI.com, " \
				" you can get it <a href='https://stablediffusionapi.com/settings/api'>here</a>\n\n  <code>model</code> is the model to be generated (in config specifies which " \
				"models are available)\n\n  <code>bad_prompt</code> - negative input. It is needed in order to remove from your " \
				"images what you don't wanna see\n\n  <code>debug</code> - if value is <i>True</i>, the response will contain" \
				" information about the generated image(s) (model, prompt, bad_prompt, steps, etc.)\n  <code>samples</code> — " \
				"number of images generated\n\n  <code>steps</code> are <i>«steps»</i> . the higher the number, the more detailed" \
				" the image will be\n\n  <code>upscale</code> - improved generation using AI\n\n\n<emoji document_id=" \
				"5406784224122384435>3️⃣</emoji> <b>Usage:</b>\nLet's suppose that you have finished the setup. Let's move on to use.\n" \
				"You need to use it like this: <code>.sd</code> &lt;prompt&gt;\nWhere &lt;prompt&gt; is whatever you wanna see on " \
				"the image"
		}

	strings_ru = {
		"_cls_doc": "Какой-то модуль для работы с StableDiffusion. Нужен API KEY!",
		"_cfg_api_key": "Укажи свой API Key от StableDiffusionAPI.com",
		"_cfg_model": "Укажи модель",
		"_cfg_bad_prompt": "Укажи негативный ввод — то, что ты не хочешь видеть на изображении",
		"_cfg_debug": "Debug мод",
		"_cfg_samples": "Количество изображений по умолчанию для генерации",
		"_cfg_steps": "Шаги - чем выше число, тем больше детальнее будет изображение.",
		"_cfg_upscale": "Использование улучшения",
		"error": "<emoji document_id=6325579261763651444>⚠</emoji> <b>Произошла ошибка!</b>\n\n<code>{}</code>",
		"key_required": "<emoji document_id=6325579261763651444>⚠</emoji> <b>Нужен API Key!</b> Укажи его в <code>.cfg StableDiffusion</code>",
		"done": "<emoji document_id=5327958075158568158>✅</emoji> <b>Изображение сгенерировано!</b>\n\n",
		"debug": "<b>Модель:</b> <code>{model}</code>\n<b>Ввод:</b> <code>{prompt}</code>\n" \
				 "<b>Негативный ввод:</b> <code>{negative}</code>\n<b>Шаги:</b> <i>{steps}, {upsc}" \
				 "улучшено с использованием ИИ{time}</i>",
		"not": "не было ",
		"drawing": "<emoji document_id=5431456208487716895>🎨</emoji> <b>Рисую…</b>",
		"help": "<emoji document_id=5325762745574891391>🥹</emoji> <b>Помощь по модулю </b><code>StableDiffusion</code>\n\n\n" \
				"<emoji document_id=5409309265460471937>1️⃣</emoji> <b>Настройка</b>.\nВся настройка проводится в конфиге — " \
				"<code>.cfg StableDiffusion</code>\n\n\n<emoji document_id=5408970203562255606>2️⃣</emoji> <b>Параметры и их описание" \
				":</b>\n  <code>api_key</code> — это ваш персональный ключ доступа к StableDiffusionAPI.com, его можно получить на" \
				" этом же сайте\n\n  <code>model</code> — это модель для генерации (в конфиге указано, какие модели есть)\n\n" \
				"  <code>bad_prompt</code> — негативный ввод. он нужен для того, чтобы убрать с ваших изображений то, " \
				"что вы не хотите видеть\n\n  <code>debug</code> — если установлено <i>True</i>, в ответе будет информация" \
				" о генерируемом(-ых) изображении(-ях) (модель, prompt, bad_prompt, steps и т.д.)" \
				"\n\n  <code>samples</code> — кол-во генерации изображений" \
				"\n\n  <code>steps</code> — это <i>«шаги»</i>. чем выше число, тем детальнее будет изображение" \
				"\n\n  <code>upscale</code> — улучшение генерации с помощью ИИ" \
				"\n\n\n<emoji document_id=5406784224122384435>3️⃣</emoji> <b>Использование</b> \nПредположим, что Вы закончили настройку. " \
				"Перейдём к использованию.\n\nИспользовать нужно так: <code>.sd</code> &lt;prompt&gt;\nГде &lt;prompt&gt; — что угодно" \
				", что вы хотите видеть на изображении"
	}

	def __init__(self): # debug: bool, bad_prompt
		self.config = loader.ModuleConfig(
			loader.ConfigValue(
				"api_key",
				None,
				lambda: self.strings("_cfg_api_key"),
				validator=loader.validators.Hidden()
			),
			loader.ConfigValue(
				"model",
				"anything-v5",
				lambda: self.strings("_cfg_model"),
				validator=loader.validators.Choice([
					'abyssorangemix2nsfw', 'anything-v4', 'anything-v5',
					'anythingelse-v4', 'bro623jbfe32', 'cetusmix', 'cnwi74tjsdfw',
					'counterfeit-v20', 'counterfeit-v30', 'dark-sushi-25d',
					'disillusionmix', 'grapefruit-nsfw-anim', 'hanfu',
					'hc-a-mecha-musume-a', 'hc-kokkoro', 'hc-kyoka', 'hc-sailor-mercury',
					'majicmixfantasy', 'meinamix', 'meinapastel', 'night-sky-yozora-sty',
					'tmnd-mix', 'troi4bwiyt4', 'ttksuperspirit'
				])
			),
			loader.ConfigValue(
				"bad_prompt",
				(
					"(bad_prompt:0.8), multiple persons, multiple views, extra hands,"
					" ugly, lowres, bad quality, blurry, disfigured, extra limbs,"
					" missing limbs, deep fried, cheap art, missing fingers, out of"
					" frame, cropped, bad art, face hidden, text, speech bubble,"
					" stretched, bad hands, error, extra digit, fewer digits, worst"
					" quality, low quality, normal quality, mutated, mutation,"
					" deformed, severed, dismembered, corpse, pubic, poorly drawn,"
					" (((deformed hands))), (((more than two hands))), (((deformed"
					" body))), ((((mutant)))), painting, extra fingers, mutated hands,"
					" poorly drawn hands, poorly drawn face, bad anatomy, bad"
					" proportions, cloned face, skinny, glitchy, double torso,"
					" extra arms, mangled fingers, missing lips, distorted face,"
					" extra legs"
				),
				lambda: self.strings("_cfg_bad_prompt"),
			),
			loader.ConfigValue(
				"debug",
				False,
				lambda: self.strings("_cfg_debug"),
				validator=loader.validators.Boolean()
			),
			loader.ConfigValue(
				"samples",
				1,
				lambda: self.strings("_cfg_samples"),
				validator=loader.validators.Integer(minimum=1, maximum=4),
			),
			loader.ConfigValue(
				"steps",
				30,
				lambda: self.strings("_cfg_steps"),
				validator=loader.validators.Integer(minimum=1, maximum=50),
			),
			loader.ConfigValue(
				"upscale",
				False,
				lambda: self.strings("_cfg_upscale"),
				validator=loader.validators.Boolean()
			)
		)


	async def getFetch(self, url):
		payload = json.dumps({"key": self.config['api_key']})
		headers = {"Content-Type": "application/json"}
		r = (await utils.run_sync(
			requests.post,
			url,
			headers=headers,
			data=payload
		)).json()

		if r.get('status') == "success":
			return r['output']
		else:
			return (await self.getFetch(url))


	@loader.command(
		ru_doc="— помощь по использованию и настройке модуля",
		alias="sdh"
	)
	async def sdhelpcmd(self, message: Message):
		"""— help on using and configure the module"""
		await utils.answer(
			message,
			response=self.strings['help']
		)


	@loader.command(
		ru_doc="<prompt> — генерация изобраения с использованием StableDiffusion API."
	)
	async def sdcmd(self, message: Message):
		"""<prompt> — generate an image using StableDiffusion API"""
		if not self.config['api_key']:
			await utils.answer(
				message,
				self.strings['key_required']
			)
			return

		await utils.answer(
			message,
			response=self.strings['drawing']
		)
		prompt = utils.get_args_raw(message)

		url =  "https://stablediffusionapi.com/api/v3/dreambooth"
		payload = json.dumps({ 
			"key": self.config['api_key'],
			"model_id": self.config['model'],
			"prompt": prompt,
			"negative_prompt": self.config['bad_prompt'],
			"width": "512",
			"height": "512",
			"samples": self.config['samples'],
			"num_inference_steps": self.config['steps'],
			"safety_checker": "no",
			"enhance_prompt": "yes",
			"seed": None,
			"guidance_scale": 7.5,
			"multi_lingual": "no",
			"panorama": "no",
			"self_attention": "no",
			"upscale": "yes" if self.config['upscale'] else "no",
			"embeddings": "embeddings_model_id",
			"lora": "lora_model_id",
			"webhook": None,
			"track_id": None
		})
		headers = {
			"Content-Type": "application/json"
		}
		r = (await utils.run_sync(requests.post, url, headers=headers, data=payload)).json()

		if r.get('status') == "error":
			await utils.answer(
				message,
				response=self.strings['error'].format(r)
			)
			return

		if r.get('output'):
			out = self.strings['done']
			if self.config['debug']:
				out += self.strings['debug'].format(
					model=r['meta']['model_id'],
					prompt=r['meta']['prompt'],
					negative=r['meta']['negative_prompt'],
					steps=r['meta']['steps'],
					upsc=self.strings['not'] if not self.config['upscale'] else "",
					time=f", {round(r['generationTime'], 2)}s"
				)
			imgs = []
			for i in r['output']:
				img = (await utils.run_sync(
					requests.get,
					i
				)).content
				imgs.append(img)
			await utils.answer_file(
				message,
				file=imgs,
				caption=out
			)
		elif r.get('status') == "processing":
			out = self.strings['done']
			if self.config['debug']:
				out += self.strings['debug'].format(
					model=r['meta']['model_id'],
					prompt=r['meta']['prompt'],
					negative=r['meta']['negative_prompt'],
					steps=r['meta']['steps'],
					upsc=self.strings['not'] if not self.config['upscale'] else "",
					time=""
				)
			rr = await self.getFetch(r)
			imgs = []
			for i in rr['output']:
				img = (await utils.run_sync(
					requests.get,
					i
				)).content
				imgs.append(img)
			await utils.answer_file(
				message,
				file=imgs,
				caption=out
			)
		else:
			await utils.answer(
				message,
				response=self.strings['error'].format(r)
			)
