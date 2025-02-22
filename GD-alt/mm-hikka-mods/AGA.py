# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/block.png
# meta developer: @mm_mods

__version__ = "1.0.0"

import asyncio
from hikka import loader, utils
import requests
import telethon as tt
from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


@loader.tds
class AbsolutGrossartigAntwortMod(loader.Module):
    """Tired of people asking you questions? Let this module answer them for you!
    P.S. Author is not responsible for all your problems after using it."""

    strings = {
        'name': 'AGA!',
        'langneeded': 'en'
    }

    strings_ru = {
        '_cls_doc': 'Достали вопросы? Этот модуль ответит на них за вас!\nP.S. Автор не несет ответственности за все '
                    'ваши проблемы после использования этого модуля.',
        'langneeded': 'ru',
        '_cmd_doc_aga': 'Используйте эту команду, чтобы ответить на вопрос.',
    }

    async def agacmd(self, m: Message):
        """Use this command to answer the question."""
        reply = await m.get_reply_message()
        if not reply:
            result = requests.post('https://somekindofapp-1-j3340894.deta.app/post/aga', json={'basetext': '',
                                                                             'lang_needed': self.strings('langneeded')})
            await utils.answer(m, result.json()['r'])
        else:
            result = requests.post('https://somekindofapp-1-j3340894.deta.app/post/aga', json={'basetext': reply.text,
                                                                             'lang_needed': self.strings('langneeded')})
            await utils.answer(m, result.json()['r'])

    async def watcher(self, m: Message):
        if m.text.casefold() == 'ага':
            await self.agacmd(m)
