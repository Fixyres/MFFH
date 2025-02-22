# meta developer: @modwini
import io
import random

import requests
from pydub import AudioSegment
from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class KeywordMod(loader.Module):
    """Присылает громкое голосовое сообщение +_+"""

    strings = {"name": "громкие гс"}

    @loader.unrestricted
    async def micmd(self, message: Message):
        """Скинуть гс"""
        args = utils.get_args_raw(message) or "<i></i>"
        mi = [
"https://github.com/Ijidishurka/gs/blob/main/%D0%B7%D0%B0%D0%B9%D1%82%D0%B8%20%D0%B2%20%D0%BA%D0%BB%D0%B5%D1%88.mp3?raw=true",
            
            "https://github.com/Ijidishurka/gs/blob/main/%D1%85%D0%B8%D1%85%D0%B8%D1%85%D0%B8%D1%85%D0%B0.m4a?raw=true",
        ]

        voice = (await utils.run_sync(requests.get, random.choice(mi))).content

        byte = io.BytesIO(b"0")
        segm = AudioSegment.from_file(io.BytesIO(voice))
        random_duration = random.randint(5000, 15000)
        end = len(segm) - random_duration
        end = len(segm) if end < 0 else end
        random_begin = random.randint(0, end)
        random_begin = 0 if end < 0 else random_begin

        segm[random_begin : min(len(segm), random_begin + random_duration)].export(
            byte,
            format="ogg",
        )

        byte.name = "mi.ogg"

        await self._client.send_file(
            message.peer_id,
            byte,
            caption=args,
            voice_note=True,
            reply_to=message.reply_to_msg_id,
        )

        if message.out:
            await message.delete()
