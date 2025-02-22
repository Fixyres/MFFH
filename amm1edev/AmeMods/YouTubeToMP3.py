#meta developer: @thisLyomi & @AmekaMods

from telethon.tl.types import Message
import os
import yt_dlp
from .. import loader, utils

@loader.tds
class YouTubeToMP3Mod(loader.Module):
    """🎵 Скачивает mp3 из видео и плейлистов YouTube"""
    strings = {"name": "YouTubeToMP3"}

    async def ytmp3cmd(self, message: Message):
        """<ссылка> - скачивает mp3 с YouTube"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("❌ <b>Укажи ссылку на видео с YouTube.</b>")
            return
        
        url = args.strip()
        await message.edit("⏳ <b>Загружаю MP3...</b>")
        
        try:
            output_path = "downloads"
            os.makedirs(output_path, exist_ok=True)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

            await message.client.send_file(
                message.chat_id, file_name, caption=f"🎵 <b>MP3 из видео:</b> <a href='{url}'>ссылка</a>", parse_mode="html"
            )
            await message.delete()
            os.remove(file_name)
        except Exception as e:
            await message.edit(f"❌ <b>Ошибка:</b> {e}")

    async def ytplmp3cmd(self, message: Message):
        """<ссылка> [число] - скачивает mp3 из плейлиста YouTube. Число - количество загружаемых mp3"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("❌ <b>Укажи ссылку на плейлист YouTube.</b>")
            return
        
        args = args.split()
        url = args[0].strip()
        limit = int(args[1]) if len(args) > 1 else None

        await message.edit("⏳ <b>Проверяю плейлист...</b>")

        try:
            output_path = "downloads"
            os.makedirs(output_path, exist_ok=True)
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'extract_flat': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(url, download=False)
                entries = playlist_info.get("entries", [])
                total_videos = len(entries)

                if limit is not None and (limit < 1 or limit > total_videos):
                    await message.edit(f"❌ <b>Ошибка:</b> число треков превышает количество видео в плейлисте ({total_videos}).")
                    return

                download_count = limit if limit else total_videos
                await message.edit(f"⏳ <b>Загружаю {download_count} треков из плейлиста...</b>")

                ydl_opts.pop('extract_flat')  # Убираем, чтобы загружать файлы
                ydl_opts['playlistend'] = download_count

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                for file in os.listdir(output_path):
                    if file.endswith(".mp3"):
                        await message.client.send_file(
                            message.chat_id, f"{output_path}/{file}", caption=f"🎵 <b>Трек:</b> {file}", parse_mode="html"
                        )
                        os.remove(f"{output_path}/{file}")
                        
                await message.edit(f"✅ <b>Загрузка завершена. Треков: {download_count}.</b>")
        except Exception as e:
            await message.edit(f"❌ <b>Ошибка:</b> {e}")
