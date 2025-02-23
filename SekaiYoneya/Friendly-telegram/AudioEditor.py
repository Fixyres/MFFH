# @Sekai_Yoneya

from pydub import AudioSegment, effects; from telethon import types; from .. import loader, utils; import math, requests, io; import numpy as np
@loader.tds
class AudioEditorMod(loader.Module):
    "Модуль для работы со звуком(???)"
    strings = {"name": "AudioEditor"}
    async def basscmd(self, m):
        """.bass [уровень bass'а 2-100 (Default 2)] <reply to audio>
        BassBoost"""
        args = utils.get_args_raw(m)
        if not args: lvl = 2
        else:
            if args.isdigit() and (1<int(args)<101): lvl = int(args)
            else: return await m.edit(f"[БассБуст] Укажи уровень от 2 до 100...")
        audio = await get_audio(m, "BassBoost")
        if not audio: return
        sample_track = list(audio.audio.get_array_of_samples())
        est_mean = np.mean(sample_track)
        est_std = 3 * np.std(sample_track) / (math.sqrt(2))
        bass_factor = int(round((est_std - est_mean) * 0.005))
        attenuate_db = 0
        filtered = audio.audio.low_pass_filter(bass_factor)
        out = (audio.audio - attenuate_db).overlay(filtered + lvl)
        await go_out(m, audio, out, audio.pref, f"{audio.pref} {lvl}lvl")
    async def fvcmd(self, m):
        """.fv [уровень шакала 2-100 (Default 25)] <reply to audio>
        Шакалинг"""
        args = utils.get_args_raw(m)
        if not args: lvl = 25
        else:
            if args.isdigit() and (1<int(args)<101): lvl = int(args)
            else: return await m.edit(f"[Шакал] Укажи уровень от 2 до 100...")
        audio = await get_audio(m, "Шакал")
        if not audio: return
        out = audio.audio + lvl
        await go_out(m, audio, out, audio.pref, f"{audio.pref} {lvl}lvl")
    async def echoscmd(self, m):
        """.echos <reply to audio>
            Эхо эффект"""
        audio = await get_audio(m, "Эхо эффект")
        if not audio: return
        out = AudioSegment.empty()
        n = 200
        none = io.BytesIO()
        out += audio.audio + AudioSegment.from_file(none)
        for i in range(5):
            echo = audio.audio - 10
            out = out.overlay(audio.audio, n)
            n += 200
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def volupcmd(self, m):
        """.volup <reply to audio>
            Увеличить громкость на 10dB"""
        audio = await get_audio(m, "+10dB")
        if not audio: return
        out = audio.audio + 10
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def voldwcmd(self, m):
        """.voldw <reply to audio>
            Уменьшить громкость на 10dB"""
        audio = await get_audio(m, "-10dB")
        if not audio: return
        out = audio.audio - 10
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def revscmd(self, m):
        """.revs <reply to audio>
            Развернуть аудио"""
        audio = await get_audio(m, "Reverse")
        if not audio: return
        out = audio.audio.reverse()
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def repscmd(self, m):
        """.reps <reply to audio>
            Повторить аудио 2 раза подряд"""
        audio = await get_audio(m, "Повтор")
        if not audio: return
        out = audio.audio*2
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def slowscmd(self, m):
        """.slows <reply to audio>
            Замедлить аудио 0.5x"""
        audio = await get_audio(m, "Замедление")
        if not audio: return
        s2 = audio.audio._spawn(audio.audio.raw_data, overrides={"frame_rate": int(audio.audio.frame_rate * 0.5)})
        out = s2.set_frame_rate(audio.audio.frame_rate)
        await go_out(m, audio, out, audio.pref, audio.pref, audio.duration*2)
    async def fastscmd(self, m):
        """.fasts <reply to audio>
        Ускорить аудио 1.5x"""
        audio = await get_audio(m, "Ускорение")
        if not audio: return
        s2 = audio.audio._spawn(audio.audio.raw_data, overrides={"frame_rate": int(audio.audio.frame_rate * 1.5)})
        out = s2.set_frame_rate(audio.audio.frame_rate)
        await go_out(m, audio, out, audio.pref, audio.pref, round(audio.duration/2))
    async def rightscmd(self, m):
        """.rights <reply to audio>
            Весь звук в правый канал"""
        audio = await get_audio(m, "Правый канал")
        if not audio: return
        out = effects.pan(audio.audio, +1.0)
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def leftscmd(self, m):
        """.lefts <reply to audio>
            Весь звук в левый канал"""
        audio = await get_audio(m, "Левый канал")
        if not audio: return
        out = effects.pan(audio.audio, -1.0)
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def normscmd(self, m):
        """.norms <reply to audio>
            Нормализовать звук (Из тихого - нормальный)"""
        audio = await get_audio(m, "Нормализация")
        if not audio: return
        out = effects.normalize(audio.audio)
        await go_out(m, audio, out, audio.pref, audio.pref)
    async def byrobertscmd(self, m):
        '''.byroberts <reply to audio>
            Добавить в конец аудио "Directed by Robert B Weide"'''
        audio = await get_audio(m, "Directed by...")
        if not audio: return
        out = audio.audio + AudioSegment.from_file(io.BytesIO(requests.get("https://raw.githubusercontent.com/Daniel3k00/files-for-modules/master/directed.mp3").content)).apply_gain(+8)
        await go_out(m, audio, out, audio.pref, audio.pref)
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []
    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()
async def get_audio(m, pref):
    class audio_ae_class(): audio = None; duration = None; voice = None; pref = None; reply = None
    reply = await m.get_reply_message()
    if reply and reply.file and reply.file.mime_type.split("/")[0] == "audio":
        ae = audio_ae_class()
        ae.pref = pref
        ae.reply = reply
        ae.voice = reply.document.attributes[0].voice
        ae.duration = reply.document.attributes[0].duration
        await m.edit(f"[{pref}] Скачиваю...")
        ae.audio = AudioSegment.from_file(io.BytesIO(await reply.download_media(bytes)))
        await m.edit(f"[{pref}] Работаю...")
        return ae
    else: await m.edit(f"[{pref}] reply to audio..."); return None
async def go_out(m, audio, out, pref, title, fs=None):
    o = io.BytesIO()
    o.name = "audio." + ("ogg" if audio.voice else "mp3")
    if audio.voice: out.split_to_mono()
    await m.edit(f"[{pref}] Экспортирую...")
    out.export(o, format="mp3" if audio.voice else "wav", bitrate="44100" if audio.voice else None, codec="u16le" if audio.voice else None)
    o.seek(0)
    await m.edit(f"[{pref}] Отправляю...")
    await m.client.send_file(m.to_id, o, reply_to=audio.reply.id, voice_note=audio.voice, attributes=[types.DocumentAttributeAudio(duration = fs if fs else audio.duration, title=title, performer="@Sekai_Yoneya")] if not audio.voice else None)
    await m.delete()
