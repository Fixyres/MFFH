# scope: user
# meta developer: @Hikimuro
# ver: 2.0.0

from .. import loader, utils
import cloudscraper
import random
import logging
from bs4 import BeautifulSoup
import aiohttp
import os

logger = logging.getLogger(__name__)

AVAILABLE_CATEGORIES = [
    "Oral", "Vaginal", "Sex Toys", "Group",
    "Lesbian", "Handjob", "Futanari", "Porn", "Hentai",
    "Shemale", "Newhalf", "Footfetish", "Femdom", "Milf",
    "Anal", "Teen", "Bdsm", "Yaoi", "Yuri", "Guro"
]

@loader.tds
class FapReactorMod(loader.Module):
    """Отправляет случайное NSFW изображение с fapreactor.com по категории"""

    strings = {
        "name": "FapReactor",
        "no_category": "❌ Категория не установлена. Используй .setfapcategory <категория>",
        "not_found": "❌ Не удалось найти изображения.\n\nПричина: {}",
        "downloading": "🔍 Ищу изображение..."
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "category",
                "Porn",
                lambda: "Категория с fapreactor.com (доступные: {})".format(", ".join(AVAILABLE_CATEGORIES))
            )
        )
        self.scraper = cloudscraper.create_scraper()

    @loader.command()
    async def setfapcategory(self, message):
        """Устанавливает категорию (раздел)"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("⚠️ Укажи категорию.\nДоступные: " + ", ".join(AVAILABLE_CATEGORIES))
            return
        if args not in AVAILABLE_CATEGORIES:
            await message.edit(f"❌ Категория `{args}` недоступна.\nДоступные: {', '.join(AVAILABLE_CATEGORIES)}")
            return
        self.config["category"] = args
        await message.edit(f"✅ Категория установлена на: `{args}`")

    @loader.command()
    async def fap(self, message):
        """Отправляет рандомное NSFW изображение с fapreactor.com"""
        category = self.config["category"]
        if not category:
            await message.edit(self.strings("no_category"))
            return

        await message.edit(self.strings("downloading"))

        try:
            for _ in range(5):
                page = random.randint(1, 1000)
                url = f"https://fapreactor.com/tag/{category}/all/{page}"
                r = self.scraper.get(url, timeout=10)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, "html.parser")
                posts = soup.select("div.image > a > img")
                if posts:
                    break
            else:
                raise ValueError("Не найдено изображений после 5 попыток.")

            images = [img["src"] for img in posts if "src" in img.attrs]
            image_url = random.choice(images)
            if image_url.startswith("//"):
                image_url = "https:" + image_url

            temp_file = "fapreactor_image.jpg"

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Referer": "https://fapreactor.com/"
            }

            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(image_url) as resp:
                    if resp.status != 200:
                        raise ValueError(f"Ошибка загрузки изображения: {resp.status}")
                    data = await resp.read()
                    with open(temp_file, "wb") as f:
                        f.write(data)

            await message.client.send_file(message.chat_id, temp_file)
            await message.delete()
            os.remove(temp_file)

        except Exception as e:
            logger.exception("Ошибка при получении изображения с fapreactor")
            await message.edit(self.strings("not_found").format(str(e)))
