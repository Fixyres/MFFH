# чатгпт кормит, больные мозги тоже
#
# meta banner: https://files.catbox.moe/swqxd1.png
# meta developer: @HikkaZPM
#
# The module is made as a joke, all coincidences are random :P
# 
#       кот вахуи
#       /\_____/\
#      /  o   o  \
#     ( ==  ^  == )
#      )         (
#     (           )
#    ( (  )   (  ) )
#   (__(__)___(__)__)
# 
#
from .. import loader, utils
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import logging

logger = logging.getLogger(__name__)

UD_API_KEY = "99729790b5mshd8ec94082f78c14p1dbb97jsn52ae508bea0d"

@loader.tds
class UrbanDictionaryMod(loader.Module):
    """Поиск сленговых значений в UrbanDictionary, пишите на английском для лучшего поиска (перевод в будующем)"""
    
    strings = {"name": "UrbanDictionary"}

    async def ud_search(self, term: str):
        """Запрос к Urban Dictionary API"""
        url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        headers = {
            "X-RapidAPI-Key": UD_API_KEY,
            "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com"
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params={"term": term}) as resp:
                    if resp.status != 200:
                        return {"error": f"API Error: {resp.status}"}
                    return (await resp.json()).get("list", [])[:3]
        except Exception as e:
            logger.error(f"Urban error: {e}")
            return {"error": str(e)}

    @loader.unrestricted
    async def udcmd(self, message: types.Message):
        """Поиск обозначения"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5237993272109967450>❌</emoji> Укажите слово для поиска!")
            return

        result = await self.ud_search(args)
        
        if isinstance(result, dict) and "error" in result:
            await utils.answer(message, f"<emoji document_id=5210952531676504517>❌</emoji> Ошибка: {result['error']}")
            return
        
        if not result:
            await utils.answer(message, f"<emoji document_id=5316509307255137126>🔍</emoji> Нет результатов для '{args}'")
            return

        response = f"<emoji document_id=5341355074587206546>📖</emoji> <b>{args}</b> в Urban Dictionary:\n\n"
        for idx, item in enumerate(result, 1):
            definition = item.get("definition", "No definition").replace("[", "").replace("]", "")
            example = item.get("example", "No example").replace("[", "").replace("]", "")
            
            response += (
                f"{idx}. <emoji document_id=5461010063135088912>👍</emoji> {item.get('thumbs_up', 0)} | "
                f"<emoji document_id=5463294908427148871>👎</emoji> {item.get('thumbs_down', 0)}\n"
                f"<i>{definition[:250]}</i>\n"
                f"<emoji document_id=5443038326535759644>💬</emoji> Пример: <i>{example[:200]}</i>\n\n"
            )
            
        msg = await utils.answer(message, response)
        
""" патом как нибудб 😊
    
        # Создаем кнопки перевода
        keyboard = InlineKeyboardMarkup().row(
            InlineKeyboardButton("🇷🇺 Русский", callback_data=f"tr_ru_{msg.id}"),
            InlineKeyboardButton("🇬🇧 Английский", callback_data=f"tr_en_{msg.id}")
        )
        
        # Добавляем кнопки к сообщению
        await msg.edit_reply_markup(keyboard)

    @loader.callback_handler(lambda call: call.data.startswith("tr_"))
    async def translate_handler(self, call: types.CallbackQuery):
        ###Обработчик кнопок перевода###
        lang, msg_id = call.data.split("_")[1], call.data.split("_")[2]
        msg = await self.client.get_messages(call.message.chat.id, ids=int(msg_id))
        
        try:
            translated = await self.client.translate_message(
                chat_id=msg.chat.id,
                message_id=msg.id,
                to_lang=lang
            )
            await msg.edit(
                text=f"<emoji document_id=5447410659077661506>🌐</emoji> {translated.text}",
                reply_markup=msg.reply_markup
            )
        except Exception as e:
            logger.error(f"Translate error: {e}")
            await call.answer("<emoji document_id=5420323339723881652>⚠️</emoji> Ошибка перевода!", show_alert=True)
        
        await call.answer()

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
"""        