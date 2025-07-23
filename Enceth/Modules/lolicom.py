__version__ = (1, 0, 1)
# meta developer: @Enceth
# change-log: fix link


from telethon.tl.functions.messages import ImportChatInviteRequest
import random
from .. import loader, utils

@loader.tds
class Lolicom(loader.Module):
    """
    Абсолютно рандомные лоли комиксы 
    """

    strings = {
        "name": "Lolicom",
        "forwarding": "📥 Ща будет",
        "done": "✅ Вот",
        "error": "❌ Ошибка: {}",
        "no_messages": "❌ Ну все пизда",
    }

    async def client_ready(self, client, db):
        self.client = client

    async def _join_chat(self, invite_link):
        """
        ах ох ох
        """
        try:
            return await self.client.get_entity(invite_link)
        except Exception:
            await self.client(ImportChatInviteRequest(invite_link.split("+")[1]))
            return await self.client.get_entity(invite_link)

    @loader.command(
        ru_doc="Рандом лоли-комиксы",
        en_doc="Randrom loli comics ",
    )
    async def lolicom(self, message):
        """
        Рандомный лоли-комикс (NSFW)
        """
        chat_invite_link = "https://t.me/+NDssABFs5HtiY2Uy"

        try:
            entity = await self._join_chat(chat_invite_link)
            await utils.answer(message, self.strings["forwarding"])

            messages = await self.client.get_messages(entity, limit=300)
            if not messages:
                await utils.answer(message, self.strings["no_messages"])
                return

            random_msg = random.choice(messages)
            await self.client.send_message(
                message.to_id,
                random_msg.message,
                file=random_msg.media,
            )
            await utils.answer(message, self.strings["done"])
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(e))
