from .. import loader, utils
import requests
import os

@loader.tds
class OfftopTextMod(loader.Module):
    """Обход в оффтопе хикки"""

    strings = {
        "name": "Обход",
        "no_text": "Напиши сообщение",
        "sending": "загрузочка...",
        "sent": "Отправлено"
    }

    async def oftcmd(self, message):
        """Отправить сообщение"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_text"])
            return

        await utils.answer(message, self.strings["sending"])
        
        voice_url = "https://0x0.st/s/F0y1vcZGlqTKHj8z0ooT2Q/XFVC.oga"
        voice_path = "voice.oga"
        
        response = requests.get(voice_url)
        with open(voice_path, "wb") as f:
            f.write(response.content)
            
        chat = await self.client.get_entity("@hikka_offtop")
        
        await self.client.send_file(
            chat,
            voice_path,
            voice_note=True,
            caption=args
        )
        
        os.remove(voice_path)
        await utils.answer(message, self.strings["sent"])
