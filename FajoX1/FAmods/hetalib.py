#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: HetaLib
# Description: Модуль для работы с heta
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/hetalib.png?raw=true
# requires: heta==1.0.2 requests
# ---------------------------------------------------------------------------------

import heta
import asyncio
import requests

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class HetaLib(loader.Module):
    """Модуль для работы с heta"""

    strings = {
        "name": "HetaLib",

        "no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть <code>{}hsearch [запрос]</code></b>",
        "no_hh": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть <code>{}decode_hhash [хэш]</code></b>",
        "no_repo": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть <code>{}mods_repo [ссылка_на_репозиторий]</code></b>",

        "invalid_hh": "<b>😕 Неверный хэш</b>",
        "invalid_repo": "<b>😕 Неверный репозиторий модулей</b>",
        "no_modules_in_repo": "<b>😕 Нету модулей в репозитории</b>",

        "searching": "<emoji document_id=5307710821936145414>🔄</emoji> <b>Поиск модулей...</b>",
        "receiving_modules": "<emoji document_id=5325792861885570739>🔄</emoji> <b>Получаю модули...</b>",
        "decoding": "<emoji document_id=5307981757063110606>🔄</emoji> <b>Декодирую хэш...</b>",
    }

    app_name = "famods Hetalib"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "search_limit_result",
                5,
                lambda: "Максимум результатов поиска будет при поиске модулей.",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client

    @loader.command()
    async def hsearch(self, message):
        """Поиск модуля в heta"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"].format(self.get_prefix()))
        
        await utils.answer(message, self.strings['searching'])

        smods = heta.search(query=q, limit=self.config["search_limit_result"], app_name=self.app_name)
        
        mtext = f"""<b>⛩ Heta search ⛩

<emoji document_id=5188311512791393083>🔎</emoji> Запрос: </b><code>{q}</code>

"""

        for mod in smods:
            mtext += f"""<b>🖥 {mod['module']['name']} (<a href="{mod['module']['link']}">source</a>) by {mod['module']['dev']}
ℹ️ </b><i>{mod['module']['cls_doc']}</i><b>
<code>{self.get_prefix()}dlh {mod['module']['hash']}</code>
——
</b>"""
        
        await utils.answer(message, mtext)

    @loader.command()
    async def decode_hhash(self, message):
        """Декодировать heta hash"""

        hhash = utils.get_args_raw(message)
        if not hhash:
            return await utils.answer(message, self.strings["no_hh"].format(self.get_prefix()))
        
        await utils.answer(message, self.strings['decoding'])

        try:
           hh_info = heta.decode_hash(mhash=hhash, app_name=self.app_name)
        except requests.exceptions.JSONDecodeError:
            return await utils.answer(message, self.strings['invalid_hh'])
        
        await utils.answer(message, f"""<b>
🖥 {hh_info['name']} (<a href="{hh_info['link']}">source</a>)
<code>{self.get_prefix()}dlh {hhash}</code>
</b>""")
        
    @loader.command()
    async def mods_repo(self, message):
        """Получить модули с репозитория"""

        rep = utils.get_args_raw(message)
        if not rep:
            return await utils.answer(message, self.strings["no_repo"].format(self.get_prefix()))
        
        await utils.answer(message, self.strings['receiving_modules'])

        try:
            mods = heta.repo.get_modules(repo=rep)
        except requests.exceptions.MissingSchema:
            return await utils.answer(message, self.strings['invalid_repo'])
        if mods == "no modules":
            return await utils.answer(message, self.strings['no_modules_in_repo'])
        
        mdsrepo = f"""
<b>🖥 Модули из <a href="{rep}">этого</a> репозитория</b>

"""
        
        for mod in mods:
            mdsrepo += f"<i>{mod['name']}</i> (<i><a href='{mod['link']}'>ссылка</a></i>)\n"
        
        await utils.answer(message, mdsrepo)
