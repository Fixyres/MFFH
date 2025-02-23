# -----------------------Immports---------------
# scope: hikka_only
# requires: Hikka-TL-New, pytz

__version__ = (1, 8, 0)

import contextlib
import hikkatl
from hikkatl.tl.functions.channels import GetParticipantsRequest
from hikkatl.errors import TimeoutError, BotResponseTimeoutError
from hikkatl.errors.rpcerrorlist import (
    FloodWaitError,
    MessageNotModifiedError,
)
from hikkatl.tl.types import (
    Message,
    User,
    MessageEntityPhone,
    MessageEntityMentionName,
    MessageEntityTextUrl,
    MessageEntityMention,
    MessageEntityUrl,
    Channel,
    PeerChannel,
    MessageReplies,
)
from hikkatl.tl.types import ChannelParticipantsSearch

from .. import loader, utils
from typing import Union, Optional, Any
from ..inline.types import InlineCall

import pytz
import re
import asyncio
from asyncio.exceptions import TimeoutError
from datetime import datetime, timedelta
import logging
import json as Json

from random import SystemRandom

randint = SystemRandom().randint
choices = SystemRandom().choices
uniform = SystemRandom().uniform

import unicodedata

MEP = MessageEntityPhone
MEMN = MessageEntityMentionName
METU = MessageEntityTextUrl
MENT = MessageEntityMention
MEU = MessageEntityUrl

logger = logging.getLogger('BioWars')
re._MAXCAСHE = 3000
DT_FORMAT = '%d/%m/%Y %H:%M:%S'
DT_FORMAT2 = '%d.%m.%Y'


# ---------------------------Module--------------------

def check_trash_bio(trash):
    return 'лаб' in trash.lower() and 'топ' in trash.lower()


def isbio(text):
    bio_items = text[text.find('1. '):]
    bio_trash = text[:text.find('1. ')]
    if not check_trash_bio(bio_trash):
        return False, False
    if len(bio_items) <= 1:
        return False, False
    bio_list = bio_items.splitlines()
    m = len(bio_list)
    for i in range(m):
        if not bio_list[i].startswith(f"{i + 1}. "):
            return False, False
    return True, len(bio_trash.splitlines())


class Timezone_Validator(loader.validators.Validator):
    def __init__(self):
        super().__init__(self._validate,
                         {
                             'ru': 'временной зоной для pytz',
                             'en': 'timezone for pytz'
                         }
                         )

    @staticmethod  #
    def _validate(value: Any) -> str:
        if value.lower() not in [_.lower() for _ in pytz.all_timezones]:
            raise loader.validators.ValidationError(
                f'Временая зона "{value}" не существует.')

        return f'{value}'


class iris:
    bots = [
        707693258,  # 🔵 Iris | Чат-менеджер
        5226378684,  # 🟣 Iris | Deep Purple
        5137994780,  # 🟡 Iris | Bright Sophie
        5434504334,  # ⚪️ Iris | Moonlight Dyla
        5443619563,  # 🎩 Iris | Black Diamond
    ]

    chats = [
        -1001491081717,  # 👨🏼‍💻 Iris | Помощь по функционалу
        -1001421482914,  # 🪒 Iris | Оффтоп
        -1001284208391,  # 📛 Iris | Антиспам дружина
        -1001463965279,  # 🌕 Iris | Биржа
        -1001316297204,  # 🦠 Iris | Биовойны
        -1001323663801,  # 🍬 Iris | Акции и бонусы
        -1001687821774,  # 📣 Iris | Чат Короткие новости
        -1001283847535,  # ✍️ Iris | Отзывы об агентах
        -1001667453682,  # 🔫 Iris | Золотые дуэли
    ]

    prefs = [
        'ирис', 'ириска',
        '.', '/', '!'
    ]

    _prefs = [
        'ирис ', 'ириска ',
        '.', '/', '!',
        '. ', '/ ', '! '
    ]


def _exp(exp: str) -> int:
    """опыт с жертвы в инт"""
    exp = ''.join(exp.split()).lower().replace('к', 'k').replace('.', ',')

    if not 'k' in exp:
        exp = exp

    else:
        if not ',' in exp:
            exp = exp[:len(exp) - 1] + '000'

        else:
            exp = exp[:len(exp) - 1].replace(',', '') + '00'

    return int(exp)


def time_emoji(time: str):
    """показывает кд"""
    emj = {
        'exp': 'кд'
    }

    return emj[min(emj)]


def dict_split(Dict: dict, s: int = 50, reverse: bool = True) -> list:
    keys = list(Dict.keys()) if not reverse else list(reversed(Dict.keys()))
    lists = []

    for i in range(0, len(keys), s):
        e_c = keys[i: s + i]
        if len(e_c) < s:
            e_c = e_c + [None for y in range(s - len(e_c))]
        lists.append(e_c)

    return lists


def sanitise_text(text: str) -> str:  # by hikari
    """
    Replaces all animated emojis in text with normal ones,
    bc aiogram doesn't support them
    :param text: text to sanitise
    :return: sanitised text
    """
    return re.sub(r"</?emoji.*?>", "", text)


def repair_text(text: str) -> str:
    """
    Удаляет с текста зальго, теги
    """
    return utils.escape_html(
        ''.join(
            _ for _ in unicodedata.normalize('NFD', text)
            if unicodedata.category(_) != 'Mn'
        )
    )


def get_ne_pridumal(text: str, at: bool = False) -> list:
    """
    Возвращает все юзернеймы и айди из текста
    """
    users = []

    for _ in range(len(text)):
        before_len = len(text)

        if r := re.search(r'tg://user\?id=(\d+)', text, flags=re.ASCII):
            users.append(r.group(1))
            text = text.replace(r.group(0), '')

        if r := re.search(r'@(\d+)', text, flags=re.ASCII):
            users.append(r.group(1))
            text = text.replace(r.group(0), '')

        if r := re.search(r'@([a-zA-Z][\w\d]{3,30}[a-zA-Z\d])',
                          text):  # from https://tl.telethon.dev/methods/contacts/resolve_username.html#:~:text=UsernameInvalidError
            users.append(r.group(1))
            text = text.replace(r.group(0), '')

        if r := re.search(r'tg://openmessage\?user_id=(\d+)', text, flags=re.ASCII):
            users.append(r.group(1))
            text = text.replace(r.group(0), '')

        if r := re.search(r'(https://|)t\.me/([a-zA-Z][\w\d]{3,30}[a-zA-Z\d])', text, flags=re.ASCII):
            users.append(r.group(2))
            text = text.replace(r.group(0), '')

        if before_len == len(text):
            break

    _users = []
    for _ in users:
        if _ not in _users:
            _users.append(_)

    if at:
        return [f'@{_}' for _ in _users]

    return _users


def unix_dt(date: float) -> datetime:
    """
    Unix дату в объект datetime
    """
    return datetime.fromtimestamp(date)


def strtime(date: Union[datetime, float]):
    if isinstance(date, float):
        date = unix_dt(date)

    return da


@loader.tds
class BioWars(loader.Module):
    """📡 Бот для био-войн Lapik Edition (beta)"""

    # emj = {
    #    'exp': '<emoji document_id=5280697968725340044>☢️</emoji>'
    # }

    strings = {
        "name": "BioWars",
        "link_id": "tg://openmessage?user_id=",
        "link_username": "https://t.me/",

        "сommands": {
            "z": "[args] [reply] ",
            "id": "[arg/reply] -",
            "ids": "[args] [reply] - Чекает айди по реплаю",
            "dov": "Показывает информацию по доверке",
            'zz': 'Аналог команды .б из био',
            'nik': '[id] [имя] - запись человека',
            'pref': '[id] [префикс] - записывает префикс дова'
        },
        # Зарлист
        'zar.search':
            "✅ Жертва {} приносит\n"
            "☣️ +{} опыта\n"
            '🔭 Заражение до {} ',

        '_zar.search':
            "✅ Жертва {} приносит\n"
            "☣️ +{} опыта {} \n"
            '🔭 Заражение до {}',

        'zar.save':
            "✅ Жертва <code>{}</code> сохранена\n"
            "☣️<s>{}</s> +{} опыта \n"
            "🔭 Заражение до {} ",

        'z.nf': '❎ Не удалось найти информацию по жертве <code>{}</code>',
        '_z.nf': '❌ Пользователя <code>{}</code> не существует!',

        'edit_nik': '✅ Имя жертвы «<a href = "tg://openmessage?user_id={0}">{1}</a>» успешно записано',
        'edit_pref': '✅ Префикс «{}» успешно записан для <code>@{}</code>',
        # Руководства по модулю
        "bio.commands": "\n\n"
                        "📡 Бот для био-войн Lapik Edition (beta): \n\n🗺 Личный префикс: <code>{0}</code>\n\n"

                        "📌 Команды бота:\n"
                        "🍪 <code>{0}помощь</code> — вывод этого сообщения\n"
                        "🍪 <code>{0}ping</code> — узнать скорость ответа бота\n"
                        "🍪 л — вывести краткую информацию о лабе\n"
                        "🍪 заразить, зарази, еб, ёб, бей — атаковать\n"
                        "🍪 вак, хи, лечись — покупает вакцину\n"
                        "🍪 био, з — отобразить опыт с жертв\n"
                        "🍪 к — подсчитать стоимость прокачек\n"
                        "🍪 <code>{0}pref</code> — записывает префикс дова\n"
                        "🍪 <code>{0}ids</code> <code>{0}id</code> — чекает айди по реплаю\n"
                        "🍪 <code>{0}dov</code> — вывод дов команд\n"
                        "🆕 список жертв — вывод списка сохранённых жертв\n"
                        "🆕 топ жертв — вывод списка топ жертв\n"
                        "🆕 <code>{0}nik</code> — добавление имён жертв\n"
                        "🆕 бол, болезни — вывод ваших болезней\n"
                        "🆕 жд — ручное сохранение\n\n"

                        "🔖 <code>{0}помощь инфо</code> - сохраненные данные модуля \n",
        'bio.info':
            '⚙️ Небольшая информация: \n\n'
            '📊 Жертв в зарлисте: {} \n'
            '🧬 Ежедневная премия: {} био-ресурса\n'
            '🖍 Известных: {} \n'
            '🍪 Доверенных пользователей: {}',

        "bio.zar": "тут пусто",
        "bio.dov": "тут пусто",
        'bio.dov.levels':
            '⚙️ Информация об уровнях доверки: \n\n'
            '🔧 Существует 4 уровня доверки \n\n'
            '🍪 1 уровень: \n'
            '   <i>Возможности</i>: Доступ к заражениям | вакцина | доступ к зарлисту \n'
            '🍪 2 уровень: \n'
            '   <i>Возможности</i>: Управление зарлистом | просмотр жертв \n'
            '🍪 3 уровень: \n'
            '   <i>Возможности</i>:  болезни | мешок | чек навыков \n'
            '🍪 4 уровень: \n'
            '   <i>Возможности</i>: Фулл лаба | смена (пата|лабы) | включать вирусы | прокачка навыков \n\n'
            '🔖 Примечание: \n'
            'Всем овнерам автоматически ставится 4 уровень доверки \n',
        # Все что относится к доверке
        "dov": "⚙️ Информация по доверке\n\n🗺 Доверенный префикс: <code>{1}</code>\n\n"
               "📌 Команды dov:\n"
               "🍪 <code>{0}dov dovs</code> — список доверенных пользователей \n"
               "🍪 <code>{0}dov prefs</code> — список доверенных вам пользователей \n"
               '🍪 <code>{0}dov set</code> — добавить|Удалить саппорта \n'
               "🍪 <code>{0}dov set</code> — добавить| повысить/Понизить уровень доверки\n"
               "🍪 <code>{0}dov nik</code> [ник] — сменить доверенный префикс \n"
               "🍪 <code>{0}dov st</code> — включение/выключение доверки \n"
               "🆗 Статус доверки: {3} \n\n"
               "🔖 <code>{0}помощь доверка -уровни</code> — Подробнее об уровнях доверки:",

        'dov.users': '📊 Список доверенных пользователей: \n' \
                     '{}',
        "dov.users.chat": '📊 Список доверенных пользователей в беседе: \n' \
                          '{}',
        "dov.prefs": '📊 Список доверивших пользователей в боте: \n'
                     '{}',
        "dov.prefs.chat": '📊 Список доверевших пользователей в чате: \n' \
                          '{}',

        # Команды доверки
        "dov.rem": "✅ Пользователь <code>@{}</code> успешно удалён из доверенных",
        "dov.add":
            "✅ Пользователь <code>@{}</code> <b>успешно назначен доверенным \n"
            "❌ Уровень доверки: {}",
        'dov.edit_level':
            '🍪 Уровень доверки у <code>@{}</code> был изменён \n'
            '✅ <b> <s>{}</s> ⇨ {}</b>',
        "nick.rename": "" \
                       "✅ Доверенный префикс успешно сменён <s>{0}</s> ⇨ <b><code>{1}</code></b>",
        "dov.status.True": "✅ Доверка запущена",
        "dov.status.False": "❎ Доверка приостановлена",
        # Ошибки
        "no.reply": "🙄 Отсуствует реплай",
        "no.args": "🙄 Отсуствуют нужные аргументы",
        "no.args_and_reply": "📋 Справка по команде 'бей':\n\n"
                             "🖊 Данная команда умеет заражать как указанную жертву в своих параметрах, так и целый список жертв, которые были прикреплены к команде.\n\n"
                             "🖍 При запуске заражения по списку, команда принимает номер уникального пользователя из приложенного сообщения; если этот параметр не указать, то будет заражаться весь список.\n\n"
                             "🖋 Команда поддерживает несколько номеров жертв через пробелы и интервалы, например, 'бей 2 3 5-10'",
        "args_error": '🙄 Аргументы введены неправильно',
        "len_error": "📘 Превышено допустимое количество символов. Лимит 8 символов",
        "hueta": "😶 Тебе не кажется что тут что-то не так?",
        # просто слова
        "messages.biotop": [
            "📖 Список известных заражений:\n",
        ],
        'messages.misc': [
            "📖 Список известных заражений:\n",
        ],
        'wrong_click': [
            '🔞 Тебе тут делать нечего..',
            '⚠️ НЕ ТРОЖЬ ЧУЖИЕ КНОПКИ',
            'Пальцы отрежу и собакам отдам',
            "⚠️ Любопытной Варваре на базаре нос оторвали ",
        ],
        "get_user": "🚀Пользователь: \n"
                    "🥷🏻 <a href='tg://openmessage?user_id={}'>{}</a> \n"
                    "📃 Юзернейм: @{} \n"
                    "🆔 Айди: <code>@{}</code>",

        'calc_formul': {
            'zar': 2.5,
            'imun': 2.45,
            'sb': 2.1,
            'kvala': 2.6,
            'pat': 2,
            'letal': 1.95
        }

    }

    # -----------------------Functions-------------------

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Режим био",
                True,
                "Режим команды био\n"
                # лень читать валидаторы хикки, да и зачем больше 2х мОдов)
                "True - Первый, False - Второй",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Вкл/Выкл доверки",
                True,
                "Статус доверки",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Автозапись жертв",
                True,
                "Автозапись жертв",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Тихое сохранение",
                True,
                "Сообщения о сохранении в логи уровня WARNING (30)",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Автохилл",
                True,
                "Автохилл(БЕТА) \nМожет работать некоректно",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Удаление смс",
                False,
                "Автоудаление смс содержащих инлайн клавиатуру",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Временная зона",
                "Europe/Moscow",
                "",
                validator=Timezone_Validator(),
            ),
            loader.ConfigValue(
                'Аргументы лабы',
                'p np be br f',
                'Аргументы для стандартного вывода лабы',
                validator=loader.validators.String(),
            ),
            # loader.ConfigValue(
            #    "Сохранение ников",
            #    False,
            #    "Автоматическое сохранение ников",
            #    validator=loader.validators.Boolean(),
            # ),
        )
        self.tz = self.config['Временная зона']

    async def client_ready(self, client, db):
        # Nummod + BioWars
        self.client = client
        self.db = db
        # NumMod
        if not self.db.get("NumMod", "numfilter"):
            # Добвление овнеров юб в список доверевшихся людей
            # Айди аккаунта там тоже присуствуе
            owners = list(getattr(self.client.dispatcher.security, "owner"))
            self.db.set(
                "NumMod",
                "numfilter",
                {"users": owners, "filter": None, "status": False},
            )
        # infList        # infList
        if not self.db.get("NumMod", "infList"):
            self.db.set("NumMod", "infList", {})

        if not self.db.get("BioWars", "DovUsers"):
            # Добавление овнеров юб в список доверевшихся людей
            # Айди аккаунта там тоже присуствуе
            owners = list(getattr(self.client.dispatcher.security, "owner"))
            users = {}
            for i in self.db.get("NumMod", "numfilter")["users"]:
                users[str(i)] = 1
            for i in owners:
                users[str(i)] = 4
            self.db.set("BioWars", "DovUsers", users)

        if not self.db.get('BioWars', 'FamousUsers'):
            self.db.set('BioWars', 'FamousUsers', {})
            # {id : username }
        if not self.db.get('BioWars', 'LastInfect'):
            self.db.set('BioWars', 'LastInfect', None)

        if not self.db.get('BioWars', 'InfectionBefore'):
            self.db.set('BioWars', 'InfectionBefore', {})

        if not self.db.get('BioWars', 'YourLetal'):
            self.db.get('BioWars', 'YourLetal', 1)
            # Ваш летал, будет использоватся при записи жертв в зарлист
        if not self.db.get('BioWars', 'UsersNik'):
            self.db.set('BioWars', 'UsersNik', {})
            # user_id : желаемый ник
        if not self.db.get('BioWars', 'FamousPrefs'):
            self.db.set('BioWars', 'FamousPrefs', {})
            # user_id : pref
        # При заражении ставится True
        # Статус заражения
        self.db.set("BioWars", "infStatus", False)
        # Интервал между заражениями
        self.db.set("BioWars", "infInterval", 5)
        # Для определения кд # 'id': 'time'
        if not self.db.get('BioWars', 'Cooldown'):
            self.db.set('BioWars', 'Cooldown', {})
        # автохилл
        if not self.get('AutoHill') or not isinstance(self.get('AutoHill'), str):
            self.set('AutoHill', '26/03/2023 09:00:00')
        if not self.db.get('BioWars', 'Diseases'):
            """Для кастомной версии 'мои болезни"""
            self.db.set('BioWars', 'Diseases', {})

        self.zl = self.db.get("NumMod", "infList")
        self.zl_do = self.db.get('BioWars', 'InfectionBefore')
        self.bol = self.db.get('BioWars', 'Diseases')
        self.fau = self.db.get('BioWars', 'FamousUsers')
        self.dovs = self.db.get("BioWars", "DovUsers")
        self.niks = self.db.get('BioWars', 'UsersNik')
        self.prefs = self.db.get('BioWars', 'FamousPrefs')
        self.letal = self.db.get('BioWars', 'YourLetal')
        self._cooldown = self.db.get('BioWars', 'Cooldown')
        # await self.subscibe_channel()

    @loader.loop(interval=(60 * 60), autostart=True)
    async def loop(self):
        for key, value in self._cooldown.copy().items():
            """очищает бд от неактуальных"""
            cd_time = datetime.strptime(value, DT_FORMAT)
            cd_time = str(
                (cd_time - datetime.now())).split('.')[0]
            if '-' in cd_time:
                del self._cooldown[key]

        # for _ in self.get('messages_for_clear', []):
        #    """удаляет сообщения, которые не удалось удалить во время conversation"""
        #    with contextlib.suppress(Exception):
        #        await self.client.delete_messages(_[0], _[1])

    def save_victim(self, user: Union[str, int], exp: int):
        user = str(user)
        letal = self.letal if self.letal != 1 else None

        if user in self.zl.keys():
            del self.zl

        self.zl[user] = {
            'exp': _exp(exp),
            'date': datetime.now().timestamp(),
            'date_to': (datetime.now() + timedelta(days=letal)).timestamp() if letal else None,
        }

    def get_victim(user: Union[str, int]):
        user = str(user)
        if user not in self.zl.keys():
            return False

        return {'id': int(user), **self.zl[user]}

    async def last_msg(self, message: Message):
        """
        Возвращает последнее сообщение в чате
        """
        return [
            _ async for _ in self._client.iter_messages(
                message.peer_id, 1, max_id=message.id
            )
        ][0]

    async def zar_search(self, message: Message, user: str) -> None:

        if not user[1:].isdigit():
            r = await self.return_user(username=user.lower())
            if r == 'FloodWait':
                await message.reply('флудвейт, ищи по айди')
                # return 'FloodWait'
                return
            elif r == 'ValueError':
                await message.reply(self.strings('_z.nf').format(user))
                # return 'ValueError'
                return
            else:
                user = '@' + str(r)

        user_id = user
        if user not in self.zl.keys():
            return await self.fwib(message, self.strings('z.nf').format(user), user_id)

        user = self.zl[user]
        infectBefore = self.db.get(
            'BioWars', 'InfectionBefore')
        zar_do = infectBefore[user_id] if user_id in infectBefore else 'Неизвестно'
        niks = self.db.get('BioWars', 'UsersNik')

        if str(user_id[1:]) in niks.keys():
            nik = niks[str(user_id[1:])]
            usr = f'<a href="tg://openmessage?user_id={user_id[1:]}">{utils.escape_html(nik)}</a>'
        else:
            usr = f'<code>{user_id}</code>'

        if cd := await self.cooldown(user_id[1:]):
            emj = time_emoji(cd)
            cd = f'| {emj} {cd}'
            r = await message.get_reply_message()

        text = self.strings('_zar.search').format(
            usr, user[0], cd, zar_do)

        if cd:
            await message.respond(
                text,
                reply_to=r if r else message,
                link_preview=False)
        else:
            await self.fwib(message, text, user_id)

    async def fwib_markups(self, message: Message, text: str, user: str) -> 'reply_markup':  # type: ignore
        """
        инлайн кнопки для fwib() и _fwib()
        list[list[dict{}]]
        """
        return [
            [
                {
                    'text': f'Заразить {user}',
                    'callback': self._fwib,
                    'args': (message, text, user, 0)
                },
            ],
            [
                {
                    'text': f'Закрыть',
                    'callback': self.inline__close
                },
            ]
        ]

    async def fwib(self, message: Message, text: str, user: str) -> None:
        """Отправляет форму с инлайн кнопками для заражения"""
        a = await self.inline.form(
            text,
            reply_markup=(await self.fwib_markups(message, text, user)),
            message=message,
            disable_security=True,
            silent=True
        )
        # По истечению времени удаляет сообщение
        if self.config['Удаление смс']:
            await asyncio.sleep(300)
            with contextlib.suppress(Exception):
                await a.delete()

    async def fwib_upd(self, call: InlineCall, message: Message, text: str, user: str):
        await call.edit(
            text,
            reply_markup=(await self.fwib_markups(message, text, user)),
            disable_security=False,
        )

    async def _fwib(self, call: InlineCall, message: Message, text: str, user: str, attempts: int) -> None:
        """Обработчик нажатий на инлайн кнопки"""
        if str(call['from']['id']) not in self.dovs.keys():
            return await call.answer(choices(self.strings('wrong_click'))[0])

        call_upd = asyncio.create_task(
            self.fwib_upd(call, message, text, user)
        )

        if self.db.get("BioWars", "infStatus"):
            await message.reply('❎ Заражения еще не завершены')
            return await asyncio.gather(call_upd)

        if self.config['Удаление смс']:
            await call.delete()

        await self.autohill(message)
        await asyncio.gather(call_upd)

        self.db.set("BioWars", "infStatus", True)
        attempts = f' {attempts}' if attempts else ''

        r = await message.get_reply_message()
        if m := (
                await self.client.send_message(
                    message.peer_id,
                    f'заразить{attempts} {user}',
                    reply_to=r if r else message,
                    # reply_to=message,
                    link_preview=False
                )
        ).out:
            await self.save_last_infect(user)
            self.db.set("BioWars", "infStatus", False)
            # При нажатии на кнопку заразить, удаляет сообщение с чеком жертвы
        await asyncio.gather(call_upd)
        return

    async def cooldown(self, user: str, write: bool = False) -> str:
        date_now = datetime.now()
        if write:
            self._cooldown[user] = (
                    date_now + timedelta(hours=6)).strftime(DT_FORMAT)
            return True

        if user not in self._cooldown.keys():
            return ''

        cd_time = datetime.strptime(self._cooldown[user], DT_FORMAT)
        cd_time = str(
            (cd_time - date_now)).split('.')[0]

        return '' if '-' in cd_time else cd_time

    async def autohill(self, message: Message, reset: bool = False, write: int = False) -> bool:
        """Автоматически покупает вакцину при заражении"""
        if not self.config['Автохилл']:
            return True

        def Reset():
            return self.set('AutoHill', '26/03/2023 09:00:00')

        date = self.get('AutoHill', '26/03/2023 09:00:00')
        fever_date = datetime.strptime(date, DT_FORMAT)

        if write is not False:
            fever_date_to = (datetime.now() + timedelta(minutes=write))

            if fever_date_to < fever_date:
                return False

            return self.set('AutoHill', fever_date_to.strftime(DT_FORMAT))

        if reset:
            return Reset()

        if datetime.now() > fever_date:
            return True

        sms = await message.reply('хилл...')

        while datetime.now() < fever_date:
            if re.search(
                    r'📝 У вас нет горячки. Нет необходимости покупать вакцину|'
                    r'💉 Вакцина излечила вас от горячки|'
                    r'📝 У вас нет столько био-ресурсов или ирис-коинов',
                    (hill_sms := await self.message_q('!купить вакцину', timeout=5))
            ):
                break

        Reset()
        with contextlib.suppress(FloodWaitError):
            await sms.edit(sms.text + '\n' + hill_sms)

        await asyncio.sleep(1.9)
        return True

    async def send(self, text: str, message: Message) -> None:
        """
        Если возникает ошибка при отправке сообщения с инлайн клавиатурой, 
        то отправляется обычное сообщение с таким же текстом
        """
        try:
            sms = await asyncio.wait_for(
                self.inline.form(
                    text, message,
                    {
                        'text': 'Закрыть',
                        'callback': self.inline__close
                    },
                    disable_security=True
                ),
                timeout=(4)
            )
        except TimeoutError:
            sms = await message.reply(text)

        if not self.config['Удаление смс']:
            return

        with contextlib.suppress(Exception):
            await asyncio.sleep(300)
            await sms.edit('\xad')
            await sms.delete()

    async def inline__close(self, call) -> None:
        """убирает весь текст из инлайн формы и удаляет ее"""
        if not (
                str(call['from']['id']) in self.dovs.keys()
                and self.dovs[str(call['from']['id'])] >= 3
        ):
            return await call.answer(choices(self.strings('wrong_click'))[0])

        await call.edit('\xad')
        await call.delete()

    async def return_user(self, username: str, without_resolve: bool = False) -> Union[str, int]:
        if without_resolve:
            for k, v in self.fau.items():
                if not v:
                    continue

                if v.lower() == username:
                    user_id = k
                    return user_id
            return username

        if username.lower() not in self.db.get('BioWars', 'FamousUsers').values():
            r = await self._write_user(username=username)
            if r:
                return r

        famous_users = self.db.get('BioWars', 'FamousUsers')
        for k, v in famous_users.items():
            if not v:
                continue

            if v.lower() == username:
                user_id = k
                return user_id

    async def save_nik(self, user_id: int, nik: str) -> None:
        users_nik = self.db.get('BioWars', 'UsersNik')
        users_nik[str(user_id)] = nik
        self.db.set('BioWars', 'UsersNik', users_nik)

    async def save_pref(self, user_id: int, nik: str) -> None:
        users_nik = self.db.get('BioWars', 'FamousPrefs')
        users_nik[str(user_id)] = nik
        self.db.set('BioWars', 'FamousPrefs', users_nik)

    async def _write_user(self, username: Optional[str] = None, user_id: Optional[int] = None) -> Optional[str]:
        famous_users = self.db.get('BioWars', 'FamousUsers')

        if username and user_id:
            famous_users[user_id] = username.lower()
        # Если есть юзер айди, вытаскиваем юзернейм и сохраняем его
        if not username:
            if user_id not in famous_users.keys():
                try:
                    user = await self.client.get_entity(user_id)
                    username = user.username if user.username else None
                    famous_users[int(user.id)] = username.lower()
                # Если флудвайт
                except FloodWaitError:
                    return 'FloodWait'

                # Если пользователь не найден
                except ValueError:
                    return 'ValueError'
        else:
            # Если есть юзернейм, то вытаскиваем с помощью него юзер айди
            if username not in famous_users.values():
                try:
                    user = await self.client.get_entity(username)
                    user_id = user.id
                    famous_users[int(user_id)] = username.lower()
                # Если флудвайт
                except FloodWaitError:
                    return 'FloodWait'

                # Если пользователь не найден
                except ValueError:
                    return 'ValueError'

        # Сохраняем все
        self.db.set('BioWars', 'FamousUsers', famous_users)
        return None

    async def save_last_infect(self, user: Optional[str]) -> None:

        if user:
            user = user.replace('@', '').replace('https://t.me/', '')
            if not user.isdigit():
                user = await self.return_user(username=user)

        save = user if user else None
        self.db.set('BioWars', 'LastInfect',
                    save)

    # Нужен класс чата, а не айди чата
    async def get_members_chat(self, chat: Channel) -> Union[list, str]:
        offset_user = 0  # номер участника, с которого начинается считывание
        limit_user = 50  # максимальное число записей, передаваемых за один раз

        users = []  # список всех участников канала

        filter_user = ChannelParticipantsSearch('')
        try:
            while True:
                participants = await self.client(GetParticipantsRequest(
                    chat,
                    filter_user,
                    offset_user,
                    limit_user,
                    hash=0))
                if not participants.users:
                    break

                users.extend(participants.users)
                offset_user += len(participants.users)
            ids = [i.id for i in users]
            return ids

        except TypeError:
            return 'NotChat'

    async def _handler_link(self, link) -> Optional[str]:
        if link.startswith(self.strings("link_id")):
            return "@" + link.replace(self.strings("link_id"), "")
        elif link.startswith(self.strings("link_username")):
            return "@" + link.replace(self.strings("link_username"), "")
        else:
            return None

    async def number_convert(self, number: int) -> str:
        if number >= 1000000000:
            return f"{number / 1000000000:.1f}B"
        elif number >= 1000000:
            return f"{number / 1000000:.1f}M"
        elif number >= 1000:
            return f"{number / 1000:.1f}k"
        else:
            return str(number)

    async def get_pref(self) -> str:
        return self.db.get("hikka.main", "command_prefix", ".")

    async def get_lab(self, lab_raw: str, lab_args: list) -> Optional[str]:
        sms = ''
        args = ['d', 's', 'c', 'n', 'p', 'q', 'nk', 'np', 'inf', 'imm',
                'm', 'ss', 'be', 'br', 'so', 'prev', 'i', 'dis', 'f']
        lab_lines = lab_raw.splitlines()

        for arg in lab_args:
            if arg in args:
                for i in lab_lines:  # цикл for по всем строкам в тексте лабы
                    if "🔬 Досье лаборатории" in i and arg == 'd':
                        sms += f"{i}\n"

                    elif "Руководитель" in i and arg == 's':
                        sms += f"{i}\n"
                    elif "В составе Корпорации" in i and arg == 'c':
                        sms += f"{i}\n"
                    elif "🏷 Имя патогена:" in i and arg == 'n':
                        sms += f"{i}\n"
                    elif "🧪 Готовых патогенов:" in i and arg == 'p':
                        s = i.replace("🧪 Готовых патогенов:", "")
                        sms += f"🧪 Пробирок:{s}\n"
                    elif "👨‍🔬 Квалификация учёных:" in i and arg == 'nk':
                        sms += f"{i}\n"
                    elif "⏱ Новый патоген:" in i and arg == 'np':
                        s = i.replace("⏱ Новый патоген:", "")
                        sms += f"⏱ Новая{s}\n"
                    elif "🦠 Заразность:" in i and arg == 'inf':
                        sms += f"{i}\n"
                    elif "🛡 Иммунитет:" in i and arg == 'imm':
                        sms += f"{i}\n"
                    elif "☠️ Летальность:" in i and arg == 'm':
                        sms += f"{i}\n"
                    elif "🕵️‍♂️ Служба безопасности:" in i and arg == 'ss':
                        sms += f"{i}\n"
                    elif "☣️ Био-опыт:" in i and arg == 'be':
                        s = i.replace("☣️ Био-опыт:", "")
                        sms += f"☣️ Опыта:{s}\n"
                    elif "🧬 Био-ресурс:" in i and arg == 'br':
                        s = i.replace("🧬 Био-ресурс:", "")
                        sms += f"🧬 Био-ресурсов:{s}\n\n"
                    elif "😷 Спецопераций:" in i and arg == 'so':
                        sms += f"{i}\n"
                    elif "🥽 Предотвращены:" in i and arg == 'prev':
                        sms += f"{i}\n"
                    elif "🤒 Заражённых:" in i and arg == 'i':
                        sms += f"{i}\n"
                    elif "🤒 Своих болезней:" in i and arg == 'dis':
                        sms += f"{i}\n"
                    elif "❗️ Руководитель в состоянии горячки вызванной болезнью" in i and arg == 'f':
                        s = i.replace(
                            "❗️ Руководитель в состоянии горячки вызванной болезнью", "")
                        sms += f"❗ {s}\n"
                    elif "❗️ Руководитель в состоянии горячки ещё" in i and arg == 'f':
                        s = i.replace("❗️ Руководитель в состоянии горячки ещё ", "")
                        sms += f"️❗️ Горячка ещё {s}\n"
            else:
                sms += f'Неизвестный аргумент: <code>{arg}</code>\n'

        return sms

    async def _generator_links(self, reply, args: str) -> Union[list, str]:
        list_args, lis = [], []
        for i in args.split(" "):
            if "-" in i:
                ot_do = i.split("-")
                try:
                    list_args.extend(
                        str(x) for x in range(int(ot_do[0]), int(ot_do[1]) + 1)
                    )
                except Exception:
                    return "wrong_ot-do"

            else:
                list_args.append(i)

        a = reply.text
        entity = reply.get_entities_text()
        users = []
        # validate_text = await self.validate_text(text)

        for e in entity:
            if isinstance(e[0], MENT):
                url = e[1]
                # if not url.startswith('@'):
                # continue

                users.append(url)

            elif isinstance(e[0], METU):
                url = await self._handler_link(e[0].url)
                users.append(url)

            elif isinstance(i[0], MEU):
                url = await self._handler_link(e[1])
                users.append(url)
        try:
            for arg in list_args:
                lis.append(users[int(arg) - 1])
        except:
            return "wrong_ot-do"

        return lis

    async def _o_generator_links(self, reply: Message) -> Union[list, str]:
        lis = []
        json = Json.loads(reply.to_json())
        try:
            for i in range(len(reply.entities)):
                try:
                    link = json["entities"][i]["url"]
                    if link.startswith("tg"):
                        users = "@" + link.split("=")[1]
                        lis.append(users)
                    elif link.startswith("https://t.me"):
                        a = "@" + str(link.split("/")[3])
                        lis.append(a)
                    else:
                        return "hueta"
                except Exception:
                    blayt = reply.raw_text[
                            json["entities"][i]["offset"]: json["entities"][i]["offset"]
                                                           + json["entities"][i]["length"]
                            ]
                    lis.append(blayt)
            return lis
        except TypeError:
            return "hueta"

    async def get_top_zhertv(self, message: Message, num_list: int) -> None:
        import operator
        # Cортировка зарлиста
        infList = self.db.get('NumMod', 'infList')
        a = {}
        num_list = int(num_list)

        for k, v in infList.items():
            a[k] = int(float((v[0]))) if not 'k' in v[0] else int(
                float(v[0][:-1].replace(',', '.')) * 1000)

        sort = sorted(a.items(), key=operator.itemgetter(1), reverse=True)

        sort_dict = dict(sort)

        zhertvs = dict_split(sort_dict, reverse=False)
        if num_list > len(zhertvs):
            await utils.answer(message, f'❌ Ты указал номер страницы больше максимальной! ({num_list}/{len(zhertvs)})')
            return
        # ------------------------------------------------
        # Генерация текста с жертвами

        infectBefore = self.db.get(
            'BioWars', 'InfectionBefore')
        niks = self.db.get('BioWars', 'UsersNik')
        all_exps = int(sum([eval(i[0].replace(",", ".").replace(
            'k', '*1000')) for i in list(infList.values())]))
        bio_exp = await self.number_convert(all_exps)
        all_exps = '{:,}'.format(all_exps).replace(',', ' ')

        sms = f'📓 Топ ваших «жертв»:\n\n'
        count = 1

        for i in zhertvs[num_list - 1]:
            if not i:
                continue
            user = infList[i]
            zar_do = infectBefore[i] if i in infectBefore.keys(
            ) else 'хз'
            if i[1:] in niks.keys():
                nik = niks[str(i[1:])]
                usr = f'<a href="tg://openmessage?user_id={i[1:]}">{nik}</a>'
            else:
                usr = i
            sms += f'{count}. {usr} | до {zar_do} | +{user[0]}  \n'
            count += 1

        sms += f'\n📊 Итого: {len(infList)} заражённых\n'
        sms += f'🧬 Ежа: {all_exps} био-ресурсов \n'
        sms += f'📖 Страница ({num_list}/{len(zhertvs)})'
        await self.send(sms, message)

    async def get_zhertv(self, message: Message, num_list: int) -> None:
        infList = self.db.get('NumMod', 'infList')
        zhertvs = dict_split(infList)

        # генерация сообщения
        if num_list > len(zhertvs):
            await utils.answer(message, f'❌ Ты указал номер страницы больше максимальной! ({num_list}/{len(zhertvs)})')
            return

        infectBefore = self.db.get('BioWars', 'InfectionBefore')
        niks = self.db.get('BioWars', 'UsersNik')
        all_exps = int(sum([eval(i[0].replace(",", ".").replace(
            'k', '*1000')) for i in list(infList.values())]))
        bio_exp = await self.number_convert(all_exps)
        all_exps = '{:,}'.format(all_exps).replace(',', ' ')

        sms = f'📓 Список «жертв»: \n\n'
        count = 1

        for i in zhertvs[num_list - 1]:
            if not i:
                continue
            user = infList[i]
            zar_do = infectBefore[i] if i in infectBefore.keys(
            ) else 'хз'
            if i[1:] in niks.keys():
                nik = niks[str(i[1:])]
                usr = f'<a href="tg://openmessage?user_id={i[1:]}">{nik}</a>'
            else:
                usr = i
            sms += f'{count}. {usr} | до {zar_do} | +{user[0]}  \n'
            count += 1

        sms += f'\n📊 Итого: {len(infList)} заражённых\n'
        sms += f'🧬 Ежа: {all_exps} био-ресурса\n'
        sms += f'📖 Страница ({num_list}/{len(zhertvs)})'
        await self.send(sms, message)

    async def get_bolezni(self, message: Message, num_list: int) -> None:
        if len((organizers := dict_split(self.bol))) < 1:
            return await message.reply('empty...')

        if len(organizers) < num_list:
            num_list = len(organizers)

        No, sms = 0, f'🤒 Список ваших болезней:\n'  # ({num_list}/{len(organizers)})
        for _ in filter(lambda x: x != None, organizers[num_list - 1]):
            No += 1
            name = '<a href="{}">{}</a>'.format(
                f'tg://openmessage?user_id={_}'
                if _.isdigit() else
                f'https://t.me/{_}',
                self.niks[user] if (user := await self.return_user(
                    _, without_resolve=True)) in self.niks.keys() else _
            )
            a, b, = lambda x: datetime.strptime(
                x, DT_FORMAT), lambda x: f'{x:{DT_FORMAT}}'

            date, date_to = b(await self.ch_tz(a(self.bol[_][1]))), b(await self.ch_tz((a(self.bol[_][2])))).split()[0]

            date = (
                f'сегодня в {date.split()[1][:-3]}'
                if date.split()[0] == b(datetime.now(pytz.timezone(
                    self.config['Временная зона']))).split()[0] else date.split()[0]
            )

            sms += f'{No}. {name} — ☢️ +{self.bol[_][0]} | {date} до {date_to}\n'
            sms += f'{self.bol[_][3]}\n' if self.bol[_][3] else ''

        await self.send(sms, message)

    async def ch_tz(self, datetime: datetime):
        return datetime.astimezone(
            pytz.timezone(self.config['Временная зона'])
        )

    async def bio(self, reply: Message, me: User) -> None:
        infList = self.db.get("NumMod", "infList")
        b = reply.raw_text.splitlines()
        niks = self.db.get('BioWars', 'UsersNik')
        chat_flag, lines_to_pop = isbio(reply.raw_text)
        if chat_flag:
            for _ in range(lines_to_pop):
                b.pop(0)
        else:
            b.pop(0)
        sms = ''
        exps = []
        # Add exp
        for i in b:
            try:
                a = i.split('|')
                if not chat_flag:
                    continue
                exps.append(a[-2])
            except:
                pass

        json = Json.loads(reply.to_json())

        if len(exps) == 0:
            count = 1

            for i in get_ne_pridumal(reply.text, at=True):

                if not i[1:].isdigit():
                    r = await self.return_user(i[1:])
                    if r == 'FloodWait':
                        sms += f'{count}. {i} | Не удалось получить инфу о юз.:Флудвейт \n'
                        count += 1

                        continue
                    elif r == 'ValueError':
                        sms += f'{count}. {i} | ❎ Пользователя не существует! \n'
                        count += 1

                        continue
                    else:
                        i = '@' + str(r)

                if str(i[1:]) == str(me.id):
                    name = me.first_name
                    sms += f'{str(count)}. 🔆 <a href= "tg://openmessage?user_id={me.id}">{name}</a>\n'
                    count += 1
                    continue

                if str(i[1:]) in niks:
                    nik = niks[str(i[1:])]
                    name = f"<a href='tg://openmessage?user_id={i[1:]}'>{nik}</a>"
                else:
                    name = i

                if cd := await self.cooldown(i[1:]):
                    emj = time_emoji(cd)
                    cd_ = f'| {emj} {cd}'
                else:
                    cd_ = ''

                exp = infList[i][0] if i in infList else None

                if not self.config['Режим био']:
                    exp = f'<emoji document_id=5280697968725340044>☢️</emoji> {exp} опыта' if exp else '🆕 Новая жертва'
                    sms += f'{count}. {name} | {exp} {cd_}\n'
                else:
                    exp = f'<emoji document_id=5280697968725340044>☢️</emoji> {exp} опыта' if exp else '🆕 Новая жертва'
                    sms += f'{count}. {name} | {exp} {cd_}\n'
                count += 1
            return sms

        else:
            count = 1
            metu_counter = 0
            for i in range(0, len(b)):
                try:
                    exp = exps[i].replace(",", ".")
                    s = exp.find(' опыт')
                    exp = exp[1:s].replace(' ', '')
                    if 'k' in exp:
                        exp_count = float(exp[:-1])
                        if exp_count < 10.0:
                            exp = int(round(exp_count * 100, 0))

                        else:
                            exp_count = float(exp[:-1])
                            exp_count = int(exp_count)
                            exp = str(exp_count / 10) + 'k'

                    else:
                        exp_count = int(exp)
                        exp = exp_count // 10

                except:
                    exp = None

                while "url" not in list(json["entities"][metu_counter].keys()):
                    metu_counter += 1

                link = json["entities"][metu_counter]["url"]
                metu_counter += 1
                bla = []
                if link.startswith('tg'):
                    for i in link.split('='):
                        bla.append(i)

                    if str(bla[1]) == str(me.id):
                        name = me.first_name
                        sms += f'{str(count)}. 🔆 <a href= "tg://openmessage?user_id={me.id}">{name}</a> | {exp} опыта \n'
                        count += 1
                        continue

                    user_id = bla[1]
                    if '@' + str(user_id) in infList:
                        if chat_flag:
                            user = infList['@' + str(user_id)]
                            usr_exp = user[0].replace(',', '.')
                            exp_count = str(exp)

                            if usr_exp[-1] == 'k':
                                usr_exp = float(usr_exp[:-1]) * 1000

                            if exp_count[-1] == 'k':
                                exp_count = float(exp_count[:-1]) * 1000

                            result = int(float(exp_count) - float(usr_exp))

                            # abc.append(str(result))

                            if result > 0:
                                if result < 1000:
                                    result = f'(✅ +{str(result)})'
                                else:
                                    result = f'(✅ +{str(round(float(result) / 1000, 1))}k)'
                            elif result == 0:
                                result = f' 🟰 [{str(result)}]'

                            else:
                                if result > -1000:
                                    result = f'(❌ {str(result)})'
                                else:
                                    result = f'(❌ {str(round(float(result) / 1000, 1))}k)'

                            if not self.config['Режим био']:
                                zh = f" {result}"
                            else:
                                zh = f"{user[0]} опыта {result}"
                        else:
                            zh = f"<emoji document_id=5280697968725340044>☢️</emoji> (+{infList['@' + str(user_id)][0]})"
                    else:
                        if chat_flag:  # если это чат и жертвы нет в зарлисте
                            exp_count1 = str(exp)
                            if exp_count1[-1] == 'k':
                                exp_count1 = float(exp_count1[:-1]) * 1000

                            if round(float(exp_count1), 1) < 10000.0:  # +{}к
                                zh = f' 🆕 +{round(float(exp_count1) / 1000, 1)}k'
                            else:  # + {}
                                zh = f' 🆕 +{round(float(exp_count1) / 1000, 1)}k'
                        else:
                            zh = ''

                    if cd := await self.cooldown(str(bla[1])):
                        zh += f' {time_emoji(cd)}'

                    try:
                        if str(bla[1]) in niks:
                            nik = niks[str(bla[1])]
                            name = f"<a href='tg://openmessage?user_id={bla[1]}'>{nik}</a>"
                        else:
                            name = '@' + str(bla[1])

                        exp = f'| {exp}'
                        # sms += f'{str(count)}.\n {name}\n {zh}\n {exp} опыта \n'

                        if not self.config['Режим био']:
                            sms += f'{count}. {name} | {zh} \n'
                        else:
                            sms += f'{str(count)}. {name} | {zh} \n'

                    except:
                        if str(bla[1]) in niks:
                            nik = niks[str(bla[1])]
                            name = f"<a href='tg://openmessage?user_id={bla[1]}'>{nik}</a>"
                        else:
                            name = '@' + str(bla[1])

                        exp = f'| {exp}'
                        # sms += f'{str(count)}.\n {name}\n {zh}\n {exp} опыта \n'

                        if not self.config['Режим био']:
                            sms += f'{count}. {name}  |{zh} \n'
                        else:
                            sms += f'{str(count)}. {name} | {zh} \n'

                count += 1
            return sms

        # -------------------------------------------------------------------------------------------------------------------------#
        return
        infList = self.db.get("NumMod", "infList")
        b = reply.raw_text.splitlines()
        niks = self.db.get('BioWars', 'UsersNik')
        chat_flag = True if '🔬 ТОП ЛАБОРАТОРИЙ' in b[0] or '🏢 УЧАСТНИКИ КОРПОРАЦИИ' in b[0] else False
        b.pop(0)
        sms = ''
        exps = []
        # Add exp
        for i in b:
            try:
                a = i.split('|')
                if not chat_flag:
                    continue
                exps.append(a[-2])
            except:
                pass

        json = Json.loads(reply.to_json())

        if len(exps) == 0:

            entity = reply.get_entities_text()
            users = []

            for e in entity:
                if isinstance(e[0], MENT):
                    url = e[1]
                    users.append(url)

                elif isinstance(e[0], METU):
                    url = await self._handler_link(e[0].url)
                    users.append(url)

                elif isinstance(e[0], MEU):
                    url = await self._handler_link(e[1])
                    users.append(url)

            count = 1

            for i in users:

                if not i[1:].isdigit():
                    r = await self.return_user(i[1:])
                    if r == 'FloodWait':
                        sms += f'{count}. {i} | Не удалось получить инфу о юз.:Флудвейт \n'
                        count += 1

                        continue
                    elif r == 'ValueError':
                        sms += f'{count}. {i} | ❎ Пользователя не существует! \n'
                        count += 1

                        continue
                    else:
                        i = '@' + str(r)

                if str(i[1:]) == str(me.id):
                    name = me.first_name
                    sms += f'{str(count)}. 🔆 <a href= "tg://openmessage?user_id={me.id}">{name}</a>\n'
                    count += 1
                    continue

                if str(i[1:]) in niks:
                    nik = niks[str(i[1:])]
                    name = f"<a href='tg://openmessage?user_id={i[1:]}'>{nik}</a>"
                else:
                    name = i

                if cd := await self.cooldown(i[1:]):
                    emj = time_emoji(cd)
                    cd_ = f'| {emj} {cd}'
                else:
                    cd_ = ''

                exp = infList[i][0] if i in infList else None

                if not self.config['Режим био']:
                    exp = f'<emoji document_id=5280697968725340044>☢️</emoji> {exp} опыта' if exp else '🆕 Новая жертва'
                    sms += f'{count}. {name} | {exp} | {cd_}\n'
                else:
                    exp = f'<emoji document_id=5280697968725340044>☢️</emoji> {exp} опыта' if exp else '🆕 Новая жертва'
                    sms += f'{count}. {name} | {exp} | {cd_}\n'
                count += 1
            return sms

        else:
            count = 1
            for i in range(0, len(b)):
                try:
                    exp = exps[i].replace(",", ".")
                    s = exp.find(' опыт')
                    exp = exp[1:s].replace(' ', '')
                    if 'k' in exp:
                        exp_count = float(exp[:-1])
                        if exp_count < 10.0:
                            exp = int(round(exp_count * 100, 0))

                        else:
                            exp_count = float(exp[:-1])
                            exp_count = int(exp_count)
                            exp = str(exp_count / 10) + 'k'

                    else:
                        exp_count = int(exp)
                        exp = exp_count // 10

                except:
                    exp = None

                link = json["entities"][i]["url"]
                bla = []
                if link.startswith('tg'):
                    for i in link.split('='):
                        bla.append(i)

                    if str(bla[1]) == str(me.id):
                        name = me.first_name
                        sms += f'{str(count)}. 🔆 <a href= "tg://openmessage?user_id={me.id}">{name}</a> | {exp} опыта \n'
                        count += 1
                        continue

                    user_id = bla[1]
                    if '@' + str(user_id) in infList:
                        if chat_flag:
                            user = infList['@' + str(user_id)]
                            usr_exp = user[0].replace(',', '.')
                            exp_count = str(exp)

                            if usr_exp[-1] == 'k':
                                usr_exp = float(usr_exp[:-1]) * 1000

                            if exp_count[-1] == 'k':
                                exp_count = float(exp_count[:-1]) * 1000

                            result = int(float(exp_count) - float(usr_exp))

                            # abc.append(str(result))

                            if result > 0:
                                if result < 1000:
                                    result = f'(✅ +{str(result)})'
                                else:
                                    result = f'(✅ +{str(round(float(result) / 1000, 1))}k)'
                            elif result == 0:
                                result = f' 🟰 [{str(result)}]'

                            else:
                                if result > -1000:
                                    result = f'(❌ {str(result)})'
                                else:
                                    result = f'(❌ {str(round(float(result) / 1000, 1))}k)'

                            if not self.config['Вкл/Выкл Био']:
                                zh = f" {result}"
                            else:
                                zh = f"{user[0]} опыта {result}"
                        else:
                            zh = f"<emoji document_id=5280697968725340044>☢️</emoji> (+{infList['@' + str(user_id)][0]})"
                    else:
                        if chat_flag:  # если это чат и жертвы нет в зарлисте
                            exp_count1 = str(exp)
                            if exp_count1[-1] == 'k':
                                exp_count1 = float(exp_count1[:-1]) * 1000

                            if round(float(exp_count1), 1) < 10000.0:  # +{}к
                                zh = f' 🆕 +{round(float(exp_count1) / 1000, 1)}k'
                            else:  # + {}
                                zh = f' 🆕 +{round(float(exp_count1) / 1000, 1)}k'
                        else:
                            zh = ''

                    if cd := await self.cooldown(str(bla[1])):
                        zh += f' {time_emoji(cd)}'

                    try:
                        if str(bla[1]) in niks:
                            nik = niks[str(bla[1])]
                            name = f"<a href='tg://openmessage?user_id={bla[1]}'>{nik}</a>"
                        else:
                            name = '@' + str(bla[1])

                        exp = f'| {exp}'
                        # sms += f'{str(count)}.\n {name}\n {zh}\n {exp} опыта \n'

                        if not self.config['Режим био']:
                            sms += f'{count}. {name} | {zh} \n'
                        else:
                            sms += f'{str(count)}. {name} | {zh} \n'

                    except:
                        if str(bla[1]) in niks:
                            nik = niks[str(bla[1])]
                            name = f"<a href='tg://openmessage?user_id={bla[1]}'>{nik}</a>"
                        else:
                            name = '@' + str(bla[1])

                        exp = f'| {exp}'
                        # sms += f'{str(count)}.\n {name}\n {zh}\n {exp} опыта \n'

                        if not self.config['Режим био']:
                            sms += f'{count}. {name} | {zh} \n'
                        else:
                            sms += f'{str(count)}. {name} | {zh} \n'

                count += 1
            return sms

    async def message_q(  # отправляет сообщение боту и возращает ответ
            self,
            text: str,
            bot_id: int = 5443619563,
            mark_read: bool = True,
            delete: bool = True,
            timeout: int = None,
    ) -> str:
        """Отправляет сообщение и возращает ответ"""
        async with self.client.conversation(bot_id, exclusive=False) as conv:
            await conv.cancel_all()

        async with self.client.conversation(bot_id, exclusive=False, timeout=timeout) as conv:
            try:
                a = self.get('messages_for_clear', [])

                msg = await conv.send_message(text)
                a.append([msg.chat_id, msg.id])

                response = await conv.get_response()
                a.append([response.chat_id, response.id])

                if mark_read:
                    await conv.mark_read()
                if delete:
                    await msg.delete()
                    await response.delete()
                return response.text
            except TimeoutError:
                return "Timeout"

    # -----------------------Commands in watcher----------

    async def z_command(self, message: Message, args_raw: str, text: str, reply: Message) -> None:
        if self.db.get("BioWars", "infStatus"):
            await message.reply('⚠️ Другие заражения уже запущены')
            return

        if not args_raw and not reply:  # .z - аргументов нет
            text = self.strings("no.args_and_reply")
            await utils.answer(message, text)
            return

        if (reply and not args_raw):
            rt = reply.text
            entity = reply.get_entities_text()

            if rt.startswith(r"🕵️‍♂️ Служба безопасности лаборатории") or rt.startswith(
                    r"🕵️‍♂️ Служба безопасности Вашей лаборатории"):
                user = await self._handler_link(entity[1][0].url)

            elif '<a href="tg://user?id=' in rt:
                href1 = rt.find('<a href="tg://user?id=') + \
                        len('<a href="tg://user?id=')
                href2 = rt.rfind('">')

                user = '@' + rt[href1:href2]

            elif '@' in rt:
                for i in entity:
                    if i[1].startswith('@'):
                        user = i[1]
                        break

            elif '<a href="tg://openmessage?user_id=' in rt:
                href1 = rt.find('tg://openmessage?user_id=') + \
                        len('tg://openmessage?user_id=')
                href2 = rt.find('">')

                user = '@' + rt[href1:href2]

            elif '<a href="https://t.me/' in rt:
                href1 = rt.find('<a href="https://t.me/') + \
                        len('<a href="https://t.me/')
                href2 = rt.find('">')
                user = '@' + rt[href1:href2]

            else:
                user = '@' + str(reply.sender_id)

            await self.autohill(message)
            await message.reply(f'заразить {user}')
            await self.save_last_infect(user)

            return

        if reply and args_raw == 'о':

            ids = await self._o_generator_links(reply)
            self.db.set("BioWars", "infStatus", True)

            await asyncio.sleep(0.3)
            await message.client.send_message(
                message.peer_id, f"заразить {ids[0]}", reply_to=reply
            )

            for i in ids[1:]:
                interval = self.db.get("BioWars", "infInterval")
                await asyncio.sleep(interval)
                await message.client.send_message(
                    message.peer_id, f"заразить {i}", reply_to=reply
                )
            else:
                await asyncio.sleep(1)
                await message.reply('✅ Заражения окончены')

            self.db.set("BioWars", "infStatus", False)
            return

        if reply and args_raw:
            r = await self._generator_links(reply, args_raw)
            if r == "wrong_ot-do":
                await message.reply('Ошибка использование команды от-до')
                return

            users = r

            if len(users) == 1:

                self.db.set("BioWars", "infStatus", True)
                await message.reply(f"заразить {users[0]}")

                await self.save_last_infect(users[0])
                self.db.set("BioWars", "infStatus", False)

            else:
                self.db.set("BioWars", "infStatus", True)
                await asyncio.sleep(0.3)
                await message.reply(f"заразить {users[0]}", )

                for infect in users[1:]:
                    if self.db.get("BioWars", "infStatus"):
                        interval = self.db.get("BioWars", "infInterval", 4)
                        await self.autohill(message)
                        interval = self.db.get("BioWars", "infInterval", 4)
                        await asyncio.sleep(interval)
                        await self.save_last_infect(infect)
                        await message.reply(f"заразить {infect}")
                    else:
                        return
                else:
                    await asyncio.sleep(1)
                    await message.reply('✅ Заражения окончены')

                self.db.set("BioWars", "infStatus", False)
                return

    async def id_command(self, message: Message, args: str, reply) -> None:
        if not args and not reply:
            user = await self.client.get_me()

        elif reply:
            user_id = reply.sender_id
            user = await message.client.get_entity(user_id)

        elif args.startswith("@"):
            if args[1:].isdigit():
                user_id = int(args[1:])
            else:
                user_id = args[1:]

            user = await message.client.get_entity(user_id)
        else:
            return

        username = user.username if user.username else "Отсуствует"
        await self.write_user(username.lower(), user.id)
        await self.client.send_message(
            message.chat_id,
            self.strings("get_user").format(
                user.id, user.first_name, username, user.id
            ),
            reply_to=reply,
        )

    async def ids_command(self, message: Message, args_raw: str, reply) -> None:
        if not reply:
            await utils.answer(message, self.strings("no.reply"))
            return
        ids = (
            await self._generator_links(reply, args_raw)
            if args_raw
            else await self._o_generator_links(reply)
        )
        for i in ids:
            await message.client.send_message(
                message.peer_id, f".ид {i}", reply_to=reply
            )
            await asyncio.sleep(3.5)
        else:
            await message.respond("✅ Все айди прочеканы")

    async def dov_command(
            self, message: Message, args_list: list, args_raw: str, reply
    ) -> None:

        numfilter = self.db.get("NumMod", "numfilter")
        biowars_dovs = self.db.get("BioWars", "DovUsers")
        pref = await self.get_pref()

        if not args_raw and not reply:
            status_emj = "▶️" if self.config["Вкл/Выкл доверки"] else "⏸"
            status = "Включено" if self.config["Вкл/Выкл доверки"] else "Выключено"
            nik = numfilter["filter"] if numfilter["filter"] else "Не   установлен"

            text_message = self.strings("dov").format(
                pref, nik, status_emj, status
            )
            await self.send(text_message, message)
            return

        if args_list[0].lower() == "set":
            # Если 2 аргумента то ставим первый уровень, если 3 аргументы и 3 типа инт ставим уровень указанный в нем

            level = None
            data = args_list[1:]
            logging.info(f'{data}')
            if reply:
                user_id = str(reply.sender_id)
                if data:
                    level = int(data[0]) if data[0].isdigit() else None
                if not level:
                    level = None

            elif re.fullmatch(r"@\d+", data[0]):
                user_id = data[0].replace('@', '')
                # try:
                if len(data) >= 2:
                    level = int(data[1]) if data[1].isdigit() else None
                if not level:
                    level = None
                # except Exception:
                # await utils.answer(message, self.strings('args_error'))
                # return
            else:
                await utils.answer(message, self.strings('args_error'))
                return
            # Я знаю что in распостраняется только на user_id

            if level and user_id in biowars_dovs.keys():
                old_level = biowars_dovs[user_id]
                biowars_dovs[user_id] = level
                self.db.set("BioWars", "DovUsers", biowars_dovs)
                await utils.answer(message, self.strings('dov.edit_level').format(user_id, old_level, level))

                return

            elif str(user_id) in biowars_dovs.keys():
                numfilter["users"].remove(str(user_id))
                biowars_dovs.pop(user_id)
                self.db.set("BioWars", "DovUsers", biowars_dovs)
                await utils.answer(message, self.strings("dov.rem").format(user_id))
                return
            else:
                logging.info(
                    f'{user_id} - {level}')
                level = level if level else 1
                numfilter["users"].append(user_id)
                biowars_dovs[user_id] = level
                text_message = self.strings("dov.add").format(user_id, level)
                self.db.set("BioWars", "DovUsers", biowars_dovs)

                await utils.answer(message, text_message)
                return

        elif args_list[0].lower() == "nik":
            if args_list[1]:
                if len(args_list[1]) > 8 or len(args_list) >= 3:
                    await utils.answer(message, self.strings("len_error"))
                    return

                old_nik = numfilter["filter"] if numfilter["filter"] else "Отсуствует"
                nik = args_list[1]
                numfilter['filter'] = nik
                self.db.set("NumMod", "numfilter", numfilter)
                await utils.answer(message,
                                   self.strings("nick.rename").format(
                                       old_nik, nik)
                                   )

            else:
                await utils.aswer('Какой ник будем ставить?')
                return

        elif args_list[0].lower() == "dovs":
            niks = self.db.get('BioWars', 'UsersNik')

            dovs_users = ''

            if len(args_list) > 1 and args_list[1].lower() == 'chat':
                r = await self.get_members_chat(message.chat)
                if r == 'NotChat':
                    await utils.answer(message, 'Это не чат')
                    return
                else:
                    users = r
                i = 1
                for user in users:
                    if str(user) in biowars_dovs.keys():
                        level = biowars_dovs[str(user)]

                        level = '❗️ (полный доступ)' if level == 4 else f'{level} ур'

                        if str(user) in niks.keys():
                            nik = niks[str(user)]
                            usr = f'<a href="tg://openmessage?user_id={user}">{nik}</a>'
                        else:
                            usr = f'<code>@{user}</code>'

                        dovs_users += f'{i}) {usr} - {level} \n'
                        i += 1
                dovs_users = dovs_users if dovs_users else 'В этом чате никого нет'

                await self.send(self.strings('dov.users.chat').format(dovs_users), message)
                return
            for i, (user_id, level) in enumerate(biowars_dovs.items(), start=1):

                level = '❗️ (полный доступ)' if level == 4 else f'{level} ур'

                if str(user_id) in niks.keys():
                    nik = niks[str(user_id)]
                    usr = f'<a href="tg://openmessage?user_id={user_id}">{nik}</a>'
                else:
                    usr = f'<code>@{user_id}</code>'

                dovs_users += f'{i}) {usr} - {level} \n'
            await self.send(self.strings('dov.users').format(dovs_users), message)
            return

        elif args_list[0].lower() == "prefs":
            prefs_users = self.db.get('BioWars', 'FamousPrefs')
            niks = self.db.get('BioWars', 'UsersNik')
            prefs = ''
            if len(args_list) > 1 and args_list[1].lower() == 'chat':
                r = await self.get_members_chat(message.chat)
                if r == 'NotChat':
                    await utils.answer(message, 'Это не чат')
                    return
                else:
                    users = r
                i = 1
                for user in users:
                    if str(user) in prefs_users.keys():
                        pref = prefs_users[str(user)]

                        if str(user) in niks.keys():
                            nik = niks[str(user)]
                            usr = f'<a href="tg://openmessage?user_id={user}">{nik}</a>'
                        else:
                            usr = f'<code>@{user}</code>'

                        prefs += f'{i}) {usr} | {pref} \n'
                        i += 1
                prefs = prefs if prefs else 'В этом чате никого нет'

                await self.send(self.strings('dov.prefs.chat').format(prefs), message)
                return

            for i, (user_id, pref) in enumerate(prefs_users.items(), start=1):
                if str(user_id) in niks.keys():
                    nik = niks[str(user_id)]
                    usr = f'<a href="tg://openmessage?user_id={user_id[1:]}">{nik}</a>'
                else:
                    usr = f'<code>@{user_id}</code>'
                prefs += f'{i}) {usr} | {pref} \n'

            prefs = prefs if prefs else 'Тут никого нет'

            await self.send(self.strings('dov.prefs').format(prefs), message)
            return

        elif args_list[0].lower() == "st":
            status = self.config["Вкл/Выкл доверки"]
            if status:
                self.config["Вкл/Выкл доверки"] = False
                await utils.answer(message, self.strings("dov.status.   False"))
            else:
                self.config["Вкл/Выкл доверки"] = True
                await utils.answer(message, self.strings("dov.status.True"))

    async def bio_command(self, message: Message, reply: Message, me) -> None:
        if reply.text.startswith('🔬 ТОП ЛАБОРАТОРИЙ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:'):
            sms = choices(self.strings('messages.biotop'))[0] + '\n'
        else:
            sms = choices(self.strings('messages.misc'))[0] + '\n'

        sms += await self.bio(reply, me)

        await self.send(sms, message)

    async def nik_command(self, message: Message, args_list: list, args_raw: str) -> None:

        user_id = args_list[0].replace('@', '')
        user_nikname = ' '.join(args_list[1:])
        await self.save_nik(user_id, user_nikname)
        await utils.answer(message, self.strings('edit_nik').format(user_id, user_nikname))

    async def pref_command(self, message: Message, args_list: list) -> None:
        user_id = args_list[0].replace('@', '')
        user_pref = ' '.join(args_list[1:])
        await self.save_pref(user_id, user_pref)
        await utils.answer(message, self.strings('edit_pref').format(user_pref, user_id))

    # -----------------------Commands-------------------

    async def помощьcmd(self, message: Message) -> None:
        """Помощь по модулю"""
        args_raw = utils.get_args_raw(message)
        infList = self.db.get("NumMod", "infList")
        famous_users = self.db.get('BioWars', 'FamousUsers')
        dov_users = self.db.get("BioWars", "DovUsers")
        if not args_raw:
            pref = await self.get_pref()
            commands = ""
            comm = self.strings("сommands")
            for com, desc in comm.items():
                commands += f"▫️ <code>{pref}{com}</code> {desc} \n"
                text = self.strings("bio.commands").format(
                    pref, commands)

        elif args_raw.lower() == "зарлист":
            text = self.strings("bio.zar").format()
        elif args_raw.lower() == "доверка":
            text = self.strings("bio.dov").format()
        elif args_raw.lower() == 'доверка -уровни':
            text = self.strings("bio.dov.levels")
        elif args_raw.lower() == 'инфо':
            exps = int(sum([eval(i[0].replace(",", ".").replace(
                'k', '*1000')) for i in list(infList.values())]))
            text = self.strings("bio.info").format(
                len(infList.keys()),
                '{:,}'.format(exps).replace(',', ' '),
                len(famous_users.keys()),
                len(dov_users.keys())
            )

        else:
            await utils.answer(message, "Что то явно не так")
            return
        await self.send(text, message)
        return

    @loader.watcher(only_messages=True)
    async def autohill__diseases(self, message: Message):
        if not (text := message.text):
            return

        me = await self.client.get_me()

        if (sender := message.from_id) == me.id:
            for _ in iris._prefs:
                if (
                        (txt := message.raw_text.lower()) == 'купить вакцину'
                        or txt.splitlines()[0] == _ + 'купить вакцину'
                ):
                    return await self.autohill(message, reset=True)

        if not (reg := re.search(
                r'☠️ Горячка на (\d+) минут[ы]*\n'
                r'🤒 Заражение на (\d+) д.+',
                text
        )
        ):
            return

        letal = [int(reg.group(1)), int(reg.group(2))]

        if reg := re.search(
                r'подверг[ла]* заражению .+tg://user\?id=(\d+)', text
        ):
            if int(reg.group(1)) == me.id:
                await self.autohill(message, write=letal[0])

        if not (reg := re.search(
                r'<a href="(https://t\.me/([a-zA-Z]{1}[a-zA-Z0-9_]{3,31})|tg://openmessage\?user_id=(\d+))">.+ '
                r'подверг[ла]* заражению ((неизвестным патогеном)|патогеном («.+»)) <a href="tg://user\?id=(\d+)">',
                text
        )
        ):
            return

        if int(reg.group(7)) != me.id or sender not in iris.bots:
            return

        org_inf = reg.group(2) if reg.group(2) else reg.group(3)
        if org_inf in self.bol.keys():
            del self.bol[org_inf]

        # ид/юзер = str: опыт, str: дата, str: дата до, str/None: имя патогена
        self.bol[org_inf] = (
            [
                str(_exp(re.search(r'☣️ \+(.+) био-опыта', text).group(1))),
                f'{datetime.now():{DT_FORMAT}}',
                f'{(datetime.now() + timedelta(days=letal[1])):{DT_FORMAT}}',
                reg.group(6)
            ]
        )

    @loader.watcher(only_messages=True)
    async def append_famous(self, message: Message):
        """расширяет базу ников и юзернеймов"""
        if (
                not (text := message.text)
                or not (raw_text := message.raw_text)
        ):
            return

        by_iris = message.from_id in iris.bots
        try:
            reply = await message.get_reply_message()
        except:
            reply = None

        if choices([True, False], weights=[5, 95])[0]:
            sender = await message.get_sender()

            if sender and isinstance(sender, User):
                if sender.id and sender.username:
                    # logger.warning(f'sender.id and sender.username "{sender.id}", "{sender.username}"')

                    self.fau[str(sender.id)] = sender.username.lower()

                if sender.id and sender.first_name:
                    # logger.warning(f'sender.id and sender.first_name "{sender.id}", "{sender.first_name}"')

                    if str(sender.id) not in self.niks.keys():
                        self.niks[str(sender.id)] = repair_text(sender.first_name)

        if re.search(r'подверг[ла]* заражению', text) and by_iris:
            for _ in range(len((_text := text))):
                if reg := re.search(r'<a href="tg://user\?id=(\d+)">(.+)</a>', _text):
                    id, nik = reg.group(1), repair_text(reg.group(2))
                    _text = _text.replace(reg.group(0), '')

                elif reg := re.search(r'<a href="tg://openmessage\?user_id=(\d+)">(.+)</a>', _text):
                    id, nik = reg.group(1), repair_text(reg.group(2))
                    _text = _text.replace(reg.group(0), '')

                else:
                    break

                # logger.warning(f'r"подверг[ла]* заражению" and by_iris "{id}", "{nik}"')

                if id not in self.niks.keys():
                    self.niks[id] = repair_text(nik)

        if reg := re.search(
                r'💢 Попытка заразить (.+) провалилась|'
                r'🥽 Иммунитет объекта «(.+)» оказался стойким к вашему патогену|'
                r'🦠 .+ подверг[ла]* заражению неизвестным патогеном (.+)|'
                r'🦠 .+ подверг[ла]* заражению патогеном «.+» (.+)',
                raw_text
        ):
            if not reply or not by_iris:
                return

            if not (user := re.search(r'(.+|)заразить @(\d+)', reply.raw_text.splitlines()[0])):
                return

            nik = ...
            for _ in range(1, 4):
                if reg.group(_) is not None:
                    nik = repair_text(reg.group(_))
                    break

            if nik is ...:
                return

            # logger.warning(f'рег "{user.group(2)}", "{nik}"')

            if user.group(2) not in self.niks.keys():
                self.niks[user.group(2)] = nik

        return

        # Чат айди локдауна  и не только
        if message.chat_id in iris.chats:
            return

        if re.fullmatch(r"жд\s@\d{3,12}.{,10}", text, flags=re.ASCII):
            if str(sender.id) != (me.id):
                return

        elif re.fullmatch(r"жл\s@\d{3,12}", text, flags=re.ASCII):
            if str(sender.id) != str(me.id):
                return

    @loader.watcher(only_messages=True)
    async def autosave_watcher(self, message: Message):
        """Ватчер для автосейва"""
        if (
                not message.text
                or not self.config["Автозапись жертв"]
        ):
            return
        # здесь могла бы быть ваша реклама
        try:
            reply = await message.get_reply_message()
        except:
            reply = None
        text = message.text
        me = await self.client.get_me()
        raw_text = message.raw_text
        sndr_id = message.sender_id
        infList = self.db.get("NumMod", "infList")
        msg_splitlines_1 = message.raw_text.splitlines()[0] if text else ''

        # Относится к автозаписе жертв
        # Берем айди/юзернейм из собщения пользователя и сохраняем в бд (в бд будет лежать айди зараженного)
        if mes := re.fullmatch(r'(/заразить|заразить) (?P<lvl>[1-9]?[0]?\s)?((https?://)?t\.me/|@)([0-9a-z_A-Z]+)',
                               msg_splitlines_1.lower()):
            if str(me.id) != str(sndr_id):
                return
            user = mes.group(5)
            await self.save_last_infect(user)
            return

        if re.search(r'(/заразить|заразить) (?P<lvl>[1-9]?[0]?\s)?(равного|слабее|сильнее|р|=|-|\+)',
                     msg_splitlines_1.lower()):
            if str(me.id) != str(sndr_id):
                return
            user = None
            await self.save_last_infect(user)
            return

        # Автозапись жертв
        # Если ссылки на сообщение нету берем ее из бд
        if (
                'подверг заражению' in text
                or 'подвергла заражению' in text
        ):
            if not '☣' in text or message.text.startswith('🕵️‍♂️ Служба безопасности'):
                return
            get_me = me
            vremya = datetime.now(pytz.timezone(
                self.config["Временная зона"]))
            msg_text = text
            split_text = text.splitlines()
            split_text_raw = message.raw_text.splitlines()

            if sndr_id not in iris.bots:
                return

            line = split_text[3] if "🗓 Отчёт об операции заражения объекта:" in msg_text else split_text[0]
            line_raw = split_text_raw[3] if "🗓 Отчёт об операции заражения объекта:" in msg_text else split_text_raw[0]
            lines = line.split("заражению", maxsplit=2)

            """проверялка на ид/юзер"""
            if '<a href="https://t.me/' in lines[0]:
                _user = lines[0].split("/")
                _user = _user[3].split('">')[0]
                if me.username:
                    if _user != get_me.username.lower():
                        return
                else:
                    return
            elif '<a href="tg://' in lines[0]:
                user_id = lines[0].split("=")
                user_id = user_id[2].split('">')[0]
                if int(user_id) != me.id:
                    return
            else:
                return

            reg = r"""🤒 Заражение на (\d+) дн[яей]{,2}
☣️ +(.*) био-опыта"""

            s = re.compile(reg)
            info = s.search(msg_text)

            letal = int(info.group(1))
            count = info.group(2).replace('+', '')

            try:
                x = msg_text.index('user?id=') + 8
                user = msg_text[x:].split('"', maxsplit=1)[0]
                self.db.set('BioWars', 'LastInfect', None)

            except ValueError:  # Если нет ссылки на жертву то берем ее из бд
                # Если в заражение от бота есть реплай, то берем айди из реплая, иначе из бд
                if reply:
                    t = reply.raw_text.splitlines()[0]
                    if '@' in t:
                        s = t.find('@')
                        user = t[s:].replace('@', '')
                    else:
                        s = t.find('https://t.me/')
                        user = t[s:].replace('https://t.me/', '')

                    if not user.isdigit():
                        user = await self.return_user(username=user)

                    self.db.set('BioWars', 'LastInfect', None)

                else:
                    # Берем данные о последнем зараженном
                    # Если статус Тру(тоесть еще не заражли его)
                    # То берем его айди и записываем его в дб
                    user = self.db.get('BioWars', 'LastInfect')
                    # self.db.set('BioWars', 'LastInfect',
                    #            {'user_id': user['user_id'],
                    #            'status': False})
                    self.db.set('BioWars', 'LastInfect', None)

                    # user = user['user_id']
            if not user:
                return
            # добавляет ник из смс ириса, если его нет в базе
            # name = line_raw.split()[-1]
            # if self.config['Сохранение ников'] and str(user) not in self.db.get('BioWars', 'UsersNik') and 1>2:
            #    self.db.get('BioWars', 'UsersNik')[str(user)] = name

            # if not self.config['Сохранение ников']:
            #    pass

            letal_in_db = self.db.get('BioWars', 'YourLetal')
            user = '@' + str(user)
            if letal != letal_in_db:
                self.db.set('BioWars', 'YourLetal', letal)

            vremya1 = vremya.strftime('%d.%m.%Y')  # strftime("%d.%m")
            vremya_do = vremya.strftime("%d.%m") if letal == 1 else (vremya +
                                                                     timedelta(days=int(letal))).strftime("%d.%m.%Y")

            # Хранит данные до какого числа заражение
            # Используется для того чтобы не портить структуры зарлиста наммода
            infectBefore = self.db.get('BioWars', 'InfectionBefore')
            infectBefore[user] = vremya_do

            self.db.set('Biowars', 'InfectionBefore', infectBefore)
            old_count = ' ' + str(infList[user][0]) if user in infList else ''
            if user in infList:
                del infList[user]

            infList[user] = [str(count), vremya1]
            self.db.set("NumMod", "infList", infList)

            # записывает дату окончания кд в базу
            await self.cooldown(user[1:], write=True)

            sms = self.strings('zar.save').format(
                user, old_count, count, vremya_do)

            # Чат айди локдауна  и не только
            if (
                    message.chat_id in iris.chats
                    or self.config['Тихое сохранение']
            ):
                return logger.warning(sanitise_text(sms))

            # Сохранение текстом
            if message.chat_id != -1316297204:
                await message.reply(self.strings('zar.save').format(user, old_count, count, vremya_do))
            return

            if re.fullmatch(r"жд\s@\d{3,12}.{,10}", text, flags=re.ASCII):
                if str(sndr_id) != (me.id):
                    return

            elif re.fullmatch(r"жл\s@\d{3,12}", text, flags=re.ASCII):
                if str(sndr_id) != str(me.id):
                    return

        # -----------------------Commands-------------------

    @loader.watcher(only_messages=True)
    async def watcher_dov(self, message: Message):
        """Ватчер для доверки"""
        try:
            reply = await message.get_reply_message()
        except:
            reply = None
        text = message.text if message.text else ''
        sndr_id = message.sender_id
        me = await self.client.get_me()
        args_list, args_raw = utils.get_args(
            message), utils.get_args_raw(message)

        numfilter = self.db.get("NumMod", "numfilter")
        if self.config["Вкл/Выкл доверки"] and str(sndr_id) in self.db.get("BioWars", "DovUsers").keys() and numfilter[
            'filter']:
            nik = numfilter['filter'].lower()

            if not text.lower().startswith(nik):  # and sndr_id != me.id:
                return

            dov_users = self.db.get("BioWars", "DovUsers")

            level = dov_users[str(sndr_id)]
            # убираем из текста имя доверки

            # text = text.replace(
            #    f"{nik} ", '', 1).replace(f'{nik}', '', 1)

            # Сделано из-за небольших проблем к командой replace
            # Оно может случайно и удалить часть вводимой команды
            # Пример: вир +вирусы
            # Убирало вир и убирало вир из +вирусы, в итоге осталовалось +усы
            if not message.out or 1 == 1:
                text = text[len(
                    nik) + 1:] if f'{nik} ' in text.lower() else text[len(nik):]
            text_low = text.lower()
            text_norm = text.replace('-f', '')

            args_raw = text
            args_list = text.split(' ')
            args = [_ for _ in args_list if _]
            if level >= 1:
                if re.fullmatch('з', text_norm):  # and reply:
                    reply = reply if reply else await self.last_msg(message)

                    if reply.text.startswith(r"🕵️‍♂️ Служба безопасности"):
                        return await self.zar_search(message,
                                                     get_ne_pridumal(
                                                         [
                                                             _ for _ in reply.text.splitlines()
                                                             if _.startswith('Организатор заражения')
                                                         ][0],
                                                         at=True
                                                     )[0]
                                                     )

                    return await self.zar_search(
                        message,
                        f'@{reply.from_id}' if not (user := get_ne_pridumal(reply.text, at=True)) else user[0]
                    )

                elif send_mesа := re.search(r"з\s", text):
                    # logger.info(args_raw)
                    if args_raw.split()[1] == '-f' and reply:
                        user = '@' + str(reply.from_id)
                    else:
                        en = message.entities[0]
                        link = message.raw_text[en.offset:en.offset + en.length]
                        user = await self._handler_link(link) if '@' not in link else link
                    await self.zar_search(message, user)
                    return

                    # await message.reply(self.strings('zar.search').format(usr, user[0], user[1], zar_do))
                # Калькулятор находиться на лоработке
                elif mes := re.fullmatch(r'(калькулятор|к|калк) (\w+) (\d+(-\d+)?)', text_low):
                    pass
                    skill = mes.group(2)
                    n = mes.group(3).split('-')

                    if re.search(r"зз|зараз[уканость]{,5}", text_low, flags=re.ASCII):
                        n1, n2 = int(n[0]), int(n[1])
                        step = self.strings('calc_formul')['zar']
                        total = 0
                        for i in range(n1 + 1, n2 + 1):
                            total += int(i ** step)
                        total = '{:,}'.format(total).replace(',', '.')

                        text_msg = f'<b>💵 Улучшение с</b> <i>{n1}</i> <b>до</b> <i>{n2}</i> <b>заразности стоит:</b> <i>{total}</i> <b>био-ресурсов</b>'
                        await message.reply(text_msg)
                        return

                    elif re.search(r"(?P<let>летал[укаьность]{,5})", text_low, flags=re.ASCII):
                        n1, n2 = int(n[0]), int(n[1])
                        step = self.strings('calc_formul')['letal']
                        total = 0
                        for i in range(n1 + 1, n2 + 1):
                            total += int(i ** step)
                        total = '{:,}'.format(total).replace(',', '.')

                        text_msg = f'<b>💵 Улучшение с</b> <i>{n1}</i> <b>до</b> <i>{n2}</i> <b>летальности стоит:</b> <i>{total}</i> <b>био-ресурсов</b>'
                        await message.reply(text_msg)
                        return

                    elif re.search(r"(?P<pat>пат[огены]{,5})", text_low, flags=re.ASCII):
                        n1, n2 = int(n[0]), int(n[1])
                        step = self.strings('calc_formul')['pat']
                        total = 0
                        for i in range(n1 + 1, n2 + 1):
                            total += int(i ** step)
                        total = '{:,}'.format(total).replace(',', '.')

                        text_msg = f'<b>💵 Улучшение с</b> <i>{n1}</i> <b>до</b> <i>{n2}</i> <b>патогена стоит:</b> <i>{total}</i> <b>био-ресурсов</b>'
                        await message.reply(text_msg)
                        return

                    elif re.search(r"(?P<kvala>квал[улаификация]{,8}|разраб[откау]{,4})", text_low, flags=re.ASCII):
                        n1, n2 = int(n[0]), int(n[1])
                        step = self.strings('calc_formul')['kvala']
                        total = 0
                        for i in range(n1 + 1, n2 + 1):
                            total += int(i ** step)
                        total = '{:,}'.format(total).replace(',', '.')

                        text_msg = f'<b>💵 Улучшение с</b> <i>{n1}</i> <b>до</b> <i>{n2}</i> <b>квалификации стоит:</b> <i>{total}</i> <b>био-ресурсов</b>'
                        await message.reply(text_msg)
                        return

                    elif re.search(r"(?P<imun>иммун[уеитетка]{,4}|имун[уеитетка]{,4})", text_low, flags=re.ASCII):
                        n1, n2 = int(n[0]), int(n[1])
                        step = self.strings('calc_formul')['imun']
                        total = 0
                        for i in range(n1 + 1, n2 + 1):
                            total += int(i ** step)
                        total = '{:,}'.format(total).replace(',', '.')

                        text_msg = f'<b>💵 Улучшение с</b> <i>{n1}</i> <b>до</b> <i>{n2}</i> <b>иммунитета стоит:</b> <i>{total}</i> <b>био-ресурсов</b>'
                        await message.reply(text_msg)
                        return

                    elif re.search(r'(?P<sb>сб|безопасно[сть]{,3}|служб[ау]{,2})', text_low):
                        n1, n2 = int(n[0]), int(n[1])
                        step = self.strings('calc_formul')['sb']
                        total = 0
                        for i in range(n1 + 1, n2 + 1):
                            total += int(i ** step)
                        total = '{:,}'.format(total).replace(',', '.')

                        text_msg = f'<b>💵 Улучшение с</b> <i>{n1}</i> <b>до</b> <i>{n2}</i> <b>безопасности стоит:</b> <i>{total}</i> <b>био-ресурсов</b>'

                        await message.reply(text_msg)
                        return
                    else:
                        return

                elif inf := re.search(
                        r"(бей{,3}|кус[ьайни]{,3}|зарази[тьть]{,3}|еб[ниажшь]{,3}|"
                        r"уеб[иаошть]{,3}|опуст[и]{,3}|организуй горячку{,3})",
                        text_low, flags=re.ASCII):
                    inf = inf.group(1)

                    text = text.replace(
                        f"{inf} ", '').replace(inf, '')

                    args_raw = text
                    args_list = args_raw.split(' ')

                    if args_raw.lower() == 'стоп':
                        status = self.db.get("BioWars", "infStatus")
                        if status:
                            self.db.set("BioWars", "infStatus", False)
                            await utils.answer(message, '✅ Заражения остановлены')
                            return
                        else:
                            await utils.answer(message, '❎ Заражения не запущены')
                            return

                    if args_list[0] == 'интервал':
                        if args_list[1] and args_list[1].isdigit():
                            time = float(args_list[1].replace(',', '.'))
                            self.db.set("BioWars", "infInterval", time)
                            await utils.answer(message, f'⏱ Установлен интервал между заражениями: {time} с')
                            return
                        else:
                            await utils.answer(message, f'❎ Укажите интвервал!')
                            return
                    # re.search(r"(?P<lvl>[1-9]?[0]?\s)?(?P<link>@[0-9a-zA-Z_]+|(?:https?://)?t\.me/[0-9a-zA-Z_]+|tg://openmessage\?user_id=(?P<id>[0-9]+))", text):
                    if send_mesа := re.search(
                            r"(?P<lvl>[\d]+?[0]?\s)?(?P<link>@[0-9a-zA-Z_]+|(?:https?://)?t\.me/[0-9a-zA-Z_]+|tg://openmessage\?user_id=(?P<id>[0-9]+))",
                            text):
                        if self.db.get("BioWars", "infStatus"):
                            await message.reply('❎ Заражения еще не завершены')
                            return

                        send_mesа = send_mesа.groupdict()

                        send_mesа['link'], send_mesа['id'] = '@' + \
                                                             send_mesа['id'] if send_mesа['id'] else send_mesа[
                            'link'], ''
                        send_mesа['lvl'] = send_mesа['lvl'] or ''

                        # если число патоген больше 10, то будет использовано 10
                        try:
                            if int(send_mesа['lvl']) > 10:
                                send_mesа['lvl'] = '10 '
                        except:
                            pass

                        mes = ''.join(send_mesа.values())

                        user = send_mesа['id'] if send_mesа['id'] else send_mesа['link']

                        user = user.replace(
                            '@', '').replace('https://t.me/', '')

                        await self.autohill(message)
                        await self.save_last_infect(user)
                        self.db.set("BioWars", "infStatus", True)
                        await message.reply(f'заразить {mes}')
                        self.db.set("BioWars", "infStatus", False)
                        return

                    await self.z_command(message, args_raw, text, reply)
                    return

                elif re.search(r"вак[цинау]{,3}|леч[ись]{,2}|хи[лльсяйинг]{,2}|лек[арство]{,2}",
                               text_low, flags=re.ASCII
                               ):
                    await self.autohill(message, reset=True)
                    await message.reply('!купить вакцину')
                    return

                elif re.fullmatch(r"л[ау]{,2}", text, flags=re.ASCII):  # регулярка
                    lab_raw = await self.message_q(  # отправляет сообщение боту и возвращает текст
                        f".лаб",
                        5443619563,
                        mark_read=True,
                        delete=True,
                    )
                    if lab_raw == 'Timeout':
                        await message.respond('❎ Ошибка выполнения команды, Ирис не отвечает на запрос')

                    lab_lines = lab_raw.splitlines()  # текст с лабой, разбитый на строки
                    lab_args = self.config['Аргументы лабы'].split()

                    if "🔬 Досье лаборатории" not in lab_lines[0]:
                        return

                    sms = await self.get_lab(lab_raw, lab_args)
                    await message.reply(sms)
                    return
                elif args_raw.lower() == 'био' or args_raw.lower() == 'б':
                    if not reply:
                        await utils.answer(message, self.strings('no.reply'))
                        return
                    await self.bio_command(message, reply, me)
                    return

            if level >= 2:
                # Запись жертв с помощью дова
                # Пример: вир жд @777000 1.1к
                if text_low.startswith('жд') and len(args) in [2, 3]:
                    args.pop(0)

                    if len(args) == 1:
                        if not reply:
                            return

                        user = reply.from_id

                    else:
                        if not (user := get_ne_pridumal(args[0])):
                            return

                        args.pop(0)

                        if not (user := user[0]).isdigit():
                            user = await self.return_user(username=user)

                    try:
                        exp = str(_exp(args[0]))
                    except Exception as e:
                        return logger.exception(e)

                    old, old_do = None, None
                    if (user := f'@{user}') in self.zl.keys():
                        old = self.zl[user]
                        del self.zl[user]

                    if user in self.zl_do.keys():
                        old_do = self.zl_do[user]

                    self.zl[user] = [
                        exp, datetime.now(tz=pytz.timezone(self.tz)).strftime(DT_FORMAT)
                    ]

                    if self.letal != 1:
                        self.zl_do[user] = (
                                datetime.now(tz=pytz.timezone(self.tz)) + timedelta(days=self.letal)
                        ).strftime(DT_FORMAT2)

                    async def cancel_zhd(call: InlineCall) -> 'не ебу шо возвращает и лень чекать':
                        """
                        отменяет ручное сохранение жертвы
                        """
                        if str(call['from']['id']) not in self.dovs.keys():
                            return await call.answer(choices(self.strings('wrong_click'))[0])

                        if old_do:
                            self.zl_do[user] = old_do

                        if old:
                            self.zl[user] = old

                        else:
                            with contextlib.suppress(Exception):
                                del self.zl[user]
                                del self.zl_do[user]

                        await call.delete()

                    await self.inline.form(
                        self.strings('zar.save').format(
                            (
                                # f'<a href="tg://openmessage?user_id={user[1:]}">{self.niks[user[1:]]}</a>'
                                # if user[1:] in self.niks.keys() else
                                f'<code>{user}</code>'
                            ),
                            ' ' + old[0] if old else '',
                            exp,
                            self.zl_do[user] if user in self.zl_do.keys() else '😢 Неизвестно'
                        ),
                        message,
                        {'text': '✖️ Отменить', 'callback': cancel_zhd},
                        disable_security=True
                    )
                # Удаление жертв с помощью дова
                # Пример: вир жу @777000 1.1к
                if text_low.startswith('жу') and len(args) == 1:
                    if not (user := get_ne_pridumal(args[0])):
                        return

                    if not (user := user[0]).isdigit():
                        user = await self.return_user(username=user)

                        # Чек ежедневки
                elif reg := re.fullmatch(r'(топ жертв[ыау]{,2})( (\d+)|())', text_low, flags=re.ASCII):
                    n = reg.group(2) if reg.group(2) else 1
                    await self.get_top_zhertv(message=message, num_list=n)
                    return

                elif reg := re.fullmatch(r'(список жертв[ыау]{,2})( (\d+)|())', text_low, flags=re.ASCII):
                    n = reg.group(2) if reg.group(2) else 1
                    await self.get_zhertv(message=message, num_list=int(n))
                    return

            if level >= 3:
                # Чек болезней
                if re.fullmatch(r"(болезни|бол) -rt", text_low, flags=re.ASCII):
                    await message.reply('/мои болезни')
                    return

                elif reg := re.fullmatch(r'(бол[езни]*)( (\d+)|())', text_low, flags=re.ASCII):
                    n = reg.group(2) if reg.group(2) else 1
                    await self.get_bolezni(message, int(n))
                    return
                # ферма
                elif re.search(r'ферма', text_low):
                    await message.respond('ферма')
                # Просмотр мешка
                elif re.fullmatch(r'мешок -rt', text_low):
                    await message.respond('.мешок')
                    return

                elif re.fullmatch(r'мешок', text_low):
                    q = await self.message_q('.мешок')
                    if q == 'Timeout':
                        await message.respond('Время ожидание ответа от ириса истекло')
                        return

                    if not q.startswith('💰 В мешке'):
                        return
                    q = q.replace(
                        '💬 Запасы можно пополнить, введя команду "купить {число}"', '')
                    await utils.answer(message, q)
                    return

                if send_mesа := re.search(r"лаб[ау]{,2}(?P<args>(\s(\w{1,12})){1,})", text_low, flags=re.ASCII):

                    send_mesа = send_mesа.groupdict()
                    lab_args = send_mesа['args'].split()
                    lab_raw = await self.message_q(  # отправляет сообщение боту и возвращает текст
                        f".лаб",
                        5443619563,
                        mark_read=True,
                        delete=True,
                    )
                    if lab_raw == 'Timeout':
                        await message.respond('❎ Ошибка выполнения команды, Ирис не отвечает на запрос')

                    lab_lines = lab_raw.splitlines()  # текст с лабой, разбитый на строки
                    if "🔬 Досье лаборатории" not in lab_lines[0]:
                        return

                    sms = ""
                    sms += await self.get_lab(lab_raw, lab_args)

                    await message.reply(sms)
                    return

            if level == 4:
                # Прокачка навыков
                if send_mes := re.search(
                        r"(?P<ch>зараз[куаность]{,5} чек[нутьиай]{,4}\s|чек[айниуть]{,4} зараз[куаность]{,5}\s)(?P<lvl>[0-5]+)",
                        text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['ch'] = '+заразность '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)

                elif send_mes := re.search(
                        r"(?P<pat>пат[огены]{,5} чек[айниуть]\s|чек[айниуть]{,4} пат[огены]{,5}\s)(?P<lvl>[0-5]+)",
                        text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['pat'] = '+патоген '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(
                        r"(?P<let>летал[каьностьу]{,5} чек[айниуть]{,4}\s|чек[айниуть]{,4} летал[каьностьу]{,5}\s)(?P<lvl>[1-5]+)",
                        text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['let'] = '+летальность '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(
                        r"(?P<kvala>квал[лаификацияу]{,8} чек[айниуть]{,4}\s|разраб[откау]{,4} чек[айниуть]{,4}\s|чек[айниуть]{,4} разраб[откау]{,4}\s|чек[айниуть]{,4} квал[улаификация]{,8}\s)(?P<lvl>[0-5]+)",
                        text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['kvala'] = '+квалификация '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(
                        r"(?P<imun>чек[айниуть]{,4} иммун[еитеткау]{,4}\s|чек[айниуть]{,4} имун[еитеткау]{,4}\s|имун[еитеткау]{,4} чек[айниуть]{,4}\s|иммун[еитеткау]{,4} чек[айниуть]{,4}\s)(?P<lvl>[0-5]+)",
                        text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['imun'] = '+иммунитет '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(
                        r"(?P<sb>сб чек[айниуть]{,4}\s|безопасно[сть]{,3} чек[айниуть]{,4}\s|служб[ау]{,2} чек[айниуть]{,4}\s|чек[айниуть]{,4} служб[ау]{,2}\s|чек[айниуть]{,4} безопасно[сть]{,3}\s|чек[айниуть]{,4} сб\s)(?P<lvl>[0-5]+)",
                        text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['sb'] = '+безопасность '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                # кач    алки
                elif send_mes := re.search(r"(?P<zar>зараз[уканость]{,5}\s)(?P<lvl>[0-5]+)", text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['zar'] = '++заразность '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(r"(?P<pat>пат[огены]{,5}\s)(?P<lvl>[0-5]+)", text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['pat'] = '++патоген '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(r"(?P<let>летал[укаьность]{,5}\s)(?P<lvl>[1-5]+)", text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['let'] = '++летальность '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(r"(?P<kvala>квал[улаификация]{,8}\s|разраб[откау]{,4}\s)(?P<lvl>[0-5]+)",
                                           text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['kvala'] = '++квалификация '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(r"(?P<imun>иммун[уеитетка]{,4}|имун[уеитетка]{,4}\s)(?P<lvl>[0-5]+)",
                                           text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['imun'] = '++иммунитет '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)
                elif send_mes := re.search(r"(?P<sb>сб\s|безопасно[сть]{,3}\s|служб[ау]{,2}\s)(?P<lvl>[0-5]+)",
                                           text_low, flags=re.ASCII):
                    send_mes = send_mes.groupdict()
                    send_mes['sb'] = '++безопасность '
                    send_mes['lvl'] = send_mes['lvl'] or ''
                    mes = ''.join(send_mes.values())
                    await message.reply(mes)

                # управление вирусами
                elif re.search(r'\+вирус[аы]{,2}|увед[ыомления]', text_low):
                    await message.reply('+вирусы')

                elif re.search(r'-вирус[аы]{,2}', text_low):
                    await message.reply('-вирусы')

                # Смена имени лабы и пата

                elif send_mesa := re.search(r'\+пат[оген]{,4}(?P<pat>(\s(\w{1,12})){1,})', text_norm):

                    send_mesa = send_mesa.groupdict()
                    pat = ' '.join(send_mesa['pat'].split())

                    await message.reply(f'+имя патогена {pat}')
                    return

                elif send_mesa := re.search(r'\+лаб[a]{,1}(?P<lab>(\s(\w{1,12})){1,})', text_norm):

                    send_mesa = send_mesa.groupdict()
                    pat = ' '.join(send_mesa['lab'].split())

                    await message.reply(f'+имя лаборатории {pat}')
                    return

                elif send_mesa := re.search(r'-пат[оген]{,4}', text_low):
                    await message.reply(f'-имя патогена')
                    return

                elif send_mesa := re.search(r'-лаб[a]{,1}', text_low):
                    await message.reply(f'-имя лаборатории')
                    return

                # Чек фулл лабы
                if re.fullmatch(r'моя лаба', text):
                    await message.respond('моя лаба')

    @loader.watcher(only_messages=True)
    async def watcher_commands(self, message: Message):
        """Ватчер для команд"""
        if not message.text:
            return
        try:
            reply = await message.get_reply_message()
        except:
            reply = None
        text = message.text
        sndr_id = message.sender_id
        me = await self.client.get_me()
        pref = await self.get_pref()
        args_list, args_raw = utils.get_args(
            message), utils.get_args_raw(message)
        owners = list(getattr(self.client.dispatcher.security, "owner"))

        if text.startswith(pref) and sndr_id in owners:
            try:
                command = text.replace(pref, "").split()[0].lower()
            except IndexError:
                return

            if command not in self.strings("сommands"):
                return

            if command == "z":
                await self.z_command(message, args_raw, text, reply)
                return
            elif command == "id":
                await self.id_command(message, args_raw, reply)
                return
            elif command == "ids":
                await self.ids_command(message, args_raw, reply)
                return
            elif command == "dov":
                await self.dov_command(message, args_list, args_raw, reply)
                return
            elif command == 'zz':
                await self.bio_command(reply, me)
                return
            elif command == 'nik':
                await self.nik_command(message, args_list, args_raw)
                return
            elif command == 'pref':
                await self.pref_command(message, args_list)
                return