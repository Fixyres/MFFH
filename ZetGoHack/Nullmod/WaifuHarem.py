__version__ = (2,0,3)
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
# H:Mods Team [💎]


# meta developer: @nullmod

from hikkatl.tl.functions.chatlists import CheckChatlistInviteRequest, JoinChatlistInviteRequest, LeaveChatlistRequest
from hikkatl.tl.functions.messages import ImportChatInviteRequest, CheckChatInviteRequest
from hikkatl.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from hikkatl.tl.functions.contacts import BlockRequest, UnblockRequest
from hikkatl.tl.types import Message, InputChatlistDialogFilter, UpdateDialogFilter
from hikkatl.errors import YouBlockedUserError, InviteRequestSentError
from .. import loader
import asyncio
import time
import re


@loader.tds
class WaifuHarem(loader.Module):
    """Automatization module for @garem_chatbot"""
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ab",
                False,
                "Автобонус(/bonus, бонус за подписки, 'lights out')",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "interval",
                4,
                "Интервал между автобонусом",
                validator=loader.validators.Float(2.0)
            )
        )
    strings = {
        "name": "WaifuHarem"
    }
    async def client_ready(self):
        self.id = 6704842953
        self.blockBot = False
        
    def getmarkup(self):
        return [
                [
                    {
                        "text": "[✔️] Автобонус" if self.config["ab"] else "[❌] Автобонус", 
                        "callback": self.callback_handler,
                        "args": ("ab",)
                    }
                ],
                [
                    {
                        "text":"[➖] Автоловля",
                        "action":"answer",
                        "show_alert": True,
                        "message": "Довольно сложно даже самому угадать имя любого перса по одному арту. Если вы нашли совпадение в Google Lens, то теперь нужно угадать как разрабы придумали назвать этого персонажа в боте.."
                    },
                    {
                        "text":"[➖] Вывод вайфу", 
                        "action":"answer",
                        "show_alert": True,
                        "message": "может всю базу вайфу с гарема выкачать и так идти...?))"
                    }
                ],
                [
                    {
                        "text":"🔻 Закрыть меню", 
                        "callback":self.callback_handler,
                        "args": ("close",)
                    }
                ]
            ]

    ########loop########
    @loader.loop(interval=1, autostart=True)
    async def check_loop(self):
        if self.config["ab"]:
            if (not self.get("ABonus_time") or (time.time() - self.get("ABonus_time")) >= int(3600*self.config["interval"])):
                await self.autobonus()
                
    ########loop########

    ########Блок ботов########
    @loader.watcher("only_messages")
    async def watcher(self, message: Message):
        """Watcher"""
        if self.blockBot:
            bot = await self.client.get_entity(message.from_id)
            if bot.bot:
                botf = await self.client.get_fulluser(message.from_id)
                if botf.full_user.settings.request_chat_title is not None:
                    await self.client(BlockRequest(botf.users[0].id))
                    await self.client.delete_dialog(botf.users[0].id)
                    self.blockBot = False
                    return
                        


    ########Заработок########
    async def autobonus(self):
        wait_boost = False
        async with self._client.conversation(self.id) as conv:
            try:
                await conv.send_message("/bonus")
            except YouBlockedUserError:
                await self.client(UnblockRequest(self.id))
                await conv.send_message("/bonus")
            try:
                r = await conv.get_response()
            except:
                while True:
                    try:
                        r = await conv.get_response()
                        break
                    except:
                        pass
            self.set("ABonus_time", int(time.time()))
            if "Доступен бонус за подписки" in r.text:
                await conv.send_message("/start flyer_bonus")
                try:
                    r = await conv.get_response()
                except:
                    while True:
                        try:
                            r = await conv.get_response()
                            break
                        except:
                            pass
                if "проверка пройдена" not in r.text:
                    to_leave, to_block, folders, chats_in_folders = [], [], [], []
                    wait_boost = False
                    if r.reply_markup:
                        a = r.buttons
                        for i in a:
                            for button in i: # каждая кнопка...
                                if button.url:
                                    alr = False # "уже зашёл"
                                    if "addlist/" in button.url: # добавление папок
                                        slug = button.url.split("addlist/")[-1]
                                        peers = await self.client(CheckChatlistInviteRequest(slug=slug))
                                        if peers:
                                            peers = peers.peers
                                            try:
                                                a = await self.client(JoinChatlistInviteRequest(slug=slug, peers=peers))
                                                chats_in_folders.append(peers) # для выхода
                                                for update in a.updates:
                                                    if isinstance(update, UpdateDialogFilter):
                                                        folder.append(InputChatlistDialogFilter(filter_id=update.id)) # для удаления папки
                                            except: pass
                                        continue
                                    if "t.me/boost" in button.url: # бустить не обязательно
                                        wait_boost = True
                                        continue
                                    if not bool(re.match(r"^https?:\/\/t\.me\/[^\/]+\/?$", button.url)): # дополнительные вложения отметаем
                                        continue
                                    if "t.me/+" in button.url: # приватные чаты
                                        try:
                                            a = await self.client(CheckChatInviteRequest(button.url.split("+")[-1]))
                                            if not hasattr(a, "request_needed") or not a.request_needed: # получить айди приватного чата/канала с приглашениями без входа невозможно
                                                pass
                                            else:
                                                url = button.url.split("?")[0] if "?" in button.url else button.url
                                                self.blockBot = True ######
                                                try:
                                                    await self.client(ImportChatInviteRequest(button.url.split("+")[-1]))
                                                except InviteRequestSentError: pass
                                                await asyncio.sleep(3)
                                                try:
                                                    entity = await self.client.get_entity(url)
                                                except ValueError:
                                                    try:
                                                        await asyncio.sleep(15)
                                                        entity = await self.client.get_entity(url)
                                                    except: 
                                                        self.blockBot = False
                                                        continue
                                                except:
                                                    pass
                                                self.blockBot = False
                                                alr = True
                                        except: continue
                                    url = button.url.split("?")[0] if "?" in button.url else button.url
                                    if not alr:
                                        try:
                                            entity = await self.client.get_entity(url)
                                        except:
                                            entity = (await self.client(ImportChatInviteRequest(button.url.split("+")[-1]))).chats[0] #gotten class Updates
                                            alr = True
                                    if hasattr(entity, "broadcast"):
                                        if not alr:
                                            await self.client(JoinChannelRequest(button.url))
                                            to_leave.append(entity.id)
                                        else:
                                            to_leave.append(entity.chat.id) if hasattr(entity,"chat") else to_leave.append(entity.id) if hasattr(entity,"id") else None
                                    elif hasattr(entity, "bot"):
                                        try:
                                            await self.client(UnblockRequest(entity.username))
                                        except: print("блин")
                                        await self.client.send_message(entity, "/start")
                                        to_block.append(entity.username)
                        flyer_messages = await self.client.get_messages(self.id, limit=1)
                        if wait_boost:
                            await asyncio.sleep(150)
                        for m in flyer_messages:
                            await asyncio.sleep(5)
                            await m.click()
                            await asyncio.sleep(5)
                        for folder, chats in zip(folders, chats_in_folders):
                            await self.client(LeaveChatlistRequest(peers=chats, chatlist=folder))
                        for bot in to_block:
                            await self.client(BlockRequest(bot))
                            await self.client.delete_dialog(bot)
                        for channel in to_leave:
                            try:
                                await self.client(LeaveChannelRequest(channel))
                            except Exception as e:
                                pass
                count = 0
                if not self.get("last_lout") or int(time.time()) - self.get("last_lout") > 43200:
                    while count <= 2:
                        await conv.send_message("/lout")
                        try:
                            r = await conv.get_response()
                        except:
                            while True:
                                try:
                                    r = await conv.get_response()
                                    break
                                except:
                                    pass
                        if r.reply_markup:
                            m = await r.respond(".")
                            await self.lightsoutW(m,r)
                            await m.delete()
                            self.set("last_lout", int(time.time()))
                            count += 1
                        else:
                            break
    @loader.command()
    async def WaifuMenu(self,message):
        """Меню конфигурации"""
        self.call = await self.inline.form(
            message = message, 
            text = "Меню для @garem_chatbot", 
            reply_markup = self.getmarkup()
        )

    async def callback_handler(self, callback, data):
        if data == "close":
            await self.call.edit(text="Меню закрыто.")
        elif data:
            self.config[data] = not self.config[data]
            if data == "ab":
                self.check_loop.start() if self.config[data] else self.check_loop.stop()
            await callback.edit(reply_markup=self.getmarkup())
        

    
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