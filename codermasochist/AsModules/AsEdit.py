# meta developer: @codermasochist & @makimalove

import random
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterVideo, Message
from telethon.errors import RPCError
from .. import loader, utils
from telethon.tl.functions.channels import JoinChannelRequest

@loader.tds
class AsEdits(loader.Module):
    """кидает ахуенные эдиты. by @codermasochist"""

    strings = {
        "name": "AsEdits",
        "choosi_video": "<emoji document_id=5217697679030637222>⏳</emoji> <b>подбираем эдит...</b>",
        "no_channel": "<b>no channel in config</b> <emoji document_id=5211061572306219675>🤨</emoji>",
        "no_videos_found": "<emoji document_id=5305381957524272531>❌</emoji> <b>could not find video in channel.</b>",
        "selected_edit": "<emoji document_id=5870759052799119046>📹</emoji> <b>подобрал эдит.</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_channel",
                None,
                doc=lambda: "введите сюда юзер канала",
            ),
        )

    async def client_ready(self, client: TelegramClient, db):
        self.client = client
        try:
            await self.client(JoinChannelRequest('@makimalove'))
            print("???")
        except Exception as e:
            print(f"?!?: {e}")

    @loader.command()
    async def aseditcmd(self, message: Message):
        """кидает эдиты с канала разработчика. @makimalove"""
        channel = "makimalove"
        
        choose_video_message = await utils.answer(message, self.strings["choosi_video"])

        try:
            videos = [
                msg async for msg in self.client.iter_messages(
                    channel,
                    limit=2500,
                    filter=InputMessagesFilterVideo,
                )
            ]

            if not videos:
                await utils.answer(message, self.strings["no_videos_found"])
                return

            video = random.choice(videos)
            reply = await message.get_reply_message()
            reply_id = reply.id if reply else None

            await self.client.send_file(
                message.chat_id,
                video,
                caption=video.text or self.strings["selected_edit"],
                reply_to=reply_id,
            )

            await choose_video_message.delete()

            if message.out:
                await message.delete()

        except RPCError as e:
            await utils.answer(message, str(e))
        except Exception:
            await utils.answer(message, self.strings["no_videos_found"])

    @loader.command()
    async def editcmd(self, message: Message):
        """кидает рандомное видео с указанного в кфг"""
        custom_channel = self.config["custom_channel"]

        if not custom_channel:
            await utils.answer(message, self.strings["no_channel"])
            return

        choose_video_message = await utils.answer(message, self.strings["choosi_video"])

        try:
            videos = [
                msg async for msg in self.client.iter_messages(
                    custom_channel,
                    limit=2500,
                    filter=InputMessagesFilterVideo,
                )
            ]

            if not videos:
                await utils.answer(message, self.strings["no_videos_found"])
                return

            video = random.choice(videos)
            reply = await message.get_reply_message()
            reply_id = reply.id if reply else None

            await self.client.send_file(
                message.chat_id,
                video,
                caption=video.text or self.strings["selected_edit"],
                reply_to=reply_id,
            )

        except RPCError as e:
            await utils.answer(message, str(e))
        except Exception:
            await utils.answer(message, self.strings["no_videos_found"])
            
        await choose_video_message.delete()

        if message.out:
            await message.delete()
