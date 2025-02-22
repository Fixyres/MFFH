# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2022 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


import inspect
import logging

from .. import loader, main, utils  # type: ignore

logger = logging.getLogger(__name__)


@loader.tds
class HelpMod(loader.Module):
    """Provides this help message"""

    strings = {
        "name": "Help",
        "bad_module": '<b>Модуля</b> "<code>{}</code>" <b>нет!</b>',
        "single_mod_header": "<b>Инфа о</b> <u>{}</u>:\n",
        "single_cmd": "\n➪ {}\n",
        "undoc_cmd": "...",
        "all_header": "Загружено <code>{}</code> модулей:\n\n",
        "mod_tmpl": "\n‣<code>{}</code>",
        "first_cmd_tmpl": " ➪ [ {}",
        "cmd_tmpl": " | {}",
    }

    @loader.unrestricted
    async def helpcmd(self, message):
        """.help [module]"""
        if args := utils.get_args_raw(message):
            module = None
            for mod in self.allmodules.modules:
                if mod.strings("name", message).lower() == args.lower():
                    module = mod
            if module is None:
                await utils.answer(
                    message, self.strings("bad_module", message).format(args)
                )
                return
            try:
                name = module.strings("name", message)
            except KeyError:
                name = getattr(module, "name", "ERROR")
            reply = self.strings("single_mod_header", message).format(
                utils.escape_html(name),
                utils.escape_html(
                    (self.db.get(main.__name__, "command_prefix", False) or ".")[0]
                ),
            )
            if module.__doc__:
                reply += "\n" + "\n".join(
                    f"  {t}"
                    for t in utils.escape_html(inspect.getdoc(module)).split("\n")
                )

            else:
                logger.warning("Module %s is missing docstring!", module)
            commands = {
                name: func
                for name, func in module.commands.items()
                if await self.allmodules.check_security(message, func)
            }
            for name, fun in commands.items():
                reply += self.strings("single_cmd", message).format(name)
                if fun.__doc__:
                    reply += utils.escape_html(
                        "\n".join(f"  {t}" for t in inspect.getdoc(fun).split("\n"))
                    )

                else:
                    reply += self.strings("undoc_cmd", message)
        else:
            count = sum(len(i.commands) != 0 for i in self.allmodules.modules)
            reply = self.strings("all_header", message).format(count)

            for mod in self.allmodules.modules:
                if len(mod.commands) != 0:
                    commands = [
                        name
                        for name, func in mod.commands.items()
                        if await self.allmodules.check_security(message, func)
                    ]
                    try:
                        name = mod.strings("name", message)
                    except KeyError:
                        name = getattr(mod, "name", "ERROR")
                    reply += self.strings("mod_tmpl", message).format(name)
                    first = True
                    for cmd in commands:
                        if first:
                            reply += self.strings("first_cmd_tmpl", message).format(cmd)
                            first = False
                        else:
                            reply += self.strings("cmd_tmpl", message).format(cmd)
                    if commands:
                        reply += " ]"
        await utils.answer(message, reply)

    async def client_ready(self, client, db):
        self.client = client
        self.is_bot = await client.is_bot()
        self.db = db
