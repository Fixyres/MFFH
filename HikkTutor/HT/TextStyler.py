__version__ = (1, 0, 5)
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ© Copyright 2024
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤhttps://t.me/unnic
# 🔒ㅤㅤㅤㅤㅤLicensed under the GNU AGPLv3
# 🌐ㅤㅤhttps://www.gnu.org/licenses/agpl-3.0.html
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
# author: @unnic
# name: TextStyler
#██╗░░░██╗███╗░░██╗███╗░░██╗██╗░█████╗░
#██║░░░██║████╗░██║████╗░██║██║██╔══██╗
#██║░░░██║██╔██╗██║██╔██╗██║██║██║░░╚═╝
#██║░░░██║██║╚████║██║╚████║██║██║░░██╗
#╚██████╔╝██║░╚███║██║░╚███║██║╚█████╔╝
#░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚═╝░╚════╝
from telethon import events
from telethon.tl.types import Message
from .. import loader

@loader.tds
class TextStylerMod(loader.Module):
    """Модуль для форматирования текста в чате"""

    strings = {
        "name": "TextStyler"
    }

    def __init__(self):
        super().__init__()
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ignore_char",
                ".",
                lambda: "Префикс, указывающий на игнорирование сообщения.",
                validator=loader.validators.String(min_len=1, max_len=1)
            ),
            loader.ConfigValue(
                "enable_bold",
                False,
                lambda: "Включить/выключить автоматическое жирное форматирование текста.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_italic",
                False,
                lambda: "Включить/выключить автоматическое курсивное форматирование текста.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_strikethrough",
                False,
                lambda: "Включить/выключить автозачеркнутый текст.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_underlined",
                False,
                lambda: "Включить/выключить автоматическое подчеркивание текста.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_spoiler",
                False,
                lambda: "Включить/выключить автоматический скрытый текст.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_mono",
                False,
                lambda: "Включить/выключить автоматический моноширинный текст.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_quoted",
                False,
                lambda: "Включить/выключить автоматический цитируемый текст.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "enable_code_block",
                False,
                lambda: "Включить/выключить автоматический блок кода.",
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "ignore_formatting",
                False,
                lambda: "Игнорировать форматирование текста для сообщений в канале.",
                validator=loader.validators.Boolean()
            )
        )

    async def client_ready(self, client, db):
        self._client = client
        client.add_event_handler(self.message_handler, events.NewMessage())

    def format_text(self, text):
        if self.config["enable_bold"]:
            text = f"<b>{text}</b>"
        if self.config["enable_italic"]:
            text = f"<i>{text}</i>"
        if self.config["enable_underlined"]:
            text = f"<u>{text}</u>"
        if self.config["enable_strikethrough"]:
            text = f"<s>{text}</s>"
        if self.config["enable_spoiler"]:
            text = f"<tg-spoiler>{text}</tg-spoiler>"
        if self.config["enable_mono"]:
            text = f"<code>{text}</code>"
        if self.config["enable_quoted"]:
            text = f"<blockquote>{text}</blockquote>"
        if self.config["enable_code_block"]:
            text = f"<pre>{text}</pre>"
        return text

    async def message_handler(self, event):
        try:
            if not hasattr(self, 'config'):
                return

            original_message = event.raw_text

            if event.message.media:
                return

            if original_message.startswith(self.config["ignore_char"]):
                return

            if (event.is_channel and self.config["ignore_formatting"]) and not (event.is_group or event.is_private):
                return

            formatted_message = self.format_text(original_message)

            if formatted_message and formatted_message != original_message:
                await event.edit(formatted_message, parse_mode='html')

        except Exception as e:
            print(f"Error in message_handler: {e}")
  
    async def tshelpcmd(self, message: Message):
        """Показывает инструкцию по использованию модуля"""
        instruction = (
            "<blockquote><b>Информация о модуле и его функционале</b></blockquote>\n"
            "<blockquote><b><emoji document_id=4971987363145188045>🛑</emoji> Все исходящие сообщения автоматически форматируются, если включено то или инное форматирование.</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Если сообщение начинается с символа игнорирования, оно не будет изменено.</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Модуль не изменяет текст, содержащий только эмодзи, стикеры, GIF и медиафайлы.</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Модуль не действует в каналах.</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Hikka не поддерживает форматирование: <code><𝗕𝗹𝗼𝗰𝗸𝗾𝘂𝗼𝘁𝗲></code></b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Эмодзи и стикеры в тексте останутся без изменений, если выключены все форматирования.</b>\n\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Информация настроек:</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Символ игнорирования по умолчанию: «<code>.</code>»</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Ты можешь изменить игнорируемый символ на любой другой 1 символ, через конфиг.</b>\n"
            "<emoji document_id=4971987363145188045>🛑</emoji> <b>Ты можешь включить/выключить игнор для каналов.</b></blockquote>\n"
            "<blockquote><emoji document_id=5875452644599795072>🔞</emoji> <b>Разработчик: @unnic</b></blockquote>"
        )
        await message.edit(instruction, parse_mode='html')
