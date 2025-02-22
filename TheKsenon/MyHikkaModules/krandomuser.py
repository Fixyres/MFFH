from .. import loader, utils
import requests

__version__ = (1, 0, 0)
# meta developer: @kmodules

@loader.tds
class RandomUserMod(loader.Module):
    """Генератор случайных пользовательских данных."""

    strings = {
        "name": "K:RandomUser",
        "error": "Error occurred while fetching data",
    }
    
    strings_ru = {
        "name": "K:RandomUser", 
        "error": "Произошла ошибка при получении данных"
    }

    @loader.command()
    async def randuser(self, message):
        """Сгенерировать случайные данные"""
        try:
            response = requests.get('https://randomuser.me/api/')
            data = response.json()['results'][0]
            
            text = (
                f"<emoji document_id=5251752131123234530>🔥</emoji> <b>Сгенерированные данные:</b>\n\n"
                f"<emoji document_id=5251429849662243654>🦋</emoji><b> Пол:</b> {data['gender']}\n\n"
                f"<emoji document_id=5251705066871603418>⚡️</emoji><b> Имя:</b> {data['name']['first']}\n"
                f"<emoji document_id=5251270514965496574>🕊</emoji><b> Фамилия:</b> {data['name']['last']}\n"
                f"<emoji document_id=5251722139366606502>💼</emoji><b> Город:</b> {data['location']['city']}\n"
                f"<emoji document_id=5248953835375844296>💡</emoji><b> Страна:</b> {data['location']['country']}\n"
                f"<emoji document_id=5251571901410592268>🎮</emoji><b> Пост-код:</b> {data['location']['postcode']}\n"
                f"<emoji document_id=5249326449558570589>🐐</emoji><b> Координаты:</b> {data['location']['coordinates']['latitude']}, {data['location']['coordinates']['longitude']}\n\n"
                f"<emoji document_id=5251358557500098290>💙</emoji><b> Юзернейм:</b> @{data['login']['username']}\n"
                f"<emoji document_id=5251703937295207873>❤️</emoji><b> Номер:</b> {data['phone']}\n"
                f"<emoji document_id=5251578932272056912>🔇</emoji><b> Почта:</b> {data['email']}\n"
                f"<emoji document_id=5249346451221267681>🐈</emoji><b> Пароль:</b> {data['login']['password']}"
            )
            
            await utils.answer(message, text)
            
        except Exception:
            await utils.answer(message, self.strings["error"])
          
