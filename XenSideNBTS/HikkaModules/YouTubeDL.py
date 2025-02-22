import os
import subprocess
from yt_dlp import YoutubeDL
from telethon.tl.types import Message
from .. import loader, utils

#░█░█░█▀▀░█▀█░█▀▀░▀█▀░█▀▄░█▀▀
#░▄▀▄░█▀▀░█░█░▀▀█░░█░░█░█░█▀▀
#░▀░▀░▀▀▀░▀░▀░▀▀▀░▀▀▀░▀▀░░▀▀▀

# 🔒 Licensed under the AGPL-3.0
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta developer: @XenSideMOD

@loader.tds
class YouTubeDLMod(loader.Module):
    strings = {
        "name": "YouTubeDL",
        "args": "🎞 <b>You need to specify link</b>",
        "downloading": "🎞 <b>Downloading...</b>",
        "not_found": "🎞 <b>Video not found...</b>",
    }

    strings_ru = {
        "args": "🎞 <b>Укажи ссылку на видео</b>",
        "downloading": "🎞 <b>Скачиваю...</b>",
        "not_found": "🎞 <b>Видео не найден...</b>",
        "_cmd_doc_yt": "[mp3] <ссылка> - Скачать видео YouTube",
        "_cls_doc": "Скачать YouTube видео",
    }

    @loader.unrestricted
    async def ytcmd(self, message: Message):
        args = utils.get_args_raw(message)
        message = await utils.answer(message, self.strings("downloading"))

        ext = False
        if len(args.split()) > 1:
            ext, args = args.split(maxsplit=1)

        if not args:
            return await utils.answer(message, self.strings("args"))

        path = "/tmp/%(title)s.%(ext)s"
        ydl_opts = {
            'format': 'best',
            'outtmpl': path,
            'quiet': True,
        }

        if ext == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(args, download=True)
                path = ydl.prepare_filename(info)
                if ext == "mp3":
                    path = path.rsplit(".", 1)[0] + ".mp3"
        except Exception:
            return await utils.answer(message, self.strings("not_found"))

        await self._client.send_file(message.peer_id, path)
        os.remove(path)

        if message.out:
            await message.delete()
