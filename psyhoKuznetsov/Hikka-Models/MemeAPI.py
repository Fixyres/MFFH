__version__ = (1, 2, 0)
# meta developer: @psyhomodules

from .. import loader, utils
import random
import asyncio
import aiohttp
import json

@loader.tds
class Meme(loader.Module):
    """Модуль для получения случайных мемов"""
    strings = {
        "name": "MemeAPI",
        "loading": "⌛",
        "error_load": "❌ <b>Не удалось загрузить мем!</b>",
        "error_send": "❌ <b>Не удалось отправить мем с {}!</b>",
        "error_photo": "❌ <b>Ошибка загрузки изображения!</b>",
        "error_translate": "❌ <b>Не удалось перевести название мема!</b>"
    }

    def __init__(self):
        self.apis = [
            (self._get_imgflip_meme, "ImgFlip"),
            (self._get_meme_api, "MemeAPI"),
        ]
        self._translation_cache = {}
        self._url_cache = set()  
        self._max_cache_size = 1000  

     async def client_ready(self, client, db):
        self.client = client
        self.db = db
         
    async def _translate_text(self, text):
        if not text:
            return ""
        
        if text in self._translation_cache:
            return self._translation_cache[text]

        url = "https://translate.googleapis.com/translate_a/single"
        
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "ru",
            "dt": "t",
            "q": text
        }
        
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, params=params, timeout=10) as response:
                        if response.status != 200:
                            await asyncio.sleep(1)
                            continue
                            
                        data = await response.json()
                        
                       
                        translated_text = ""
                        for sentence in data[0]:
                            if sentence[0]:
                                translated_text += sentence[0]
                        
                        if translated_text:
                            self._translation_cache[text] = translated_text
                            return translated_text
            except Exception as e:
                await asyncio.sleep(1)
                continue
        
        return text

    @loader.command(ru_doc="Получить случайный мем")
    async def meme(self, message):
        args = utils.get_args_raw(message)
        
        if args and args.isdigit() and 1 <= int(args) <= len(self.apis):
            api_index = int(args) - 1
            apis_to_try = [self.apis[api_index]]
        else:
            shuffled_apis = random.sample(self.apis, len(self.apis))
            apis_to_try = shuffled_apis
        
        await utils.answer(message, self.strings["loading"])
        
        meme_data = None
        source_name = "неизвестный источник"
        
        for api_func, api_name in apis_to_try:
            try:
                result = await api_func()
                if result:
                    meme_data = result
                    source_name = api_name
                    break
            except Exception:
                continue

        if not meme_data:
            await utils.answer(message, self.strings["error_load"])
            return

        meme_url, meme_name = meme_data

        try:
            meme_title = await self._translate_text(meme_name)
            caption = f"<pre>{meme_title}</pre>"
        except Exception:
            caption = f"<pre>{meme_name}</pre>"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(meme_url, timeout=15) as resp:
                    if resp.status != 200:
                        await utils.answer(message, self.strings["error_photo"])
                        return
                    meme_bytes = await resp.read()

            await message.client.send_file(
                message.to_id,
                meme_bytes,
                caption=caption,
                parse_mode="HTML"
            )
            await message.delete()
        except Exception:
            await utils.answer(
                message, 
                self.strings["error_send"].format(source_name)
            )

    async def _get_imgflip_meme(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.imgflip.com/get_memes", timeout=10) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                memes = data.get("data", {}).get("memes", [])
                if not memes:
                    return None
                random_meme = random.choice(memes)
                return random_meme.get("url"), random_meme.get("name", "Безымянный мем")

    async def _get_meme_api(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.com/gimme", timeout=10) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data.get("url"), data.get("title", "Безымянный мем")
                

            return None
