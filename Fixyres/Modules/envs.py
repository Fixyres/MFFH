# ------------------------------------------------------
#░█░█░█▀▀░█▀█░█▀▀░▀█▀░█▀▄░█▀▀
#░▄▀▄░█▀▀░█░█░▀▀█░░█░░█░█░█▀▀
#░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀░░▀▀▀

# 🔒 Licensed under the AGPL-3.0
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @XenSideMOD

import io

from requests import post

from .. import loader, utils  # pylint: disable=relative-beyond-top-level


@loader.tds
class envsMod(loader.Module):
    """Uploader envs.sh"""

    strings = {"name": "envs.sh Uploader"}

    async def client_ready(self, client, db):
        self.client = client

    @loader.sudo
    async def envscmd(self, message):
        await message.edit("<b>Uploading...</b>")
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("<b>Reply to message!</b>")
            return
        media = reply.media
        if not media:
            file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
            file.name = "txt.txt"
        else:
            file = io.BytesIO(await self.client.download_file(media))
            file.name = (
                reply.file.name if reply.file.name else reply.file.id + reply.file.ext
            )
        try:
            x0at = post("https://envs.sh", files={"file": file})
        except ConnectionError as e:
            await message.edit(ste(e))
            return
        url = x0at.text
        output = f'<a href="{url}">URL: </a><code>{url}</code>'
        await message.edit(output)