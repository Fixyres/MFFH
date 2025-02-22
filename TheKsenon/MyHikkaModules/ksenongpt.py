from .. import loader, utils
import requests
import io
import aiohttp
import logging

logger = logging.getLogger(__name__)

# meta developer: @kmodules
# changelog: Фиксы, обновитесь обязательно 

__version__ = (1, 5, 4)
version = __version__

@loader.tds
class KsenonGPTMod(loader.Module):
    """KsenonGPT module for text and image generation using KsenonAPI"""

    strings = {
        "name": "KsenonGPT",
        "no_api_key": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>You have not set up the API key!</b>\n\n<emoji document_id=5879585266426973039>🌐</emoji> <b>The key is very easy to get, it's free.</b>\n\n<emoji document_id=6034962180875490251>🔓</emoji> <b>Bot: </b><b>@ksenonapi_gettoken_bot</b>",
        "generating_text": "<emoji document_id=5891243564309942507>💬</emoji> <b>Responding to your message...</b>",
        "text_generated": "<emoji document_id=5870984130560266604>💬</emoji> <b>Request:</b> <code>{}</code>\n\n<emoji document_id=5891243564309942507>💬</emoji> {}",
        "generating_image": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Generating image...</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Model:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Request:</b> <code>{}</code>",
        "image_generated": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Image generated!</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Model:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Request:</b> <code>{}</code>\n\n<emoji document_id=5877307202888273539>📥</emoji> <b>Link:</b> {}",
        "error_blocked": "<emoji document_id=5832546462478635761>🔒</emoji> <b>You have been blocked!</b>\n\n<emoji document_id=5879896690210639947>🗑</emoji><b>NSFW | politics etc. generation is prohibited.</b>",
        "error_occurred": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>An error occurred!</b>\n\n<emoji document_id=5967816500415827773>💻</emoji> <b>Model:</b> {}\n<emoji document_id=5874986954180791957>📶</emoji> <b>Server status, code:</b> {}\n<emoji document_id=5832251986635920010>➡️</emoji> <b>Error:</b> {}",
        "text_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Text models:</b>\n\n<blockquote>o1-preview\ngpt-4o\nclaude-3-5-sonnet\nsearchgpt (GPT + Internet)\nblackboxai-pro\nclaude-3-5-sonnet-20240620\nclaude-3-haiku-ddg\ngemini-1.5-pro-latest\nllama-3.1-405b\ngpt-3.5-turbo-202201\ngpt-4o-mini-ddg\ngpt-4o-2024-05-13\nmicrosoft/Phi-3.5-mini-instruct\nQwen/Qwen2.5-Coder-32B-Instruct\nQwen/QwQ-32B-Preview</blockquote>\n\n<emoji document_id=5843908536467198016>✅️</emoji> <b>We have 150+ models!</b>\n<emoji document_id=5778423822940114949>🛡</emoji><b><b> https://t.me/ksenonapi_models</b>",
        "image_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Image models:</b>\n\n<blockquote><b>flux-pro-mg\nflux-dev\nsd3-ultra\npixart-alpha</b></blockquote>",
        "no_args": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>No arguments provided!</b>",
        "update_available": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>KsenonGPT update available!</b>\n\n<emoji document_id=5449683594425410231>🔼</emoji> <b>New version: {}</b>\n<emoji document_id=5447183459602669338>🔽</emoji> <b>Current version: {}</b>\n\n<emoji document_id=5447410659077661506>🌐</emoji> <b>Changelog:</b>\n<emoji document_id=5458603043203327669>🔔</emoji> <i>{}</i>\n\n<emoji document_id=5206607081334906820>✔️</emoji> <b>Command to update:</b>\n<code>.dlmod https://raw.githubusercontent.com/TheKsenon/MyHikkaModules/refs/heads/main/ksenongpt.py</code>",
        "latest_version": "<emoji document_id=5370870691140737817>🥳</emoji> <b>You have the latest version of KsenonGPT!</b>\n\n<emoji document_id=5447644880824181073>⚠️</emoji><b>Developers are making updates and fixes almost every day, check frequently!</b>",
        "select_model": "<b>🤖 Select AI model:\n\n🔑 You can also specify a model directly by using .setmodel model_name</b>",
        "model_set": "<b>🎯 Model has been set to: {}</b>",
        "invalid_model": "<b>❌ Invalid model specified!</b>",
        "need_set_model": "<emoji document_id=5222148368955877900>🔥</emoji> <b>Please set the model using .setmodel command!</b>"
    }

    strings_ru = {
        "name": "KsenonGPT",
        "no_api_key": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Вы не настроили API ключ!</b>\n\n<emoji document_id=5879585266426973039>🌐</emoji> <b>Ключ очень легко достать, он бесплатный.</b>\n\n<emoji document_id=6034962180875490251>🔓</emoji> <b>Бот: </b><b>@ksenonapi_gettoken_bot</b>",
        "generating_text": "<emoji document_id=5891243564309942507>💬</emoji> <b>Отвечаю на ваше сообщение...</b>",
        "text_generated": "<emoji document_id=5870984130560266604>💬</emoji> <b>Запрос:</b> <code>{}</code>\n\n<emoji document_id=5891243564309942507>💬</emoji> {}",
        "generating_image": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Генерирую изображение...</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Модель:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Запрос:</b> <code>{}</code>",
        "image_generated": "<emoji document_id=5766879414704935108>🖼</emoji> <b>Изображение сгенерировано!</b>\n\n<emoji document_id=5994544674604322765>🤖</emoji> <b>Модель:</b> <code>{}</code>\n<emoji document_id=5877465816030515018>🔗</emoji> <b>Запрос:</b> <code>{}</code>\n\n<emoji document_id=5877307202888273539>📥</emoji> <b>Ссылка:</b> {}",
        "error_blocked": "<emoji document_id=5832546462478635761>🔒</emoji> <b>Вы были заблокированы!</b>\n\n<emoji document_id=5879896690210639947>🗑</emoji><b>Запрещено генерировать NSFW | политика и т.д.</b>",
        "error_occurred": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Произошла ошибка!</b>\n\n<emoji document_id=5967816500415827773>💻</emoji> <b>Модель:</b> {}\n<emoji document_id=5874986954180791957>📶</emoji> <b>Статус сервера, код:</b> {}\n<emoji document_id=5832251986635920010>➡️</emoji> <b>Ошибка:</b> {}",
        "text_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Текстовые модели:</b>\n\n<blockquote>o1-preview\ngpt-4o\nclaude-3-5-sonnet\nsearchgpt (GPT + Internet)\nblackboxai-pro\nclaude-3-5-sonnet-20240620\nclaude-3-haiku-ddg\ngemini-1.5-pro-latest\nllama-3.1-405b\ngpt-3.5-turbo-202201\ngpt-4o-mini-ddg\ngpt-4o-2024-05-13\nmicrosoft/Phi-3.5-mini-instruct\nQwen/Qwen2.5-Coder-32B-Instruct\nQwen/QwQ-32B-Preview</blockquote>\n\n<emoji document_id=5843908536467198016>✅️</emoji> <b>У нас 150+ моделей!</b>\n<emoji document_id=5778423822940114949>🛡</emoji><b><b> https://t.me/ksenonapi_models</b>",
        "image_models": "<emoji document_id=5879585266426973039>🌐</emoji> <b>Модели для изображений:</b>\n\n<blockquote><b>flux-pro-mg\nflux-dev\nsd3-ultra\npixart-alpha</b></blockquote>",
        "no_args": "<emoji document_id=5881702736843511327>⚠️</emoji> <b>Не указаны аргументы!</b>",
        "update_available": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Доступно обновление KsenonGPT!</b>\n\n<emoji document_id=5449683594425410231>🔼</emoji> <b>Новая версия: {}</b>\n<emoji document_id=5447183459602669338>🔽</emoji> <b>Текущая версия: {}</b>\n\n<emoji document_id=5447410659077661506>🌐</emoji> <b>Список изменений:</b>\n<emoji document_id=5458603043203327669>🔔</emoji> <i>{}</i>\n\n<emoji document_id=5206607081334906820>✔️</emoji> <b>Команда для обновления:</b>\n<code>.dlmod https://raw.githubusercontent.com/TheKsenon/MyHikkaModules/refs/heads/main/ksenongpt.py</code>",
        "latest_version": "<emoji document_id=5370870691140737817>🥳</emoji> <b>У вас последняя версия KsenonGPT!</b>\n\n<emoji document_id=5447644880824181073>⚠️</emoji><b>Разработчики делают обновления и исправления почти каждый день, проверяйте чаще!</b>",
        "select_model": "<b>🤖 Выберите ИИ модель:\n\n🔑 Также вы можете указать конкретную модель, напишите .setmodel название_модели</b>",
        "model_set": "<b>🎯 Модель установлена: {}</b>",
        "invalid_model": "<b>❌ Указана неверная модель!</b>",
        "need_set_model": "<emoji document_id=5222148368955877900>🔥</emoji> <b>Поставьте модель в .setmodel!</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                "API key from @ksenonapi_gettoken_bot",
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "default_model",
                "",
                "Default AI model to use",
            )
        )
        
    def _create_model_buttons(self):
        buttons = []
        models = [
            ("DeepSeek R1", "deepseek-r1"),
            ("GPT-4o", "gpt-4o"),
            ("Claude 3.5 Sonnet", "claude-3-5-sonnet"),
            ("SearchGPT", "searchgpt"),
            ("P1", "p1"),
            ("Gemini 2.0 Flash", "gemini-flash-2.0")
        ]
        
        row = []
        for i, (name, model_id) in enumerate(models):
            row.append({"text": name, "callback": self._set_model, "args": (model_id,)})
            if len(row) == 2:
                buttons.append(row)
                row = []
        if row:
            buttons.append(row)
            
        return buttons

    async def setmodelcmd(self, message):
        """Set default AI model for text generation"""
        args = utils.get_args_raw(message)
        if args:
            self.config["default_model"] = args
            await utils.answer(message, self.strings["model_set"].format(args))
            return

        await self.inline.form(
            text=self.strings["select_model"],
            message=message,
            reply_markup=self._create_model_buttons())

    async def _set_model(self, call, model):
        self.config["default_model"] = model
        await call.edit(
            self.strings["model_set"].format(model),
            reply_markup=None)

    async def gentextcmd(self, message):
        """Generate text - .gentext <prompt>"""
        if not self.config["api_key"]:
            await utils.answer(message, self.strings["no_api_key"])
            return

        if not self.config["default_model"]:
            await utils.answer(message, self.strings["need_set_model"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        prompt = args
        model = self.config["default_model"]

        msg = await utils.answer(message, self.strings["generating_text"])

        headers = {
            "Authorization": self.config["api_key"],
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "prompt": prompt
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://aeza.theksenon.pro/v1/api/text/generate",
                headers=headers,
                json=data
            ) as response:
                result = await response.json()

                if response.status != 200:
                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            response.status,
                            result.get("error", "Unknown error")
                        )
                    )
                    return

                if "error" in result:
                    if result["error"] == "Your token has been blocked":
                        await utils.answer(msg, self.strings["error_blocked"])
                        return

                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            "N/A",
                            result["error"]
                        )
                    )
                    return

                await utils.answer(
                    msg,
                    self.strings["text_generated"].format(
                        prompt,
                        result["response"]
                    )
                )

    async def genimgcmd(self, message):
        """Generate image - .genimg <prompt> <model>"""
        if not self.config["api_key"]:
            await utils.answer(message, self.strings["no_api_key"])
            return

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_args"])
            return

        try:
            prompt, model = args.rsplit(maxsplit=1)
        except ValueError:
            prompt = args
            model = "flux-pro-mg"

        msg = await utils.answer(
            message,
            self.strings["generating_image"].format(model, prompt)
        )

        headers = {
            "Authorization": self.config["api_key"],
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "prompt": prompt
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://aeza.theksenon.pro/v1/api/image/generate",
                headers=headers,
                json=data
            ) as response:
                result = await response.json()

                if response.status != 200:
                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            response.status,
                            result.get("error", "Unknown error")
                        )
                    )
                    return

                if "error" in result:
                    if result["error"] == "Your token has been blocked":
                        await utils.answer(msg, self.strings["error_blocked"])
                        return

                    await utils.answer(
                        msg,
                        self.strings["error_occurred"].format(
                            model,
                            "N/A",
                            result["error"]
                        )
                    )
                    return

                image_url = result["url"]
                async with session.get(image_url) as response:
                    if response.status != 200:
                        await utils.answer(
                            msg,
                            self.strings["error_occurred"].format(
                                model,
                                response.status,
                                "Failed to download image"
                            )
                        )
                        return

                    image_data = io.BytesIO(await response.read())
                    image_data.name = "image.png"

                    await self._client.send_file(
                        message.peer_id,
                        image_data,
                        caption=self.strings["image_generated"].format(
                            model,
                            prompt,
                            image_url
                        ),
                        reply_to=message.reply_to_msg_id
                    )

                    if message.out:
                        await message.delete()

    async def txtmodelscmd(self, message):
        """List of text models"""
        await utils.answer(message, self.strings["text_models"])

    async def imgmodelscmd(self, message):
        """List of image models"""
        await utils.answer(message, self.strings["image_models"])
        
    async def kupdatecmd(self, message):
        """Check for updates"""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/TheKsenon/MyHikkaModules/refs/heads/main/ksenongpt.py") as response:
                if response.status != 200:
                    return
                    
                content = await response.text()
                
                try:
                    version_line = [line for line in content.split("\n") if "__version__" in line][0]
                    latest_version = tuple(map(int, version_line.split("(")[1].split(")")[0].split(",")))
                    
                    if latest_version > version:
                        changelog = "New version available!" 
                        
                        await utils.answer(
                            message,
                            self.strings["update_available"].format(
                                ".".join(map(str, latest_version)),
                                ".".join(map(str, version)),
                                changelog
                            )
                        )
                    else:
                        await utils.answer(message, self.strings["latest_version"])
                except:
                    logger.error("Failed to parse version from GitHub")
