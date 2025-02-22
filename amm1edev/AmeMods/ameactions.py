#meta developer: @thisLyomi & @AmekaMods

from hikkatl.types import Message
from .. import utils, loader


@loader.tds
class AmeActions(loader.Module):
    """AmeActions"""
    strings = {"name": "AmeActions — Действия"}
    
    @loader.command()
    async def kiss(self, message: Message):
        """- kiss [reply] Целовать человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ |<b> Самолюбие конечно хорошо, но держи его при себе.</b>")
            else:
                await utils.answer(message, f"<emoji document_id=5222102889547185747>💋</emoji> | <b> <a href='tg://user?id={sid}'>{susr}</a> поцеловал(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def hug(self, message: Message):
        """- hug [reply] Обнимать человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ | <b>Кто тебе запрещает обняться с самим собой в реальной жизни? </b>")
            else:
                await utils.answer(message, f"<emoji document_id=5222325171284622461>💘</emoji> |  <b><a href='tg://user?id={sid}'>{susr}</a> обнял(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def push(self, message: Message):
        """- push [reply] Толкать человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ | <b>Покажи всем как ты толкаешь самого себя.</b>")
            else:
                await utils.answer(message, f"<emoji document_id=5449552292980214333>🙌</emoji> | <b> <a href='tg://user?id={sid}'>{susr}</a> толкнул(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def hit(self, message: Message):
        """- hit [reply] Ударить человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ | <b>Мазохизм не приветствуется.</b>")
            else:
                await utils.answer(message, f"<emoji document_id=5404854933402965409>💔</emoji> | <b> <a href='tg://user?id={sid}'>{susr}</a> ударил(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def scold(self, message: Message):
        """- scold [reply] Ругать человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ | <b>Я посмотрю как ты наругаешь самого себя. </b>")
            else:
                await utils.answer(message, f"<emoji document_id=5222102889547185747>💋</emoji> | <b> <a href='tg://user?id={sid}'>{susr}</a> наругал(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def kill(self, message: Message):
        """- kill [reply] Убить человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ | <b>Суицид? </b>")
            else:
                await utils.answer(message, f"<emoji document_id=5449603119623193071>⚰️</emoji> | <b> <a href='tg://user?id={sid}'>{susr}</a> убил(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def bite(self, message: Message):
        """- bite [reply] Кусать человека из репли"""
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,"❌ | <b>Это какой-то фетиш? </b>")
            else:
                await utils.answer(message, f"👄 | <b> <a href='tg://user?id={sid}'>{susr}</a> укусил(а) <a href='tg://user?id={uid}'>{usr}</a></b>")
                
    @loader.command()
    async def caction(self, message: Message):
        """- caction (args) [reply] Кастомное действие"""
        args = utils.get_args_raw(message)
        me = await self._client.get_me()
        reply = await message.get_reply_message()
        susr = me.first_name
        sid = me.id
        if reply == None:
            await utils.answer(message,"❌ | <b>Команда работает в ответ на сообщение пользователя.</b>")
        elif reply != None:
            usr = reply.sender.first_name
            uid = reply.sender.id
            if sid == uid:
                await utils.answer(message,f"❌ | <b>Увы, но на себе эту команду применить нельзя.</b>")
            else:
                await utils.answer(message, f"👤 | <b> <a href='tg://user?id={sid}'>{susr}</a> {args} <a href='tg://user?id={uid}'>{usr}</a></b>")
