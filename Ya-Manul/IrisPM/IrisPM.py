"""Модуль для взаимодействия с Iris ботом"""

from datetime import timedelta
import random
import logging

from telethon import functions
from telethon.tl.types import Message
from telethon.tl.custom import Message
from .. import utils, loader

__version__ = (2, 2, 8)

# meta developer: @YA_ManuI

logger = logging.getLogger(__name__)

CUBES = [
    "🎲 Выпало: 1",
    "🎲 Выпало: 2",
    "🎲 Выпало: 3",
    "🎲 Выпало: 4",
    "🎲 Выпало: 5",
    "🎲 Выпало: 6",
]


@loader.tds
class IrisMods(loader.Module):
    """Ирис чат менеджер для пользования в лс"""

    strings = {
        "name": "IrisPM",
        "loading_photo": "⏳ Загрузка графика...",
        "error_args": "❌ Ошибка: Неверные аргументы",
        "error_transfer": "❌ Ошибка: Требуется указать ириски/голд или од",
        "error_conclusion": "❌ Ошибка: Требуется указать анк/та",
    }

    def __init__(self):
        self.name = self.strings["name"]
        self.iris_bot = "@iris_black_bot"
        # self.iris_moon_bot = "@iris_moon_bot"
        self.iris_id = 5443619563
        self.client = None
        self.db = None
        self.myid = None

    async def client_ready(self, client, db):
        """Инициализация при запуске"""
        self.client = client
        self.db = db
        self.myid = (await client.get_me()).id

    async def message_q(
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
    ) -> Message:
        """Отправляет сообщение и возвращает ответ"""
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()

            if mark_read:
                await conv.mark_read()

            if delete:
                await msg.delete()
                await response.delete()

            return response

    @loader.command()
    async def Кубик(self, m):
        """Выкидывает рандом сторону кубика"""
        randomfraza = random.choice(CUBES)
        await utils.answer(m, randomfraza)

    @loader.command()
    async def передать(self, message: Message) -> None:
        """Передать {что} {колво} {кому} - передает ириски/голд или од"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["error_args"])
            return

        try:
            item_type, amount, *recipient = args.split()
            amount = int(amount)

            if message.is_reply:
                replied = await message.get_reply_message()
                recipient = f"@{replied.from_id}"
            else:
                recipient = recipient[0]

            transfer_type = {
                "голд": " голд",
                "ириски": "",
                "ирис": "",
                "од": " од",
            }.get(item_type)

            if transfer_type is None:
                await utils.answer(message, self.strings["error_transfer"])
                return

            text = f"Передать{transfer_type} {amount} {recipient}"

            if " | " in args:
                text += f"\n{args.split(' | ')[1]}"

            response = await self.message_q(
                text, self.iris_bot, mark_read=True, delete=True
            )
            await utils.answer(message, response.text)

        except (ValueError, IndexError):
            await utils.answer(message, self.strings["error_args"])

    @loader.command()
    async def ГМИ(self, message: Message) -> None:
        """Информация о путешествии ваших ирисок"""
        response = await self.message_q(
            "где мои ириски", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def ГМЗ(self, message: Message) -> None:
        """Информация о путешествии ваших голд"""
        response = await self.message_q(
            "где моя голда", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def бот(self, message: Message) -> None:
        """Проверка работоспособности бота"""
        response = await self.message_q(
            "бот", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def укрф(self, message: Message) -> None:
        """Показывает вашу суточную статью по ирису"""
        response = await self.message_q(
            "!моя статья", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def ГМП(self, message: Message) -> None:
        """Информация о путешествии ваших од"""
        response = await self.message_q(
            "где мои пончики", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def мешок(self, message: Message) -> None:
        """Показывает содержимое вашего мешка"""
        response = await self.message_q("Мешок", self.iris_bot, delete=True)
        await utils.answer(message, response.text)

    @loader.command()
    async def биржа(self, message: Message) -> None:
        """Информация о текущем состоянии биржи"""
        response = await self.message_q(
            "биржа", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def график(self, message: Message) -> None:
        """Вывод графика цен голды"""
        loading = await utils.answer(message, self.strings["loading_photo"])

        async with self.client.conversation(self.iris_bot) as conv:
            await conv.send_message(".биржа график")
            response = await conv.get_response()

            if response.photo:
                await loading.delete()
                await message.client.send_message(
                    message.peer_id,
                    file=response.photo,
                    reply_to=getattr(message, "reply_to_msg_id", None),
                )

    @loader.command()
    async def хелп(self, message: Message) -> None:
        """Вывод помощи по ирису"""
        response = await self.message_q(
            ".помощь", self.iris_bot, mark_read=True, delete=False
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def итоп(self, message: Message) -> None:
        """Вывод топа дня"""
        response = await self.message_q(
            "бтоп дня", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def ипинг(self, message: Message) -> None:
        """Вывод активности ириса"""
        response = await self.message_q(
            ".актив ириса", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def ф(self, message: Message) -> None:
        """Запуск фармы"""
        response = await self.message_q(
            "фарма", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def голд(self, message: Message) -> None:
        """Вывод топа хранителей голды"""
        response = await self.message_q(
            "золотой рейтинг", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def ком(self, message: Message) -> None:
        """Вывод команд ириса"""
        response = await self.message_q(
            "команды", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def ач(self, message: Message) -> None:
        """{та/анк} {@/реплай} Вывод анкеты или ачивок пользователя"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["error_args"])
            return

        try:
            parts = args.split()
            if len(parts) < 1:
                await utils.answer(message, self.strings["error_args"])
                return

            item_type = parts[0]

            recipient = None
            if len(parts) > 1:
                recipient = parts[1]

            elif message.is_reply:
                replied = await message.get_reply_message()
                recipient = f"@{replied.sender_id}"

            transfer_type = {
                "та": "твои ачивки",
                "анк": "анкета",
            }.get(item_type)

            if transfer_type is None:
                await utils.answer(message, self.strings["error_conclusion"])
                return

            if item_type == "та" and not recipient:
                text = ".мои ачивки"
            else:
                text = transfer_type
                if recipient:
                    text += f" {recipient}"

            if " | " in args:
                text += f"\n{args.split(' | ')[1]}"

            response = await self.message_q(
                text, self.iris_bot, mark_read=True, delete=True
            )
            await utils.answer(message, response.text)

        except Exception as e:
            logger.error(f"Ошибка в команде ппт: {e}")
            await utils.answer(message, self.strings["error_args"])

    @loader.command()
    async def лс(self, message: Message) -> None:
        """Быстрый доступ к лс ириса"""
        text = (
            "✏️ ЛС Ириса здесь</b>\n"
            "<b><i><a href='https://t.me/iris_black_bot'>Iris | Black Diamond</a></i></b>\n"
        )
        await utils.answer(message, text)

    @loader.command()
    async def саб(self, message: Message) -> None:
        """Подписка/отписка на аккаунт: саб {+/-} {@/реплай}"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["error_args"])
            return

        try:
            action, *recipient = args.split()
            if action not in ["+", "-"]:
                await utils.answer(
                    message, "❌ Укажите + для подписки или - для отписки"
                )
                return

            if message.is_reply:
                replied = await message.get_reply_message()
                recipient = f"@{replied.from_id}"
            else:
                recipient = recipient[0]

            text = f"{action}саб {recipient}"
            if " | " in args:
                text += f"\n{args.split(' | ')[1]}"

            response = await self.message_q(
                text, self.iris_bot, mark_read=True, delete=True
            )
            await utils.answer(message, response.text)

        except (ValueError, IndexError):
            await utils.answer(message, self.strings["error_args"])

    @loader.command()
    async def ибраки(self, message: Message) -> None:
        """Вывод первой страницы топа браков"""
        response = await self.message_q(
            "топ браков", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def мсаб(self, message: Message) -> None:
        """Вывод списка ваших подписчиков"""
        response = await self.message_q(
            "мои сабы", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def мпдп(self, message: Message) -> None:
        """Вывод списка ваших подписок"""
        response = await self.message_q(
            "мои подписки", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def сабы(self, message: Message) -> None:
        """Вывод топа по подписчикам"""
        response = await self.message_q(
            "все сабы", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def погода(self, message: Message) -> None:
        """Вывод погоды: погода {город}"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите город")
            return

        text = f"!погода {args}"
        response = await self.message_q(
            text, self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def испам(self, message: Message) -> None:
        """Вывод ваших банов во вселенной ирис"""
        response = await self.message_q(
            "Мой спам", self.iris_bot, mark_read=True, delete=True
        )
        await utils.answer(message, response.text)

    @loader.command()
    async def хелпирис(self, message: Message) -> None:
        """Помощь по модулю Ирис для лс"""
        help_text = (
            "🍀| <b>Помощь по командам:</b>\n\n"
            "<code>.передать</code> - передаёт ириски/голд/од. .передать {что} {колво} {@/реплай}\n"
            "<code>.гми</code> - выводит путешествие ваших ирисок\n"
            "<code>.гмз</code> - выводит путешествие ваших голд\n"
            "<code>.гмп</code> - выводит путешествие ваших од\n"
            "<code>.мешок</code> - показывает ваш мешок\n"
            "<code>.биржа</code> - выводит стакан заявок биржи\n"
            "<code>.график</code> - вывод графика цен биржи\n"
            "<code>.хелп</code> - выводит меню помощи ириса\n"
            "<code>.итоп</code> - показывает топ дня\n"
            "<code>.ипинг</code> - показывает активность ботов ирис\n"
            "<code>.ф</code> - запускает ферму\n"
            "<code>.голд</code> - показывает топ хранителей голды\n"
            "<code>.кубик</code> - бросает кубик\n"
            "<code>.ком</code> - показывает команды ириса\n"
            "<code>.оси</code> - показывает основные чаты ириса\n"
            "<code>.бот</code> - проверка работоспособности бота\n"
            "<code>.укрф</code> - показывает вашу суточную статью\n"
            "<code>.ач</code> - показывает анкету или достижения пользователей. "
            "<code>.лс</code> - быстрый доступ к лс Черного ириса\n"
            "<code>.саб</code> - подписка/отписка на пользователя\n"
            "<code>.ибраки</code> - показывает топ браков\n"
            "<code>.мсаб</code> - показывает ваших подписчиков\n"
            "<code>.мпдп</code> - показывает ваши подписки\n"
            "<code>.сабы</code> - показывает топ по подписчикам\n"
            "<code>.погода</code> - показывает погоду в городе\n"
            "<code>.испам</code> - показывает ваши баны в ирисе\n"
        )
        await utils.answer(message, help_text)

    @loader.command()
    async def оси(self, message: Message) -> None:
        """Официальная сетка ириса"""
        network_text = (
            "🗓| <b>Чаты из сетки «ирис_чм»:\n\n"
            "<b><i>1. <emoji document_id=5319161050128459957>👨‍💻</emoji> "
            "<a href='https://t.me/iris_cm_chat'>Iris | Помощь по функционалу</a></i></b>\n\n"
            "<b><i>2. <emoji document_id=5291897920583381342>🥵</emoji> "
            "<a href='https://t.me/iris_talk'>Iris | Оффтоп</a></i></b>\n\n"
            "<b><i>3. <emoji document_id=5213224006735376143>💩</emoji> "
            "<a href='https://t.me/+PjZR20ZQHt44ZWNi'>Iris | Антиспам дружина</a></i></b>\n\n"
            "<b><i>4. <emoji document_id=5240379805047728736>💰</emoji> "
            "<a href='https://t.me/iris_trade'>Iris | Биржа</a></i></b>\n\n"
            "<b><i>5. <emoji document_id=5224570799230298867>☣️</emoji> "
            "<a href='https://t.me/iris_biogame'>Iris | Биовойны</a></i></b>\n\n"
            "<b><i>6. <emoji document_id=5404573776253825754>🍬</emoji> "
            "<a href='https://t.me/iris_bonus'>Iris | Акции и бонусы</a></i></b>\n\n"
            "<b><i>7. <emoji document_id=5314678293977378981>☎️</emoji> "
            "<a href='https://t.me/iris_brief_chat'>Iris | Мастерская идей</a></i></b>\n\n"
            "<b><i>8. <emoji document_id=5215209935188534658>📝</emoji> "
            "<a href='https://t.me/iris_feedback'>Iris | Отзывы об агентах</a></i></b>\n\n"
            "<b><i>9. <emoji document_id=5402320181143811311>🤨</emoji> "
            "<a href='https://t.me/iris_duels'>Iris | Золотые дуэли</a></i></b>\n\n"
            "<b><i>10. <emoji document_id=5019824691708167395>⭐️</emoji> "
            "<a href='https://t.me/+yWT9IUF4FxhiMTdi'>Iris | Звездный оффтоп</a></i></b>\n"
        )
        await utils.answer(message, network_text)
