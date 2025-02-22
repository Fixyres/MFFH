# meta developer: @RemoveWoman

from .. import loader, utils
from telethon import events
from telethon.tl.types import UpdateUserTyping, UpdateChatUserTyping
import asyncio

class SosaloinatorMod(loader.Module):
    """Давно мечтали забайтить дурга на сосал? ЭТОТ МОДУЛЬ ДЛЯ ТАКИХ ЖЕ ИДИОТОВ КАК Я КОТОРЫЕ ЛЮБЯТ БАЙТИТЬ КАЖДОГО ВТОРОГО. В конфиге можно указывать значение что надо написать моментально как человек начнет печатать. (кд 3 минуты на ответ человека)"""

    strings = {"name": "Sosaloinator",
               "no_reply": "<b>❌ Ответьте на сообщение пользователя, чтобы использовать эту команду в группе.</b>",
               "watching": "<b>🔍 Отслеживаю статус 'печатает'...</b>",
               "not_typing": "Уже не надо, спасибо"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "text", "Сосал?",
            "Ответ, отправляемый при статусе 'печатает'."
        )
        self.tasks = {}

    async def voprcmd(self, message):
        """[текст] Вводя это вы соглашаетесь что вас будут ненавидеть все. (если что эта штука в группах используется реплаем на забайченого человека)"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chat = message.chat_id

        if message.is_private:
            target_id = message.to_id.user_id
        else:
            if not reply:
                await utils.answer(message, self.strings["no_reply"])
                return
            target_id = reply.sender_id

        task_key = (chat, target_id)
        if task_key in self.tasks:
            self.tasks[task_key].cancel()

        if args:
            await message.edit(args)
        else:
            await message.delete()

        self.tasks[task_key] = asyncio.create_task(self.watch_typing(chat, target_id, message.client))

    async def watch_typing(self, chat_id, user_id, client):
        try:
            typing_detected = asyncio.Event()

            @client.on(events.Raw)
            async def handler(event):
                if isinstance(event, UpdateUserTyping):
                    if event.user_id == user_id and chat_id == user_id:
                        typing_detected.set()

                if isinstance(event, UpdateChatUserTyping):
                    if event.user_id == user_id and event.chat_id == chat_id:
                        typing_detected.set()

            client.add_event_handler(handler)

            for _ in range(900):
                if typing_detected.is_set():
                    await client.send_message(chat_id, self.config["text"])
                    break
                await asyncio.sleep(0.2)

            else:
                await client.send_message(chat_id, self.strings["not_typing"])

            client.remove_event_handler(handler)

        except asyncio.CancelledError:
            pass
