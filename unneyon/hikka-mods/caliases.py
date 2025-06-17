__version__ = (1, 0, 0)
#          █▄▀ ▄▀█ █▀▄▀█ █▀▀ █▄▀ █  █ █▀█ █▀█
#          █ █ █▀█ █ ▀ █ ██▄ █ █ ▀▄▄▀ █▀▄ █▄█ ▄
#                © Copyright 2025
#            ✈ https://t.me/kamekuro

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit, distribute or redistribute this file without direct permission from the author.

# meta banner: https://raw.githubusercontent.com/kamekuro/hikka-mods/main/banners/caliases.png
# meta pic: https://raw.githubusercontent.com/kamekuro/hikka-mods/main/icons/caliases.png
# meta developer: @kamekuro_hmods
# scope: hikka_only
# scope: hikka_min 1.6.3

import logging

from telethon import types

from .. import loader, utils


logger = logging.getLogger(__name__)


@loader.tds
class CustomAliasesMod(loader.Module):
    """Module for custom aliases"""

    strings = {
        "name": "CAliases",
        "c404": "<emoji document_id=5312526098750252863>❌</emoji> <b>Command <code>{}</code> not found!</b>",
        "a404": "<emoji document_id=5312526098750252863>❌</emoji> <b>Custom alias <code>{}</code> not found!</b>",
        "no_args": "<emoji document_id=5312526098750252863>❌</emoji> <b>You must specify two args: alias name and command</b>",
        "added": (
            "<emoji document_id=5314250708508220914>✅</emoji> <b>Custom alias <i>{alias}</i> for command "
            "<code>{prefix}{cmd}</code> successfully added!</b>\n<b>Use it like:</b> <code>{prefix}{alias}{args}</code>"
        ),
        "argsopt": " [args (optional)]",
        "deleted": "<emoji document_id=5314250708508220914>✅</emoji> <b>Custom alias <code>{}</code> successfully deleted</b>",
        "list": "<emoji document_id=5974492756494519709>🔗</emoji> <b>Custom aliases ({len}):</b>\n",
        "no_aliases": "<emoji document_id=5312526098750252863>❌</emoji> <b>You have no custom aliases!</b>"
    }

    strings_ru = {
        "c404": "<emoji document_id=5312526098750252863>❌</emoji> <b>Команда <code>{}</code> не найдена!</b>",
        "a404": "<emoji document_id=5312526098750252863>❌</emoji> <b>Кастомный алиас <code>{}</code> не найден!</b>",
        "no_args": "<emoji document_id=5312526098750252863>❌</emoji> <b>Вы должны указать как минимум два аргумента: имя алиаса и команду</b>",
        "added": (
            "<emoji document_id=5314250708508220914>✅</emoji> <b>Успешно добавил алиас с названием <i>{alias}</i> "
            "для команды <code>{prefix}{cmd}</code></b>\n<b>Используй его так:</b> <code>{prefix}{alias}{args}</code>"
        ),
        "argsopt": " [аргументы (необязательно)]",
        "deleted": "<emoji document_id=5314250708508220914>✅</emoji> <b>Кастомный алиас <code>{}</code> успешно удалён</b>",
        "list": "<emoji document_id=5974492756494519709>🔗</emoji> <b>Кастомные алиасы (всего {len}):</b>\n",
        "no_aliases": "<emoji document_id=5312526098750252863>❌</emoji> <b>У вас нет кастомных алиасов!</b>"
    }


    @loader.command(
        ru_doc="👉 Получить список всех алиасов",
        alias="calist"
    )
    async def caliasescmd(self, message: types.Message):
        """👉 Get all aliases"""

        aliases = self.get("aliases", {})
        if not aliases:
            return await utils.answer(message, self.strings['no_aliases'])

        out = self.strings['list'].format(len=len(aliases.keys()))
        for alias in aliases.keys():
            cmd = aliases[alias]['command']
            if aliases[alias]['args']:
                cmd += f" {aliases[alias]['args']}"
            out += f"  <emoji document_id=5280726938279749656>▪️</emoji> <code>{alias}</code> " \
                   f"<emoji document_id=5960671702059848143>👈</emoji> <code>{cmd}</code>\n"

        await utils.answer(message, out)


    @loader.command(
        ru_doc="<имя> 👉 Удалить алиас"
    )
    async def rmcaliascmd(self, message: types.Message):
        """<name> 👉 Remove alias"""

        args = utils.get_args(message)
        aliases = self.get("aliases", {})
        if args[0] not in aliases:
            return await utils.answer(message, self.strings['a404'])

        del aliases[args[0]]
        self.set("aliases", aliases)
        await utils.answer(message, self.strings['deleted'].format(args[0]))


    @loader.command(
        ru_doc="<имя> <команда> [аргументы] 👉 Добавить новый алиас (может содержать ключевое слово {args})"
    )
    async def caliascmd(self, message: types.Message):
        """<name> <command> [args] 👉 Add new alias (may contain {args} keyword)"""

        rargs = " ".join(utils.get_args_raw(message).split(' ')[2:])
        args = utils.get_args(message)
        if len(args) < 2:
            return await utils.answer(message, self.strings['no_args'])
        name = args[0]
        cmd = args[1]
        cmdargs = rargs
        if cmd not in self.allmodules.commands.keys():
            return await utils.answer(message, self.strings['c404'].format(cmd))

        aliases = self.get("aliases", {})
        aliases[str(args[0])] = {"command": cmd, "args": cmdargs}
        self.set("aliases", aliases)
        await utils.answer(message, self.strings['added'].format(
            alias=name,
            prefix=self.get_prefix(),
            cmd=cmd+' '+cmdargs if cmdargs else cmd,
            args=self.strings["argsopt"] if "{args}" in cmdargs else ""
        ))


    @loader.tag(
        only_messages=True, no_media=True, no_inline=True,
        out=True
    )
    async def watcher(self, message):
        aliases = self.get("aliases", {})
        command = message.raw_text.lower().split()[0]
        if (command[0] == self.get_prefix()) and (command[1:] in aliases.keys()):
            text = message.raw_text.lower()
            args = utils.get_args_raw(message)
            ass = aliases[command[1:]]

            await self.allmodules.commands[ass['command']](
                await utils.answer(
                    message,
                    (self.get_prefix() + ass['command'] + '@me ' + ass['args']).format(args=args)
                )
            )