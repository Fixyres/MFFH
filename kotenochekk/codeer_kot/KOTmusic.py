# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель этого модуля.
from .. import loader, utils

class KOTmusicModule(loader.Module):
    """Модуль для поиска музыки."""
    
    strings = {'name': 'KOTmusic'}
    
    @loader.command()
    async def трекcmd(self, message):
        """Ищет песни по названию."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args:
            return await message.edit("<b>Не указано название трека.</b>")

        try:
            await message.edit(f"<blockquote><b>Ищем трек: {args}...</b><emoji document_id=5319272710688226013>⏰</emoji></blockquote>")
            music = await message.client.inline_query("LyBot", args)
            await message.delete()

            await message.client.send_file(
                message.to_id,
                music[0].result.document,
                reply_to=reply.id if reply else None,
            )
        except Exception as e:
            return await message.client.send_message(
                message.chat_id,
                f"<blockquote>Музыка с названием <code>{args}</code> не найдена.</blockquote>"
          )
