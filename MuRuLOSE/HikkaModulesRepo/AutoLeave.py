from telethon.types import Message
from .. import loader, utils

# meta developer: @BruhHikkaModules


@loader.tds
class AutoLeave(loader.Module):
    """Auto leaving from channels and chats (maybe pm's)"""

    strings = {
        "name": "AutoLeave",
        "added": "Chat {} added"
    }

    strings_ru = {
        "_cls_doc": "Авто выход из каналов и чатов (может личных чатов)",
        "added": "Чат {} добавлен"
    }

    async def client_ready(self, client, db):
        self._common_lib = await self.import_lib("https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/libaries/common.py")

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ids",
                [],
                lambda: "list of ids for auto leave",
                validator=loader.validators.Series()
            )
        )

    @loader.command()
    async def addchatal(self, message: Message):
        """ [id / username] - Add chat to auto leave list"""
        args = utils.get_args_raw(message)
        uid = await self._common_lib._resolve_username_id(args)
        self.config["ids"].append(uid)
        await utils.answer(
            message,
            self.strings["added"].format(
                uid
            )
        )

    @loader.loop(autostart=True, interval=3600)
    async def leave_chat(self):
        for uid in self.config["ids"]:
            await self.client.delete_dialog(uid)

