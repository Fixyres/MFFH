# meta developer: @codermasochist

from .. import loader, utils
import asyncio

@loader.tds
class Asdlbot(loader.Module):
    """качает видео с тт/инст & ютуб/пин через ботов"""
    strings = {"name": "Asdlbot"}

    async def is_conversation_active(self, bot):
        conversations = await self.client.get_dialogs()
        for dialog in conversations:
            if dialog.name == bot:
                return True
        return False

    async def vdlcmd(self, message):
        """<ссылка> — скачать видео с тт/инст"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5253577054137362120>🔗</emoji><b> indicate the link, dumbass.</b>.")
            return
        
        ttsave_bot = "@ttsavebot"
        chat_id = message.chat_id

        if await self.is_conversation_active(ttsave_bot):
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> <b>another conversation is already active with this bot.</b>")
            return

        async with self.client.conversation(ttsave_bot) as conv:
            try:
                await conv.send_message(args)
                response = await conv.get_response()
                
                while not response.media:
                    await asyncio.sleep(5)
                    response = await conv.get_response()
                
                await self.client.send_file(
                    chat_id, 
                    response.media, 
                    caption="<emoji document_id=5224607267797606837>☄️</emoji> <b>successfully downloaded.</b>"
                )
                await message.delete()
            except Exception as e:
                await utils.answer(message, f"<emoji document_id=5210952531676504517>❌</emoji> <b>error while downloading.</b>\n{str(e)}")

    async def ypdlcmd(self, message):
        """<ссылка> — скачать видео с ютуб/пинтерест"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5253577054137362120>🔗</emoji><b> indicate the link, dumbass.</b>.")
            return
        
        primesaver_bot = "@PrimeSaverBot"
        chat_id = message.chat_id

        if await self.is_conversation_active(primesaver_bot):
            await utils.answer(message, "<emoji document_id=5210952531676504517>❌</emoji> <b>another conversation is already active with this bot.</b>")
            return

        async with self.client.conversation(primesaver_bot) as conv:
            try:
                await conv.send_message(args)
                response = await conv.get_response()
                
                while not response.media:
                    await asyncio.sleep(5)
                    response = await conv.get_response()
                
                await self.client.send_file(
                    chat_id, 
                    response.media, 
                    caption="<emoji document_id=5224607267797606837>☄️</emoji> <b>successfully downloaded.</b>"
                )
                await message.delete()
            except Exception as e:
                await utils.answer(message, f"<emoji document_id=5210952531676504517>❌</emoji> <b>error while downloading.</b>\n{str(e)}")
