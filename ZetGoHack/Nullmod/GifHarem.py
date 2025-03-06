__version__ = (1,0,3) ###Да, это -- копирка модуля HornyHarem. Я не виноват, что у разраба во всей связке ботов код одинаковый.🥰

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

from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.contacts import BlockRequest, UnblockRequest
from hikkatl.tl.functions.messages import ImportChatInviteRequest
from hikkatl.tl.types import Message
from .. import loader, utils
import asyncio
import time
import re

@loader.tds
class GifHarem(loader.Module):
    """Automatization module for @GIFgarem_bot"""

    strings = {
        "name": "GifHarem"
    }
    async def client_ready(self):
        self.state = False
        self.outptt = True
        self.bonus = False
        self.id = 7084965046
        self.last_time = 0
        self.lout = 0
        self.wait_boost = False

    ########Ловец########
    @loader.watcher("only_messages","only_media")
    async def watcher(self, message: Message):
        """Watcher"""
        if self.state and message.sender_id == self.id:
            text = message.text.lower()
            if "заблудилась" in text:
                if int(time.time()) - int(self.last_time) > 14400:
                    try:
                        await message.click()
                        msgs = await message.client.get_messages(message.chat_id, limit=4)
                        for msg in msgs:
                            if self.outptt and msg.mentioned and "забрали" in msg.text:

                                match = re.search(r", Вы забрали (.+?)\. Вайфу", msg.text)
                                waifu = match.group(1)
                                caption = f"{waifu} в вашем гареме! <emoji document_id=5395592707580127159>😎</emoji>"
                                await self.client.send_file(self.id, caption=caption, file=message.media)
                                self.last_time = time.time()
                    except Exception as e:
                        pass
                        
    @loader.command()
    async def catchGH(self, message):
        """Переключить режим ловли. Вывод арта украденной вайфу в лс бота"""
        self.state = not self.state
        await message.edit(f"{'<emoji document_id=5269315712685448697>👍</emoji> Я ловлю вайфу.' if self.state else '<emoji document_id=5269428966678077523>👎</emoji> Я не ловлю вайфу.'}")
    @loader.command()
    async def catchGH_output(self, message):
        """Переключить вывод арта украденной вайфу."""
        self.outptt = not self.outptt
        await message.edit(f"{'Я показываю вайфу.' if self.outptt else 'Я не показываю вайфу.'}")
    ########Ловец########


    ########Заработок########
    @loader.command()
    async def autobonusGH(self, message):
        """Автоматически собирает бонус(а также бонус за подписку и отыгрывает 3 игры в /lout) каждые 4 часа"""
        if self.bonus:
            self.bonus = False
            await message.edit("<emoji document_id=5388915455069015167>❎</emoji> Автобонус выключен.")
            return
        self.bonus = True
        await message.edit("<emoji document_id=5389003252790480195>✅</emoji> Автобонус включён.")
        while self.bonus:
            async with self._client.conversation(self.id) as conv:
                await conv.send_message("/bonus")
                r = await conv.get_response()
                if "Доступен бонус за подписки" in r.text:
                    await conv.send_message("/start flyer_bonus")
                    r = await conv.get_response()
                    if "проверка пройдена" not in r.text:
                        to_leave = []
                        to_block = []
                        if r.reply_markup:
                            a = r.buttons
                            for i in a:
                                for button in i:
                                    if button.url:
                                        if "t.me/boost?" in button.url:
                                            self.wait_boost = True
                                            continue
                                        if "t.me/+" in button.url:
                                            try:
                                                await self.client(ImportChatInviteRequest(button.url.split("+")[-1]))
                                            except:
                                                await asyncio.sleep(2)
                                                await self.client(JoinChannelRequest(button.url))
                                        url = button.url
                                        if "?" in button.url:
                                            url = button.url.split("?")[0]
                                        entity = await self.client.get_entity(url)
                                        if hasattr(entity,'broadcast'):
                                            await self.client(JoinChannelRequest(button.url))
                                            to_leave.append(entity.id)
                                        elif hasattr(entity,'bot'):
                                            try:
                                                await self.client(UnblockRequest(entity.username))
                                            except:
                                                print('блин')
                                            await self.client.send_message(entity,"/start")
                                            to_block.append(entity.username)
                            flyer_messages = await message.client.get_messages(self.id, limit=1)
                            if self.wait_boost:
                                await asyncio.sleep(120)
                            for m in flyer_messages:
                                await asyncio.sleep(5)
                                await m.click()
                            for bot in to_block:
                                await self.client(BlockRequest(bot))
                                await self.client.delete_dialog(bot)
                            for channel in to_leave:
                                await self.client(LeaveChannelRequest(channel))
                count = 0
                if time.time()-self.lout > 86400:
                    while count <= 3:
                        await conv.send_message("/lout")
                        r = await conv.get_response()
                        if r.reply_markup:
                            m = await r.respond(".")
                            await self.lightsoutW(m,r)
                            await m.delete()
                            self.lout = time.time()
                            count += 1
                        else:
                            break
            await asyncio.sleep(14400)

    @loader.command()
    async def lightsoutW(self, message, r=None):
        """[ответ на соо с полем] Автоматически решает Lights Out"""
        if message.is_reply or r:
            if not r: 
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
                await message.edit("<emoji document_id=5299030091735525430>❗️</emoji> Не вижу поля игры. Это точно то сообщение?")
                return
             
        else:
            await message.edit("<emoji document_id=5299030091735525430>❗️</emoji> Пропиши команду в ответ на игру.")
            return
        if pattern:
            await message.edit("<emoji document_id=5472146462362048818>💡</emoji>")
            clicks = await self.solution(pattern)
            if not clicks:
                await message.edit("Иди код трейси гений.")
                return #*смачный пинок кодеру под зад.*
            for i in range(len(clicks)):
                if clicks[i] == 1:
                    r = await self.client.get_messages(r.chat_id,ids=r.id)
                    await r.click(i)
            await message.edit("<emoji document_id=5395592707580127159>😎</emoji> Готово.")
        else:
            await message.edit("<emoji document_id=5299030091735525430>❗️</emoji> Ты ответил не на поле игры.")
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
