# meta developer: @angellmodules
import random
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.messages import GetHistoryRequest

from .. import loader, utils


@loader.tds
class RandomCircleMod(loader.Module):
    """Модуль для отправки рандомного мемного кружочка"""

    strings = {"name": "RandomCircle"}

    async def rccmd(self, message):
        """Отправляет рандомный кружочек."""
        channels = ["memeswave", "memkrujki"]
        await message.edit("🔄 Ищу кружочек...")

        try:
            random_channel = random.choice(channels)
            entity = await message.client.get_entity(f"t.me/{random_channel}")
            peer = InputPeerChannel(entity.id, entity.access_hash)

            history = await message.client(
                GetHistoryRequest(
                    peer=peer,
                    limit=50,
                    offset_date=None,
                    offset_id=0,
                    max_id=0,
                    min_id=0,
                    add_offset=0,
                    hash=0,
                )
            )

            circles = [
                msg for msg in history.messages if msg.media and msg.media.document.mime_type == "video/mp4"
            ]

            if not circles:
                await message.edit("❌ Не удалось найти кружочки.")
                return

            random_circle = random.choice(circles)

            await message.client.send_message(
                message.chat_id, file=random_circle.media.document, message="🎥 Рандомный кружочек"
            )
            await message.delete()

        except Exception as e:
            await message.edit(f"❌ Ошибка: {str(e)}")





#made by @sawwnapix
