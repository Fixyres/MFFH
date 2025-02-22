__version__ = (3, 0, 1)

# ---------------------------------------------------------------------------------
#  /\_/\  🌐 This module was loaded through https://t.me/hikkamods_bot
# ( o.o )  🔐 Licensed under the GNU AGPLv3.
#  > ^ <   ⚠️ Owner of heta.hikariatama.ru doesn't take any responsibilities or intellectual property rights regarding this script
# ---------------------------------------------------------------------------------
# Name: HikkaVoiceMod
# Author: hikariatama
# ---------------------------------------------------------------------------------

#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.dan.tatar/voicechat_icon.png
# meta banner: https://mods.hikariatama.ru/badges/voicechat.jpg
# meta developer: @kshmods
# coded by : @hikarimods
# scope: hikka_only
# scope: hikka_min 1.3.0

import asyncio
import atexit
import contextlib
import logging
import os
import re
import shutil
import tempfile
from hikkalls import HikkaLls, StreamType, types
from hikkalls.binding import Binding
from hikkalls.environment import Environment
from hikkalls.exceptions import(
     AlreadyJoinedError,
     NoActiveGroupCall,
     TelegramServerError,
     NotInGroupCallError,
     GroupCallNotFound)

from hikkalls.handlers import HandlersHolder
from hikkalls.methods import Methods
from hikkalls.mtproto import MtProtoClient
from hikkalls.scaffold import Scaffold
from hikkalls.types import Cache
from hikkalls.methods.groups.change_volume_call import ChangeVolumeCall

from hikkalls.types.call_holder import CallHolder
from hikkalls.types.update_solver import UpdateSolver
from telethon.tl.functions.phone import CreateGroupCallRequest
from telethon.tl.types import DocumentAttributeFilename, Message
from yt_dlp import YoutubeDL
import json

from .. import loader, utils
from ..inline.form import *
from ..inline.types import InlineCall
from ..tl_cache import CustomTelegramClient
from hikkatl.errors.rpcbaseerrors import BadRequestError
import glob

logging.getLogger("hikkalls").setLevel(logging.ERROR)


@loader.tds
class HikkaVoiceMod(loader.Module):
    strings = {
        "name": "HikkaVoiceMod",
        "no_reply": "🚫 <b>Reply to a message</b>",
        "no_queue": "🚫 <b>The queue is empty</b>",
        "queue": "🎙 <b>Playlist</b>:\n\n{}",
        "queueadd": "🎧 <b>{} added to the playlist</b>",
        "queueaddv": "📼 <b>{} added to the playlist</b>",
        "playnext_err": "📚 Empty playlist. Add tracks to continue!",
        "downloading": "📥 <b>Downloading...</b>",
        "playing": " <b>Now playing {}</b>",
        "playing_with_next": " <b>Now playing {}</b>\n➡️ <b>Next: {}</b>",
        "pause": "⏸",
        "play": "▶",
        "mute": "🔇",
        "unmute": "🔈",
        "next": "⏭",
        "stopped": "⏹ <b>Stopped</b>",
        "stop": "⏹ ",
        "loop_b": "🔁",
        "loop_a": "🔄",
        "close": "🚫 Close",
        "vol": "🔊 Volume",
        "volup": "🔊 Louder",
        "voldown": "🔉 Quieter",
        "playlist": "📚 Playlist",
        "back": "🔙 Back",
        "choose_delete": "♻️ <b>Select a queue item to delete</b>",
        "play_err": "🚫 <b>Add a song first.</b>"
    }

    strings_ru = {
        "name": "HikkaVoiceMod",
        "no_reply": "🚫 <b>Ответьте на сообщение</b>",
        "no_queue": "🚫 <b>Очередь пуста</b>",
        "queue": "🎙 <b>Плейлист</b>:\n\n{}",
        "queueadd": "🎧 <b>{} добавлен в плейлист</b>",
        "queueaddv": "📼 <b>{} добавлен в плейлист</b>",
        "playnext_err": "📚 Плейлист пуст. Добавьте треки, чтобы продолжить!",
        "downloading": "📥 <b>Загрузка...</b>",
        "playing": " <b>Играет {}</b>",
        "playing_with_next": " <b>Играет {}</b>\n➡️ <b>Далее: {}</b>",
        "pause": "⏸",
        "play": "▶",
        "mute": "🔇",
        "unmute": "🔈",
        "next": "⏭",
        "stopped": "⏹ <b>Остановлено</b>",
        "stop": "⏹ ",
        "loop_b": "🔁",
        "loop_a": "🔄",
        "close": "🚫 Закрыть",
        "vol": "🔊 Громкость",
        "volup": "🔊 Громче",
        "voldown": "🔉 Тише",
        "playlist": "📚 Плейлист",
        "back": "🔙 Назад",
        "choose_delete": "♻️ <b>Выберите элемент очереди для удаления</b>",
        "play_err": "🚫 <b>Для начала добавьте песню.</b>"
    }

    strings_ua = {
        "name": "HikkaVoiceMod",
        "no_reply": "🚫 <b>Відповідайте на повідомлення</b>",
        "no_queue": "🚫 <b>Черга порожня</b>",
        "queue": "🎙 <b>Плейлист</b>:\n\n{}",
        "queueadd": "🎧 <b>{} додано до плейлиста</b>",
        "queueaddv": "📼 <b>{} додано до плейлиста</b>",
        "playnext_err": "📚 Порожній список відтворення. Додайте треки, щоб продовжити!",
        "downloading": "📥 <b>Завантаження...</b>",
        "playing": " <b>Грає {}</b>",
        "playing_with_next": " <b>Грає {}</b>\n➡️ <b>Далі: {}</b>",
        "pause": "⏸",
        "play": "▶",
        "mute": "🔇",
        "unmute": "🔈",
        "next": "⏭",
        "stopped": "⏹ <b>Зупинено</b>",
        "stop": "⏹ ",
        "loop_b": "🔁",
        "loop_a": "🔄",
        "close": "🚫 Закрити",
        "vol": "🔊 Гучність",
        "volup": "🔊 Гучніше",
        "voldown": "🔉 Тихіше",
        "playlist": "📚 Плейлист",
        "back": "🔙 Назад",
        "choose_delete": "♻️ <b>Оберіть елемент черги для видалення</b>",
        "play_err": "🚫 <b>Спочатку додайте пісню.</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "silent_queue",
                False,
                "Do not notify about track changes in chat",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "repeat",
                True,
                "Repeat the queue",
                validator=loader.validators.Boolean(),
            )
        )

        self._emoji_indices = {}
        self._calls = {}
        self._muted = {}
        self._forms = {}
        self._volume = {}
        self._queue = {}
        self._save_queue = {}

    async def client_ready(self, client, db):
        class HikkaTLClient(MtProtoClient):
            def __init__(
                    self,
                    cache_duration: int,
                    client: CustomTelegramClient,
            ):
                self._bind_client = None
                from hikkalls.mtproto.telethon_client import TelethonClient

                self._bind_client = TelethonClient(
                    cache_duration,
                    client,
                )

        class CustomPyTgCalls(HikkaLls):
            def __init__(
                    self,
                    app: CustomTelegramClient,
                    cache_duration: int = 120,
                    overload_quiet_mode: bool = False,
            ):
                Methods.__init__(self)
                Scaffold.__init__(self)
                ChangeVolumeCall.__init__(self)
                self._app = HikkaTLClient(
                    cache_duration,
                    app,
                )
                self._is_running = False
                self._env_checker = Environment(
                    self._REQUIRED_NODEJS_VERSION,
                    self._REQUIRED_PYROGRAM_VERSION,
                    self._REQUIRED_TELETHON_VERSION,
                    self._app.client,
                )
                self._call_holder = CallHolder()
                self._cache_user_peer = Cache()
                self._wait_result = UpdateSolver()
                self._on_event_update = HandlersHolder()
                self._change_volume_call = ChangeVolumeCall()
                self._binding = Binding(
                    overload_quiet_mode,
                )

                def cleanup():
                    if self._async_core is not None:
                        self._async_core.cancel()

                atexit.register(cleanup)

        self._app = CustomPyTgCalls(client)
        self._dir = tempfile.mkdtemp()
        await self._app.start()
        self._app._on_event_update.add_handler("STREAM_END_HANDLER", self.stream_ended)
        self.musicdl = await self.import_lib(
            "https://gitlab.com/frost_shard/libs/raw/main/musicdl.py",
            suspend_on_error=True,
        )

    async def stream_ended(self, client: HikkaLls, update: types.Update):
        chat_id = update.chat_id
        with contextlib.suppress(IndexError):
            if self.config["repeat"]:
                track = self._queue[chat_id][0]
                track["playing"] = False
                self._queue[chat_id].append(track)
            self._queue[chat_id].pop(0)

        if not self._queue.get(chat_id):
            with contextlib.suppress(Exception):
                await client.leave_group_call(chat_id)
            return

        self._queue[chat_id][0]["playing"] = True

        if self._queue[chat_id][0]["audio"]:
            await self.play(chat_id, self._queue[chat_id][0]["data"])
        else:
            if self._queue[chat_id][0]["youtube"]:
                await self.play_video_yt(chat_id, self._queue[chat_id][0]["data"])
            else:
                await self.play_video(chat_id, self._queue[chat_id][0]["data"])

    async def _play(
            self,
            chat_id: int,
            stream,
            stream_type,
            reattempt: bool = False,
    ):
        self._muted.setdefault(chat_id, False)
        try:
            await self._app.join_group_call(
                chat_id,
                stream,
                stream_type=stream_type,
            )
        except AlreadyJoinedError:
            await self._app.change_stream(chat_id, stream)
        except NoActiveGroupCall:
            if reattempt:
                raise

            await self._client(CreateGroupCallRequest(chat_id))
            await self._play(chat_id, stream, stream_type, True)

    async def _download_audio(self, name: str, message: Message) -> bytes:
        result = await self.musicdl.dl(name, only_document=True)
        try:
            return await self._client.download_file(result, bytes), self._get_fn(result)
        except Exception:
            return None, None

    def _get_fn(self, message: Message) -> str:
        filename = None
        with contextlib.suppress(Exception):
            attr = next(
                attr for attr in getattr(message, "document", message).attributes
            )
            filename = (
                    getattr(attr, "performer", "") + " - " + getattr(attr, "title", "")
            )

        if not filename:
            with contextlib.suppress(Exception):
                filename = next(
                    attr
                    for attr in getattr(message, "document", message).attributes
                    if isinstance(attr, DocumentAttributeFilename)
                ).file_name

        return filename

    async def play(self, chat_id: int, array: bytes):
        file = os.path.join(self._dir, f"{utils.rand(8)}.ogg")
        with open(file, "wb") as f:
            f.write(array)

        await self._play(
            chat_id,
            types.AudioPiped(
                file,
                types.HighQualityAudio()
            ),
            StreamType().pulse_stream,
        )
        await asyncio.sleep(1)
        if not self.config["silent_queue"]:
            msg, markup = await self._get_inline_info(chat_id)
            with contextlib.suppress(Exception):
                await self._forms[chat_id].delete()
            self._forms[chat_id] = await self.inline.form(
                chat_id, msg, reply_markup=markup
            )
             
    async def play_video(self, chat_id: int, array: bytes):
        file = os.path.join(self._dir, f"{utils.rand(8)}.mp4")
        with open(file, "wb") as f:
            f.write(array)

        await self._play(
            chat_id,
            types.AudioVideoPiped(
                file,
                types.HighQualityAudio(),
                types.HighQualityVideo(),
            ),
            StreamType().pulse_stream,
        )
        await asyncio.sleep(1)
        if not self.config["silent_queue"]:
            msg, markup = await self._get_inline_info(chat_id)
            try:
                if chat_id in self._forms:
                    await self._forms[chat_id].delete()
            except Exception as e:
                print(f"Ошибка при удалении предыдущего сообщения: {e}")
            self._forms[chat_id] = await utils.answer(message=chat_id, text=msg, reply_markup=markup)

    async def play_video_yt(self, chat_id: int, link: str):
        try:
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "-g",
                "-f",
                "b",
                link,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            await self._play(
                chat_id,
                types.AudioVideoPiped(
                    stdout.decode().split("\n")[0],
                    types.HighQualityAudio(),
                    types.HighQualityVideo(),
                ),
                StreamType().pulse_stream,
            )
            await asyncio.sleep(1)
            if not self.config["silent_queue"]:
                msg, markup = await self._get_inline_info(chat_id)
                try:
                    if chat_id in self._forms:
                        await self._forms[chat_id].delete()
                except Exception as e:
                    print(f"Ошибка при удалении предыдущего сообщения: {e}")
                self._forms[chat_id] = await utils.answer(message=chat_id, text=msg, reply_markup=markup)
        except TelegramServerError:
            await self.play_video_yt(chat_id, link)
        except Exception as e:
            await self.play_video_yt(chat_id, link)


    @loader.command(
        ru_doc="<ответ на песню или ее имя> - Добавить песню в очередь прослушивания чата",
        ua_doc="<відповідь на пісню або її ім'я> - Додати пісню до черги прослуховування чату"
    )
    async def addm(self, message: Message):
        """<reply to song or its name> - Add song to chat's voicechat queue"""
        reply = await message.get_reply_message()
        song = utils.get_args_raw(message)
        if (not reply or not reply.media) and not song:
            await utils.answer(message, self.strings("no_reply"))
            return

        message = await utils.answer(message, self.strings("downloading"))
        filename = None

        if not reply or not reply.media and song:
            song, filename = await self._download_audio(song, message)
            if not song:
                await utils.answer(message, self.strings("no_reply"))
                return

        if song:
            raw_data = song
        else:
            raw_data = await self._client.download_file(reply.document, bytes)
            filename = self._get_fn(reply)
        if not filename:
            filename = "Some cool song"
        filename = re.sub(r"\(.*?\)", "", filename)
        chat_id = utils.get_chat_id(message)
        self._queue.setdefault(chat_id, []).append(
            {"data": raw_data, "filename": filename, "playing": False, "audio": True}
        )
        if not any(i["playing"] for i in self._queue[chat_id]):
            self._queue[chat_id][-1]["playing"] = True
            await self.play(chat_id, raw_data)

        msg, markup = await self._get_inline_info(chat_id)
        try:
            if chat_id in self._forms:
                await self._forms[chat_id].delete()
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")
        combined_message = f"{msg}\n{self.strings('queueadd').format(filename)}"
        self._forms[chat_id] = await utils.answer(message, combined_message, reply_markup=markup)

    @loader.command(ru_doc="<ответить на видео или ссылку> - Добавить видео в очередь голосового чата",
                    ua_doc="<відповісти на відео або посилання> - додайте відео до черги голосового чату")
    async def addv(self, message: Message):
        """<reply to video or link> - Add video to chat's voicechat queue"""
        reply = await message.get_reply_message()
        link = utils.get_args_raw(message)
        if (not reply or not reply.media) and not link:
            await utils.answer(message, self.strings("no_reply"))
            return

        filename = None
        message = await utils.answer(message, self.strings("downloading"))
        if reply and reply.media:
            raw_data = await self._client.download_file(reply.document, bytes)

            filename = self._get_fn(reply)

        else:
            raw_data = link
            with contextlib.suppress(Exception):
                with YoutubeDL() as ydl:
                    filename = ydl.extract_info(link, download=False).get(
                        "title",
                        None,
                    )

        if not filename:
            filename = "Some cool video"

        filename = re.sub(r"\(.*?\)", "", filename)

        chat_id = utils.get_chat_id(message)

        self._queue.setdefault(chat_id, []).append(
            {
                "data": raw_data,
                "filename": filename,
                "playing": False,
                "audio": False,
                "youtube": not (reply and reply.media),
            }
        )

        try:
            if not any(i["playing"] for i in self._queue[chat_id]):
                self._queue[chat_id][-1]["playing"] = True
                if self._queue[chat_id][-1]["youtube"]:
                    await self.play_video_yt(chat_id, raw_data)
                else:
                    await self.play_video(chat_id, raw_data)
        except BadRequestError as e:
            if "TOPIC_CLOSED" in str(e):
                await utils.answer(message,
                                   f"Добавлено в очередь: {filename}\nЭто форум, используйте команды управления.")
            else:
                raise
        msg, markup = await self._get_inline_info(chat_id)
        try:
            if chat_id in self._forms:
                await self._forms[chat_id].delete()
        except Exception as e:
            print(f"Ошибка при удалении предыдущего сообщения: {e}")
        combined_message = f"{msg}\n{self.strings('queueadd').format(filename)}"
        self._forms[chat_id] = await utils.answer(message, combined_message, reply_markup=markup)

    @loader.command(ru_doc="Пропускает текущую композицию в очереди",
                    ua_doc="Пропускає поточну композицію в черзі")
    async def next(self, message: Message):
        """Skips current sound in queue"""
        chat_id = utils.get_chat_id(message)

        if len(self._queue.get(chat_id, [])) <= 1:
            await utils.answer(message, self.strings("no_queue"))
            return

        self._queue[chat_id].pop(0)
        self._queue[chat_id][0]["playing"] = True
        if self._queue[chat_id][0]["audio"]:
            await self.play(chat_id, self._queue[chat_id][0]["data"])
        else:
            if self._queue[chat_id][0]["youtube"]:
                await self.play_video_yt(chat_id, self._queue[chat_id][0]["data"])
            else:
                await self.play_video(chat_id, self._queue[chat_id][0]["data"])

        await message.delete()

    @loader.command(ru_doc="Получить текущую очередь чата", ua_doc="Отримати поточну чергу чату")
    async def list(self, message: Message):
        """Get current chat's queue"""
        chat_id = utils.get_chat_id(message)
        if not self._queue.get(chat_id):
            await utils.answer(message, self.strings("no_queue"))
            return

        await utils.answer(
            message,
            self.strings("queue").format(
                "\n".join(
                    [
                        ("🎧" if i["playing"] else "🕓")
                        + ("" if i["audio"] else "🎬")
                        + f" {i['filename']}"
                        for i in self._queue[chat_id]
                    ]
                )
            ),
        )

    @loader.command(ru_doc="Сохранить очередь",
                    ua_doc="Зберегти чергу")
    async def list_save(self, message):
        """Save the queue"""
        chat_id = utils.get_chat_id(message)
        if chat_id not in self._queue:
            await utils.answer(message, "No queue to save.")
            return

        data = self._queue[chat_id]
        self._save_queue[chat_id] = data.copy()
        await utils.answer(message, "Queue saved successfully!")

    @loader.command(ua_doc="Завантажте збережену чергу", ru_doc="Загрузить сохраненную очередь")
    async def list_load(self, message):
        """Load the saved queue"""
        chat_id = utils.get_chat_id(message)
        if chat_id not in self._save_queue:
            await utils.answer(message, "No saved queue to load.")
            return

        data = self._save_queue[chat_id]
        self._queue[chat_id] = data.copy()
        await utils.answer(message, "Queue loaded successfully!")

    @loader.command(ru_doc="Включите функцию «повторять эту очередь вечно»",
                    ua_doc="Перемкніть «повторювати цю чергу назавжди».")
    async def replay(self, message):
        """Switch the 'repeat this queue forever'"""
        self.config["repeat"] = not self.config["repeat"]
        await utils.answer(message, f"loop is now: {self.config['repeat']}")

    @loader.command(ru_doc="Удалить песню из очереди",
                    ua_doc="Видалити пісню з черги")
    async def rem(self, message: Message):
        """Remove song from queue"""
        chat_id = utils.get_chat_id(message)
        if not self._queue.get(chat_id):
            await utils.answer(message, self.strings("no_queue"))
            return

        await self.inline.form(
            message=message,
            text=self.strings("choose_delete"),
            reply_markup=utils.chunks(
                [
                    {
                        "text": ("🎧" if i["audio"] else "🎬") + " " + i["filename"],
                        "callback": self._inline__delete,
                        "args": (chat_id, index),
                    }
                    for index, i in enumerate(self._queue[chat_id])
                ],
                2
            ),
        )

    @loader.command(ru_doc="Повторно присоединитесь к звонку.",
                    ua_doc="Повторно приєднайтеся до дзвінка.")
    async def rst(self, message: Message):
        """Rejoin the call"""
        chat_id = utils.get_chat_id(message)
        is_playing = next((x for x in self._queue[chat_id] if x["playing"]), None)
        if not is_playing:
            return

        with contextlib.suppress(AlreadyJoinedError):
            await self._app.leave_group_call(chat_id)

        if self._queue[chat_id][0]["audio"]:
            await self.play(chat_id, self._queue[chat_id][-1]["data"])
        else:
            if self._queue[chat_id][-1]["youtube"]:
                await self.play_video_yt(chat_id, self._queue[chat_id][-1]["data"])
            else:
                await self.play_video(chat_id, self._queue[chat_id][-1]["data"])
        await message.delete()

    @loader.command(ru_doc="Возобновить очередь текущего чата",
                    ua_doc="Відновити поточну чергу чату")
    async def resume(self, message: Message):
        """Resume current chat's queue"""
        chat_id = utils.get_chat_id(message)
        with contextlib.suppress(Exception):
            await self._app.resume_stream(chat_id)
        try:
            msg, markup = await self._get_inline_info(chat_id)
            try:
                if chat_id in self._forms:
                    await self._forms[chat_id].delete()
            except Exception as e:
                print(f"Ошибка при удалении предыдущего сообщения: {e}")
            self._forms[chat_id] = await utils.answer(message=chat_id, text=msg, reply_markup=markup)
        except TypeError as e:
            await message.edit(self.strings("play_err"))

    @loader.command(ru_doc="Приостановить очередь текущего чата",
                    ua_doc="Призупинити поточну чергу чату")
    async def pause(self, message: Message):
        """Pause current chat's queue"""
        chat_id = utils.get_chat_id(message)
        with contextlib.suppress(Exception):
            await self._app.pause_stream(chat_id)
        try:
            msg, markup = await self._get_inline_info(chat_id)
            try:
                if chat_id in self._forms:
                    await self._forms[chat_id].delete()
            except Exception as e:
                print(f"Ошибка при удалении предыдущего сообщения: {e}")
            self._forms[chat_id] = await utils.answer(message=chat_id, text=msg, reply_markup=markup)
        except TypeError as e:
            await message.edit(self.strings("play_err"))

    @loader.command(ru_doc="Остановить очередь текущего чата",
                    ua_doc="Зупинити поточну чергу чату")
    async def stop(self, message: Message):
        """Stop current chat's queue"""
        await self._inline__stop(message, utils.get_chat_id(message))

    @loader.command(ru_doc="Показать панель управления",
                    ua_doc="Показати панель керування")
    async def panel(self, message: Message):
        """Show control panel"""
        chat_id = utils.get_chat_id(message)
        try:
            msg, markup = await self._get_inline_info(chat_id)
            try:
                if chat_id in self._forms:
                    await self._forms[chat_id].delete()
            except Exception as e:
                print(f"Ошибка при удалении предыдущего сообщения: {e}")
            self._forms[chat_id] = await utils.answer(message=chat_id, text=msg, reply_markup=markup)
        except TypeError as e:
            await message.edit(self.strings("play_err"))

    async def _get_inline_info(self, chat_id: int) -> tuple:
        if not self._queue.get(chat_id):
            return None, None

        emoji_index = self._emoji_indices.get(chat_id, 0)
        EMOJIS = ["🎵", "🎤", "🎶", "🎧", "🎼"]
        emoji = EMOJIS[emoji_index]

        self._emoji_indices[chat_id] = (emoji_index + 1) % len(EMOJIS)

        if len(self._queue[chat_id]) == 1:
            msg = emoji + self.strings("playing").format(
                utils.escape_html(self._queue[chat_id][0]["filename"]),
            )
        else:
            msg = emoji + self.strings("playing_with_next").format(
                utils.escape_html(self._queue[chat_id][0]["filename"]),
                utils.escape_html(self._queue[chat_id][1]["filename"]),
            )

        try:
            call = await self._app.get_call(chat_id)
            is_playing = call.status == "playing"
        except Exception:
            is_playing = True

        markup = [
            [
                {
                    "text": self.strings("loop_a") if self.config["repeat"] else self.strings("loop_b"),
                    "callback": self._inline__repeat_on if self.config["repeat"] else self._inline__repeat_off,
                    "args": (chat_id,),
                },
                {
                    "text": self.strings("stop"),
                    "callback": self._inline__stop,
                    "args": (chat_id,),
                },
                {
                    "text": self.strings("pause") if is_playing else self.strings("play"),
                    "callback": self._inline__pause if is_playing else self._inline__play,
                    "args": (chat_id,),
                },
                {
                    "text": self.strings("mute") if not self._muted.get(chat_id, False) else self.strings("unmute"),
                    "callback": self._inline__mute if not self._muted.get(chat_id, False) else self._inline__unmute,
                    "args": (chat_id,),
                },
                {
                    "text": self.strings("next"),
                    "callback": self._inline__next,
                    "args": (chat_id,),
                },
            ],
            [
                {
                    "text": self.strings("vol"),
                    "callback": self._inline__volume_menu,
                    "args": (chat_id,),
                },
                {
                    "text": self.strings("playlist"),
                    "callback": self._inline__playlist,
                    "args": (chat_id,),
                },
            ],
            [
                {
                    "text": self.strings("close"),
                    "callback": self._inline__close,
                    "args": (),
                },
            ],
        ]

        return msg, markup

    def _inline__back(self, chat_id: int):
        """Handles the callback query when the back button is pressed"""
        markup = [
            {
                "text": self.strings("back"),
                "callback": self._inline__back_button,
                "args": (chat_id,),
            }
        ]

        return markup

    async def _inline__repeat_on(self, call: InlineCall, chat_id: int):
        """Повторить"""
        self.config["repeat"] = not self.config["repeat"]
        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__repeat_off(self, call: InlineCall, chat_id: int):
        """Повторить"""
        self.config["repeat"] = not self.config["repeat"]
        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__volume_menu(self, call: InlineCall, chat_id: int):
        """Показать меню управления громкостью"""
        msg = f"Текущая громкость: {self._volume.get(chat_id, 100)}"
        buttons = [
            [{"text": self.strings("volup"), "callback": self._increase_volume, "args": (chat_id,)},
             {"text": self.strings("voldown"), "callback": self._decrease_volume, "args": (chat_id,)}],
            [{"text": self.strings("back"), "callback": self._inline__back_button, "args": (chat_id,)}]
        ]
        await call.edit(msg, reply_markup=buttons)

    async def _inline__volume(self, call: InlineCall, chat_id: int, volume: int):
        """Изменить громкость и обновить сообщение"""
        self._volume[chat_id] = volume
        await self._app.change_volume_call(chat_id, volume)
        await self._inline__volume_menu(call, chat_id)

    async def _increase_volume(self, call: InlineCall, chat_id: int):
        """Увеличить громкость"""
        current_volume = self._volume.get(chat_id, 100)
        new_volume = min(current_volume + 10, 200)
        await self._inline__volume(call, chat_id, new_volume)

    async def _decrease_volume(self, call: InlineCall, chat_id: int):
        """Уменьшить громкость"""
        current_volume = self._volume.get(chat_id, 100)
        new_volume = max(current_volume - 10, 10)
        await self._inline__volume(call, chat_id, new_volume)

    async def _inline__close(self, call: InlineCall):
        """Удалить сообщение"""
        await call.answer("OK")
        try:
            await call.delete()
        except Exception as e:
            print(f"Error deleting message: {e}")

    async def _inline__back_button(self, call: InlineCall, chat_id: int):
        """Кнопка возвращения в главное меню"""
        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__playlist(self, call: InlineCall, chat_id: int):
        """Показать текущий плейлист"""
        if not self._queue.get(chat_id):
            await call.edit(text=self.strings("no_queue"), reply_markup=None)
            return

        queue_str = "\n".join(
            [
                ("🎧" if i["playing"] else "🕓")
                + ("" if i["audio"] else "🎬")
                + f" {i['filename']}"
                for i in self._queue[chat_id]
            ]
        )

        msg = self.strings("queue").format(queue_str)
        markup = self._inline__back(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__delete(self, call: InlineCall, chat_id: int, index: int):
        """Удалить сообщение"""
        del self._queue[chat_id][index]
        await call.answer("OK")
        await call.delete()

    async def _inline__pause(self, call: InlineCall, chat_id: int):
        """Кнопка паузы"""
        try:
            await self._app.pause_stream(chat_id)
        except GroupCallNotFound:
            await call.edit(call, "Добавь песню в плейлист")

        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__play(self, call: InlineCall, chat_id: int):
        """Запустить, если на паузе"""
        await self._app.resume_stream(chat_id)
        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__mute(self, call: InlineCall, chat_id: int):
        await self._app.mute_stream(chat_id)
        self._muted[chat_id] = True
        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__unmute(self, call: InlineCall, chat_id: int):
        await self._app.unmute_stream(chat_id)
        self._muted[chat_id] = False
        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)

    async def _inline__stop(self, call: InlineCall, chat_id: int):
        with contextlib.suppress(KeyError):
            del self._queue[chat_id]

        with contextlib.suppress(KeyError):
            del self._forms[chat_id]

        with contextlib.suppress(KeyError):
            del self._muted[chat_id]

        try:
            await self._app.leave_group_call(chat_id)
            await utils.answer(call, self.strings("stopped"))
        except NotInGroupCallError:
            await utils.answer(call, "Бот не находится в голосовом чате.")

    async def _inline__next(self, call: InlineCall, chat_id: int):
        try:
            self._queue[chat_id].pop(0)
            self._queue[chat_id][0]["playing"] = True
        except IndexError:
            return utils.answer(self.strings("no_reply"))
        if self._queue[chat_id][0]["audio"]:
            await self.play(chat_id, self._queue[chat_id][0]["data"])
        else:
            if self._queue[chat_id][0]["youtube"]:
                await self.play_video_yt(chat_id, self._queue[chat_id][0]["data"])
            else:
                await self.play_video(chat_id, self._queue[chat_id][0]["data"])

        msg, markup = await self._get_inline_info(chat_id)
        await call.edit(msg, reply_markup=markup)
