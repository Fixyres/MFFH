__version__ = (1, 0, 0)
#          █  █ █▄ █ █▄ █ █▀▀ ▀▄▀ █▀█ █▄ █
#          ▀▄▄▀ █ ▀█ █ ▀█ ██▄  █  █▄█ █ ▀█ ▄
#                © Copyright 2025
#            ✈ https://t.me/unneyon

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit, distribute or redistribute this file without direct permission from the author.

# meta banner: https://mods.unneyon.ru/banners/caliases.png
# meta pic: https://static.unneyon.ru/mods/caliases_icon.png
# meta developer: @unneyon_hmods
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
		"c404": "<emoji document_id=5312526098750252863>❌</emoji> Command <code>{}</code> not found!",
		"a404": "<emoji document_id=5312526098750252863>❌</emoji> Custom alias <code>{}</code> not found!",
		"no_args": "<emoji document_id=5312526098750252863>❌</emoji> You must specify two args: alias name and command",
		"added": (
			"<emoji document_id=5427009714745517609>✅</emoji> Custom alias <code>{alias}</code> "
			"for command <code>{prefix}{cmd}</code> successfully added\nUse it like: <code>{prefix}{alias}{args}</code>"
		),
		"argsopt": " [args (optional)]",
		"deleted": (
			"<emoji document_id=5427009714745517609>✅</emoji> Custom alias <code>{}</code> successfully deleted"
		),
		"list": "<emoji document_id=5373334855612375386>🔗</emoji> Custom aliases ({len}):\n",
		"no_aliases": "<emoji document_id=5312526098750252863>❌</emoji> You don't have custom aliases!"
	}

	strings_ru = {
		"c404": "<emoji document_id=5312526098750252863>❌</emoji> Команда <code>{}</code> не найдена!",
		"a404": "<emoji document_id=5312526098750252863>❌</emoji> Кастомный алиас <code>{}</code> не найден!",
		"no_args": "<emoji document_id=5312526098750252863>❌</emoji> Вы должны указать как минимум два аргумента: имя алиаса и команду",
		"added": (
			"<emoji document_id=5427009714745517609>✅</emoji> Успешно добавил алиас с названием <b>{alias}</b> "
			"для команды <code>{prefix}{cmd}</code>\nИспользуй его так: <code>{prefix}{alias}{args}</code>"
		),
		"argsopt": " [аргументы (необязательно)]",
		"deleted": (
			"<emoji document_id=5427009714745517609>✅</emoji> Кастомный алиас <code>{}</code> успешно удалён"
		),
		"list": "<emoji document_id=5373334855612375386>🔗</emoji> Кастомные алиасы (всего {len}):\n",
		"no_aliases": "<emoji document_id=5312526098750252863>❌</emoji> У вас нет кастомных алиасов!"
	}


	@loader.command(
		ru_doc="👉 Получить список всех алиасов",
		alias="calist"
	)
	async def caliasescmd(self, message: types.Message):
		"""👉 Get all aliases"""
		aliases = self.get("aliases", {})

		if len(aliases.keys()) == 0:
			await utils.answer(message, self.strings['no_aliases'])
			return

		out = self.strings['list'].format(len=len(aliases.keys()))
		for i in aliases.keys():
			out += f"  <emoji document_id=5280726938279749656>▪️</emoji> <code>{self.get_prefix()}{i}</code> &lt;- " \
				   f"<code>{self.get_prefix()}{aliases[i]['command'] + ('' if not aliases[i]['args'] else ' '+aliases[i]['args'])}</code>\n"

		await utils.answer(message, out)


	@loader.command(
		ru_doc="<имя> 👉 Удалить алиас"
	)
	async def rmcaliascmd(self, message: types.Message):
		"""<name> 👉 Remove alias"""
		args = utils.get_args(message)
		aliases = self.get("aliases", {})

		if not aliases.get(args[0]):
			await utils.answer(message, self.strings['a404'])
			return

		del aliases[args[0]]
		await utils.answer(message, self.strings['deleted'].format(args[0]))


	@loader.command(
		ru_doc="<имя> <команда>\n[аргументы] 👉 Добавить новый алиас (может содержать ключевое слово {args})"
	)
	async def caliascmd(self, message: types.Message):
		"""<name> <command>
		[args] 👉 Add new alias (may contain {args} keyword)"""
		rargs = utils.get_args_raw(message).split('\n')
		args = rargs[0].split()
		if len(args) < 2:
			await utils.answer(message, self.strings['no_args'])
			return

		name = args[0]
		cmd = args[1]
		cmdargs = "" if len(rargs) < 2 else rargs[1]

		if cmd not in self.allmodules.commands.keys():
			await utils.answer(message, self.strings['c404'].format(cmd))
			return

		aliases = self.get("aliases") if self.get("aliases") else {}
		als = aliases.get(args[0])
		aliases.update({args[0]: {"command": cmd, "args": cmdargs}})
		self.set("aliases", aliases)

		await utils.answer(message, self.strings['added'].format(
			alias=name, prefix=self.get_prefix(), cmd=cmd+' '+cmdargs if cmdargs else cmd, args=self.strings["argsopt"] if "{args}" in cmdargs else ""
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