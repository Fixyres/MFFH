# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM          
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd 
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `" 
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.  
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8 
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/sticker.png
# meta developer: @mm_mods

__version__ = "1.0.0"

from .. import loader, utils
import random

from telethon.tl.types import Message
import logging

logger = logging.getLogger(__name__)


# Database in format {name: {id: in_chat_id}}
db = {
    'cherry': {'1': 2, '2': 3, '3': 4},
    'fox1': {'1': 5, '2': 6, '3': 7, '4': 8},
    'goose': {'1': 9, '2': 10, '3': 11, '4': 12, '5': 13, '6': 14},
    'balloon': {'1': 15, '2': 16, '3': 17, '4': 18},
    'cats': {'1': 19, '2': 20, '3': 21, '4': 22, '5': 23},
    'croco1': {'1': 24, '2': 25, '3': 26, '4': 27, '5': 28},
    'puppy': {'1': 29, '2': 30},
    'peach': {'1': 31, '2': 32},
    'monkey1': {'1': 33, '2': 34},
    'fox2': {'1': 35, '2': 36, '3': 37, '4': 38},
    'duck': {'1': 39, '2': 40, '3': 41, '4': 42},
    'fire': {'1': 43, '2': 44, '3': 45, '4': 46},
    'tiger': {'1': 47, '2': 48, '3': 49, '4': 50},
    'bud': {'1': 51, '2': 52},
    'croco2': {'1': 53, '2': 54, '3': 55, '4': 56},
    'lady': {'1': 57, '2': 58, '3': 59},
    'cat1': {'1': 60, '2': 61, '3': 62},
    'crab': {'1': 63},
    'bunny': {'1': 64, '2': 65, '3': 66, '4': 67, '5': 68},
    'arts': {'1': 69, '2': 70, '3': 71},
    'lamb': {'1': 72, '2': 73, '3': 74},
    'hands': {'1': 75, '2': 76, '3': 77, '4': 78},
    'shiba': {'1': 79, '2': 80, '3': 81},
    'cloud': {'1': 82},
    'cang': {'1': 83},
    'made': {'1': 84, '2': 85},
    'donut': {'1': 86},
    'frog': {'1': 87},
    'dog': {'1': 88, '2': 89},
    'monkey2': {'1': 90, '2': 91},
    'hearts': {'1': 92, '2': 93},
    'seagull': {'1': 94, '2': 95, '3': 96},
    'cat2': {'1': 97, '2': 98, '3': 99},
    'dino': {'1': 100, '2': 101, '3': 102},
    'strawberry': {'1': 103, '2': 104, '3': 105, '4': 106},
      }


@loader.tds
class PSAMod(loader.Module):
    """Send premium stickers without premium! Advanced version of Hikariatama's module."""
    strings = {
        'name': 'PremiumStickers2',
        'pack?': '🟨 <b>You need to specify a pack name.</b>',
        'pack?!': '🟥 <b>There is no such pack.</b>',
        'sticker?': '🟨 <b>You need to specify a sticker number.</b>',
        'sticker?!': '🟥 <b>There is no such sticker in this pack.</b>',
        'args?': '🟨 <b>No arguments.</b>\n<b>Usage:</b> <code>.psa pack_name sticker_number</code>',
        'packs': '📜 <b>Available packs:</b>\n'
    }

    strings_ru = {
        'pack?': '🟨 <b>Вы должны указать название пака.</b>',
        'pack?!': '🟥 <b>Такого пака нет.</b>',
        'sticker?': '🟨 <b>Вы должны указать номер стикера.</b>',
        'sticker?!': '🟥 <b>Такого стикера в этом паке нет.</b>',
        'args?': '🟨 <b>Нет аргументов.</b>\n<b>Использование:</b> <code>.psa название_пака номер_стикера</code>',
        'packs': '📜 <b>Доступные паки:</b>\n',
        '_cls_doc': 'Отправляй премиум-стикеры без премиума! Улучшеная версия модуля от Хикари (@hikarimods).',
        '_cmd_doc_psa': 'Отправить стикер из пака … под номером … .',
        '_cmd_doc_psalist': 'Список паков и количество стикеров в них.'
    }

    strings_uk = {
        'pack?': '🟨 <b>Ви повинні вказати назву паку.</b>',
        'pack?!': '🟥 <b>Такого паку немає.</b>',
        'sticker?': '🟨 <b>Ви повинні вказати номер стікера.</b>',
        'sticker?!': '🟥 <b>Такого стікера в цьому паку немає.</b>',
        'args?': '🟨 <b>Немає аргументів.</b>\n<b>Використання:</b> <code>.psa назва_паку номер_стікера</code>',
        'packs': '📜 <b>Доступні паки:</b>\n',
        '_cls_doc': 'Відправляй преміум-стікери без преміума! Покращена версія модуля від Хікарі (@hikarimods).',
        '_cmd_doc_psa': 'Відправити стікер з паку … під номером … .',
        '_cmd_doc_psalist': 'Список паків і кількість стікерів в них.'
    }

    async def psacmd(self, m: Message):
        """Sends from pack … sticker number … ."""
        args = utils.get_args_raw(m)
        if args == '':
            return await utils.answer(m, self.strings('args?'))
        if ' ' not in args:
            return await utils.answer(m, self.strings('sticker?'))
        pack, num = args.split(' ', 1)
        if not num.isdigit():
            return await utils.answer(m, self.strings('sticker?!'))
        if pack not in db.keys():
            return await utils.answer(m, self.strings('pack?!'))
        if num not in db[pack].keys():
            return await utils.answer(m, self.strings('sticker?!'))
        if m.out:
            await m.delete()
        await m.respond(f'<a href="https://t.me/hikka_premum_stickers/{db[pack][num]}">­</a>')


    async def psalistcmd(self, m: Message):
        """Packs list."""
        plist = self.strings('packs')
        for i in db.keys():
            plist += f'<code>{i}</code> (<a href="https://t.me/hikka_premum_stickers/{db[i]["1"]}">{len(db[i])}</a>)\n'
        await utils.answer(m, plist)
