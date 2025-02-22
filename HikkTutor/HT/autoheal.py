__version__ = (1, 0, 4)
# ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ© Copyright 2024
# ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤhttps://t.me/unnic
# 🔒ㅤㅤㅤㅤㅤLicensed under the GNU AGPLv3
# 🌐ㅤㅤhttps://www.gnu.org/licenses/agpl-3.0.html
# ┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
# ┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
# ┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
# ┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
# ┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
# ┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: @unnic
# name: autoheal
# ██╗░░░██╗███╗░░██╗███╗░░██╗██╗░█████╗░
# ██║░░░██║████╗░██║████╗░██║██║██╔══██╗
# ██║░░░██║██╔██╗██║██╔██╗██║██║██║░░╚═╝
# ██║░░░██║██║╚████║██║╚████║██║██║░░██╗
# ╚██████╔╝██║░╚███║██║░╚███║██║╚█████╔╝
# ░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚═╝░╚════╝

from .. import loader
import asyncio
import traceback

class SmartAutoHeal(loader.Module):
    """Модуль для автохила при заражении или горячке в ЛС игрового бота"""

    strings = {'name': 'AutoHeal'}
    vaccine_needed = False
    healing_in_progress = False
    module_disabled = False
    spam_in_progress = False

    allowed_bots = {
        5443619563,
        5226378684,
        707693258,
        5137994780,
        5434504334
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "BOT_CHAT_ID",
                5443619563,
                "ID чата игрового бота, с которым будет работать модуль"
            )
        )

    async def client_ready(self, client, db):
        self.me = await client.get_me()

        bot_chat_id = self.config["BOT_CHAT_ID"]
        if bot_chat_id not in self.allowed_bots:
            self.config["BOT_CHAT_ID"] = 5443619563
            await client.send_message(self.me.id, "<b>Некорректный ID бота в конфигурации. ID сброшен на стоковый: 5443619563</b>")

    async def buy_vaccine_if_needed(self, client, chat):
        if not self.vaccine_needed and not self.healing_in_progress:
            self.vaccine_needed = True
            self.healing_in_progress = True

            await asyncio.sleep(1.5)
            await client.send_message(chat, "!купить вакцину")
            await asyncio.sleep(5)

            last_message = (await client.get_messages(chat, limit=1))[0]
            if "📝 У вас нет столько био-ресурсов или ирис-коинов" in last_message.raw_text:
                self.module_disabled = True
                self.vaccine_needed = False
            else:
                self.healing_in_progress = False

    def is_infected_message(self, message_text):
        return ("Кто-то подверг заражению неизвестным патогеном" in message_text or
                "подверг заражению патогеном" in message_text)

    def is_fever_message(self, message_text):
        return "🤒 У вас горячка, вызванная" in message_text

    def is_cured_message(self, message_text):
        return "💉 Вакцина излечила вас от горячки" in message_text

    def is_buy_vaccine_command(self, message_text):
        return "!купить вакцину" in message_text

    def is_infect_command(self, message_text):
        return any(cmd in message_text for cmd in ["!заразить", "/заразить", "заразить"])

    async def watcher(self, message):
        try:
            bot_chat_id = self.config["BOT_CHAT_ID"]

            if bot_chat_id not in self.allowed_bots:
                await message.client.send_message(message.chat_id, "<b>Неправильный ID бота. Убедитесь, что вы используете правильный id бота.</b>")
                self.config["BOT_CHAT_ID"] = 5443619563
                await message.client.send_message(message.chat_id, "<b>ID сброшен на стоковый: 5443619563</b>")
                return

            if message.chat_id == bot_chat_id:
                if not self.module_disabled:
                    if self.is_infected_message(message.raw_text) or self.is_fever_message(message.raw_text):
                        if self.spam_in_progress:
                            return

                        self.spam_in_progress = True
                        await self.buy_vaccine_if_needed(message.client, message.chat_id)
                        self.spam_in_progress = False

                    if self.is_cured_message(message.raw_text):
                        self.vaccine_needed = False

                if "📝 У вас нет столько био-ресурсов или ирис-коинов" in message.raw_text:
                    self.module_disabled = True
                    await message.client.send_message(message.chat_id, "<b>Модуль отключён из-за недостатка ресурсов.</b>")

                if self.is_buy_vaccine_command(message.raw_text) or self.is_infect_command(message.raw_text):
                    if self.module_disabled:
                        self.module_disabled = False
                        await message.client.send_message(message.chat_id, "<b>Я вижу, вы начали пользоваться ботом.\nВключаю автохил.</b>")

        except Exception as e:
            error_trace = traceback.format_exc()
            await message.client.send_message(message.chat_id, f"<b>Ошибка при автоматическом лечении:</b>\n{str(e)}\n{error_trace}")

    @loader.command(ru_doc="Показать список игровых ботов")
    async def show_bots(self, message):
        """Список разрешённых ботов и их id"""
        await message.client.send_message(
            message.chat_id,
            f"<b>Список разрешённых игровых ботов:</b>\n\n"
            f"🎩 <a href='tg://user?id=5443619563'>Iris | Black Diamond</a> ⮕ <code>5443619563</code>\n"
            f"🟣 <a href='tg://user?id=5226378684'>Iris | Deep Purple</a> ⮕ <code>5226378684</code>\n"
            f"🔵 <a href='tg://user?id=707693258'>Iris | Чат-менеджер</a> ⮕ <code>707693258</code>\n"
            f"🟡 <a href='tg://user?id=5137994780'>Iris | Bright Sophie</a> ⮕ <code>5137994780</code>\n"
            f"⚪️ <a href='tg://user?id=5434504334'>Iris | Moonlight Dyla</a> ⮕ <code>5434504334</code>\n\n"
            f"<b>Внимание!</b> id бота используйте по назначению.\n"
            f"id бота используется в конфиге, без @\n\n"
            f"<b>По умолчанию работаю с: </b> 🎩 <a href='tg://user?id=5443619563'>Iris | Black Diamond</a>",
            parse_mode="HTML"
        )

# Хер # Херня # Хератень # Нахер # Захер # Похер
# Может быть                     # Не может быть
