from hikkatl.tl.types import (
    ReplyInlineMarkup,
    KeyboardButtonCallback,
    KeyboardButtonUrl,
)

from .. import utils, loader

from hikkatl.tl.patched import Message

# meta developer: @sqlmerr_m
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/quicktools.png?raw=true
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/quicktools.png?raw=true


@loader.tds
class QuickTools(loader.Module):
    """Module with various quick and useful tools"""

    strings = {
        "name": "QuickTools",
        "id_cmd_text": (
            "<emoji document_id=5974526806995242353>🆔</emoji> <b>Id</b>\n"
            "<b>·</b> <emoji document_id=5417843850808926945>🫵</emoji> <b>Your id: </b><code>{}</code>\n"
            "<b>·</b> <emoji document_id=5443038326535759644>💬</emoji> <b>Chat id:</b> <code>{}</code>\n"
            "<b>·</b> <emoji document_id=5366526456274891907>🎈</emoji> <b>User id:</b> <code>{}</code>\n"
            "<b>·</b> <emoji document_id=5974187156686507310>💬</emoji> <b>Replied Message id:</b> <code>{}</code>\n"
        ),
        "reply_markup_cmd_text": "<emoji document_id=5397782960512444700>📌</emoji> <b>Buttons:</b>\n{}",
        "empty": "Empty",
        "no_reply": "<emoji document_id=5210952531676504517>❌</emoji> <b>No reply!</b>",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> <b>No args!</b>",
        "no_reply_markup": "<emoji document_id=5210952531676504517>❌</emoji> No reply markup!",
    }

    strings_ru = {
        "id_cmd_text": (
            "<emoji document_id=5974526806995242353>🆔</emoji> <b>Айди</b>\n"
            "<b>·</b> <emoji document_id=5417843850808926945>🫵</emoji> <b>Твой айди: </b><code>{}</code>\n"
            "<b>·</b> <emoji document_id=5443038326535759644>💬</emoji> <b>Айди чата:</b> <code>{}</code>\n"
            "<b>·</b> <emoji document_id=5366526456274891907>🎈</emoji> <b>Айди пользователя:</b> <code>{}</code>\n"
            "<b>·</b> <emoji document_id=5974187156686507310>💬</emoji> <b>Айди ответного сообщения:</b> <code>{}</code>\n"
        ),
        "reply_markup_cmd_text": "<emoji document_id=5397782960512444700>📌</emoji> <b>Кнопки:</b>\n{}",
        "empty": "Отсутствует",
        "no_reply": "<emoji document_id=5210952531676504517>❌</emoji> <b>Вы не ответили на сообщение!</b>",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> <b>Вы не передали аргументы!</b>",
        "no_reply_markup": "<emoji document_id=5210952531676504517>❌</emoji> Вы ответили на сообщение, где нет кнопок!",
        "_cls_doc": "Модуль с разными быстрыми и полезными инструментами",
    }

    @loader.command(
        ru_doc="<реплай на сообщение> Получить айди пользователя/чата/отправителя/сообщения"
    )
    async def id(self, message: Message) -> None:
        """<reply to message> Get user/chat/sender/replied message/message ID"""
        reply: Message = await message.get_reply_message()

        sender_id = message.from_id
        chat_id = message.chat_id
        user_id = reply.from_id if reply else self.strings("empty")
        message_id = reply.id if reply else self.strings("empty")
        text = self.strings("id_cmd_text").format(
            sender_id, chat_id, user_id, message_id
        )
        await utils.answer(message, text)

    @loader.command(ru_doc="<реплай на сообщение> Получить текст сообщения")
    async def text(self, message: Message) -> None:
        """<reply to message> Get replied message text"""

        reply: Message = await message.get_reply_message()
        text = reply.text if (reply and reply.text) else ""
        await utils.answer(message, f"<pre>{utils.escape_html(text)}</pre>")

    @loader.command(ru_doc="<реплай на сообщение> Получить кнопки сообщения")
    async def reply_markup(self, message: Message) -> None:
        """<reply to message> Get replied message reply markup (buttons)"""

        reply: Message = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        reply_markup = reply.reply_markup

        if not reply_markup or not isinstance(reply_markup, ReplyInlineMarkup):
            await utils.answer(message, self.strings("no_reply_markup"))
            return

        buttons = []
        for row in reply_markup.rows:
            buttons.extend(row.buttons)

        text = ""
        for button in buttons:
            if isinstance(button, KeyboardButtonCallback):
                value = button.data.decode("utf-8")
                value_type = "data"
            elif isinstance(button, KeyboardButtonUrl):
                value = button.url
                value_type = "url"
            else:
                text += f"  - <i>{button.text}</i>\n"
                continue

            text += f"  - <i>{button.text}</i> - {value_type}: <code>{value}</code>\n"

        await utils.answer(message, self.strings("reply_markup_cmd_text").format(text))
