from telethon.types import Message
from .. import loader, utils
import asyncio
import random
from telethon.errors.common import AlreadyInConversationError


"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    YamiManager
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HYVA.jpg
# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class YamiManager(loader.Module):
    """Module for @YamiChat_bot"""

    strings = {
        "name": "YamiManager",
        "timeout-error": "🚫 <b>The bot did not respond within three minutes, it is disabled or you asked it too complex request in /img</b>",
        "wait": "<i>Waiting...</i>\n\nInteresting fact! If the bot doesn't respond within three minutes, there will be an error",
        "alive": "💖 Bot is alive",
        "dead": "💔 Bot is dead...",
        "answer": "🔀 <b>Bot answer</b>:\n\n{}",
        "aleardyconv": "⛔ You can't execute more than one command",
        "genimgdisabled": "At the moment generate images disabled:\n\n{}",
        "sub-req": "Subscription is required for yami work, otherwise the module will not be removed and will not work before subscription",
        "copyright": "Result from <a href='tg://resolve?domain=YamiChat_bot'>Yami's bot 💘</a>",
    }

    strings_ru = {
        "timeout-error": "🚫 <b>Бот не ответил в течении трёх минут, он отключён либо же вы задали ему слишком сложный запрос в /img</b>",
        "wait": "<i>Ожидаю...</i>\n\nИнтересный факт! Если бот не ответит в течении трёх минут, то будет ошибка",
        "alive": "💖 Бот жив!",
        "dead": "💔 Бот мёртв...",
        "answer": "🔀 <b>Ответ бота</b>:\n\n{}",
        "aleardyconv": "⛔ Нельзя выполнять больше одной команды",
        "genimgdisabled": "В данный момент генерация изображений отключена:\n\n{}",
        "sub-req": "Подписка необходима для работы ями, иначе модуль не будет удалён и не будет работать до подписки",
        "copyright": "Результат из <a href='tg://resolve?domain=YamiChat_bot'>бота Ями 💘</a>",
        "_cls_doc": "Модуль для @YamiChat_bot",
    }

    def __init__(self):
        self.bot = "YamiChat_bot"

    async def check_ban(self, text, message):
        if "Не пиши" in text:
            await utils.answer(
                message, "Как ты мог обидеть ями? Теперь я тоже обижена!"
            )
            return await self.invoke("unloadmod", "YamiManager", message.peer_id)

    @loader.command(
        ru_doc=" [команда] [запрос] - Отправить команду Ями бот\nПример: .scmmnd /img аргументы с запросом"
    )
    async def scmmnd(self, message: Message):
        """[cmd] [request] - Send command to Yami bot\nExample: .scmmnd /img arguments with req"""
        args = utils.get_args_raw(message).split()
        req = " ".join(args[1:])

        await utils.answer(message, f"☁ {self.strings['wait']}")
        try:
            async with self.client.conversation(self.bot, timeout=180) as conv:
                try:
                    await conv.send_message(f"{args[0]} {req}")
                    res = await conv.get_response()
                    await self.check_ban(res.raw_text, message)

                    if "Вы не подписаны на все каналы" in res.raw_text:
                        await utils.answer(
                            message, f"Check @{self.inline.bot_username}"
                        )

                        return await self.request_join(
                            "YamiChannel",
                            f"{self.strings['sub-req']}",
                            assure_joined=True,
                        )

                    if (
                        "✅ Запрос принят! Пожалуйста подожди 1-3 минуты, оно того стоит :3"
                        in res.raw_text
                    ):
                        await asyncio.sleep(10)
                        res = await conv.get_response()

                    elif (
                        "❌Генерация изображений отключена на данный момент! Мы уже работаем над восстановлением!"
                        in res.raw_text
                    ):
                        return await utils.answer(
                            message, self.strings["genimgdisabled"].format(res.text)
                        )

                    await conv.mark_read()

                except asyncio.TimeoutError:
                    return await utils.answer(message, self.strings["timeout-error"])
        except AlreadyInConversationError:
            return await utils.answer(message, self.strings["aleardyconv"])

        if res.media is not None:
            return await utils.answer(
                message,
                res.media,
                caption=self.strings["answer"].format(res.text)
                + (
                    ("\n\n") + self.strings["copyright"]
                    if random.randint(0, 10) <= 5
                    else ""
                ),
                as_file=True,
            )

        else:
            return await utils.answer(
                message,
                self.strings["answer"].format(res.text)
                + (
                    ("\n\n") + self.strings["copyright"]
                    if random.randint(0, 10) <= 5
                    else ""
                ),
            )

    @loader.command(ru_doc=" - Проверьте, жив ли бот")
    async def chalive(self, message: Message):
        """- Check, to see if the bot is alive"""
        try:
            async with self.client.conversation(self.bot, timeout=10) as conv:
                try:
                    await conv.send_message("/start")
                    res = await conv.get_response()
                    await self.check_ban(res.raw_text, message)
                except asyncio.TimeoutError:
                    return await utils.answer(message, self.strings["dead"])

                finally:
                    conv.cancel()

        except AlreadyInConversationError:
            return await utils.answer(message, self.strings["aleardyconv"])

        await utils.answer(message, self.strings["alive"])
