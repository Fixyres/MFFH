# @Sekai_Yoneya

from asyncio import sleep
import random
from telethon import functions
from userbot.events import register
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon import events
from .. import loader, utils

def register(cb):
    cb(SpamBotMod())

class SpamBotMod(loader.Module):
    """Показывает ваши ограничения."""
    strings = {'name': 'SpamBot'}

    def init(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    async def spambotcmd(self, event):
        """Смотреть статус ограничений."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, '/start')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)

    async def thankbotcmd(self, event):
        """Написать 'хорошо, спасибо', когда есть инлайн."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, 'Хорошо, спасибо')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)

    async def okbotcmd(self, event):
        """Написать 'Ок', когда есть инлайн."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, 'ОК')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)

    async def whatbotcmd(self, event):
        """Спросить, почему на Вас могли жаловаться, когда есть инлайн."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, 'Почему на меня могли жаловаться?')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)

    async def plsbotcmd(self, event):
        """Попросить снять Вам ограничения, когда есть инлайн."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, 'Признаю свою вину, снимите ограничения')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)
            
    async def ponspsbotcmd(self, event):
        """Написать 'Понятно, спасибо', когда есть инлайн."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, 'Понятно, спасибо')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)
            
    async def infobotcmd(self, event):
        """Узнать больше о спаме, когда есть инлайн."""
        chat = '@spambot'
        async with event.client.conversation(chat) as conv:
            try:
                response = conv.wait_event(events.NewMessage(incoming=True, from_users= 178220800 ))
                await event.client.send_message(chat, 'Хочу узнать больше')
                response = await response
            except YouBlockedUserError:
                await event.edit('<code>Разблокируй @spambot</code>')
                return
            await event.edit(response.text)
