from .. import loader, utils
import requests

__version__ = (1, 0, 0)
# meta developer: @kmodules

male = "<emoji document_id=5999325196543071034>🖤</emoji>"
female = "<emoji document_id=5996979985485665124>❤️‍🔥</emoji>"
unknown = "<emoji document_id=5996716235838985244>🩵</emoji>"

@loader.tds
class GenderGuesserMod(loader.Module):
    """Узнать примерный гендеор пользователя"""

    strings = {
        "name": "GenderGuesser",
        "thinking": "<emoji document_id=5307675706283533118>🫥</emoji> <b>Думаю о гендере {}</b>...",
        "result": "<emoji document_id=5879770735999717115>👤</emoji> <b>Примерный гендер {}</b>:\n\n{} <b>{}</b>",
        "need_args": "<b>Укажите имя</b>"
    }

    strings_ru = {
        "name": "GenderGuesser",
        "thinking": "<emoji document_id=5307675706283533118>🫥</emoji> <b>Думаю о гендере {}</b>...", 
        "result": "<emoji document_id=5879770735999717115>👤</emoji> <b>Примерный гендер {}</b>:\n\n{} <b>{}</b>",
        "need_args": "<b>Укажите имя</b>"
    }
    



    @loader.command()
    async def gender(self, message):
        """Примерный гендер по username/reply
        Пример: .gender @username or reply"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        
        if not reply and not args:
            return await message.edit("<b>❗ Нужен юзернейм или репли!</b>")
            
        if reply:
            user = await reply.get_sender()
            name = user.first_name
        else:
            user = await self._client.get_entity(args)
            name = user.first_name
            
        await message.edit(self.strings["thinking"].format(name))
        
        response = requests.get(f"https://api.genderize.io?name={name}")
        result = response.json()
        
        if result["gender"] == "female":
            emoji = female
            gender = "Женщина"
        elif result["gender"] == "male":
            emoji = male
            gender = "Мужчина"
        else:
            emoji = unknown
            gender = "Неизвестно"
            
        await message.edit(
            self.strings["result"].format(
                name,
                emoji,
                gender
            )
        )

    @loader.command()
    async def gendername(self, message):
        """Примерный гендер по имени.
        Пример: .gendername Максим"""
        args = utils.get_args_raw(message)
        
        if not args:
            return await message.edit(self.strings["need_args"])
            
        await message.edit(self.strings["thinking"].format(args))
        
        response = requests.get(f"https://api.genderize.io?name={args}")
        result = response.json()
        
        if result["gender"] == "female":
            emoji = female
            gender = "Женщина"
        elif result["gender"] == "male":
            emoji = male
            gender = "Мужчина"
        else:
            emoji = unknown
            gender = "Неизвестно"
            
        await message.edit(
            self.strings["result"].format(
                args,
                emoji,
                gender
            )
        )
      
