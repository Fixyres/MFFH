# meta developer: @modwini
import datetime
from telethon import events, utils
from telethon.tl import types

from .. import loader, utils


@loader.tds
class MessageStatsMod(loader.Module):
    """Показывает статистику сообщений в текущем чате"""
    strings = {"name": "MessageStats"}

    def __init__(self):
        self.name = self.strings["name"]
        self._client = None
        self.today = datetime.datetime.now().date()
        self.week_ago = self.today - datetime.timedelta(days=7)
        self.month_ago = self.today.replace(day=1)
        self.all_time = None

    async def client_ready(self, client, db):
        self._client = client
        me = await self._client.get_me()
        async for dialog in self._client.iter_dialogs():
            if dialog.entity.id == me.id:
                self.all_time = (await self._client.get_messages(dialog, limit=1))[0].date.date()
                break

    async def statscmd(self, message: types.Message):
        """Показать статистику сообщений"""
        await utils.answer(message, f"<b>👺🔪Считаю сообщения...</b>")
        day_count = week_count = month_count = all_count = 0
        async for msg in self._client.iter_messages(message.to_id):
            if msg.date.date() == self.today:
                day_count += 1
            if self.week_ago <= msg.date.date() <= self.today:
                week_count += 1
            if self.month_ago <= msg.date.date() <= self.today:
                month_count += 1
            if msg.date.date() >= self.all_time:
                all_count += 1

        day_text = f"<b>За день:</b> <code>{day_count}</code>"
        week_text = f"<b>За неделю:</b> <code>{week_count}</code>"
        month_text = f"<b>За месяц:</b> <code>{month_count}</code>"
        all_text = f"<b>За все время:</b> <code>{all_count}</code>"

        await utils.answer(message, f"<b>👾Вот ваша статистика активности в этом чате:</b>\n{day_text}\n{week_text}\n{month_text}\n{all_text}")
