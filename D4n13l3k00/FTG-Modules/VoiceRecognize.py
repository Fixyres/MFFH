# .------.------.------.------.------.------.------.------.------.------.
# |D.--. |4.--. |N.--. |1.--. |3.--. |L.--. |3.--. |K.--. |0.--. |0.--. |
# | :/\: | :/\: | :(): | :/\: | :(): | :/\: | :(): | :/\: | :/\: | :/\: |
# | (__) | :\/: | ()() | (__) | ()() | (__) | ()() | :\/: | :\/: | :\/: |
# | '--'D| '--'4| '--'N| '--'1| '--'3| '--'L| '--'3| '--'K| '--'0| '--'0|
# `------`------`------`------`------`------`------`------`------`------'
#
#                     Copyright 2023 t.me/D4n13l3k00
#           Licensed under the Creative Commons CC BY-NC-ND 4.0
#
#                    Full license text can be found at:
#       https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#
#                           Human-friendly one:
#            https://creativecommons.org/licenses/by-nc-nd/4.0

# meta developer: @D4n13l3k00


from io import BytesIO

# requires: pydub speechRecognition
import speech_recognition as srec
from pydub import AudioSegment as auds

from .. import loader, utils  # type: ignore


@loader.tds
class VoiceRecognitionMod(loader.Module):
    "Распознавание речи через Google Recognition API"
    strings = {"name": "VoiceRecognition", "pref": "<b>[VRC]</b> "}

    @loader.owner
    async def recvcmd(self, m):
        ".recv <reply to voice/audio> - распознать речь"
        reply = await m.get_reply_message()
        if reply and reply.file.mime_type.split("/")[0] == "audio":
            m = await utils.answer(m, self.strings["pref"] + "Downloading...")
            source = BytesIO(await reply.download_media(bytes))
            source.name = reply.file.name
            out = BytesIO()
            out.name = "recog.wav"
            m = await utils.answer(m, self.strings["pref"] + "Converting...")
            auds.from_file(source).export(out, "wav")
            out.seek(0)
            m = await utils.answer(m, self.strings["pref"] + "Processing...")
            recog = srec.Recognizer()
            sample_audio = srec.AudioFile(out)
            with sample_audio as audio_file:
                audio_content = recog.record(audio_file)
            await utils.answer(
                m,
                self.strings["pref"]
                + recog.recognize_google(audio_content, language="ru-RU"),
            )
        else:
            await utils.answer(m, self.strings["pref"] + "reply to audio/voice...")
