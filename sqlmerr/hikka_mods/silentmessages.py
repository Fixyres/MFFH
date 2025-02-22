"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""

# meta developer: @sqlmerr_m
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/silentmessages.png?raw=true
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_silentmessages.png?raw=true

from .. import loader, utils
from hikkatl.tl.patched import Message


@loader.tds
class SilentMessages(loader.Module):
    """With this module you won't miss important messages sent without sound!"""

    strings = {
        "name": "SilentMessages",
        "_cfg_chats": "Chats in which the module will monitor messages without sound",
        "_cfg_status": "Is the module working or not?",
        "_cfg_text": "The text that will be sent by your inline bot when a silent message is received",
        "enabled": "enabled",
        "disabled": "disabled",
        "toggle_message": "<emoji document_id=5222444124698853913>🔖</emoji> <b>Module {}!</b>",
    }
    strings_ru = {
        "_cfg_chats": "Чаты, в которых модуль будет следить за сообщениями без звука",
        "_cfg_status": "Работает ли модуль или нет",
        "_cfg_text": "Текст, который будет отправлен вашим инлайн ботом, когда будет получено сообщение без звука",
        "enabled": "включен",
        "disabled": "выключен",
        "toggle_message": "<emoji document_id=5222444124698853913>🔖</emoji> <b>Модуль {}!</b>",
        "_cls_doc": "С этим модулем вы не пропустите важные сообщения, отправленные без звука!",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "chats",
                [],
                lambda: self.strings("_cfg_chats"),
                validator=loader.validators.Series(loader.validators.TelegramID()),
            ),
            loader.ConfigValue(
                "status",
                False,
                lambda: self.strings("_cfg_status"),
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "text",
                "<b>New silent message in chat {chat}:</b> {link}",
                lambda: self.strings("_cfg_text"),
                validator=loader.validators.String(),
            ),
        )

    @loader.command(ru_doc="включить/выключить модуль")
    async def silentmessages(self, message: Message):
        """toggle module status"""
        self.config["status"] = not self.config["status"]
        await utils.answer(
            message,
            self.strings("toggle_message").format(
                self.strings("enabled")
                if self.config["status"]
                else self.strings("disabled")
            ),
        )

    @loader.watcher()
    async def watcher(self, message: Message):
        if not self.config["status"]:
            return

        if (
            (getattr(message, "chat", None) and message.chat.id in self.config["chats"])
            or (
                getattr(message, "sender", None)
                and message.sender.id in self.config["chats"]
            )
        ) and message.silent is True:
            link = await utils.get_message_link(message)
            chat_id = utils.get_chat_id(message)
            await self.inline.bot.send_message(
                self.tg_id, self.config["text"].format(chat=chat_id, link=link)
            )
