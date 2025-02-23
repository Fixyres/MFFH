__version__ = (1, 0, 1)
# meta developer: @psyho_Kuznetsov

import logging
from datetime import datetime
from telethon.tl.types import Message
from .. import loader, utils

@loader.tds
class DeleteChatMessagesModule(loader.Module):
    """Модуль для массового удаления сообщений в чате"""

    strings = {  
        "name": "DeleteMessages",  
        "description": "Модуль для удаления всех ваших сообщений в указанном чате.",  
        "deleting": "<b>🗑 Удаление сообщений...</b>",  
        "deleted": "<b>✅ Удаление завершено!</b>",  
        "error": "<b>❌ Ошибка при удалении:</b> {}"  
    }  

    async def client_ready(self, client, db):  
        self._client = client  
        self._db = db  
        self._me = await client.get_me()  

    async def delchatmecmd(self, message: Message):  
        """Удалить все ваши сообщения в чате.  
        Использование: <code>.delchatme [ID чата]</code>  
        Если ID чата не указан, удаление происходит в текущем чате."""  
          
        args = utils.get_args_raw(message)  
        if not args:  
            chat_id = message.chat_id  
        else:  
            try:  
                chat_id = int(args)  
            except ValueError:  
                await message.edit("<b>❌ Неверный формат ID чата!</b>")  
                return  

        try:  
            status_msg = await message.edit(self.strings["deleting"])  
              
            async for msg in self._client.iter_messages(  
                chat_id,  
                from_user=self._me.id,  
                reverse=True  
            ):  
                try:  
                    await msg.delete()  
                except Exception as e:  
                    logging.error(f"Ошибка при удалении сообщения {msg.id}: {str(e)}")  
                    continue  

            await status_msg.edit(self.strings["deleted"])  
            await status_msg.delete()  

        except Exception as e:  
            error_text = self.strings["error"].format(str(e))  
            await message.edit(error_text)  
            logging.exception(error_text)
