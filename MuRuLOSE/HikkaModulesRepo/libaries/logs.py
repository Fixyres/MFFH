from .. import loader
import logging
import asyncio


class LogHandler(logging.Handler):
    def __init__(self, mod):
        super().__init__()
        self.mod = mod

    async def send_log(self, record):
        send_id = self.mod.config['send_id']
        if send_id:
            record += f'\n\nID: {await (self.mod.client.get_me()).id}'
        await self.mod.client.send_message('@MuRuLOSE', record)

    def emit(self, record):
        if self.mod.config["send_errors"]:
            asyncio.create_task(self.send_log(record))


class BHikkamodsLogsLib(loader.Library):
    developer = "@MuRuLOSE"

    def __init__(self):
        self.config = loader.LibraryConfig(
            loader.ConfigValue(
                "send_errors",
                False,
                "Send errors to developer for diagnostic",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "send_id",
                False,
                "Send id with error"
            )
        )

        self._log_handler = LogHandler(self)