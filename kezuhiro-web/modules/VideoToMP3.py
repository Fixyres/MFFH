#     ___    __ __ ____
#    /   |  / //_//  _/
#   / /| | / ,<   / /  
#  / ___ |/ /| |_/ /   
# /_/  |_/_/ |_/___/   
#                      
#     __  _______  ____  _____
#    /  |/  / __ \/ __ \/ ___/
#   / /|_/ / / / / / / /\__ \ 
#  / /  / / /_/ / /_/ /___/ / 
# /_/  /_/\____/_____//____/
#
# meta developer: @aki_modules


from .. import loader, utils
import os
from telethon.tl.types import Message, DocumentAttributeAudio
from moviepy import VideoFileClip

@loader.tds
class VideoToMP3Mod(loader.Module):
    strings = {
        "name": "VideoToMP3",
        "not_reply": "<emoji document_id=5116275208906343429>‼️</emoji> <b>Reply to video for conversion.</b>",
        "conv_msg": "<emoji document_id=4911241630633165627>✨</emoji> <b>Converting video to audio...</b>",
        "conv_successful": "<emoji document_id=4916036072560919511>✅</emoji> <b>Conversion complete!</b>",
        "error": "<emoji document_id=4918014360267260850>⛔️</emoji> <b>An error occured:</b>\n<pre><code class='language-python'>{}</code></pre>",
    }
    strings_ru = {
        "not_reply": "<emoji document_id=5116275208906343429>‼️</emoji> <b>Ответьте на видео для конвертации.</b>",
        "conv_msg": "<emoji document_id=4911241630633165627>✨</emoji> <b>Конвертация видео в аудио...</b>",
        "conv_successful": "<emoji document_id=4916036072560919511>✅</emoji> <b>Конвертация завершена!</b>",
        "error": "<emoji document_id=4918014360267260850>⛔️</emoji> <b>Произошла ошибка:</b>\n<pre><code class='language-python'>{}</code></pre>",
    }
    
    @loader.command(ru_doc=" <reply_to_video> [имя_файла] - Конвертировать видео в аудио")
    async def mp3cmd(self, message: Message):
        """ <reply_to_video> [file_name] - Convert video to audio"""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)

        if not reply or not reply.video:
            await utils.answer(message, self.strings("not_reply"))
            return
        
        conv_msg = await utils.answer(message, self.strings("conv_msg"))
        
        video = await reply.download_media()

        try:
            audio_file = f"@aki_modules.mp3"
            video_clip = VideoFileClip(video)
            video_clip.audio.write_audiofile(audio_file)
            video_clip.close()
    
            await conv_msg.delete()
    
            await message.client.send_file(
                message.chat_id,
                audio_file,
                caption=self.strings("conv_successful"),
                attributes=[
                    DocumentAttributeAudio(
                        duration=0,
                        performer="@aki_modules",
                        title=args if args else "video.mp3",
                    )
                ],
                reply_to=reply.id
            )

            os.remove(video)
            os.remove(audio_file)
            
        except Exception as e:
            await utils.answer(message, self.strings("error").format(e))
            
            if os.path.exists(video):
                os.remove(video)
            if os.path.exists(audio_file):
                os.remove(audio_file)
