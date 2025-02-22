# meta developer: @angellmodules

from telethon import functions
from .. import loader, utils

@loader.tds
class ProfileMod(loader.Module):
    """Your profile changer"""

    strings = {"name": "Profilemanager"}

    @loader.command()
    async def cname(self, message):
        """<name> — Change display name"""
        name = utils.get_args_raw(message)
        if not name:
            await message.edit("<b>Please provide a name <emoji document_id=6039614175917903752>✏️</emoji></b>")
            return
        await message.client(functions.account.UpdateProfileRequest(first_name=name))
        await message.edit(f"<b>Name changed to:</b> {name}<emoji document_id=5774022692642492953>✅</emoji>" )

    @loader.command()
    async def cusern(self, message):
        """<username> — Change username (leave empty to remove)"""
        username = utils.get_args_raw(message)
        await message.client(functions.account.UpdateUsernameRequest(username if username else ""))
        await message.edit(f"<b>Username {'removed' if not username else 'changed to'}:</b> {username or''}")

    @loader.command()
    async def cbio(self, message):
        """<bio> — Change bio"""
        bio = utils.get_args_raw(message)
        if not bio:
            await message.edit("<b>Please provide a bio<emoji document_id=6039614175917903752>✏️</emoji></b>")
            return
        await message.client(functions.account.UpdateProfileRequest(about=bio))
        await message.edit(f"<b>Bio changed to:</b> {bio}<emoji document_id=5774022692642492953>✅</emoji>")

    @loader.command()
    async def cavatar(self, message):
        """<reply to photo> — Change avatar"""
        reply = await message.get_reply_message()
        if not reply or not reply.photo:
            await message.edit("<b>Reply to a photo to set as avatar.</b>")
            return
        photo = await message.client.download_media(reply.photo)
        await message.client(functions.photos.UploadProfilePhotoRequest(file=await message.client.upload_file(photo)))
        await message.edit("<b>Avatar changed successfully.</b><emoji document_id=5774022692642492953>✅</emoji>")





#made by @sawwnapix
