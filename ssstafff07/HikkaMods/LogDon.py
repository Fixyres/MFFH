#This mod will show your level of strength.
#Developer's telegram @ZZZOOOVVV2007
#⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿
#⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⣿
#⣿⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⠄⣿
#⣿⠄⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⠄⣿
#⣿⠄⠄⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿
#⣿⠄⠄⠄⠄⠄⣿⠄⠄⠄⠄⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿
#⣿⠄⠄⠄⠄⠄⠄⣿⣿⣿⠄⠄⣿⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
#⣿⠄⠄⠄⠄⠄⣿⠄⠄⠄⣿⣿⠄⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿
#⠄⣿⠄⠄⠄⣿⠄⠄⠄⣿⣿⠄⠄⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿
#⠄⠄⣿⠄⠄⣿⠄⠄⣿⠄⠄⠄⣿⠄⠄⠄⠄⠄⣿⠄⠄⠄⣿⣿⣿⣿⠄⣿
#⠄⠄⠄⣿⠄⣿⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⠄⣿
#⣿⣿⣿⠄⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⣿
#⣿⠄⠄⠄⣿⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⠄⠄⠄⠄⣿⠄⠄⣿
#⠄⣿⠄⠄⠄⣿⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿
#⠄⠄⣿⠄⠄⣿⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿
#⠄⠄⠄⣿⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿
#⠄⠄⠄⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⠄⠄⠄⣿
#⠄⠄⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⣿⠄⠄⠄⣿
#⠄⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⠄⠄⠄⠄⣿⣿⣿⣿
#⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿
#⠄⠄⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿
#⠄⠄⣿⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⣿
#⠄⠄⠄⣿⠄⠄⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⠄⠄⠄⠄⣿
#⠄⠄⣿⣿⣿⣿⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿

import datetime
import os
from hikkatl.tl.types import Message
from hikkatl.tl.functions.messages import GetHistoryRequest
from .. import loader, utils

def progress_bar(progress, total, length=20):
    filled_length = int(length * progress // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}] {progress}/{total}"

@loader.tds
class LogDonModule(loader.Module):
    strings = {
        "name": "LogDon",
        "saved": "☑️",
        "no_messages": "🚫 Нет сообщений для сохранения.",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(ru_doc="<число> - Сохранить указанное количество сообщений в файл")
    async def ldcmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args.isdigit():
            await utils.answer(message, "🚫 Укажите число сообщений для сохранения.")
            return

        limit = int(args)
        if limit <= 0:
            await utils.answer(message, "🚫 Число сообщений должно быть больше 0.")
            return

        chat = await message.get_chat()
        all_messages = []
        offset_id = 0
        total_count = 0

        while True:
            history = await self.client(GetHistoryRequest(
                peer=chat,
                limit=min(100, limit - total_count),
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                max_id=0,
                min_id=0,
                hash=0
            ))

            if not history.messages:
                break

            all_messages.extend(history.messages)
            total_count += len(history.messages)

            progress = progress_bar(total_count, limit)
            await utils.answer(message, f"Сбор сообщений...\n{progress}")

            if total_count >= limit:
                break

            offset_id = history.messages[-1].id

        if not all_messages:
            await utils.answer(message, self.strings("no_messages"))
            return

        log_content = ""
        for msg in reversed(all_messages):
            user_id = msg.sender_id
            date = msg.date.strftime("%d %b. %Y в %H:%M")
            text = msg.raw_text
            log_content += f"User id: tg://user?id={user_id}, [{date}]\n{text}\n\n"

        filename = f"logdon_{chat.id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(log_content)

        caption = (
            f"Дата и время: {datetime.datetime.now().strftime('%d %b. %Y в %H:%M')}\n"
            f"ID чата: {chat.id}"
        )

        await self.client.send_file("me", filename, caption=caption)
        await utils.answer(message, self.strings("saved"))

        os.remove(filename)
