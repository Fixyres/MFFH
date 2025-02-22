# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/diamond-heart.png
# meta developer: @mm_mods

__version__ = "1.0.0"

import asyncio
from .. import loader, utils
import telethon as tt
from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


# Dict with all public reactions of Telegram in format {name: emoji}
edb = {
    "like": "👍",
    "dislike": "👎",
    "love": "❤️",
    "fire": "🔥",
    "haround": "🥰",
    "clap": "👏",
    "laugh": "😁",
    "suspect": "🤔",
    "mindblown": "🤯",
    "horror": "😱",
    "angry": "🤬",
    "sad": "😢",
    "fest": "🎉",
    "stareyes": "🤩",
    "womit": "🤮",
    "poop": "💩",
    "pray": "🙏",
    "ok": "👌",
    "peace": "🕊️",
    "clown": "🤡",
    "tired": "🥱",
    "drunk": "🥴",
    "hearteyes": "😍",
    "whale": "🐳",
    "flameheart": "❤️\u200d🔥",
    "moon": "🌚",
    "hotdog": "🌭",
    "100": "💯",
    "laughcry": "😂",
    "220": "⚡",
    "banana": "🍌",
    "cup": "🏆",
    "brokenheart": "💔",
    "hm": "🤨",
    "what": "😐",
    "berry": "🍓",
    "bottle": "🍾",
    "kiss": "💋",
    "fuck": "🖕",
    "devil": "😈",
}


@loader.tds
class ReactTorMod(loader.Module):
    """Reacts manager."""
    strings = {
        'name': 'Reactor',
        'reply?': '🟨 <b>You need to reply a message.</b>',
        'name?': '🟨 <b>You need to specify a name.</b>',
        'emoji?': '🟨 <b>You need to specify an emoji.</b>',
        'name?!': '🟥 <b>Invalid name.</b>',
        'emoji?!': '🟥 <b>Invalid emoji.</b>',
        'done': '🟩 <b>Done.</b>',
        'shorthand_done': '🟩 <b>Created shorthand «{}» for {}.</b>',
    }

    strings_ru = {
        'reply?': '🟨 <b>Тебе нужно ответить на сообщение.</b>',
        'name?': '🟨 <b>Тебе нужно указать имя.</b>',
        'emoji?': '🟨 <b>Тебе нужно указать эмодзи.</b>',
        'name?!': '🟥 <b>Неверное имя.</b>',
        'emoji?!': '🟥 <b>Неверный эмодзи.</b>',
        'done': '🟩 <b>Готово.</b>',
        'shorthand_done': '🟩 <b>Создан ярлык «{}» для {}.</b>',
        '_cls_doc': 'Менеджер реакций.',
        '_cmd_doc_rshorthand': 'Создать ярлык для реакции.\n/rshorthand <имя> <эмодзи>',
        '_cmd_doc_dshorthand': 'Удалить ярлык для реакции.\n/dshorthand <имя>',
        '_cmd_doc_shorthands': 'Показать все ярлыки для реакций.',
        '_cmd_doc_react': 'Реагирует на сообщение.\n/react <имя>',
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        if not self.get("shorthands", False):
            self.set("shorthands", {})

    async def rshorthandcmd(self, m: Message):
        """Add a shorthand for a reaction.
        /rshorthand <name> <emoji>"""
        args = utils.get_args_raw(m)
        if not args:
            return await utils.answer(m, self.strings('name?'))
        args = args.split(" ")
        if len(args) < 2:
            return await utils.answer(m, self.strings('emoji?'))
        name = args[0]
        emoji = args[1]
        if name in edb.keys():
            return await utils.answer(m, self.strings('name?!'))
        if emoji not in edb.values() and not isinstance(m.entities[0], tt.tl.types.MessageEntityCustomEmoji):
            return await utils.answer(m, self.strings('emoji?!'))
        shorthands = self.get("shorthands", {})
        if name in shorthands.keys():
            return await utils.answer(m, self.strings('name?!'))
        if isinstance(m.entities[0], tt.tl.types.MessageEntityCustomEmoji):
            emoji = m.entities[0].document_id
        shorthands[name] = emoji
        self.set("shorthands", shorthands)
        await utils.answer(m, self.strings('shorthand_done').format(name, emoji))

    async def dshorthandcmd(self, m: Message):
        """Delete a shorthand for a reaction.
        /dshorthand <name>"""
        args = utils.get_args_raw(m)
        if not args:
            return await utils.answer(m, self.strings('name?'))
        shorthands = self.get("shorthands", {})
        if args not in shorthands.keys():
            return await utils.answer(m, self.strings('name?!'))
        del shorthands[args]
        self.set("shorthands", shorthands)
        await utils.answer(m, self.strings('done'))

    async def shorthandscmd(self, m: Message):
        """Show all shorthands for reactions."""
        shorthands = self.get("shorthands", {})
        text = "<b>Ярлыки реакций:</b>\n"+ "".join(f"{name} - {emoji}\n" for name, emoji in shorthands.items()) + "<b>Стандартные ярлыки реакций:</b>\n" + "".join(f"{name} - {emoji}\n" for name, emoji in edb.items())
        await utils.answer(m, text)

    async def reactcmd(self, m: Message):
        """React to a message.
        /react <name>/<emoji>"""
        args = utils.get_args_raw(m)
        if not args:
            return await utils.answer(m, self.strings('name?'))
        if args in edb.keys():
            emoji = edb[args]
        else:
            shorthands = self.get("shorthands", {})
            if args in shorthands.keys():
                emoji = shorthands[args]
            else:
                return await utils.answer(m, self.strings('name?!'))
        if not m.is_reply:
            return await utils.answer(m, self.strings('reply?'))
        reply = await m.get_reply_message()
        if isinstance(emoji, str):
            await reply.react(emoji)
        else:
            await reply.react(tt.tl.types.ReactionCustomEmoji(emoji))
        await utils.answer(m, self.strings('done'))
        await asyncio.sleep(1)
        await m.delete()
