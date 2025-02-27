#░░░░░░░░░░░░░░░░░░░░░░
#░░░░░░░░░░██░░██░░░░░░
#░░░░░░░░░████████░░░░░
#░░░░░░░░░████████░░░░░
#░░░░░░░░░░██████░░░░░░
#░░░░░░░░░░░░██░░░░░░░░
#░░░░░░░░░░░░░░░░░░░░░░
#░░░░░░░░░█▔█░░█░█░░░░░
#░░░░░░░░░██░░░░█░░░░░░
#░░░░░░░░░█▁█░░░█░░░░░░
#░░░░░░░░░░░░░░░░░░░░░░
#░░░███░███░███░███░███
#░░░░░█░█░░░░█░░█░░░█░█
#░░░░█░░███░░█░░█░█░█░█
#░░░█░░░█░░░░█░░█░█░█░█
#░░░███░███░░█░░███░███



# meta developer: @nullmod

from hikkatl.tl.types import Message
from .. import loader, utils
import asyncio
import time


@loader.tds
class HornyHaremModule(loader.Module):
    """Automatization module for @Horny_GaremBot"""

    strings = {
        "name": "HornyHarem"
    }
    async def client_ready(self):
        self.state = False
        self.outptt = True
        self.bonus = False
        me = await self._client.get_me()
        self.id = 7896566560
        self.last_time = 0

    ########Ловец########
    @loader.watcher("only_messages","from_id=7896566560","only_media")
    async def watcher(self, message: Message):
        """Watcher"""
        if self.state:
            text = message.text.lower()
            if "заблудилась" in text:
                if int(time.time()) - int(self.last_time) > 14400:
                    try:
                        await message.click()
                        if self.outptt:
                            await self.client.send_file(self.id, caption="Украл", file=message.media)
                        self.last_time = time.time()
                    except Exception as e:
                        await self.client.send_message(self.id, f"Ошибка нажатия: {e}")
                        
    @loader.command()
    async def catchW(self, message):
        """Переключить режим ловли. Вывод арта украденной вайфу в лс бота"""
        self.state = not self.state
        await message.edit(f"{'Я ловлю вайфу' if self.state else 'Я не ловлю вайфу'}")
    @loader.command()
    async def catchW_output(self, message):
        """Переключить вывод арта украденной вайфу."""
        self.outptt = not self.outptt
        await message.edit(f"{'Я показываю вайфу' if self.outptt else 'Я не показываю вайфу'}")
    ########Ловец########


    ########Заработок########
    @loader.command()
    async def autobonusW(self, message):
        """Автоматически собирает бонус каждые 4 часа"""
        if self.bonus:
            self.bonus = False
            await message.edit("Автобонус выключен.")
            return
        self.bonus = True
        await message.edit("Автобонус включён.")
        while self.bonus:
            await self.client.send_message(7896566560,"/bonus")
            await asyncio.sleep(14400)

    @loader.command()
    async def lightsoutW(self, message):
        """[ответ на соо с полем] Автоматически решает Lights Out"""
        if message.is_reply:
            r = await message.get_reply_message()
            if r.reply_markup:
                a = r.buttons
                pattern = []
                for i in a:
                    for m in i:
                        t = m.text
                        if t == "🌚":
                            pattern.append(0)
                        elif t == "🌞":
                            pattern.append(1)
                        else:
                            None
            else:
                await message.edit("Не вижу поля игры. Это точно то сообщение?")
                return
             
        else:
            await message.edit("Пропиши команду в ответ на игру.")
            return
        if pattern:
            await message.edit("<emoji document_id=5472146462362048818>💡</emoji>")
            clicks = solution(pattern)
            if not clicks:
                await message.edit("Иди код трейси гений.")
                return #*смачный пинок кодеру под зад.*
            await message.edit("Решение найдено.")
            for i in len(clicks):
                if clicks[i-1] == 1:
                    r = await client.get_messages(r.chat_id,ids=r.id)
                    await r.click(i-1)
            await message.edit("Готово.")
        else:
            await message.edit("Ты ответил не на поле игры.")
            return
    #///|
    #///|
    #///|
    #///˅
    async def solution(self, pole):
        n = len(pole)
        for num in range(2**n):
            binary_string = bin(num)[2:].zfill(n)
            presses = [int(char) for char in binary_string]
            temp = pole[:]
        
            for i in range(n):
                if presses[i]:
                    temp[i] ^= 1
                    if i % 3 > 0: temp[i - 1] ^= 1
                    if i % 3 < 2: temp[i + 1] ^= 1
                    if i >= 3: temp[i - 3] ^= 1
                    if i < 6: temp[i + 3] ^= 1
        
            if sum(temp) == 0:
                return presses

        return None
    ########Заработок########
