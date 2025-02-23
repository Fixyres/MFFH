# @Sekai_Yoneya

from .. import loader, utils 
 
@loader.tds 
class SearchMusicMod(loader.Module): 
    """ 
    Модуль SearchMusic - поиск музыки 
    Работает через бота @lybot 
    """ 
    strings = {"name": "SearchMusic"} 
 
    async def smcmd(self, message): 
        """Используй: .sm «название» чтобы найти музыку по названию.""" 
        args = utils.get_args_raw(message) 
        reply = await message.get_reply_message() 
        if not args: 
            return await message.edit("<b>Нету аргументов.</b>")  
        try: 
            await message.edit("<b>Загрузка...</b>") 
            music = await message.client.inline_query('lybot', args) 
            await message.delete() 
            await message.client.send_file(message.to_id, music[0].result.document, reply_to=reply.id if reply else None) 
        except: return await message.client.send_message(message.chat_id, f"<b>Музыка с названием <code>{args}</code> не найдена.</b>")
