import datetime
import logging
import time

from telethon.tl.types import Message

from .. import loader, main, utils

logger = logging.getLogger(__name__)


class CendPingMod(loader.Module):
    '''Испралвкный модуль CendPing от @zxcendi, испправлял @userbotik'''
    strings = {
        "name": "CendPing",
        "uptime": "🕷️ <b>Аптайм</b>",
        "com": "{} <code>{}</code> <b>мс</b>\n{}",
        "modulesupports": "Модуль поддерживает значения {time} и {uptime}",
        "pingmsg": "Тут вы можете изменить ответное сообщения команды"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ceping_message",
                "<emoji document_id=5431449001532594346>⚡️</emoji> <b>Ping:</b>",
                lambda: self.strings("cepingmsg"),
            ),
            loader.ConfigValue(
                "custom_message",
                "<emoji document_id=5445284980978621387>🚀</emoji> <b>Uptime: {uptime}</b>",
                doc=lambda: self.strings("modulesupports"),
            ),
            loader.ConfigValue(
                "download",
                "<emoji document_id=5188377234380954537>🌘</emoji>",
                doc=lambda: self.strings("modulesupports"),
            ),
            loader.ConfigValue(
                "timezone",
                "3",
                lambda: "используйте 1, -1, -3 и т. д. для корректировки времени сервера на {time}.",
            ),
        )

    def _render_ping(self):
        offset = datetime.timedelta(hours=self.config["timezone"])
        tz = datetime.timezone(offset)
        time2 = datetime.datetime.now(tz)
        time = time2.strftime("%H:%M:%S")
        uptime = utils.formatted_uptime()
        return (
            self.config["custom_message"].format(
                time=time,
                uptime=uptime,
            )
            if self.config["custom_message"] != "no"
            else (f'{self.strings("uptime")}: <b>{uptime}</b>')
        )

    @loader.command(command="p", aliases=["ping"])
    async def p(self, message: Message):
        """- Получить пинг"""
        ceping = self.config["ceping_message"]
        start = time.perf_counter_ns()
        download_config = self.config["download"]
        
        if isinstance(download_config, set):
            download_config = list(download_config)  # Преобразовать set в list
            message = await utils.answer(message, download_config)
        else:
            message = await utils.answer(message, download_config)
        
        try:
            await utils.answer(
                message,
                self.strings("com").format(
                    ceping,
                    round((time.perf_counter_ns() - start) / 10**6, 3),
                    self._render_ping(),
                ),
            )
        except TypeError:
            await utils.answer(
                message,
                "Неверное число в .config -> cenping -> timezone, пожалуйста, обновите его",
            )