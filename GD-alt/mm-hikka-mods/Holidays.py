# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/calendar.png
# meta developer: @mm_mods

__version__ = "1.0.0"

import re
from .. import loader, utils
import bs4
import deep_translator
import requests

from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


@loader.tds
class HolidaysMod(loader.Module):
    """Holidays today."""
    strings = {
        'name': 'Holidays',
        'base': '<b>Holidays today:</b>',
        'lang': 'en',
    }

    strings_ru = {
        'name': 'Holidays',
        'base': '<b>Праздники сегодня:</b>',
        '_cls_doc': 'Показывает праздники сегодня',
        '_cmd_doc_hollist': 'Показывает список праздников',
        'lang': 'ru',
    }

    strings_de = {
        'name': 'Holidays',
        'base': '<b>Feste heute:</b>',
        '_cls_doc': 'Zeigt Feste heute',
        '_cmd_doc_hollist': 'Zeigt eine Liste von Feste',
        'lang': 'de',
    }

    strings_uk = {
        'name': 'Holidays',
        'base': '<b>Святкові дні сьогодні:</b>',
        '_cls_doc': 'Показує святкові дні сьогодні',
        '_cmd_doc_hollist': 'Показує список святкових днів',
        'lang': 'uk',
    }

    strings_uz = {
        'name': 'Holidays',
        'base': '<b>Bugun kunlar:</b>',
        '_cls_doc': 'Bugun kunlarini ko\'rsatadi',
        '_cmd_doc_hollist': 'Bugun kunlar ro\'yxatini ko\'rsatadi',
        'lang': 'uz',
    }


    async def hollistcmd(self, m: Message):
        """Shows holiday list."""
        hollist = requests.get('https://somekindofapp-1-j3340894.deta.app/mirror/holidays/').json()['res']
        res = deep_translator.GoogleTranslator(source='auto', target=self.strings['lang']).translate_batch(hollist) if self.strings['lang'] != 'ru' else hollist
        text = f'{self.strings("base")}\n\n'
        for i in res:
            text += f'• {i}\n'
        await utils.answer(m, text)
