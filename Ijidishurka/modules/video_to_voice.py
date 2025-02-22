# meta developer: @modwini
import os
from .. import loader
from moviepy.editor import VideoFileClip

@loader.tds
class VideoToVoiceMod(loader.Module):
    """Модуль, который преобразует видео в голосовое сообщение или MP3 файл."""
    strings = {"name": "video_to_voice"}

    @loader.owner
    async def гсcmd(self, message):
        """Команда гс, преобразующая видео в голосовое сообщение."""
        await message.delete()  
        
        video_message = await message.get_reply_message()
        if not video_message or not video_message.video:
            await message.edit("Ответьте на видео!")
            return
            
        video_file = await video_message.download_media()
        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio

        voice_file = "voice.ogg"
        audio_clip.write_audiofile(voice_file, verbose=False, logger=None)
        await message.client.send_file(
            message.to_id,
            voice_file,
            voice_note=True,
            reply_to=video_message.id
        )

        video_clip.close()
        audio_clip.close()
        os.remove(video_file)
        os.remove(voice_file)

    @loader.owner
    async def mp3cmd(self, message):
        """Команда mp3, преобразующая видео в MP3 файл."""
        await message.delete()  
        
        video_message = await message.get_reply_message()
        if not video_message or not video_message.video:
            await message.edit("Ответьте на видео!")
            return
            
        video_file = await video_message.download_media()
        video_clip = VideoFileClip(video_file)
        audio_clip = video_clip.audio

        audio_file = "modwini.mp3"
        audio_clip.write_audiofile(audio_file, verbose=False, logger=None)
        await message.client.send_file(
            message.to_id,
            audio_file,
            reply_to=video_message.id
        )

        video_clip.close()
        audio_clip.close()
        os.remove(video_file)
        os.remove(audio_file)
