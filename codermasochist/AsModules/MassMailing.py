"""
 __  __                               _ _ _             
|  \/  | __ _ ___ ___ _ __ ___   __ _(_) (_)_ __   __ _ 
| |\/| |/ _` / __/ __| '_ ` _ \ / _` | | | | '_ \ / _` |
| |  | | (_| \__ \__ \ | | | | | (_| | | | | | | | (_| |
|_|  |_|\__,_|___/___/_| |_| |_|\__,_|_|_|_|_| |_|\__, |
                                                  |___/
"""

# meta developer: @codermasochist

from .. import loader, utils
from asyncio import sleep
from telethon.tl.types import Message

@loader.tds
class MassMailing(loader.Module):
    """массовая рассылка по всем чатам."""

    strings = {
        "name": "Mass Mailing",
        "what": "<blockquote><emoji document_id=5276477287183687194>👎</emoji> <b>ебень. вот так надо: </b><code>.rsl текст | 2 | 3</code> (задержка / повторы)</blockquote>",
        "start": "<blockquote><emoji document_id=5258332798409783582>🚀</emoji> <b>начинаю рассылку...</b></blockquote>\n<blockquote><emoji document_id=5839380464116175529>✏️</emoji> <b>задержка</b>: <code>{delay}</code> сек | <b>повторы</b>: <code>{repeat}</code></blockquote>",
        "stop": "<blockquote><emoji document_id=5253868738251335638>🤚</emoji> <b>рассылка остановлена.</b></blockquote>\n<blockquote><emoji document_id=5843908536467198016>✅️</emoji> <b>успешно отправлено</b> в {success} чатов</blockquote>\n<blockquote><emoji document_id=5271533904380046720>🙅‍♂️</emoji> <b>не удалось отправить в </b><code>{failed}</code> <b>чатов.</b></blockquote>",
        "trying_stop": "<blockquote><emoji document_id=5355133243773435190>⚠️</emoji><b> попытка остановить рассылку...</b></blockquote>",
    }

    def __init__(self):
        self._stop_rsl = False

    async def rslcmd(self, message: Message):
        """— текст | задержка | повторы (или ответом на сообщение, включая медиа)"""
        penis = utils.get_args_raw(message)
        parts = penis.split("|")
        reply = await message.get_reply_message()

        media = None
        text = ""
        delay = 0
        repeat = 0

        if reply and len(parts) == 2:
            text = reply.raw_text or reply.message or ""
            media = reply.media
            try:
                delay = int(parts[0].strip())
                repeat = int(parts[1].strip())
            except Exception:
                await utils.answer(message, self.strings["what"])
                return
        elif reply and len(parts) == 0:
            text = reply.raw_text or reply.message or ""
            media = reply.media
            delay = 2
            repeat = 1
        elif len(parts) == 3:
            try:
                text = parts[0].strip()
                delay = int(parts[1].strip())
                repeat = int(parts[2].strip())
            except Exception:
                await utils.answer(message, self.strings["what"])
                return
        else:
            await utils.answer(message, self.strings["what"])
            return

        self._stop_rsl = False
        await utils.answer(message, self.strings["start"].format(delay=delay, repeat=repeat))

        me = await message.client.get_me()
        dialogs = [
            dialog for dialog in await message.client.get_dialogs()
            if not (dialog.is_user and dialog.id == me.id)
        ]

        success = 0
        failed = 0

        for _ in range(repeat):
            if self._stop_rsl:
                await utils.answer(message, self.strings["stop"].format(success=success, failed=failed))
                return

            for dialog in dialogs:
                if self._stop_rsl:
                    await utils.answer(message, self.strings["stop"].format(success=success, failed=failed))
                    return

                try:
                    await message.client.send_file(dialog.id, media, caption=text) if media else await message.client.send_message(dialog.id, text)
                    success += 1
                    await sleep(3)
                except Exception:
                    failed += 1

            await sleep(delay)

        await utils.answer(message, self.strings["stop"].format(success=success, failed=failed))

    async def stoprslcmd(self, message: Message):
        """— стоп рассылки."""
        self._stop_rsl = True
        await self.client.send_message(message.chat_id, self.strings["trying_stop"])
