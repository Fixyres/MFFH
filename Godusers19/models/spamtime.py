# meta developer: @goduser18
from asyncio import sleep
import re
from .. import loader, utils
import time

@loader.tds
class Spamtime(loader.Module):
    strings = {"name": "spamtime"}

    def __init__(self):
        self.spam_tasks = {}

    def parse_time(self, time_str):
        match = re.match(r"(\d+)([smh])", time_str)
        if not match:
            return None
        value, unit = int(match.group(1)), match.group(2)
        if unit == "s":
            return value
        elif unit == "m":
            return value * 60
        elif unit == "h":
            return value * 60 * 60
        return None

    async def send_or_edit(self, message, text):
        owner = await self._client.get_me()
        owner_ids = owner.id
        if message.sender_id == owner_ids:
            await message.edit(text)
        else:
            await message.respond(text)

    @loader.command()
    async def startcmd(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if reply and not args:
            if not reply.text and not reply.media:
                await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Ответьте на текстовое сообщение или сообщение с фото.</b>")
                return
            args = "1m 1"

        if not args or len(args.split()) < 2:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Неверный формат надо  .start <время> <количество> [сообщение]</b>")
            return

        time_str, count_str, *content = args.split(maxsplit=2)
        interval = self.parse_time(time_str)
        if interval is None:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Неверный формат времени.</b>")
            return

        try:
            count = int(count_str)
            if count <= 0:
                raise ValueError
        except ValueError:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Неверное количество</b>")
            return

        message_content = ' '.join(content) if content else None
        if reply and not message_content:
            message_content = reply.text

        media_list = []
        if reply:
            if reply.grouped_id:
                async for msg in self.client.iter_messages(reply.chat_id, reverse=True, offset_id=reply.id - 1, limit=10):
                    if msg.grouped_id == reply.grouped_id and msg.media:
                        media_list.append(msg.media)
            elif reply.media:
                media_list.append(reply.media)

        spam_id = int(time.time())
        self.spam_tasks[spam_id] = {
            "running": True,
            "interval": interval,
            "message_content": message_content,
            "media": media_list,
            "count": count,
            "chat_id": message.chat_id
        }

        await self.send_or_edit(message, f"<emoji document_id=5256182535917940722>⤵️</emoji> <b>Рассылка #{spam_id} запущена.</b>")
        await self.run_spam_task(spam_id, message)

    async def run_spam_task(self, spam_id, message):
        task_data = self.spam_tasks[spam_id]
        try:
            while task_data["running"] and task_data["count"] > 0:
                await sleep(task_data["interval"])
                if not task_data["running"]:
                    break
                try:
                    if task_data["media"]:
                        await self.client.send_file(
                            task_data["chat_id"],
                            file=task_data["media"],
                            caption=task_data["message_content"]
                        )
                    else:
                        await self.client.send_message(
                            task_data["chat_id"],
                            task_data["message_content"]
                        )
                    task_data["count"] -= 1
                except Exception as e:
                    await self.send_or_edit(message, f"<emoji document_id=5440660757194744323>‼️</emoji> Ошибка при отправке: {e}")
                    task_data["running"] = False
                    break

            if spam_id in self.spam_tasks:
                del self.spam_tasks[spam_id]
                await self.send_or_edit(message, f"<emoji document_id=5319090522470495400>⭕️</emoji> <b>Рассылка #{spam_id} завершена.</b>")

        except Exception as e:
            await self.send_or_edit(message, f"<emoji document_id=5440660757194744323>‼️</emoji> Ошибка: {e}")
            task_data["running"] = False

    @loader.command()
    async def stopcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Укажите ID рассылки.</b>")
            return

        try:
            spam_id = int(args)
            if spam_id not in self.spam_tasks:
                await self.send_or_edit(message, f"<emoji document_id=5877477244938489129>🚫</emoji><b> Рассылка #{spam_id} не найдена.</b>")
                return

            self.spam_tasks[spam_id]["running"] = False
            await self.send_or_edit(message, f"<emoji document_id=5319090522470495400>⭕️</emoji> <b>Рассылка #{spam_id} остановлена.</b>")
        except ValueError:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Неверный формат ID.</b>")

    @loader.command()
    async def listcmd(self, message):
        if not self.spam_tasks:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Нет активных рассылок.</b>")
            return

        active_spams = []
        for spam_id, task_data in self.spam_tasks.items():
            if task_data["running"]:
                active_spams.append(
                    f"<b>Рассылка #{spam_id}</b>\n"
                    f"Сообщение: {task_data['message_content']}\n"
                    f"Медиа: {'Да' if task_data['media'] else 'Нет'}\n"
                    f"Интервал: {task_data['interval']} сек\n"
                    f"Осталось отправок: {task_data['count']}"
                )

        if active_spams:
            await self.send_or_edit(message, "<emoji document_id=5256182535917940722>⤵️</emoji> <b>Активные рассылки:</b>\n\n" + "\n\n".join(active_spams))
        else:
            await self.send_or_edit(message, "<emoji document_id=5877477244938489129>🚫</emoji><b> Нет активных рассылок.</b>")



#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан

#я еблан
#я еблан


