#meta developer: @thisLyomi & @amekamods

from .. import loader, utils

@loader.tds
class QuoteMsgMod(loader.Module):
    """Вместо репли вставляет цитату с содержимым из репли."""
    strings = {"name": "QuoteMsg"}

    async def qmsgcmd(self, message):
        """<text> - Отправить сообщение с цитированием содержимого из репли."""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>❌ Требуется репли.</b>")
            return

        text = utils.get_args_raw(message)
        if not text:
            await message.edit("<b>❌ Укажи аргумент.</b>")
            return

        username = reply.sender.first_name
        donemsg = f"<blockquote><b>{username}</b>\n {reply.text}</blockquote>\n\n{text}"
        await message.respond(donemsg, parse_mode="html")

        await message.delete()
