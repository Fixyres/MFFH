from telethon import events, types
from .. import loader, utils
import logging

logger = logging.getLogger(__name__)
__version__ = (1, 3, 0)


#░█░█░█▀▀░█▀█░█▀▀░▀█▀░█▀▄░█▀▀
#░▄▀▄░█▀▀░█░█░▀▀█░░█░░█░█░█▀▀
#░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀░░▀▀▀

# 🔒 Licensed under the AGPL-3.0
# 🥱 Im not allowing to edit this module.
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @XenSideMOD

@loader.tds
class AutoReactMod(loader.Module):
    strings = {
        "name": "AutoReact",
        "enabled": "✅ Автореакции включены в текущем чате",
        "disabled": "🚫 Автореакции выключены в текущем чате",
        "reaction_set": "✅ Установлена реакция: {}",
        "no_reaction": "⚠️ Укажите эмодзи или его ID для реакции",
        "premium_set": "✅ Установлена Premium реакция по ID: {}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "current_reaction",
            "👍",
            "Текущая реакция (эмодзи или ID)",
            
            "is_premium",
            False,
            "Является ли реакция Premium эмодзи"
        )

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.active_chats = self.get("active_chats", {})

    def get_active_chats(self):
        return self.active_chats

    def save_active_chats(self):
        self.set("active_chats", self.active_chats)

    @loader.command(ru_doc="Включить/выключить автореакции в текущем чате")
    async def artoggle(self, message):
        chat_id = str(message.chat_id)
        
        if chat_id in self.active_chats:
            del self.active_chats[chat_id]
            status = False
        else:
            self.active_chats[chat_id] = True
            status = True
            
        self.save_active_chats()
        
        await utils.answer(
            message,
            self.strings["enabled"] if status else self.strings["disabled"]
        )

    @loader.command(ru_doc="Установить реакцию (обычный эмодзи или ID для Premium)")
    async def setr(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_reaction"])
            return

        is_premium = args.isdigit()
        
        self.config["current_reaction"] = args
        self.config["is_premium"] = is_premium
        
        await utils.answer(
            message,
            self.strings["premium_set"].format(args) if is_premium else self.strings["reaction_set"].format(args)
        )

    @loader.watcher()
    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return
            
        chat_id = str(message.chat_id)
        
        if chat_id not in self.active_chats:
            return

        try:
            if self.config["is_premium"]:
                await message.react(types.ReactionCustomEmoji(document_id=int(self.config["current_reaction"])))
            else:
                await message.react(self.config["current_reaction"])
        except Exception as e:
            logger.error(f"Ошибка при установке реакции: {str(e)}")