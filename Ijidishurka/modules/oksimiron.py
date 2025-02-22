# meta developer: @modwini
from .. import loader
from asyncio import sleep


@loader.tds
class rap(loader.Module):
    strings = {"name": "Реп оксимирона"}

    @loader.owner
    async def rapcmd(self, message):
        for _ in range(1):
            for rap in ["Говно", "залупа", "пенис", "хер", "давалка", "хуй", "блядина",
"Головка", "шлюха", "жопа", "член", "еблан", "петух…", "Мудила",
"Рукоблуд", "ссанина", "очко", "блядун", "вагина",
"Сука", "ебланище", "влагалище", "пердун", "дрочила",
"Пидор", "пизда", "туз", "малафья",
"Гомик", "мудила", "пилотка", "манда"
"Анус", "вагина", "путана", "педрила",
"Шалава", "хуило", "мошонка", "елда…",
"Раунд!"]:
                await message.edit(rap)
                await sleep(0.3)
