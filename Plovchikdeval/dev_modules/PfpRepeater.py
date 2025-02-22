"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

# This module is for setting a profile photo and repeating it.

# Commands:
# .pfp <photo> - Start repeating profile photo.
# .pfpstop - Stop repeating profile photo.

# You can also reply to a photo with .pfp to set it as the profile photo.

# Disclaimer: We are not responsible for any issues that may arise with your account.

import asyncio
from telethon import functions
from .. import loader, utils

@loader.tds
class PfpRepeaterMod(loader.Module):
    """Profile Photo Repeater Module"""
    strings = {"name": "PfpRepeater"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "DELAY", 900, validator=loader.validators.Integer(),
            ),
        )

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.running = False
        self.task = None

    async def set_profile_photo(self, photo_path):
        while self.running:
            file = await self.client.upload_file(photo_path)
            await self.client(functions.photos.UploadProfilePhotoRequest(file=await self.client.upload_file(file)))
            await asyncio.sleep(self.config["DELAY"])

    @loader.command()
    async def pfp(self, message):
        """Start repeating profile photo"""
        reply = await message.get_reply_message()
        if reply and reply.photo:
            photo_path = await message.client.download_media(reply.photo)
        elif message.media and message.photo:
            photo_path = await message.client.download_media(message)
        else:
            await utils.answer(message, "Please provide the photo or reply to a photo.")
            return

        if not self.running:
            self.running = True
            self.task = asyncio.create_task(self.set_profile_photo(photo_path))
            await utils.answer(message, f"Started repeating profile photo every {self.config['DELAY']} seconds.")
        else:
            await utils.answer(message, "Profile photo repeater is already running.")

    @loader.command()
    async def pfpstop(self, message):
        """Stop repeating profile photo"""
        if self.running:
            self.running = False
            self.task.cancel()
            await utils.answer(message, "Stopped repeating profile photo.")
        else:
            await utils.answer(message, "Profile photo repeater is not running.")
