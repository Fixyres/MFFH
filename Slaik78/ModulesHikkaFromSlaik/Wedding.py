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
# meta developer: @Hicota
# translator: @jpshiro

import random
import datetime
import aiohttp
import re

from telethon.tl.types import PeerUser
from .. import loader, utils

class DBWedding():
    def __init__(self, base_url: str = "http://77.239.102.151:3400"):
        self.base_url = base_url
        self.session = aiohttp.ClientSession()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        await self.session.close()

    async def _make_request(self, method: str, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        if kwargs.get('headers', {'X-API-KEY': True})['X-API-KEY'] is None:
            raise Exception(f"API error: API key don't support NoneType, change key in module config")
        async with self.session.request(method, url, **kwargs) as response:
            if response.status != 200:
                rjson = await response.json()
                raise Exception(f"API error: {response.status} {rjson['detail']}")
            return await response.json()
        
    async def get_apikey2(self, user_id: int) -> str:
        endpoint = f"/api/get/user2"
        params = {'tgid': user_id}
        return await self._make_request("GET", endpoint, params=params)
    
    async def user_exists(self, api_key: str, user_id: int) -> bool:
        endpoint = f"/api/{user_id}/exists"
        headers = {"X-API-KEY": api_key}
        return await self._make_request("GET", endpoint, headers=headers)
    
    async def add_users(self, api_key: str, u1: int, u2: int, days: int, month: int, year: int):
        endpoint = "/api/addusers"
        headers = {"X-API-KEY": api_key}
        params = {"id": u1, "id2": u2, "days": days, "month": month, "year": year}
        return await self._make_request("POST", endpoint, headers=headers, params=params)
    
    async def get_user_info(self, api_key: str):
        endpoint = "/api/users/get"
        headers = {"X-API-KEY": api_key}
        return await self._make_request("GET", endpoint, headers=headers)
    
    async def delete_user(self, api_key: str):
        endpoint = "/api/deluser"
        headers = {"X-API-KEY": api_key}
        return await self._make_request("DELETE", endpoint, headers=headers)

@loader.tds
class Wedding(loader.Module):
    """Живите счастливо со своей половинкой"""

    strings = {
        "name": "Wedding",
        "call_marriage": "Custom template for wedding information\nArguments: {yname} {hname} {year} {month} {day} {days}",
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
        "refused": "Alas but {} is refused {}, maybe better luck next time 😢",
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
        "married": "• marriage between {} and {}\n• <b>Marriage date registration:</b> {} {} {} year\n• <b>Marriage duration:</b> {} days",
        "love": "• <b>Should not to use rp commands on others, works only with your soulmate</b>",
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
        "rplol": ['teddy', 'phone', 'watch', 'chocolate', 'car', 'pc', 'annual subscription to lavhost<emoji document_id=5192756799647785066>✌️</emoji><emoji document_id=5193117564015747203>✌️</emoji><emoji document_id=5195050806105087456>✌️</emoji><emoji document_id=5195457642587233944>✌️</emoji>'],
        "api_key": 'Key to make module work, you can get it by writing command /apikey to bot @HicotоchkaBot',
        "api_error": 'Oops.. error occurred ➡ <code>{}</code>',
        "rphelp": '↓ Mini list of RP-commands ↓\n\n'
    }

    strings_ru = {
        "call_marriage": "Кастомный шаблон для информации брака\nАргументы: {yname} {hname} {year} {month} {day} {days}",
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
        "refused": "Увы но {} отказал {}, может в следующий раз повезёт😢",
        "filed_to_divorce": "{}, ваша половинка подала развод на вас😢",
        "not_dare": "Я знал что вы на это не решитесь, и правильно",
        "decided_marry":  "{}, {} протягивает колечко к вам, он хочет быть с вами до старости, вы согласны?",
        "marry_yourself": "• <b>Игры с самолюбовью не принимаются</b>",
        "marry_bot": "• <b>Не пытайтесь завести брак с ботом</b>",
        "not_found": "• <b>А вы кого ищите то?</b>",
        "no_args": "• <b>Хм, похоже правильнее будет {}</b>",
        "cheat_on": "• <b>Жаль конечно что вы втихоря хотите променять {}</b>",
        "sure_divorce": "Вы точно хотите развестить с {}?\nМожет не стоит?",
        "no_soulmate": "• <b>Но у вас ведь нету второй половинки</b>",
        "idk": "• <b>Увы но нельзя завести брак когда у пользователя есть другая половинка</b>",
        "married": "• Брак между {} и {}\n• <b>Дата регистрации брака:</b> {} {} {} year\n• <b>Продолжительность брака:</b> {} дней",
        "love": "• <b>Рп команды работают только при реплее на второй половинке или без реплея</b>",
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
        "rplol": ['мишку', 'телефон', 'часы', 'шоколадку', 'машину', 'пк', 'годовую подписку на любой из хостингов, только сегодня и только сейчас, не упустите это шанс😁'],
        "api_key": 'Ключ чтобы модуль работал, получить его можно написав боту @HicotоchkaBot команду /apikey',
        "api_error": 'Упс.. Вылетела ошибка ➡ <code>{}</code>',
        "rphelp": '↓ Мини лист рп-команд ↓\n\n'
    }

    mrg = DBWedding()
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "BlockWedlock",
                None,
                lambda: self.strings('call_marriage'),
                validator = loader.validators.String()
            ),
            loader.ConfigValue(
                "API-KEY",
                None, 
                lambda: self.strings("api_key"),
                validator = loader.validators.Hidden()
            )
        )

    async def on_dlmod(self):
        resp = (await self.mrg.get_apikey2((await self.client.get_me()).id))
        if not resp is None:
            self.config['API-KEY'] = resp
    
    async def client_ready(self):
        self.me = await self.client.get_me()


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

    def choza(self, args, uid):
        return [
            {
                "text": self.strings('return')['yes'][2],
                "callback": self.yes,
                "args": (args, uid)
            },
            {
                "text": self.strings('return')['no'][2],
                "callback": self.no,
                "args": (args, uid)
            }
        ]    
    
    async def yes(self, call, args, uid):
        if call.from_user.id == self._tg_id:
            return await call.answer(self.strings('decide_for'))
        elif uid != call.from_user.id:
            return await call.answer(self.strings('marry_not_you'))
        daydt = datetime.date.today()
        resp = (await self.mrg.add_users(self.config['API-KEY'], self.me.id, uid, daydt.day, daydt.month, daydt.year))
        if resp['message'].startswith('Users added'): 
            await call.edit(self.strings('now_married').format(f"<a href='tg://user?id={uid}'>{args}</a>"))
        elif resp['message'].startswith('🚫 <b>API Error'):
            await call.edit(self.strings('api_error').format(resp['message']))
    
    async def no(self, call, args, uid):
        if call.from_user.id == self._tg_id:
            return await call.answer(self.strings('decide_for'))
        elif uid != call.from_user.id:
            return await call.answer(self.strings('marry_not_you'))
        await call.edit(self.strings('refused').format(f"<a href='tg://user?id={uid}'>{args}</a>", f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>"))

    async def yea(self, call, args, urluser):
        resp = (await self.mrg.delete_user(self.config['API-KEY']))
        if resp['message'].startswith('User data'):
            await call.edit(self.strings('filed_to_divorce').format(f"<a href='tg://user?id={urluser}'>{args}</a>"))
        elif resp['message'].startswith('🚫 <b>API Error'):
            await call.edit(self.strings('api_error').format(resp['message']))
    
    async def nothing(self, call):
        await call.edit(self.strings('not_dare'))

    async def dayscount(self, datedb, datenow):
        days = 0
        current_date = datedb.date()
        while current_date <= datenow:
            days += 1
            current_date += datetime.timedelta(days=1)
        return days - 1
    
    async def checkuser(self, m, args: str):
        try:
            if args:
                if args.isdigit():
                    return await self.client.get_entity(args[0])
                else:
                    args = args.split(' ', 1)[0].replace('@', '').lower()
                    return await self.client.get_entity(args[0])
            elif m.is_reply:
                return (await m.get_reply_message()).sender
            else:
                await utils.answer(m, self.strings('no_args').format(f"<code>{utils.escape_html(self.get_prefix())}wedlock @username</code>"))
        except ValueError:
            await utils.answer(m, self.strings('not_found'))

    @loader.command(ru_doc = " - сделать предложение")
    async def wedlockcmd(self, message):
        """ - make a proposal"""
        args = utils.get_args_raw(message)
        user = await self.checkuser(message, args)
        if not (await self.mrg.user_exists(self.config['API-KEY'], self.me.id)):
            if not user.bot:
                if not (await self.mrg.user_exists(self.config['API-KEY'], user.id)):
                    if user.id != self.me.id:
                        await self.inline.form(
                            message = message,
                            text = self.strings('decided_marry').format(f"<a href='tg://user?id={user.id}'>{utils.escape_html(user.first_name)}</a>", f'<a href="tg://user?id={self.me.id}">{utils.escape_html(self.me.first_name)}</a>'),
                            reply_markup = self.choza(utils.escape_html(user.first_name), user.id), 
                            disable_security = True
                        )
                    else:
                        await utils.answer(message, self.strings('marry_yourself'))
                else:
                    await utils.answer(message, self.strings('idk'))
            else:
                await utils.answer(message, self.strings('marry_bot'))  
        else:
            urluser = (await self.mrg.get_user_info(self.config['API-KEY']))['users']
            urluser = urluser[next((key for key, value in urluser.items() if value != self.me.id), None)]
            user = await self.client.get_entity(urluser)
            await utils.answer(message, self.strings('cheat_on').format(f"<a href='{urluser}'>{user.first_name}</a>"))

    @loader.command(ru_doc = " - подать на развод")
    async def divorcecmd(self, message):
        """ - file to divorce"""
        if (await self.mrg.user_exists(self.config['API-KEY'], self.me.id)):
            urluser = (await self.mrg.get_user_info(self.config['API-KEY']))['users']
            urluser = urluser[next((key for key, value in urluser.items() if value != self.me.id), None)]
            user = await self.client.get_entity(urluser)
            await self.inline.form(
                message = message,
                text = self.strings('sure_divorce').format(f"<a href='tg://user?id={urluser}'>{user.first_name}</a>"),
                reply_markup = self.lenok(user.first_name, urluser)
            )
        else:
            await utils.answer(message, self.strings('no_soulmate'))
    
    @loader.command(ru_doc = " - информация о браке")
    async def winfocmd(self, message):
        """ - marriage information"""
        if (await self.mrg.user_exists(self.config['API-KEY'], self.me.id)):
            datenow = datetime.date.today()
            dateinfo = (await self.mrg.get_user_info(self.config['API-KEY']))['date']
            datedb = datetime.datetime.strptime(F'{dateinfo["year"]}-{dateinfo["month"]}-{dateinfo["days"]}', '%Y-%m-%d')
            days = await self.dayscount(datedb, datenow)
            if (await self.mrg.user_exists(self.config['API-KEY'], self.me.id)):
                urluser = (await self.mrg.get_user_info(self.config['API-KEY']))['users']
                urluser = urluser[next((key for key, value in urluser.items() if value != self.me.id), None)]
                user = await self.client.get_entity(urluser)
                if self.config['BlockWedlock']:
                    await utils.answer(message, self.config['BlockWedlock'].format(yname=f"<a href='tg://user?id={urluser}'>{user.first_name}</a>", hname=f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>", day=datedb.day, month=datedb.strftime('%B'), year=datedb.year, days=days))
                else:
                    await utils.answer(message, self.strings('married').format(f"<a href='tg://user?id={urluser}'>{user.first_name}</a>", f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>", datedb.day, datedb.strftime('%B'), datedb.year, days))
        else:
            await utils.answer(message, self.strings('no_soulmate'))

    @loader.command(ru_doc = " - Лист РП-команд ")
    async def rplistcmd(self, message):
        ' - RP-Commands list'
        text = self.strings('rphelp')
        for key, value in self.strings('rplist').items():
            if re.search(r'^gift$|^подарок$', key):
                text += f"{key} > {value.format('OneName', 'Gift', 'TwoName')}\n"
            else:
                text += f"{key} > {value.format('OneName', 'TwoName')}\n"
        await message.edit(text)
        
    @loader.watcher(only_messages = True)
    async def watcher(self, message):
        if message.text.lower() in self.strings('rplist').keys():
            mfi = message.from_id.user_id if isinstance(message.from_id, PeerUser) else message.from_id
            if (await self.mrg.user_exists(self.config['API-KEY'], self.me.id)) and mfi == self.tg_id:
                urluser = (await self.mrg.get_user_info(self.config['API-KEY']))['users']
                urluser = urluser[next((key for key, value in urluser.items() if value != self.me.id), None)]
                user = await self.client.get_entity(urluser)
                rplist_str = self.strings('rplist')[message.text.lower()]
                wtf = random.choice(self.strings('rplol'))
                if message.is_reply and (await message.get_reply_message()).sender.id == user.id:
                    if message.text.lower() in list(self.strings('rplist').keys()) and not re.search(r'^gift$|^подарок$', message.text.lower()):
                        await utils.answer(message, rplist_str.format(f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>", f"<a href='tg://user?id={urluser}'>{user.first_name}</a>"))    
                    elif re.search(r'^gift$|^подарок$', message.text.lower()):
                        await utils.answer(message, rplist_str.format(f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>", wtf, f"<a href='tg://user?id={urluser}'>{user.first_name}</a>"))
                elif message.is_reply and (await message.get_reply_message()).sender.id != user.id: 
                    await utils.answer(message, self.strings('love'))
                elif mfi == self.tg_id:
                    if message.text.lower() in list(self.strings('rplist').keys()) and not re.search(r'^gift$|^подарок$', message.text.lower()):
                        await utils.answer(message, rplist_str.format(f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>", f"<a href='tg://user?id={urluser}'>{user.first_name}</a>"))
                    elif re.search(r'^gift$|^подарок$', message.text.lower()):
                        await utils.answer(message, rplist_str.format(f"<a href='tg://user?id={self.me.id}'>{self.me.first_name}</a>", wtf, f"<a href='tg://user?id={urluser}'>{user.first_name}</a>"))
            elif mfi == self.tg_id:
                await utils.answer(message, self.strings('no_soulmate'))
