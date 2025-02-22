#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: PhoneInfo
# Description: Информация о телефоне
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/phoneinfo.png?raw=true
# ---------------------------------------------------------------------------------

import time
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class PhoneInfo(loader.Module):
    """Информация о телефоне"""

    strings = {
        "name": "PhoneInfo",

        "no_phone": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно <code>{}{} [название телефона]</code></b>",

        "searching": "<emoji document_id=5334904192622403796>🔄</emoji> <b>Поиск телефона...</b>",
        "searching_info": "<emoji document_id=5334904192622403796>🔄</emoji> <b>Поиск информации о телефоне...</b>",

        "no_found": "<emoji document_id=5440381017384822513>❌</emoji> <b>Не нашёл такой телефон</b>",

        "cameras_txt": "<emoji document_id=5787632606484893320>📷</emoji> Cameras:",
        "software_txt": "<emoji document_id=6334742097748298141>🖥</emoji> Software:",
        "hardware_txt": "<emoji document_id=6334778871258286021>💾</emoji> Hardware:",
    }

    cameras_t = "Cameras:"
    software_t = "Software:"
    hardware_t = "Hardware:"

    opt_bt = "\nspecs prepared with ❤️ by @gsmarbot"

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "search_limit",
                5,
                lambda: "Лимит результатов в поиске",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        
    async def _get_phone_info(self, query):
        try:
            q = await self._client.inline_query("@gsmarbot", query)
            result = q.result.results[1]
            
            message = result.send_message.message
            message = message.replace(self.opt_bt, "")
            message = message.replace(self.cameras_t, self.strings['cameras_txt'])
            message = message.replace(self.software_t, self.strings['software_txt'])
            message = message.replace(self.hardware_t, self.strings['hardware_txt'])
            
            url = result.send_message.reply_markup.rows[0].buttons[0].url

            return {'info': message, 'link': url}
        except (IndexError, AttributeError):
            return {'info': "no found"}
        
    async def _get_phones(self, query):
        try:
            q = await self._client.inline_query("@gsmarbot", query)
            q.result.results[1]

            results = q.result.results

            limit = self.config["search_limit"]

            c_res = 0

            resultss = []

            for result in results:

                if c_res == limit:
                    break
                
                resultss.append({"name": result.send_message.message.split('\n')[0], "link": result.send_message.reply_markup.rows[0].buttons[0].url})

                c_res += 1

            return {'result': resultss, 'count_result_res': c_res}
        except (IndexError, AttributeError):
            return {"result": "no found"}
        
    @loader.command()
    async def pnsearch(self, message):
        """Поиск телефона"""
        
        query = utils.get_args_raw(message)

        if not query:
            return await utils.answer(message, self.strings['no_phone'].format(self.get_prefix(), 'pnsearch'))

        await utils.answer(message, self.strings['searching'])

        start_time = time.time()

        phones = await self._get_phones(query)
        
        if phones['result'] == "no found":
            return await utils.answer(message, self.strings['no_found'])
        
        txt = f"""<b>
<emoji document_id=5407025283456835913>📱</emoji> Результаты поиска

<emoji document_id=5188311512791393083>🔎</emoji> Запрос: <code>{query}</code>

</b>"""
        
        for phone in phones['result']:
            txt += f"<b>📱 {phone['name']}\n🔗 {phone['link']}</b>\n\n"
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        txt += f"<i>{phones['count_result_res']} результатов за {execution_time} сек</i>"
    
        return await utils.answer(message, txt)

    @loader.command()
    async def pninfo(self, message):
        """Получить информацию о телефоне"""
        
        query = utils.get_args_raw(message)

        if not query:
            return await utils.answer(message, self.strings['no_phone'].format(self.get_prefix(), 'pninfo'))

        await utils.answer(message, self.strings['searching_info'])

        info = await self._get_phone_info(query)
        
        if info['info'] == "no found":
            return await utils.answer(message, self.strings['no_found'])
        
        txt = f"""<b>
<emoji document_id=5407025283456835913>📱</emoji> Информация о телефоне

<emoji document_id=5188311512791393083>🔎</emoji> Запрос: <code>{query}</code>

<emoji document_id=5406809207947142040>📲</emoji> {info['info']}
</b>"""
        
        keyboard = [
            [
                {
                    "text": "Полная информация о телефоне",
                    "url": info['link'],
                }
            ],
        ]
        
       # try:
        await self.inline.form(
                text=txt,
                message=message,
                reply_markup=keyboard,
                force_me=True,
            )
   #     except Exception as e:
   #         txt += f"<b><a href='{link}'><emoji document_id=6334638004920911460>ℹ️</emoji> Полная информация о телефоне</a></b>"
   #         return await utils.answer(message, txt)
