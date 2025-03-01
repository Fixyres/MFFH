__version__ = (1, 0, 0)

#            © Copyright 2025
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: MSG

import os
import json
from datetime import datetime, timedelta
from .. import loader, utils
from telethon.tl.types import Message, DocumentAttributeVideo, DocumentAttributeAudio
import logging

@loader.tds
class MSG(loader.Module):
    """Модуль для создания заготовленных сообщений"""

    strings = {
        "name": "MSG",
        "msg_not_found": "❌ <b>Сообщение с таким названием не найдено.</b>",
        "msg_saved": "✅ <b>Сообщение сохранено под названием:</b> <code>{title}</code>",
        "msg_deleted": "🗑️ <b>Сообщение удалено:</b> <code>{title}</code>",
        "all_deleted": "🗑️ <b>Все сообщения удалены.</b> ({count})",
        "list_empty": "📭 <b>Список сообщений пуст.</b>",
        "overwrite_confirm": "❓ <b>Вы уверены, что хотите перезаписать существующее сохранение</b> ({date}, {size})?",
        "help": (
            "<b>.msg <название></b> - выводит заготовленное сообщение в чат\n"
            "<b>.msi</b> - выводит список сохранённых сообщений\n"
            "<b>.mss <название> (ответ на сообщение или текст)</b> - сохраняет сообщение\n"
            "<b>.msd <название></b> - удаляет сохранённое сообщение\n"
            "<b>.msh</b> - выводит справку по модулю\n\n"
            "<b>Пример использования:</b>\n"
            "<code>.mss привет</code> - сохраняет сообщение\n"
            "<code>.msg привет</code> - выводит сообщение"
        ),
    }

    def __init__(self):
        self.storage_path = "./saved_messages"
        self.data_file = os.path.join(self.storage_path, "messages.json")
        self.messages = self._load_messages()

    def _load_messages(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logging.error("Ошибка чтения файла JSON. Создаю новый файл.")
        return {}

    def _save_messages(self):
        os.makedirs(self.storage_path, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)

    def format_message(self, template):
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        return template.format(time=current_time, date=current_date)

    def _get_time_ago(self, past_time):
        now = datetime.now()
        diff = now - past_time

        if diff < timedelta(minutes=1):
            return f"{diff.seconds} секунд назад" if diff.seconds != 1 else "1 секунда назад"
        elif diff < timedelta(hours=1):
            minutes = diff.seconds // 60
            return f"{minutes} минут назад" if minutes != 1 else "1 минута назад"
        elif diff < timedelta(days=1):
            hours = diff.seconds // 3600
            return f"{hours} часов назад" if hours != 1 else "1 час назад"
        elif diff < timedelta(days=7):
            days = diff.days
            return f"{days} дней назад" if days != 1 else "1 день назад"
        elif diff < timedelta(days=30):
            weeks = diff.days // 7
            return f"{weeks} недель назад" if weeks != 1 else "1 неделя назад"
        elif diff < timedelta(days=365):
            months = diff.days // 30
            if months == 6:
                return "полгода назад"
            return f"{months} месяцев назад" if months != 1 else "1 месяц назад"
        else:
            years = diff.days // 365
            return f"{years} лет назад" if years != 1 else "1 год назад"

    def _get_message_count_declension(self, count):
        if count % 10 == 1 and count % 100 != 11:
            return "сообщение"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            return "сообщения"
        else:
            return "сообщений"

    def _get_size_format(self, size):
        if size < 1024:
            return f"{size} байт"
        elif size < 1024 ** 2:
            return f"{size / 1024:.2f} КБ"
        else:
            return f"{size / 1024 ** 2:.2f} МБ"

    @loader.command(
        ru_doc=" - выводит заготовленное сообщение в чат"
    )
    async def msg(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["msg_not_found"])
            return

        stored_message = self.messages.get(args)
        if not stored_message:
            await utils.answer(message, self.strings["msg_not_found"])
            return

        formatted_message = self.format_message(stored_message.get('text', ''))

        media_path = stored_message.get('media')
        progress_message = None

        if media_path and os.path.exists(media_path):
            if os.path.getsize(media_path) > 3 * 1024 * 1024:
                progress_message = await utils.answer(message, "⏳ <b>Начинаю отправку медиа...</b>")

            try:
                await self.client.send_file(
                    message.to_id,
                    media_path,
                    caption=formatted_message,
                    force_document=False
                )
                if progress_message:
                    await utils.answer(progress_message, "🔄 <b>Почти готово...</b>")
            except Exception as e:
                logging.error(f"Ошибка при отправке медиа: {e}")
                await utils.answer(message, formatted_message)
        else:
            await utils.answer(message, formatted_message)

    @loader.command(
        ru_doc=" - выводит список сохранённых сообщений"
    )
    async def msi(self, message: Message):
        if not self.messages:
            await utils.answer(message, self.strings["list_empty"])
            return

        lines = []
        for title, data in self.messages.items():
            text = data.get('text', '')
            saved_time = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S")
            time_ago = self._get_time_ago(saved_time)
            size = self._get_size_format(data.get('size', len(text.encode('utf-8'))))

            media_emoji = "📝"
            if data.get('media'):
                if data.get('is_audio', False):
                    media_emoji = "🎤"
                else:
                    media_emoji = "🖼️"

            lines.append(f"{media_emoji} <b>{title}:</b> {size}, {time_ago}")

        buttons = [
            [
                {
                    "text": "🗑️ Удалить все",
                    "callback": self.confirm_delete_all,
                }
            ]
        ]

        await self.inline.form(
            text="\n".join(lines),
            message=message,
            reply_markup=buttons
        )

    async def confirm_delete_all(self, call):
        count = len(self.messages)
        declension = self._get_message_count_declension(count)
        response = (
            f"❓ <b>Вы точно хотите удалить {count} {declension}?</b>\n"
        )

        buttons = [
            [
                {
                    "text": "✅ Да",
                    "callback": self.delete_all_messages,
                },
                {
                    "text": "🚫 Нет",
                    "callback": self.close_message,
                }
            ]
        ]

        await call.edit(
            text=response,
            reply_markup=buttons
        )

    async def delete_all_messages(self, call):
        count = len(self.messages)
        for title, data in self.messages.items():
            media_path = data.get('media')
            if media_path and os.path.exists(media_path):
                os.remove(media_path)
        self.messages.clear()
        self._save_messages()

        declension = self._get_message_count_declension(count)
        response = f"🗑️ <b>Все {count} {declension} были удалены.</b>"
        await call.edit(text=response)

    async def close_message(self, call):
        await call.delete()

    @loader.command(
        ru_doc=" - сохраняет сообщение для вывода"
    )
    async def mss(self, message: Message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            await utils.answer(message, self.strings["msg_not_found"])
            return

        title, *text = args.split(maxsplit=1)
        text = text[0] if text else (reply.text if reply else "")

        if title in self.messages:
            stored_message = self.messages[title]
            date_saved = stored_message['date']
            size_saved = self._get_size_format(stored_message.get('size', len(stored_message['text'].encode('utf-8'))))
            response = self.strings["overwrite_confirm"].format(date=date_saved, size=size_saved)

            buttons = [
                [
                    {
                        "text": "✅ Да",
                        "callback": self.overwrite_message,
                        "args": (title, text, reply),
                    },
                    {
                        "text": "🚫 Нет",
                        "callback": self.close_message,
                    }
                ]
            ]

            await self.inline.form(
                text=response,
                message=message,
                reply_markup=buttons
            )
        else:
            await self.save_message(message, title, text, reply)

    async def overwrite_message(self, call, title, text, reply):
        await self.save_message(call, title, text, reply)

    async def save_message(self, message, title, text, reply):
        media_path = None
        progress_message = None
        is_audio = False

        if reply and reply.media:
            if reply.file.size > 3 * 1024 * 1024:
                progress_message = await utils.answer(message, "⏳ <b>Начинаю сохранение медиа...</b>")

            os.makedirs(self.storage_path, exist_ok=True)
            ext = '.unknown'
            if reply.photo:
                ext = ".jpg"
            elif reply.document:
                for attr in reply.document.attributes:
                    if isinstance(attr, DocumentAttributeVideo):
                        ext = ".mp4"
                        break
                    elif isinstance(attr, DocumentAttributeAudio):
                        ext = ".mp3"
                        is_audio = True
                        break
                else:
                    ext = os.path.splitext(reply.file.name)[1] if reply.file.name else '.unknown'

            media_path = os.path.join(self.storage_path, f"{title}_{reply.id}{ext}")
            size = reply.file.size

            await self.client.download_media(reply.media, file=media_path)

            if progress_message:
                await utils.answer(progress_message, "🔄 <b>Почти готово...</b>")

        else:
            size = len(text.encode('utf-8'))

        self.messages[title] = {
            "text": text,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "media": media_path,
            "size": size,
            "is_audio": is_audio
        }

        self._save_messages()

        if progress_message:
            await utils.answer(progress_message, self.strings["msg_saved"].format(title=title))
        else:
            await utils.answer(message, self.strings["msg_saved"].format(title=title))

    @loader.command(
        ru_doc=" - удаляет сохранённое сообщение"
    )
    async def msd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["msg_not_found"])
            return

        if args in self.messages:
            media_path = self.messages[args].get('media')
            if media_path and os.path.exists(media_path):
                os.remove(media_path)

            del self.messages[args]
            self._save_messages()

            await utils.answer(message, self.strings["msg_deleted"].format(title=args))
        else:
            await utils.answer(message, self.strings["msg_not_found"])

    @loader.command(
        ru_doc=" - выводит справку по модулю"
    )
    async def msh(self, message: Message):
        await utils.answer(message, self.strings["help"])