from hikkatl.types import Message
from .. import loader, utils
import asyncio
import logging

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    BashWatcher
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: https://0x0.st/HgiU.jpg
# meta desc:  Is it annoying to write the terminal command every time before writing something?\nNow the problem is solved! You can set a local prefix and it will work! Example: &ls -l
# meta developer: @BruhHikkaModules

logger = logging.getLogger(__name__)


@loader.tds
class BashWatcher(loader.Module):
    """
    Is it annoying to write the terminal command every time before writing something?
    Now the problem is solved! You can set a local prefix and it will work! Example: &ls -l
    """

    strings = {
        "name": "BashWatcher",
        "more-one-symbol": "<emoji document_id=5228947933545635555>😫</emoji> More than one character in the prefix is not allowed.",
        "successfull-set-prefix": "<emoji document_id=5474667187258006816>😎</emoji> Prefix {} successfully is set",
        "output-terminal": "<b>Command:</b> <code>{}</code>"
        "\n\n<b><emoji document_id=5361735750968679136>🖥</emoji> Stdout:</b>"
        "\n<code>{}</code>"
        "\n<emoji document_id=5472267631979405211>🚫</emoji> <b>Stderr:</b>"
        "\n<code>{}</code>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(loader.ConfigValue("prefix", "*"))

    @loader.watcher()
    async def watcher(self, message: Message):
        prefix = self.config["prefix"]
        me = await self.client.get_me(id)
        user_id = me.user_id
 
        if message.text.startswith(prefix) and message.from_id == user_id:
            await utils.answer(message, "<emoji document_id=5451646226975955576>⌛️</emoji>")
            commands_raw: list = message.text.split()
            del commands_raw[0]
            commands = ' '.join(commands_raw)
            stdout, stderr = await self.run_command(commands)

            await utils.answer(
                message,
                self.strings["output-terminal"].format(commands, stdout, stderr),
            )

    @loader.command(ru_doc=" [Префикс] - Поставь префикс для терминала")
    async def setprefixbash(self, message: Message):
        """[Prefix] - Set prefix for terminal"""
        args = utils.get_args_raw(message)
        if len(args) > 1:
            await utils.answer(message, self.strings["more-one-symbol"])

        self.config["prefix"] = args
        await utils.answer(message, self.strings["successfull-set-prefix"].format(args))

    async def run_command(self, command: str):
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode(), stderr.decode()


# ёбнуть black
