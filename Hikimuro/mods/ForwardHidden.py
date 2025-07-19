# module ForwardHidden
# meta developer @Hikimuro

from .. import loader, utils
from telethon.tl.types import Message
import os
import asyncio

@loader.tds
class ForwardHiddenMod(loader.Module):
    """Копирует сообщения из других чатов/каналов, включая закрытые"""
    strings = {
        "name": "ForwardHidden",
        "send_failed": "⚠️ Не удалось отправить сообщение: {}",
        "done": "✅ Готово.",
        "no_msgs": "❌ Нет сообщений.",
        "sending": "📤 Отправка {} сообщений...",
        "getid_fail": "❌ Не удалось получить chat_id: {}",
        "usage": "<b>Использование:</b> <code>.fh 1655808918 20</code>\n❓ Чтобы узнать chat_id: используй .listch или .getid",
    }

    @loader.command()
    async def fh(self, message: Message):
        """<chat_id> <кол-во> — копировать сообщения в текущий чат (обход запрета пересылки)"""
        args = utils.get_args_raw(message)
        if not args or len(args.split()) < 2:
            return await utils.answer(message, self.strings("usage", message))

        chat_id_str, count_str = args.split()
        try:
            count = int(count_str)
        except ValueError:
            return await utils.answer(message, "⚠️ Укажи число сообщений.")

        try:
            chat_id = int(chat_id_str)
        except Exception:
            try:
                entity = await message.client.get_entity(chat_id_str)
                chat_id = entity.id
            except Exception as e:
                return await utils.answer(message, self.strings("getid_fail", message).format(e))

        msgs = []
        try:
            async for msg in message.client.iter_messages(chat_id, limit=count):
                if msg.text or msg.media:
                    msgs.append(msg)
        except Exception as e:
            return await utils.answer(message, f"❌ Ошибка при получении сообщений: {e}")

        if not msgs:
            return await utils.answer(message, self.strings("no_msgs", message))

        await utils.answer(message, self.strings("sending", message).format(len(msgs)))

        for msg in reversed(msgs):
            text = msg.text or ""
            sender = await msg.get_sender()
            author = f"\n\n👤 <b>От:</b> {getattr(sender, 'first_name', 'неизвестно')}"

            try:
                if msg.media:
                    file = await message.client.download_media(msg.media)
                    await message.client.send_file(
                        message.chat_id,
                        file,
                        caption=text + author if text else author,
                    )
                    # Удаляем временный файл, если существует
                    if file and os.path.exists(file):
                        try:
                            os.remove(file)
                        except Exception:
                            pass
                else:
                    await message.client.send_message(
                        message.chat_id,
                        text + author
                    )
            except Exception as e:
                await utils.answer(message, self.strings("send_failed", message).format(e))

        await utils.answer(message, self.strings("done", message))

    @loader.command()
    async def getid(self, message: Message):
        """[username или пусто] — получить chat_id канала, группы или чата"""
        args = utils.get_args_raw(message)
        try:
            if args:
                entity = await message.client.get_entity(args)
            else:
                entity = await message.client.get_entity(message.chat_id)
            await utils.answer(message, f"<b>{getattr(entity, 'title', 'Чат')}:</b>\n<code>{entity.id}</code>")
        except Exception as e:
            await utils.answer(message, f"❌ Не удалось получить chat_id: {e}")

    @loader.command()
    async def listch(self, message: Message):
        """— показать список всех каналов и супергрупп, включая закрытые"""
        result = "<b>📋 Список чатов:</b>\n\n"
        async for dialog in message.client.iter_dialogs():
            entity = dialog.entity
            if getattr(entity, "megagroup", False) or getattr(entity, "broadcast", False):
                name = utils.escape_html(getattr(entity, "title", "Без названия"))
                chat_id = entity.id
                result += f"<b>{name}</b>\n<code>{chat_id}</code>\n\n"

        if result.strip() == "<b>📋 Список чатов:</b>":
            result += "❌ Ничего не найдено."

        await utils.answer(message, result)
