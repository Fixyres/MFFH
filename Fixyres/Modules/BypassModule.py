import json
import aiohttp
import random
import string
from hikkatl.types import Message
from .. import loader, utils

@loader.tds
class BypassModule(loader.Module):
    """Bypass module
    🌟 Создано - @aurafunny
    """
    strings = {
        "name": "BypassModule",
        "key_response": 'Ваш ключ - "{key}"',
        "link_response": 'Ссылка: {link}',
        "link_error": "Ссылка не поддерживается."
    }

    @loader.command(
        ru_doc="Использование .key <url>",
    )
    async def key(self, message: Message):
        """Получить ключ из URL"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "Использование .key <url>")
            return

        url = f"https://kobayashi-heart-attack.vercel.app/api/kobayashi?url={args[0]}&kobayashi=NoHome"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    try:
                        json_data = json.loads(data)
                        key = json_data.get("key", "")
                        await utils.answer(message, self.strings("key_response").format(key=key))
                    except json.JSONDecodeError:
                        await utils.answer(message, "Ошибка при обработке ответа.")
                else:
                    await utils.answer(message, "Ошибка при запросе к сайту.")
    
    @loader.command(
        ru_doc="Использование .generatekey <платформа>",
    )
    async def generatekey(self, message: Message):
        """Получить ссылку для генерации ключа"""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "Использование .generatekey <платформа>")
            return

        platform = args[0].lower()
        link = await self.get_link(platform)

        if link:
            await utils.answer(message, self.strings("link_response").format(link=link))
        else:
            await utils.answer(message, self.strings("link_error"))

    async def get_link(self, name: str):
        def generate_random_numeric_id(length=10):
            return ''.join(random.choices(string.digits, k=length))

        def generate_random_numeric_hwid(length=25):
            return ''.join(random.choices(string.digits, k=length))

        if name == 'delta':
            random_id = generate_random_numeric_id()
            return f'https://gateway.platoboost.com/a/8?id={random_id}'

        elif name == 'fluxus':
            random_hwid = generate_random_numeric_hwid()
            return f'https://flux.li/android/external/start.php?HWID={random_hwid}'

        elif name == 'arceus':
            random_id = generate_random_numeric_id()
            return f'https://spdmteam.com/key-system-1?hwid={random_id}&zone=Europe/Rome&os=android'

        elif name == 'vegax':
            random_hwid = generate_random_numeric_hwid()
            return f'https://pandadevelopment.net/getkey?service=vegax&hwid={random_hwid}&provider=linkvertise'

        elif name == 'trigon':
            random_hwid = generate_random_numeric_hwid()
            return f'https://trigonevo.com/getkey/?hwid={random_hwid}'

        elif name == 'hydrogen':
            random_id = generate_random_numeric_id()
            return f'https://gateway.platoboost.com/a/2569?id={random_id}'

        return None