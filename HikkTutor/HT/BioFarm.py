__version__ = (1, 8, 3)


#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#██╗░░░██╗███╗░░██╗███╗░░██╗██╗░█████╗░
#██║░░░██║████╗░██║████╗░██║██║██╔══██╗
#██║░░░██║██╔██╗██║██╔██╗██║██║██║░░╚═╝
#██║░░░██║██║╚████║██║╚████║██║██║░░██╗
#╚██████╔╝██║░╚███║██║░╚███║██║╚█████╔╝
#░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚═╝░╚════╝
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: BioFarm
from .. import loader, utils
import asyncio
import re
from telethon import events
from telethon.errors import YouBlockedUserError
import traceback

@loader.tds
class BioFarm(loader.Module):
    """Модуль для фарма био опыта/ресурсов"""

    strings = {'name': 'BioFarm'}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "selected_farm_chat", 
                "Ирис_синий",
                lambda: "Выбранный чат для фарма",
                validator=loader.validators.Choice([
                    "Ирис_синий",
                    "Ирис_чёрный",
                    "Ирис_жёлтый",
                    "Ирис_белый",
                    "Ирис_фиолетовый"
                ])
            ),
            loader.ConfigValue(
                "infection_command", 
                "Заразить сильного",
                lambda: "Команда для заражения в фарме",
                validator=loader.validators.Choice([
                    "Заразить сильного",
                    "Заразить равного",
                    "Заразить слабого"
                ])
            )
        )
        self.farm_chats = { 
            "Ирис_синий": 707693258,
            "Ирис_чёрный": 5443619563,
            "Ирис_жёлтый": 5137994780,
            "Ирис_белый": 5434504334,
            "Ирис_фиолетовый": 5226378684
        }
        self.vaccine_needed = False
        self.healing_in_progress = False
        self.spam = False
        self.command_delay = 2.0

    async def client_ready(self, client, db):
        self.me = await client.get_me()

    async def stopzarcmd(self, message):
        """Остановить фарм"""
        if not self.spam:
            await message.edit("<b>Нечего останавливать</b> ❗️")
            return
        self.spam = False
        await message.edit("<b>Фарм остановлен</b> ✋")

    async def zarcmd(self, message):
        """(@id/@user/t.me) Заражение по ID или юзернейму"""
        if self.spam:
            await message.edit("<b>Я не могу одновременно фармить и заражать, я не волшебный 😡</b>")
            return

        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Вы не указали ID или юзернейм</b> ❗️")
            return
        
        if not self.is_valid_username(args):
            await message.edit("<b>Неверный формат юзернейма или ID. Пожалуйста, проверьте и попробуйте снова.</b> ❗️")
            return

        selected_chat_key = self.config["selected_farm_chat"]
        chat_id = self.farm_chats.get(selected_chat_key, 0)
        if chat_id == 0:
            await message.edit("<b>ID чата не задан.</b>")
            return

        async with message.client.conversation(chat_id) as conv:
            try:
                while True:
                    if self.vaccine_needed:
                        await message.edit("<b>Вас заразили, лечу</b>")
                        await self.handle_infection(message.client, chat_id)

                    await message.client.send_message(chat_id, f"Заразить {str(args)}")

                    try:
                        evt = await asyncio.wait_for(conv.wait_event(events.NewMessage(incoming=True, from_users=chat_id)), timeout=5)
                        message_text = evt.message.message
                    except asyncio.TimeoutError:
                        await message.edit("<b>Ошибка: ID или юзернейм не настоящие. (возможно просто лагает ирис)</b> ❗️")
                        return

                    await message.edit(message_text)

                    if ("подверг заражению патогеном" in message_text or
                        "🤒 Недавно Вы уже подвергали заражению выбранный объект." in message_text or
                        "💢 Попытка заразить" in message_text or
                        "🥽 Иммунитет объекта" in message_text or
                        "📝 Пока не произведено ни одного патогена для заражения" in message_text or
                        "📝 У вас нет столько био-ресурсов или ирис-коинов" in message_text):
                        break

                    if self.is_fever_message(message_text) or self.is_infected_message(message_text):
                        await message.edit("<b>Вас заразили, лечу</b>")
                        await self.handle_infection(message.client, chat_id)

            except YouBlockedUserError:
                irises = {
                    "Ирис_чёрный": "<a href='https://t.me/iris_black_bot'>Ирис | Black Diamond</a>",
                    "Ирис_фиолетовый": "<a href='https://t.me/iris_dp_bot'>Ирис | Deep Purple</a>",
                    "Ирис_синий": "<a href='https://t.me/iris_cm_bot'>Ирис | Чат-менеджер</a>",
                    "Ирис_жёлтый": "<a href='https://t.me/iris_bs_bot'>Ирис | Bright Sophie</a>",
                    "Ирис_белый": "<a href='https://t.me/iris_moon_bot'>Ирис | Moonlight Dyla</a>"
                }
                iris_name = irises.get(selected_chat_key, "Неизвестный ирис")
                await message.edit(f"<b>{iris_name}</b> недоступен, возможно он заблокирован. Выберите другого или исправьте проблему.</b>")
            except Exception as e:
                error_trace = traceback.format_exc()
                error_msg = f"<b>Произошла ошибка: {str(e)}</b>\n<code>{error_trace}</code>"
                await message.edit(error_msg)

    async def masszarcmd(self, message):
        """(количество) Запуск автофарма"""
        selected_chat_key = self.config["selected_farm_chat"]
        chat_id = self.farm_chats.get(selected_chat_key, 0)
        if chat_id == 0:
            await message.edit("<b>ID чата не задан.</b>")
            return
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Вы не указали количество</b> ❗️")
            return

        if not args.isdigit():
            await message.edit("<b>Количество должно быть числом</b> ❗️")
            return

        if self.spam:
            await message.edit("<b>Я и так фармлю😡</b>")
            return

        async with message.client.conversation(chat_id) as conv:
            try:
                await message.edit('<b>Фарм запущен...</b> ⚗️')
                self.spam = True
                count = 0
                infection_command = self.config["infection_command"]

                while self.spam and count < int(args):
                    if self.vaccine_needed:
                        await self.handle_infection(message.client, chat_id)

                    await message.client.send_message(chat_id, infection_command)

                    try:
                        evt = await asyncio.wait_for(conv.wait_event(events.NewMessage(incoming=True, from_users=chat_id)), timeout=7)
                        message_text = evt.message.message

                        if self.is_no_resources_message(message_text) or self.is_no_pathogens_message(message_text):
                            await message.edit("<b>Фарм завершён из-за нехватки ресурсов.</b> ⚠️")
                            self.spam = False
                            break

                        if self.is_fever_message(message_text) or self.is_infected_message(message_text):
                            self.vaccine_needed = True
                            continue

                        if self.is_cured_message(message_text):
                            self.vaccine_needed = False
                    except asyncio.TimeoutError:
                        await message.edit("<b>Ирис лагает, попробуйте позже</b> ❗️")
                        self.spam = False
                        return

                    count += 1
                    await asyncio.sleep(self.command_delay)

                self.spam = False
                await message.edit("<b>Фарм завершен</b> ✔️")
            except YouBlockedUserError:
                irises = {
                    "Ирис_чёрный": "<a href='https://t.me/iris_black_bot'>Ирис | Black Diamond</a>",
                    "Ирис_фиолетовый": "<a href='https://t.me/iris_dp_bot'>Ирис | Deep Purple</a>",
                    "Ирис_синий": "<a href='https://t.me/iris_cm_bot'>Ирис | Чат-менеджер</a>",
                    "Ирис_жёлтый": "<a href='https://t.me/iris_bs_bot'>Ирис | Bright Sophie</a>",
                    "Ирис_белый": "<a href='https://t.me/iris_moon_bot'>Ирис | Moonlight Dyla</a>"
                }
                iris_name = irises.get(selected_chat_key, "Неизвестный ирис")
                await message.edit(f"<b>{iris_name}</b> недоступен, возможно он заблокирован. Выберите другого или исправьте проблему.</b>")
            except Exception as e:
                error_trace = traceback.format_exc()
                error_msg = f"<b>Произошла ошибка: {str(e)}</b>\n<code>{error_trace}</code>"
                await message.edit(error_msg)

    async def buy_vaccine_if_needed(self, client, chat):
        if not self.healing_in_progress:
            self.healing_in_progress = True
            await asyncio.sleep(2)
            await client.send_message(chat, "!купить вакцину")
            await asyncio.sleep(self.command_delay + 0.5)
            self.healing_in_progress = False

    async def handle_infection(self, client, chat):
        await self.buy_vaccine_if_needed(client, chat)
        await asyncio.sleep(2)

    def is_infected_message(self, message_text):
        owner_initials = self.me.first_name if self.me.first_name else self.me.username
        return any(keyword in message_text for keyword in [
            f"Кто-то подверг заражению {owner_initials}",
            f"подверг заражению патогеном {owner_initials}"
        ])

    def is_no_resources_message(self, message_text):
        return "📝 У вас нет столько био-ресурсов или ирис-коинов" in message_text

    def is_no_pathogens_message(self, message_text):
        return "📝 Пока не произведено ни одного патогена для заражения" in message_text

    def is_fever_message(self, message_text):
        return "🤒 У вас горячка, вызванная" in message_text

    def is_cured_message(self, message_text):
        return "💉 Вакцина излечила вас от горячки"

    async def watcher(self, message):
        try:
            selected_chat_key = self.config["selected_farm_chat"]
            chat_id = self.farm_chats.get(selected_chat_key, 0)
            if message.chat_id == chat_id:
                if self.is_infected_message(message.raw_text) or self.is_fever_message(message.raw_text):
                    self.vaccine_needed = True
                if self.is_cured_message(message.raw_text):
                    self.vaccine_needed = False
        except Exception as e:
            error_trace = traceback.format_exc()
            await message.client.send_message(message.chat_id, f"<b>Ошибка при автоматическом лечении:</b>\n{str(e)}\n<code>{error_trace}</code>")

    def is_valid_username(self, username):
        pattern = r"^(@[A-Za-z0-9_]{1,32}|[0-9]+|https?://t\.me/[A-Za-z0-9_]+)$"
        return re.match(pattern, username) is not None
