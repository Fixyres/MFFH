__version__ = (1,1,2)
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
#H:Mods Team [💎]


# meta developer: @nullmod
# requires: python-chess
from hikkatl.tl.types import PeerUser
import asyncio, random, chess, time
from .. import loader, utils

#######Таймер#######
class Timer:#еее мой первый класс
    def __init__(self, scnds):#start
        self.timers = {"white": scnds, "black": scnds}
        self.running = {"white": False, "black": False}
        self.started = {"white": False, "black": False}
        self.last_time = time.monotonic()#Monotonic clock, cannot go backward
        self.t = None
    async def count(self):#func
        while True:
            await asyncio.sleep(0.1)
            now = time.monotonic()
            elapsed = now - self.last_time
            self.last_time = now
            for color in ("white", "black"):
                if self.running[color]:
                    self.timers[color] = max(0, self.timers[color] - elapsed)#нам не надо в минус уходить

    async def start(self): ##to use
        self.last_time = time.monotonic()
        self.t = asyncio.create_task(self.count())

    async def white(self): ##to use
        await self.turn("white")
        self.started["white"] = True
        self.started["black"] = False

    async def black(self): ##to use
        await self.turn("black")
        self.started["white"] = False
        self.started["black"] = True

    async def turn(self, color):#func
        now = time.monotonic()
        e = now - self.last_time
        self.last_time = now
        for clr in ("white", "black"):
            if self.running[clr]:
                self.timers[clr] = max(0, self.timers[clr] - e)
        self.running = {"white": color == "white", "black": color == "black"}

    async def white_time(self): ##to use
        return round(self.timers["white"], 0)

    async def black_time(self): ##to use
        return round(self.timers["black"], 0)

    async def stop(self): ##to use#а вдруг понадобится 
        if self.t:
            self.t.cancel()
        self.running = {"white": False, "black": False}
        self.timers = {"white": self.timers["white"], "black": self.timers["black"]}
        self.started = {"white": False, "black": False}

    async def clear(self): ##to use
        if self.t:
            self.t.cancel()
        self.timers = {"white": 0, "black": 0}
        self.running = {"white": False, "black": False}
        self.started = {"white": False, "black": False}
        self.t = None
    #######Таймер#######

@loader.tds
class Chess(loader.Module):
    """Шахматы для игры вдвоём."""
    strings = {
        "name": "Chess"
    }
    #####Переменные#####

    async def client_ready(self):
        self.board = {}
        self.style1 = {
            "r": "♜", "n": "♞", "b": "♝", "q": "𝗾", "k": "♚", "p": "♟",
            "R": "♖", "N": "♘", "B": "♗", "Q": "𝗤", "K": "♔", "P": "♙",
        }
        self.style2 = {
            "r": "♖⚫", "n": "♘⚫", "b": "♗⚫", "q": "♕⚫", "k": "♔⚫", "p": "♙⚫",
            "R": "♖⚪", "N": "♘⚪", "B": "♗⚪", "Q": "♕⚪", "K": "♔⚪", "P": "♙⚪",
        }
        self.chsn = False
        self.saymyname = (await self.client.get_me()).first_name
        self.reverse = False
        self.timeName = "❌ Без часов"
        self.pTime = None
        self.colorName = "рандом"
        self.you_play = None
        self.timer = False
        self.Timer = None
        self.loopState = False
        self.game = False
        self.reason = False
        self.style = self.style1

    async def purgeSelf(self):
        self.board = {}
        self.chsn = False
        self.reverse = False
        self.Board = None
        self.you_play = None
        self.you_n_me = []
        self.places = []
        self.message = None
        self.opp_id = None
        self.opp_name = None
        self.checkmate = False
        self.stalemate = False
        self.timeName = "❌ Нет часов"
        self.pTime = None
        self.colorName = "рандом"
        if self.Timer:
            await self.Timer.clear()
        self.timer = False
        if self.Timer:
            self.Timer = None
        if hasattr(self,"time_message"):
            del self.time_message
        self.loopState = False
        self.game = False
        self.reason = False

    #####Переменные#####


    #####Игра#####
        #####Настройки#####
    async def settings(self, call, nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Настройки не для вас!")
            return  
        await call.edit(
            text=f"[⚙️] Настройки этой партии\n| - > Хост играет за {self.colorName} цвет\n| - > Время: {self.timeName}\n| - > Стиль: #{1 if self.style == self.style1 else 2}",
            reply_markup=[
                [
                    {"text":f"⏱️ Время: {self.timeName}","callback":self.time, "args":(nT,)} if not nT else {"text":f"❌ Время: ...","action":"answer","show_alert":True,"message":"Приглашение находится в чате.\n\nИз-за ограничений для ботов, партии на время могут проводиться только в лс"}
                ],
                [
                    {"text":f"♟️ Цвет (хоста): {self.colorName}","callback":self.color, "args":(nT,)}
                ],
                [
                    {"text":f"🎛️ Стиль доски: #{1 if self.style == self.style1 else 2}","callback":self._style, "args":(nT,)}
                ],
                [
                    {"text":"⤴️ Вернуться","callback":self.backToInvite, "args":(nT,)}
                ]
            ]
        )

    async def backToInvite(self,call,nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Это не для вас!")
            return
        await call.edit(text = f"<a href='tg://user?id={self.opp_id}'>{self.opp_name}</a>, вас пригласили сыграть партию шахмат, примите?\n-- --\n[⚙️] Текущие настройки:\n| - > • Хост играет за {self.colorName} цвет\n| - > • Время: {self.timeName}\n| - > • Стиль: #{1 if self.style == self.style1 else 2}", 
                               reply_markup = [
                                   [
                                       {"text": "Принимаю", "callback": self.ans, "args":("y",)},
                                       {"text": "Нет", "callback": self.ans, "args":("n",)}
                                   ],
                                   [
                                       {"text": "⚙️ Настройки", "callback": self.settings, "args":(nT,)}
                                   ],
                                   [
                                       {"text": "❗ ВАЖНО","action":"answer","show_alert":True,"message":"В игре фигуры показаны ASCII-символами, но в тёмной теме их трудно различить, особенно '♕' и '♛'.\n\nДля удобства они были заменены на Q (бел) и q (чёрн).",}
                                   ]
                               ]
                       )

    async def time(self, call, nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Настройки не для вас!")
            return
        await call.edit(
            text=f"• Настройки этой партии.\n| - > [⏱️] Время: {self.timeName}",
            reply_markup=[
                [
                    {"text":"⚡ Блиц","action":"answer","message":"Блиц-Блиц - скорость без границ"}
                ],
                [
                    {"text":"3 минуты","callback":self.time_handle,"args":(3,"3 минуты",nT,)},
                    {"text":"5 минут","callback":self.time_handle,"args":(5,"5 минут",nT,)}
                ],
                [
                    {"text":"⏱️ Рапид","action":"answer","message":"Обдумай своё поражение"}
                ],
                [
                    {"text":"10 минут","callback":self.time_handle,"args":(10,"10 минут",nT,)},
                    {"text":"15 минут","callback":self.time_handle,"args":(15,"15 минут",nT,)},
                    {"text":"30 минут","callback":self.time_handle,"args":(30,"30 минут",nT,)},
                    {"text":"60 минут","callback":self.time_handle,"args":(60,"60 минут",nT,)}
                ],
                [
                    {"text":"❌ Нет часов", "callback":self.time_handle,"args":(None,"❌ Нет часов",nT,)}
                ],
                [
                    {"text":"⤴️ Обратно к настройкам", "callback":self.settings, "args":(nT,)}
                ]
            ]
        )
    async def time_handle(self,call,minutes,txt,nT):
        self.timeName = txt
        self.pTime = minutes*60
        await self.time(call,nT)

    async def color(self,call,nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Настройки не для вас!")
            return
        await call.edit(
            text=f"• Настройки этой партии.\n| - > [♟️] Хост играет за: {self.colorName} цвет.\nВыберите цвет его фигур",
            reply_markup=[
                [
                    {"text":"✅ Белые" if self.you_play == "w" else "❌ Белые","callback":self.color_handle,"args":("w","белый",nT,)},
                    {"text":"✅ Чёрные" if self.you_play == "b" else "❌ Чёрные","callback":self.color_handle,"args":("b","чёрный",nT,)}
                ],
                [
                    {"text":"🎲 Рандом" if not self.you_play else "❌ Рандом", "callback":self.color_handle,"args":(None,"рандом",nT)}
                ],
                [
                    {"text":"⤴️ Обратно к настройкам", "callback":self.settings, "args":(nT,)}
                ]
            ]
        )

    async def color_handle(self,call,color,txt,nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Настройки не для вас!")
            return
        self.colorName = txt
        self.you_play = color
        await self.color(call,nT)

    async def _style(self, call, nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Настройки не для вас!")
            return
        await call.edit(
            text=f"• Настройки этой партии.\n| - > [🎛️] Текущий стиль доски: #{1 if self.style == self.style1 else 2} цвет.\nВыберите стиль доски",
            reply_markup=[
                [
                    {"text":("✅ " if self.style == self.style1 else "❌ ") + "Стиль #1", "callback":self._show_style,"args":(1,nT,)},
                    {"text":("✅ " if self.style != self.style1 else "❌ ") + "Стиль #2", "callback":self._show_style,"args":(2,nT,)}
                ],
                [
                    {"text":"⤴️ Обратно к настройкам", "callback":self.settings, "args":(nT,)}
                ]
            ]
        )
    async def _show_style(self, call, style, nT):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Настройки не для вас!")
            return
        self.style = self.style1 if style == 1 else self.style2
        self.Board = chess.Board()
        btns = []
        # - - -
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                piece = self.Board.piece_at(chess.parse_square(coord.lower()))
                self.board[coord] =  self.style[piece.symbol()] if piece else " "
        # - - -
        self.Board = None
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                rows.append({"text": f"{self.board[f'{col}{row}']}", "action":"answer", "message":"😨 Вот это фигура, да?"})
            btns.append(rows)
        btns = btns[::-1]
        self.board = {}
        btns.append([{"text":"⤴️ Назад", "callback":self._style, "args":(nT,)}])
        await call.edit(text=f"🎛️ Выбран стиль: #{1 if self.style == self.style1 else 2}\n\nВот как он выглядит",reply_markup=btns)
        
        #####Настройки#####


    @loader.command() 
    async def chess(self, message):
        """[reply/username/id] предложить человеку сыграть партию в чате"""
        if self.board:
            await message.edit("<emoji document_id=5370724846936267183>🤔</emoji> Партия уже где-то запущена. Завершите или сбросьте её с <code>purgegame</code>")
            return
        await self.purgeSelf()#настройки мне тут не обходите ага
        self.message = message
        self.message_chat = message.chat_id
        noTimer = False
        if not isinstance(message.peer_id,PeerUser):
            noTimer = True
        if message.is_reply:
            r = await message.get_reply_message()
            opponent = r.sender
            self.opp_id = opponent.id
            self.opp_name = opponent.first_name
        else:
            args = utils.get_args(message)
            if len(args)==0:
                await message.edit("<emoji document_id=5370724846936267183>🤔</emoji> Вы не указали с кем играть")
                return
            opponent = args[0]
            try:
                if opponent.isdigit():
                    self.opp_id = int(opponent)
                    opponent = await self.client.get_entity(self.opp_id)
                    self.opp_name = opponent.first_name
                else:
                    opponent = await self.client.get_entity(opponent)
                    self.opp_name = opponent.first_name
                    self.opp_id = opponent.id
            except:
                await message.edit("❌ Я не нахожу такого пользователя")
                return
        if self.opp_id == self.message.sender_id:
            await message.edit("<emoji document_id=5384398004172102616>😈</emoji> Одиночные шахматы? Простите, нет.")
            return
        self.you_n_me = [self.opp_id, self.message.sender_id]
        await self.inline.form(message = message, text = f"<a href='tg://user?id={self.opp_id}'>{self.opp_name}</a>, вас пригласили сыграть партию шахмат, примите?\n-- --\n[⚙️] Текущие настройки:\n| - > • Хост играет за {self.colorName} цвет\n| - > • Время: {self.timeName}\n| - > • Стиль: #{1 if self.style == self.style1 else 2}", 
                               reply_markup = [
                                   [
                                       {"text": "Принимаю", "callback": self.ans, "args":("y",)},
                                       {"text": "Нет", "callback": self.ans, "args":("n",)}
                                   ],
                                   [
                                       {"text": "⚙️ Настройки", "callback": self.settings, "args":(noTimer,)}
                                   ],
                                   [
                                       {"text": "❗ ВАЖНО","action":"answer","show_alert":True,"message":"В игре фигуры показаны ASCII-символами, но в тёмной теме их трудно различить, особенно '♕' и '♛'.\n\nДля удобства они были заменены на Q (бел) и q (чёрн) в первом стиле.",}
                                   ]
                               ], 
                               disable_security = True, on_unload=self.outdated()
        )
    @loader.command() 
    async def purgeGame(self, message):
        """Грубо завершить партию, очистив ВСЕ связанные с ней данные"""
        await self.purgeSelf()
        await message.edit("Данные очищены")

    async def ans(self, call, data):
        if call.from_user.id == self.message.sender_id:
            await call.answer("Дай человеку ответить!")
            return
        if call.from_user.id not in self.you_n_me:
            await call.answer("Не тебе предлагают ж")
            return
        if data == 'y':
            self.Board = chess.Board()
            if not self.you_play:
                await call.edit(text="Выбираю стороны...")
                await asyncio.sleep(0.5)
                self.you_play = self.ranColor()
            text = await self.sttxt()
            await call.edit(text="Загрузка доски...")
            await asyncio.sleep(0.5)
            if self.pTime:
                await call.edit(text="Ставлю таймеры...")
                self.Timer = Timer(self.pTime)
                self.timer = True
                self.brd = call
                await asyncio.sleep(0.5)
            else:
                self.game = True    
            await call.edit(text="[!] Для лучшего различия фигур включите светлую тему!")
            await asyncio.sleep(2.5)
            await self.LoadBoard(text, call)
        else:
            await call.edit(text="Отклонено.")

    #####Игра#####

    #####Таймер#####
    async def start_timer(self,call):
        if call.from_user.id not in self.you_n_me:
            await call.answer("Партия не ваша!")
            return
        await self.Timer.start()    
        self.time_message = call
        self.TimerLoop.start()
        self.loopState = True
        self.game = True

    @loader.loop(interval=1)
    async def TimerLoop(self):
        if self.loopState:
            await self.time_message.edit(text=f"♔ Белые: {int(await self.Timer.white_time())}\n♚ Чёрные: {int(await self.Timer.black_time())}")
            t = await self.sttxt()
            if not self.timer and self.Timer:
                await self.LoadBoard(t,self.brd)

    #####Таймер#####

    #####Доска#####

    async def LoadBoard(self, text, call):
        if self.timer:
            if not hasattr(self,'time_message'):
                m = await self.client.send_message(self.message_chat,"Настройка таймера...")
                await self.inline.form(message=m,text=f"♔ Белые: {await self.Timer.white_time()}\n♚ Чёрные: {await self.Timer.black_time()}\n⏳ Начнём?",reply_markup=[{"text":"Начать партию", "callback":self.start_timer}],disable_security=True)

        elif self.Timer:
            self.loopState = False
            await self.time_message.edit(text=f"♔ Белые: {int(await self.Timer.white_time())}\n♚ Чёрные: {int(await self.Timer.black_time())}\n❌ Остановлен по причине: {self.reason}")
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                piece = self.Board.piece_at(chess.parse_square(coord.lower()))
                self.board[coord] =  self.style[piece.symbol()] if piece else " "



        btns = []
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                rows.append({"text": f"{self.board[f'{col}{row}']}", "callback": self.clicks_handle, "args":(coord,)})
            btns.append(rows)

        await call.edit(text = text,
            reply_markup = btns[::-1],
            disable_security = True
        )

    async def UpdBoard(self, call):
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                for place in self.places:
                    if place[2:4] == coord.lower():
                        if len(place) == 5:
                            self.board[coord] = "×↻" if (move := next((chess.Move.from_uci(p) for p in self.places if p[2:4] == coord.lower()), None)) and self.Board.is_capture(move) else "↻"
                        else:
                            self.board[coord] = "×" if (move := next((chess.Move.from_uci(p) for p in self.places if p[2:4] == coord.lower()), None)) and self.Board.is_capture(move) else "●"
                        break
                       
                    else:
                        piece = self.Board.piece_at(chess.parse_square(coord.lower()))
                        self.board[coord] =  self.style[piece.symbol()] if piece else " "

        text = await self.sttxt()  
        btns = []
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                rows.append({"text": f"{self.board[f'{col}{row}']}", "callback": self.clicks_handle, "args":(coord,)})
            btns.append(rows)

        await call.edit(text = text,
            reply_markup = btns[::-1],
            disable_security = True
        )


    #####Доска#####
    
    #####Функи#####(для будующей оптимизации кода)
    async def drawBoard(self):
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                for place in self.places:
                    if place[2:4] == coord.lower():
                        if len(place) == 5:
                            self.board[coord] = "×↻" if (move := next((chess.Move.from_uci(p) for p in self.places if p[2:4] == coord.lower()), None)) and self.Board.is_capture(move) else "↻"
                        else:
                            self.board[coord] = "×" if (move := next((chess.Move.from_uci(p) for p in self.places if p[2:4] == coord.lower()), None)) and self.Board.is_capture(move) else "●"
                        break
                       
                    else:
                        piece = self.Board.piece_at(chess.parse_square(coord.lower()))
                        self.board[coord] =  self.style[piece.symbol()] if piece else " "
        return
       
         
    async def moveTo(s,ca,c):
        s.Board.push(chess.Move.from_uci(c))
        s.reverse = not s.reverse
        s.chsn = False
        t = await s.sttxt()
        await s.LoadBoard(t,ca)
            
    
    #####Функи#####

    #####Ходы#####
    
    async def choose_figure(self,p,c):
        text = await self.sttxt()  
        btns = []
        await self.drawBoard()
        for row in range(1,9):
            rows = []
            for col in "ABCDEFGH":
                coord = f"{col}{row}"
                rows.append({"text": f"{self.board[f'{col}{row}']}", "action":"answer", "message":"Вы не можете ходить, пока не будет сделан выбор","show_alert":True})
            btns.append(rows)
        p = p[0:4]
        btns = btns[::-1]
        btns.append([{"text":"⬇️↻⬇️", "action":"answer", "message":"Выберите фигуру для превращения"}])
        btns.append([{"text":"♛","callback":self.are_u,"args":(p+"q",)},{"text":"♜","callback":self.are_u,"args":(p+"r",)},{"text":"♞","callback":self.are_u,"args":(p+"n",)},{"text":"♝","callback":self.are_u,"args":(p+"b",)},])
        await c.edit(text = text,
            reply_markup = btns,
            disable_security = True
        )
    async def are_u(s,c,p):#SCP FOUNDATION
        current_player = s.message.sender_id if (s.you_play == "w") ^ s.reverse else s.opp_id
        if c.from_user.id != current_player:
            await c.answer("Выбор за вашим оппонентом")
            return
        await s.moveTo(c,p)

    async def clicks_handle(self, call, coord):
        if self.checkmate or self.stalemate or self.fifty or self.reason:
            await call.answer("Партия окончена. Доступных ходов нет.")
            await self.purgeSelf()
            return
        if call.from_user.id not in self.you_n_me:
            await call.answer("Партия не ваша или уже сброшена")
            return
        if not self.game:
            await call.answer("Вы не запустили таймер")
            return    
        current_player = self.message.sender_id if (self.you_play == "w") ^ self.reverse else self.opp_id
        if call.from_user.id != current_player:
            await call.answer("Кыш от моих фигур")
            return

        if self.chsn == False:
            await self.checkMove(call,coord)
        else:
            matching_place = None
            for place in self.places:
                if place[2:4] == coord.lower():
                    if len(place) == 5:
                        await self.choose_figure(place,call)######
                        return
                    matching_place = place
                    break
                else:
                    matching_place = None
            if matching_place:
                self.Board.push(chess.Move.from_uci(matching_place))
                self.reverse = not self.reverse
                self.chsn = False
            else:
                prev_place = next((place for place in self.places if place[0:2] == coord.lower()), None)
                text = await self.sttxt()
                if prev_place:
                    self.chsn = False
                    self.places = []
                    await self.LoadBoard(text,call)
                    return
                if not await self.checkMove(call,coord):
                    self.chsn = False
                    self.places = []
                    await self.LoadBoard(text,call)
                    return
                else:
                    return
            text = await self.sttxt()
            await self.LoadBoard(text,call)

    async def checkMove(self,call,coord):
        if self.Board.piece_at(chess.parse_square(coord.lower())):
            square = chess.parse_square(coord.lower())
            moves = [move for move in self.Board.legal_moves if move.from_square == square]
            self.places = [p for p in [move.uci() for move in moves]]
            if not self.places:
                await call.answer("Для этой фигуры нет ходов!")
                return None
        else:
            await call.answer("Тут нет фигуры")
            self.places = []
            self.chsn = False
            return None

        self.chsn = True
        await call.answer(f"Доступные ходы:")
        await self.UpdBoard(call)
        return True

    async def sttxt(self):
        check = False
        self.checkmate = False
        self.stalemate = False
        self.fifty = False
        if self.Board.is_checkmate():
            self.checkmate = True
            self.timer = False
            self.reason = "Шах и мат"
        elif self.Board.is_check():
            check = True
        elif self.Board.is_stalemate():
            self.stalemate = True
            self.timer = False
            self.reason = "Пат"
        elif self.Board.can_claim_fifty_moves():
            self.Board.outcome()
            self.fifty = True
            self.timer = False
            self.reason = "50 ходов"
        elif self.timer:
            if int(await self.Timer.black_time()) == 0:
                self.timer = False
                self.reason = "Истекло время у чёрных"
            elif int(await self.Timer.white_time()) == 0:
                self.timer = False
                self.reason = "Истекло время у белых"

        if not self.checkmate and not check and not self.stalemate and not self.reason:
            if self.reverse:
                if self.Timer:
                    await self.Timer.black()
                if self.you_play == "w":
                    return f"[..] ♔ Белые - {self.saymyname}\n[👉] ♚ Чёрные - {self.opp_name} (ваш ход)"
                else:
                    return f"[..] ♔ Белые - {self.opp_name}\n[👉] ♚ Чёрные - {self.saymyname} (ваш ход)"
            else:
                if self.Timer:
                    await self.Timer.white()
                if self.you_play == "w":
                    return f"[👉] ♔ Белые - {self.saymyname} (ваш ход)\n[..] ♚ Чёрные - {self.opp_name}"
                else:
                    return f"[👉] ♔ Белые - {self.opp_name} (ваш ход)\n[..] ♚ Чёрные - {self.saymyname}"
        elif self.checkmate:
            if self.reverse:
                if self.you_play == "w":
                    return f"♔ Белые - {self.saymyname}\n♚ Чёрные - {self.opp_name}\n\n🎉 Шах и мат! Победил(а) {self.saymyname}"
                else:
                    return f"♔ Белые - {self.opp_name}\n♚ Чёрные - {self.saymyname}\n\n🎉 Шах и мат! Победил(а) {self.opp_name}"
            else:
                if self.you_play == "w":
                    return f"♔ Белые - {self.saymyname} \n♚ Чёрные - {self.opp_name}\n\n🎉 Шах и мат! Победил(а) {self.opp_name}"
                else:
                    return f"♔ Белые - {self.opp_name} \n♚ Чёрные - {self.saymyname}\n\n🎉 Шах и мат! Победил(а) {self.saymyname}"
        elif check:
            if self.reverse:
                if self.Timer:
                    await self.Timer.black()
                if self.you_play == "w":
                    return f"[..] ♔ Белые - {self.saymyname}\n[👉] ♚ Чёрные - {self.opp_name}\n\n❗ Шах!"
                else:
                    return f"[..] ♔ Белые - {self.opp_name}\n[👉] ♚ Чёрные - {self.saymyname}\n\n❗ Шах!"
            else:
                if self.Timer:
                    await self.Timer.white()
                if self.you_play == "w":
                    return f"[👉] ♔ Белые - {self.saymyname} \n[..] ♚ Чёрные - {self.opp_name}\n\n❗ Шах!"
                else:
                    return f"[👉] ♔ Белые - {self.opp_name} \n[..] ♚ Чёрные - {self.saymyname}\n\n❗ Шах!"
        elif self.stalemate:
            if self.reverse:
                if self.you_play == "w":
                    return f"♔ Белые - {self.saymyname}\n♚ Чёрные - {self.opp_name}\n\n🤝 Пат. Ничья"
                else:
                    return f"♔ Белые - {self.opp_name}\n♚ Чёрные - {self.saymyname}\n\n🤝 Пат. Ничья"
            else:
                if self.you_play == "w":
                    return f"♔ Белые - {self.saymyname} \n♚ Чёрные - {self.opp_name}\n\n🤝 Пат. Ничья"
                else:
                    return f"♔ Белые - {self.opp_name} \n♚ Чёрные - {self.saymyname}\n\n🤝 Пат. Ничья"
        elif self.fifty:
            if self.reverse:
                if self.you_play == "w":
                    return f"♔ Белые - {self.saymyname}\n♚ Чёрные - {self.opp_name}\n\n🤝 Правило 50 ходов. Ничья"
                else:
                    return f"♔ Белые - {self.opp_name}\n♚ Чёрные - {self.saymyname}\n\n🤝 Правило 50 ходов. Ничья"
            else:
                if self.you_play == "w":
                    return f"♔ Белые - {self.saymyname} \n♚ Чёрные - {self.opp_name}\n\n🤝 Правило 50 ходов. Ничья"
                else:
                    return f"♔ Белые - {self.opp_name} \n♚ Чёрные - {self.saymyname}\n\n🤝 Правило 50 ходов. Ничья"
        elif self.Timer and self.reason:
            if int(await self.Timer.white_time()) == 0:
                return f"♔ Белые - {self.saymyname}\n♚ Чёрные - {self.opp_name}\n\n❗⏱️ Истекло время: {self.opp_name}. 🎉 Победил(а) {self.saymyname}"
            else:
                return f"♔ Белые - {self.opp_name}\n♚ Чёрные - {self.saymyname}\n\n❗⏱️ Истекло время: {self.saymyname}. 🎉 Победил(а) {self.opp_name}"


    #####Ходы#####


    ##########
    async def outdated(self):
        await self.purgeSelf()
        return


    def ranColor(self):
        return "w" if random.randint(1,2) == 1 else "b"
    #########