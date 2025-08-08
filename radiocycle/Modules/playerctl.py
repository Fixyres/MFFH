# meta developer: bio.kezuhiro.fun

from .. import loader, utils
import asyncio
import os
import requests

@loader.tds
class PlayerCTLMod(loader.Module):
    """Управление музыкой через playerctl. Только для Linux."""
    strings_ru = {
        "name": "PlayerCTL",
        "no_player": "<b>Нет доступного плеера</b>",
        "now_playing": (
            "<b>Сейчас играет:</b>\n"
            "<b>Название:</b> {title}\n"
            "<b>Исполнитель:</b> {artist}\n"
            "<b>Альбом:</b> {album}\n"
            "<b>Ссылка на трек:</b> {link}"
        ),
    }

    async def _run_(self, cmd):
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode().strip(), stderr.decode().strip()

    @loader.command(ru_doc="- Переключить воспроизведение")
    async def mtoggle(self, message):
        await self._run_("playerctl play-pause")
        await utils.answer(message, "<b>Воспроизведение переключено.</b>")

    @loader.command(ru_doc="- Следующий трек")
    async def mnext(self, message):
        await self._run_("playerctl next")
        await utils.answer(message, "<b>Переключен на следующий трек.</b>")

    @loader.command(ru_doc="- Предыдущий трек")
    async def mprev(self, message):
        await self._run_("playerctl previous")
        await utils.answer(message, "<b>Переключен на предыдущий трек.</b>")

    @loader.command(ru_doc="- Показать текущий трек и позицию")
    async def mnow(self, message):

        if not await self._run_("command -v playerctl"):
            await utils.answer(message, self.strings("no_player", message))
            return

        metadata, err = await self._run_("playerctl metadata --format '{{title}}␟{{artist}}␟{{album}}␟{{xesam:url}}'")
        parts = metadata.split("␟")

        if err or not metadata:
            await utils.answer(message, self.strings("no_player", message))
            return

        title, artist, album, url = parts

        link = "<a href='{}'>тык</a>".format(url)

        text = self.strings("now_playing", message).format(
            title=title or "Нет данных",
            artist=artist or "Нет данных",
            album=album or "Нет данных",
            link=link or "Нет ссылки"
        )

        await utils.answer(message, text)
