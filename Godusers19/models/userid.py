# meta developer: @goduser18
from hikka import loader, utils  
from aiogram.types import Message  

@loader.tds  
class GetIDs(loader.Module):  
    """Получение UserID и ChatID"""  

    strings = {  
        "name": "GetIDs",  
        "userid": "🆔 <b>UserID:</b> <code>{}</code>",  
        "chatid": "💬 <b>ChatID:</b> <code>{}</code>",  
        "no_reply": "❌ <b>Ответь на сообщение или укажи @username!</b>",  
    }  

    async def client_ready(self, client, db):  
        self._client = client  

    @loader.command(alias="uid")  
    async def useridcmd(self, message: Message):  
        """Получить UserID (ответ на сообщение или @username)"""  
        args = utils.get_args_raw(message)  
        reply = await message.get_reply_message()  

        if reply:  
            user = reply.sender_id  
        elif args and args.startswith("@"):  
            try:  
                user = (await self._client.get_entity(args)).id  
            except:  
                await utils.answer(message, self.strings["no_reply"])  
                return  
        else:  
            await utils.answer(message, self.strings["no_reply"])  
            return  

        await utils.answer(message, self.strings["userid"].format(user))  

    @loader.command(alias="cid")  
    async def chatidcmd(self, message: Message):  
        """Получить ChatID"""  
        chat_id = message.chat_id  
        await utils.answer(message, self.strings["chatid"].format(chat_id))  