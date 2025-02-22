#------------------------------------------------------------------
#      ___           ___       ___                       ___     
#     /\  \         /\__\     /\  \          ___        /\__\    
#    /::\  \       /:/  /    /::\  \        /\  \      /:/  /    
#   /:/\ \  \     /:/  /    /:/\:\  \       \:\  \    /:/__/     
#  _\:\~\ \  \   /:/  /    /::\~\:\  \      /::\__\  /::\__\____ 
# /\ \:\ \ \__\ /:/__/    /:/\:\ \:\__\  __/:/\/__/ /:/\:::::\__\
# \:\ \:\ \/__/ \:\  \    \/__\:\/:/  / /\/:/  /    \/_|:|~~|~   
#  \:\ \:\__\    \:\  \        \::/  /  \::/__/        |:|  |    
#   \:\/:/  /     \:\  \       /:/  /    \:\__\        |:|  |    
#    \::/  /       \:\__\     /:/  /      \/__/        |:|  |    
#     \/__/         \/__/     \/__/                     \|__|   
#------------------------------------------------------------------ 
# meta developer: @hicota
# translator: @jpshiro
# requires: pymysql, python-dotenv

import os
import random
import pymysql
import datetime
import pymysql.cursors
from dotenv import load_dotenv

from .. import loader, utils
from ..inline.types import InlineQuery

load_dotenv()


@loader.tds
class MarriAge(loader.Module):
    """Женитесь на своей второй половинкe"""


    strings = {
        "name": "MarriAge",
        "call_marriage": "Call your marriage whatever you want",
        "return": {
            "yes": {
                1: "Yes, I sure",
                2: "Agree"
            },
            "no": {
                1: "No, guess I refuse",
                2: "Refuse"
            },
        },
        "decide_for": "Why do you decide for you soulmate?",
        "marry_not_you": "Someone is decided to marry but not you, come to terms with it",
        "now_married": "Congratulate, now you are married with {}",
        "refused": "Alas but {} is refused you, maybe better luck next time 😢",
        "filed_to_divorce": "{}, your soulmate is filed to divorce 😢",
        "not_dare": "I knew that you wouldn't dare, that's right",
        "decided_marry": "{}, {} held a ring to you, perhaps he's want to marry you🥰",
        "marry_yourself": "• <b>You can't marry yourself</b>",
        "marry_bot": "• <b>Don't try to marry a bot</b>",
        "not_found": "• <b>and who are you looking for?</b>",
        "no_args": "• <b>Hmm, I guess that more correct is {}</b>",
        "cheat_on": "• <b>It's a pity that you want to silently cheat on {}</b>",
        "sure_divorce": "Are you sure you want to divorce with {}?\nMaybe it's not worth it?",
        "no_soulmate": "• <b>But you don't have a soulmate</b>",
        "idk": "• <b>It's a pity you can't get married if the user has a soulmate</b>",
        "marriage_name": "• <b>The name of your marriage:</b> {}",
        "add_marriage_name": "\n\nJust type this command to add a marriage name {}",
        "married": "{}\n• You are married with {}\n• <b>Marriage date registration:</b> {} {} {} year\n• <b>Marriage duration:</b> {} days{}",
        "love": "• <b>Should not to use rp commands on others, works only with your soulmate</b>",
        "must_be": "Marriage name must be here",
        "rplist": {
            "kiss": "<b>💋 | {} kissed {} on the cheek</b>",
            "gift": "<b>🎁 | {} gave a gift {} to {}</b>", 
            "hug": "<b>👐 | {} hugged {}</b>",
            "fuck": "<b>🚻 | {} fucked {}</b>",
            "compliment": "<b>🤭 | {} told {} a cute compliment</b>",
            "stroke": "<b>👋 | {} stroked {} on head</b>",
            "breakfast": "<b>🥡 | {} cooked a breakfast</b>",
            "bit": "<b>🧛 | {} bit {}</b>",
            "lick": "<b>👅 | {} licked {}</b>",
            "push": "<b>🏠 | {} pushed {} against a wall</b>",
            "gave": "<b>❤‍🔥 | {} gave himself to {}</b>"
        },
        "rplol": ['teddy', 'phone', 'watch', 'chocolate', 'car', 'pc', 'annual subscription to lavhost<emoji document_id=5192756799647785066>✌️</emoji><emoji document_id=5193117564015747203>✌️</emoji><emoji document_id=5195050806105087456>✌️</emoji><emoji document_id=5195457642587233944>✌️</emoji>']
    }

    strings_ru = {
        "call_marriage": "Назовите свой брак как вам в душе хочется",
        "return": {
            "yes": {
                1: "Да, я уверен",
                2: "Согласиться"
            },
            "no": {
                1: "Нет, пожалуй откажусь",
                2: "Отказаться"
            }
        },
        "decide_for": "Зачем ты решаешь за свою вторую половинку?",
        "marry_not_you": "Не с вами решили завести брак, смиритесь",
        "now_married": "Поздравляю, вы теперь состоите в браке вместе с {}",
        "refused": "Увы но {} отказал вам, может следующий раз повезёт вам 😢",
        "filed_to_divorce": "{}, ваша половинка подала развод на вас 😢",
        "not_dare": "Я знал что вы на это не решитесь, и правильно",
        "decided_marry":  "{}, {} протянул колечко к вам, похоже он хочет завести с вам брак🥰",
        "marry_yourself": "• <b>Игры с самолюбовью не принимаются</b>",
        "marry_bot": "• <b>Не пытайтесь завести брак с ботом</b>",
        "not_found": "• <b>А вы кого ищите то?</b>",
        "no_args": "• <b>Хм, похоже правильнее будет {}</b>",
        "cheat_on": "• <b>Жаль конечно что вы втихоря хотите променять {}</b>",
        "sure_divorce": "Вы точно хотите развестить с {}?\nМожет не стоит?",
        "no_soulmate": "• <b>Но у вас ведь нету второй половинки</b>",
        "idk": "• <b>Увы но нельзя завести брак когда у пользователя есть другая половинка</b>",
        "marriage_name": "• <b>Название вашего брака:</b> {}",
        "add_marriage_name": "\n\nЧтоб добавить название для вашего брака просто введите команду {}",
        "married": "{}\n• Вы находитесь в браке вместе с {}\n• <b>Дата регистрации брака:</b> {} {} {} year\n• <b>Продолжительность брака:</b> {} дней{}",
        "love": "• <b>Эти рп команды работают только при реплее на вашей половинке или без реплея</b>",
        "must_be": "Здесь должно быть имя брака",
        "rplist": {
            "поцеловать": "<b>💋 | {} поцеловал/a в щёчку {}</b>",
            "подарок": "<b>🎁 | {} подарил/a {} {}</b>",
            "обнять": "<b>👐 | {} обнял/a {}</b>",
            "трахнуть": "<b>🚻 | {} трахнул {}</b>",
            "комплимент": "<b>🤭 | {} сказал/а ласковый комплимент {}</b>",
            "погладить": "<b>👋 | {} погладил/а по голове {}</b>",
            "завтрак": "<b>🥡 | {} приготовил/а завтрак {}</b>",
            "кусь": "<b>🧛 | {} куснул/а {}</b>",
            "лизь": "<b>👅 | {} лизнул/а {}</b>",
            "прижал": "<b>🏠 | {} прижал/а к стене {}</b>",
            "отдаться": "<b>❤‍🔥 | {} отдался/ась {}</b>"
        },
        "rplol": ['мишку', 'телефон', 'часы', 'шоколадку', 'машину', 'пк', 'годовую подписку на лавхост<emoji document_id=5192756799647785066>✌️</emoji><emoji document_id=5193117564015747203>✌️</emoji><emoji document_id=5195050806105087456>✌️</emoji><emoji document_id=5195457642587233944>✌️</emoji>']
    }

    wedbool = False
    
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "nameWedlock",
                None,
                lambda: self.string('call_marriage'),
                validator = loader.validators.String()
            ),
        )

    def user_exists(self, user):
        self.cur.execute('SELECT id FROM `wedlock` WHERE `user` = %s', [user])
        if self.cur.fetchone() == None:
            return False
        else:
            return True
    
    def user2_exists(self, user):
        self.cur.execute('SELECT id FROM `wedlock` WHERE `user2` = %s', [user])
        if self.cur.fetchone() == None:
            return False
        else:
            return True
    
    def add_user_user2(self, user, user2, days, month, year):
        self.cur.execute('INSERT INTO `wedlock` (`user`, `user2`, `days`, `month`, `year`) VALUES (%s, %s, %s, %s, %s)', [user, user2, days, month, year])
        return self.conn.commit()
    
    def get_user(self, user):
        self.cur.execute('SELECT `user` FROM `wedlock` WHERE `user2` = %s', [user])
        return self.cur.fetchall()
    
    def get_user2(self, user):
        self.cur.execute('SELECT `user2` FROM `wedlock` WHERE `user` = %s', [user])
        return self.cur.fetchall()
    
    async def get_days(self, user):
        
        if self.user_exists(self.me.username):
            self.cur.execute('SELECT `days` FROM `wedlock` WHERE `user` = %s', [user])
            return self.cur.fetchall()
            
        elif self.user2_exists(self.me.username):
            self.cur.execute('SELECT `days` FROM `wedlock` WHERE `user2` = %s', [user])
            return self.cur.fetchall()
    
    async def get_month(self, user):
        
        if self.user_exists(self.me.username):
            self.cur.execute('SELECT `month` FROM `wedlock` WHERE `user` = %s', [user])
            return self.cur.fetchall()
            
        elif self.user2_exists(self.me.username):
            self.cur.execute('SELECT `month` FROM `wedlock` WHERE `user2` = %s', [user])
            return self.cur.fetchall()
    
    async def get_year(self, user):
        
        if self.user_exists(self.me.username):
            self.cur.execute('SELECT `year` FROM `wedlock` WHERE `user` = %s', [user])
            return self.cur.fetchall()
            
        elif self.user2_exists(self.me.username):
            self.cur.execute('SELECT `year` FROM `wedlock` WHERE `user2` = %s', [user])
            return self.cur.fetchall()
    
    def delete_user2(self, user2):
        if self.user_exists(self.me.username):
            self.cur.execute('DELETE FROM wedlock WHERE user2 = %s', [user2])
        elif self.user2_exists(self.me.username):
            self.cur.execute('DELETE FROM wedlock WHERE user = %s', [user2])
        return self.conn.commit()

    async def client_ready(self):
        if not os.path.exists('.env'):
            os.system("curl -O https://raw.githubusercontent.com/Slaik78/ModulesHikkaFromSlaik/main/.env")
            await self.client.send_message(self.tg_id, 'Думаю стоит рестарнуть?')
        self.conn = pymysql.connect(host="147.45.247.194", user=os.getenv("NAMEUSER"), passwd=os.getenv("PASSWRD"), db="default_db", port=3306, cursorclass = pymysql.cursors.DictCursor)
        self.cur = self.conn.cursor()
        self.me = await self.client.get_me()
        
        if self.user_exists(self.me.username):
            self.wedbool = True
            
        elif self.user2_exists(self.me.username):
            self.wedbool = True
            
        else:
            self.wedbool = False

    def lenok(self, args, urluser):
        
        return [
            {
                "text": self.strings('return')['yes'][1], 
                "callback": self.yea, 
                "args": (args, urluser)
            },
            {
                "text": self.strings('return')['no'][1], 
                "callback": self.nothing
            }
        ]

    def choza(self, args, uid, urluser):
        
        return [
            {
                "text": self.strings('return')['yes'][2],
                "callback": self.yes,
                "args": (args, uid, urluser)
            },
            {
                "text": self.strings('return')['no'][2],
                "callback": self.no,
                "args": (args, uid, urluser)
            }
        ]    
    
    async def yes(self, call, args, uid, urluser):
        
        if call.from_user.id == self._tg_id:
            return await call.answer(self.strings('decide_for'))
            
        elif uid != call.from_user.id:
            return await call.answer(self.strings('marry_not_you'))
            
        self.wedbool = True
        daydt = datetime.date.today()
        
        try:
            self.add_user_user2(self.me.username, urluser, daydt.day, daydt.month, daydt.year)
            
        except pymysql.err.OperationalError:
            
            await call.answer("Думаю стоит ещё раз нажать")
            self.cur.close()
            self.conn.close()
            await self.client_ready()
            try:
                return await self.wedlockcmd(message)
            except NameError:
                return
            
        await call.edit(self.strings('now_married').format(f"<a href='https://t.me/{urluser}'>{args}</a>"))
    
    async def no(self, call, args, uid, urluser):
        
        if call.from_user.id == self._tg_id:
            return await call.answer(self.strings('decide_for'))
            
        elif uid != call.from_user.id:
            return await call.answer(self.strings('marry_not_you'))
            
        await call.edit(self.strings('refused').format(f"<a href='https://t.me/{urluser}'>{args}</a>"))

    async def yea(self, call, args, urluser):
        
        try:

            self.delete_user2(urluser)

        except pymysql.err.OperationalError:
            
            await call.answer("Думаю стоит ещё раз нажать")
            self.cur.close()
            self.conn.close()
            await self.client_ready()
            try:
                return await self.divorcecmd(message)
            except NameError:
                return
            
        self.wedbool = False
        await call.edit(self.strings('filed_to_divorce').format(f"<a href='https://t.me/{urluser}'>{args}</a>"))
    
    async def nothing(self, call):
        await call.edit(self.strings('not_dare'))

    @loader.command(ru_doc = " - сделать предложение")
    async def wedlockcmd(self, message):
        """ - make a proposal"""
        
        args = utils.get_args_raw(message)
        
        if args:
            
            args = args.split(' ', 1)
            urluser = args[0].replace('@', '')
            user = await message.client.get_entity(args[0])
            
            if not self.wedbool:
                
                try:
                    
                    if not user.bot:
                        
                        try:

                            if not self.user_exists(urluser) or not self.user2_exists(urluser):

                                if urluser.lower() != self.me.username.lower():
                                    
                                    await self.inline.form(
                                        message = message,
                                        text = self.strings('decided_marry').format(f"<a href='https://t.me/{urluser}'>{user.first_name}</a>", f'<a href="https://t.me/{self.me.username}">{self.me.first_name}</a>'),
                                        reply_markup = self.choza(user.first_name, user.id, urluser), 
                                        disable_security = True
                                    )
                                    
                                else:
                                    await utils.answer(message, self.strings('marry_yourself'))
                            else:
                                await utils.answer(message, self.strings('idk'))

                        except pymysql.err.OperationalError:
                    
                            await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
                            self.cur.close()
                            self.conn.close()
                            await self.client_ready()
                            return await self.wedlockcmd(message)
                    else:
                        await utils.answer(message, self.strings('marry_bot'))
                        
                except ValueError:
                    await utils.answer(message, self.strings('not_found'))
                    
            else:
                
                try:
                    
                    if self.user_exists(self.me.username):
                        
                        urluser = self.get_user2(self.me.username)[0]['user2']
                        user = await self.client.get_entity(urluser)
                        
                    elif self.user2_exists(self.me.username):
                        
                        urluser = self.get_user(self.me.username)[0]['user']
                        user = await self.client.get_entity(urluser)
                    
                    await utils.answer(message, self.strings('cheat_on').format(f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"))
                        
                except pymysql.err.OperationalError:
                    
                    await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
                    self.cur.close()
                    self.conn.close()
                    await self.client_ready()
                    return await self.divorcecmd(message)

        elif message.is_reply:
            urluser = (await self.client.get_entity((await message.get_reply_message()).from_id)).username
            user = await message.client.get_entity(urluser)
            if not self.wedbool:
                
                try:
                    
                    if not user.bot:
                        
                        try:

                            if not self.user_exists(urluser) or not self.user2_exists(urluser):
                            
                                if urluser.lower() != self.me.username.lower():
                                    
                                    await self.inline.form(
                                        message = message,
                                        text = self.strings('decided_marry').format(f"<a href='https://t.me/{urluser}'>{user.first_name}</a>", f'<a href="https://t.me/{self.me.username}">{self.me.first_name}</a>'),
                                        reply_markup = self.choza(user.first_name, user.id, urluser), 
                                        disable_security = True
                                    )
                                    
                                else:
                                    await utils.answer(message, self.strings('marry_yourself'))
                            
                            else:
                                await utils.answer(message, self.strings('idk'))
                        
                        except pymysql.err.OperationalError:
                    
                            await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
                            self.cur.close()
                            self.conn.close()
                            await self.client_ready()
                            return await self.wedlockcmd(message)
                        
                    else:
                        await utils.answer(message, self.strings('marry_bot'))
                        
                except ValueError:
                    await utils.answer(message, self.strings('not_found'))
                    
            else:
                
                try:
                    
                    if self.user_exists(self.me.username):
                        
                        urluser = self.get_user2(self.me.username)[0]['user2']
                        user = await self.client.get_entity(urluser)
                        
                    elif self.user2_exists(self.me.username):
                        
                        urluser = self.get_user(self.me.username)[0]['user']
                        user = await self.client.get_entity(urluser)
                    
                    await utils.answer(message, self.strings('cheat_on').format(f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"))
                        
                except pymysql.err.OperationalError:
                    
                    await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
                    self.cur.close()
                    self.conn.close()
                    await self.client_ready()
                    return await self.divorcecmd(message)

        else:
            await utils.answer(message, self.strings('no_args').format(f"<code>{utils.escape_html(self.get_prefix())}wedlock @username</code>"))

    @loader.command(ru_doc = " - подать на развод")
    async def divorcecmd(self, message):
        """ - file to divorce"""
        
        if self.wedbool:
            
            try:
                if self.user_exists(self.me.username):
                    urluser = self.get_user2(self.me.username)[0]['user2']
                elif self.user2_exists(self.me.username):
                    urluser = self.get_user(self.me.username)[0]['user']
            except pymysql.err.OperationalError:
                
                await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
                self.cur.close()
                self.conn.close()
                await self.client_ready()
                return await self.divorcecmd(message)
                
            user = await self.client.get_entity(urluser)
            await self.inline.form(
                message = message,
                text = self.strings('sure_divorce').format(f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"),
                reply_markup = self.lenok(user.first_name, urluser)
            )
            
        else:
            await utils.answer(message, self.strings('no_soulmate'))
    
    @loader.command(ru_doc = " - информация о браке")
    async def winfocmd(self, message):
        """ - marriage information"""
        try:
            if self.wedbool and self.user_exists(self.me.username) or self.user2_exists(self.me.username):
                    
                    daydt = datetime.date.today()
                    result = await self.get_days(self.me.username)
                    daydbdt = datetime.datetime.strptime(str(result[0]['days']), '%d')
                    result = await self.get_month(self.me.username)
                    monthdbdt = datetime.datetime.strptime(str(result[0]['month']), '%m')
                    result = await self.get_year(self.me.username)
                    yeardbdt = datetime.datetime.strptime(str(result[0]['year']), '%Y')
                    g = self.strings('marriage_name').format(self.config['nameWedlock']) if self.config['nameWedlock'] != '' else self.strings('must_be')
                    gg = self.strings('add_marriage_name').format(f"<code>{utils.escape_html(self.get_prefix())}fcfg MarriAge nameWedlock 'текст'</code>") if self.config['nameWedlock'] == '' else ''
                    
                    if self.user_exists(self.me.username):
                        
                        urluser = self.get_user2(self.me.username)[0]['user2']
                        user = await self.client.get_entity(urluser)
                        await utils.answer(message, self.strings('married').format(g, f"<a href='https://t.me/{urluser}'>{user.first_name}</a>", daydbdt.day, monthdbdt.strftime('%B'), yeardbdt.year, daydt.day - daydbdt.day, gg))
                        
                    elif self.user2_exists(self.me.username):
                        
                        urluser = self.get_user(self.me.username)[0]['user']
                        user = await self.client.get_entity(urluser)
                        await utils.answer(message, self.strings('married').format(g, f"<a href='https://t.me/{urluser}'>{user.first_name}</a>", daydbdt.day, monthdbdt.strftime('%B'), yeardbdt.year, daydt.day - daydbdt.day, gg))
                
            else:
                await utils.answer(message, self.strings('no_soulmate'))
        
        except pymysql.err.OperationalError:
                
            await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
            self.cur.close()
            self.conn.close()
            await self.client_ready()
            return await self.winfocmd(message)
        
    @loader.watcher(only_messages = True)
    async def watcher(self, message):
        
        try:
            
            if message.text.lower() in self.strings('rplist'):
                
                if self.wedbool and message.from_id == self.tg_id:
                    if self.user_exists(self.me.username):
                        urluser = self.get_user2(self.me.username)[0]['user2']
                        user = await self.client.get_entity(urluser)
                    elif self.user2_exists(self.me.username):
                        urluser = self.get_user(self.me.username)[0]['user']
                        user = await self.client.get_entity(urluser)
                    rplist_str = self.strings('rplist')[message.text.lower()]
                    wtf = random.choice(self.strings('rplol'))
                    
                    if message.is_reply and (await message.get_reply_message()).from_id == user.id:
                          
                        if message.text.lower() in list(self.strings('rplist').keys()) and not ('gift' in message.text.lower() or 'подарок' in message.text.lower()):
                            await utils.answer(message, rplist_str.format(f"<a href='https://t.me/{self.me.username}'>{self.me.first_name}</a>", f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"))
                                
                        elif 'gift' in message.text.lower() or 'подарок' in message.text.lower():
                            await utils.answer(message, rplist_str.format(f"<a href='https://t.me/{self.me.username}'>{self.me.first_name}</a>", wtf, f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"))
                                
                    elif message.is_reply and (await message.get_reply_message()).from_id != user.id: 
                        await utils.answer(message, self.strings('love'))
                        
                    elif message.from_id == self.tg_id:
                            
                        if message.text.lower() in list(self.strings('rplist').keys()) and not ('gift' in message.text.lower() or 'подарок' in message.text.lower()):
                            await utils.answer(message, rplist_str.format(f"<a href='https://t.me/{self.me.username}'>{self.me.first_name}</a>", f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"))
                            
                        elif 'gift' in message.text.lower() or 'подарок' in message.text.lower():
                            await utils.answer(message, rplist_str.format(f"<a href='https://t.me/{self.me.username}'>{self.me.first_name}</a>", wtf, f"<a href='https://t.me/{urluser}'>{user.first_name}</a>"))
                                
                elif message.from_id == self.tg_id:
                    await utils.answer(message, self.strings('no_soulmate'))
                    
        except pymysql.err.OperationalError:
                
            await utils.answer(message, "<emoji document_id=5382021057601348544>🤯</emoji>")
            self.cur.close()
            self.conn.close()
            await self.client_ready()
            return await self.watcher(message)