# meta developer: @xdesai

from .. import loader, utils
from telethon.tl.types import User, ChannelParticipantsBots, ChannelParticipantsAdmins


@loader.tds
class ChatMembersMod(loader.Module):
    strings = {
        "name": "ChatMembers",
        "bots_header": "<emoji document_id=5276127848644503161>🤖</emoji> <b>Bots in <code>{group_name}</code> ({count}):</b>\n\n",
        "users_header": "<emoji document_id=5275979556308674886>👤</emoji> <b>Users in <code>{group_name}</code> ({count}):</b>\n\n",
        "admins_header": "<emoji document_id=5276229330131772747>👑</emoji> <b>Admins in <code>{group_name}</code> ({count}):</b>\n\n",
        "list_temp": "<a href='tg://user?id={id}'>{full_name}</a>\n",
        "no_data": "<emoji document_id=5278578973595427038>🚫</emoji> <b>No data.</b>",
        "not_a_chat": "<emoji document_id=5276240711795107620>⚠️</emoji> <b>It works only in groups!</b>",
    }

    strings_ru = {
        "name": "ChatMembers",
        "bots_header": "<emoji document_id=5276127848644503161>🤖</emoji> <b>Ботов в <code>{group_name}</code> ({count})</b>:\n\n",
        "users_header": "<emoji document_id=5275979556308674886>👤</emoji> <b>Участников в <code>{group_name}</code> ({count}):</b>\n\n",
        "admins_header": "<emoji document_id=5276229330131772747>👑</emoji> <b>Админов в <code>{group_name}</code> ({count}):</b>\n\n",
        "list_temp": "<a href='tg://user?id={id}'>{full_name}</a>\n",
        "no_data": "<emoji document_id=5278578973595427038>🚫</emoji> <b>Данных нет.</b>",
        "not_a_chat": "<emoji document_id=5276240711795107620>⚠️</emoji> <b>Работает только в группах!</b>",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(ru_doc="Получить список ботов в группе")
    async def botscmd(self, m):
        """Get the list of bots in group"""
        return await self.printout(m, "bots")

    @loader.command(ru_doc="Получить список админов в чате")
    async def admins(self, m):
        """Get the list of admins in group"""
        return await self.printout(m, "admins")

    @loader.command(ru_doc="Получить список всех участников")
    async def users(self, m):
        """Get the list of all users in group"""
        return await self.printout(m, "users")

    async def printout(self, m, type):
        chat = await m.get_chat()

        if isinstance(chat, User):
            return await utils.answer(m, self.strings("not_a_chat"))

        if type == "bots":
            filter_type = ChannelParticipantsBots()
            header = self.strings("bots_header")
            emoji = "<emoji document_id=5314485570204869485>🟣</emoji>"
        elif type == "admins":
            filter_type = ChannelParticipantsAdmins()
            header = self.strings("admins_header")
            emoji = "<emoji document_id=5316712579467321913>🔴</emoji>"
        elif type == "users":
            filter_type = None
            header = self.strings("users_header")
            emoji = "<emoji document_id=5314378500965145730>🔵</emoji>"
        else:
            return await utils.answer(m, self.strings("no_data"))

        participants = await self.client.get_participants(chat, filter=filter_type)

        if not participants:
            return await utils.answer(m, self.strings("no_data"))

        output = header.format(group_name=chat.title, count=len(participants))
        for participant in participants:
            id = participant.id
            full_name = (
                f"{participant.first_name or ''} {participant.last_name or ''}".strip()
            )
            output += f"{emoji} {self.strings('list_temp').format(id=id, full_name=full_name)}"

        return await utils.answer(m, output)
