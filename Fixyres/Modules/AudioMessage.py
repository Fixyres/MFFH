from .. import loader, utils
from telethon.tl.types import DocumentAttributeAudio
import os

@loader.tds
class AudioMessageMod(loader.Module):
    """Модуль для отправки аудиосообщений с визуальной длительностью"""
    strings = {"name": "AudioMessage"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.command()
    async def audiomsg(self, message):
        """<длительность:часы> - отправляет аудиосообщение длительностью <длительность> часов (визуально)"""
        args = utils.get_args_raw(message).split()
        if len(args) < 1:
            await message.edit("Укажи длительность в часах.")
            return
        
        try:
            hours = int(args[0])
            duration = hours * 3600  # Преобразование часов в секунды
        except ValueError:
            await message.edit("Укажи корректную длительность в часах.")
            return

        reply = await message.get_reply_message()
        if not reply or not reply.file:
            await message.edit("Пожалуйста, ответьте на сообщение с файлом.")
            return

        # Получаем путь к файлу
        file = await message.client.download_media(reply.media)

        attributes = [DocumentAttributeAudio(duration=duration, voice=True)]
        
        await self.client.send_file(message.to_id, file, voice_note=True, attributes=attributes)
        
        # Удаляем временный файл
        os.remove(file)
        
        await message.edit(f"Отправлено аудиосообщение длительностью {hours} часов (визуально).")
