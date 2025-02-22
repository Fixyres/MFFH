# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM          
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd 
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `" 
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.  
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8 
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/emoji/344/mechanical-arm.png
# meta developer: @mm_mods

__version__ = "1.0.3"

from .. import loader, utils
from telethon.tl.types import Message, PeerChannel, ChannelParticipantsAdmins
import logging

logger = logging.getLogger(__name__)


@loader.tds
class RechteMod(loader.Module):
    """Group rights viewer and manager."""

    strings = {
        "name": "Rechte",
        "group?!": "👥 <b>This command must be used in group.</b>",
        "rightslist": "📜 <b>Group members rights:</b>",
        "on": "👤 <b>Now only admins can {}.</b>",
        "off": "🤖 <b>Now all members can {}.</b>",
        "status-on": "👤❕ <b>Only admins can {} here.</b>",
        "status-off": "🤖❕ <b>All members can {} here.</b>",
        "rights?!": "😔 <b>Error….</b>\nCode: <code>{}</code>",
        "adminslist": "👥 <b>Group admins:</b>",
        "loading": "🔄 <b>Loading….</b>",
        'send-right': 'send messages',
        'ib-right': 'use inline bots',
        'media-right': 'send media',
        'stickers-right': 'send stickers',
        'gifs-right': 'send GIFs',
        'games-right': 'send games',
        'embed-right': 'send links preview',
        'polls-right': 'send polls',
        'info-right': 'change chat info',
        'invite-right': 'invite users',
        'pin-right': 'pin messages',
        'addadmin-right': 'add admins',
        'anonymous-right': 'send anonymous messages',
        'ban-right': 'ban users',
        'delete-right': 'delete messages',
        'edit-right': 'edit messages',
        'call-management-right': 'manage voice chats',
        'is-banned': '🚫 <b>User is banned.</b>',
        'is-left': '🚫 <b>User left the chat.</b>',
        'is-admin': '👤 <b>User is admin.</b>',
        'is-creator': '👤 <b>User is creator.</b>',
        'default': '⭕ <b>User have default permissions.</b>',
    }

    strings_ru = {
        "name": "Rechte",
        "group?!": "👥 <b>Работает лишь в группах.</b>",
        "rightslist": "📜 <b>Права участников группы:</b>",
        "on": "👤 <b>Теперь лишь админы могут {}.</b>",
        "off": "🤖 <b>Теперь все могут {}.</b>",
        "status-on": "👤❕ <b>Здесь лишь админы могут {}.</b>",
        "status-off": "🤖❕ <b>Здесь все могут {}.</b>",
        "rights?!": "😔 <b>Ошибка…</b>\nКод: <code>{}</code>",
        "adminslist": "👥 <b>Админы группы:</b>",
        "loading": "🔄 <b>Загрузка…</b>",
        'send-right': 'отправлять сообщения',
        "_cls_doc": "Переключает и проверяет права.",
        "_cmd_doc_switchsend": "Переключает права на отправку сообщений",
        "_cmd_doc_checksend": "Проверяет права на отправку сообщений",
        "_cmd_doc_checkib": "Проверяет права на использование инлайн-ботов.",
        "_cmd_doc_switchib": "Переключает права на использование инлайн-ботов",
        "_cmd_doc_switchmedia": "Переключает права на отправку медиа",
        "_cmd_doc_checkmedia": "Проверяет права на отправку медиа",
        "_cmd_doc_switchstickers": "Переключает права на отправку стикеров",
        "_cmd_doc_checkstickers": "Проверяет права на отправку стикеров",
        "_cmd_doc_switchgifs": "Переключает права на отправку GIF",
        "_cmd_doc_checkgifs": "Проверяет права на отправку GIF",
        "_cmd_doc_switchgames": "Переключает права на отправку игр",
        "_cmd_doc_checkgames": "Проверяет права на отправку игр",
        "_cmd_doc_switchembed": "Переключает права на отправку предпросмотра ссылок",
        "_cmd_doc_checkembed": "Проверяет права на отправку предпросмотра ссылок",
        "_cmd_doc_switchpolls": "Переключает права на отправку опросов",
        "_cmd_doc_checkpolls": "Проверяет права на отправку опросов",
        "_cmd_doc_switchinfo": "Переключает права на изменение информации чата",
        "_cmd_doc_checkinfo": "Проверяет права на изменение информации чата",
        "_cmd_doc_switchinvite": "Переключает права на приглашение пользователей",
        "_cmd_doc_checkinvite": "Проверяет права на приглашение пользователей",
        "_cmd_doc_switchpin": "Переключает права на закрепление сообщений",
        "_cmd_doc_checkpin": "Проверяет права на закрепление сообщений",
        "_cmd_doc_checkall": "Выдаёт список прав обычных учаcтников",
        "_cmd_doc_checkadmins": "Выдаёт список админов",
        'ib-right': 'использовать инлайн-ботов',
        'media-right': 'отправлять медиа',
        'stickers-right': 'отправлять стикеры',
        'gifs-right': 'отправлять GIF',
        'games-right': 'отправлять игры',
        'embed-right': 'отправлять предпросмотр ссылок',
        'polls-right': 'отправлять опросы',
        'info-right': 'менять информацию о чате',
        'invite-right': 'приглашать пользователей',
        'pin-right': 'закреплять сообщения',
        'addadmin-right': 'добавлять администраторов',
        'anonymous-right': 'отправлять анонимные сообщения',
        'ban-right': 'банить пользователей',
        'delete-right': 'удалять сообщения',
        'edit-right': 'редактировать сообщения',
        'call-management-right': 'управлять звонками',
        'is-banned': '🚫 <b>Пользователь забанен.</b>',
        'is-left': '🚫 <b>Пользователь покинул чат.</b>',
        'is-admin': '👤 <b>Пользователь — администратор.</b>',
        'is-creator': '👤 <b>Пользователь — создатель.</b>',
        'default': '⭕ <b>У пользователя стандартные права.</b>',
    }

    strings_de = {
        "name": "Rechte",
        "group?!": "👥 <b>Funktioniert nur in Gruppen.</b>",
        "rightslist": "📜 <b>Gruppenmitgliedern Rechteliste:</b>",
        "on": "👤 <b>Nun können nur Admins {}.</b>",
        "off": "🤖 <b>Nun können alle {}.</b>",
        "status-on": "👤❕ <b>Hier können nur Admins {}.</b>",
        "status-off": "🤖❕ <b>Hier können alle {}.</b>",
        "rights?!": "😔 <b>Fehler…</b>\nCode: <code>{}</code>",
        "adminslist": "👥 <b>Adminsliste:</b>",
        "loading": "🔄 <b>Wird geladen…</b>",
        "_cls_doc": "Schaltet und überprüft Rechte.",
        "_cmd_doc_switchsend": "Schaltet das Senden von Nachrichten",
        "_cmd_doc_checksend": "Überprüft das Senden von Nachrichten",
        "_cmd_doc_switchib": "Schaltet Rechte für Inline-Bots um",
        "_cmd_doc_checkib": "Überprüft Rechte für Inline-Bots",
        "_cmd_doc_switchmedia": "Schaltet Rechte für Medien um",
        "_cmd_doc_checkmedia": "Überprüft Rechte für Medien",
        "_cmd_doc_switchstickers": "Schaltet Rechte für Sticker um",
        "_cmd_doc_checkstickers": "Überprüft Rechte für Sticker",
        "_cmd_doc_switchgif": "Schaltet Rechte für GIF um",
        "_cmd_doc_checkgif": "Überprüft Rechte für GIF",
        "_cmd_doc_switchgames": "Schaltet Rechte für Spiele um",
        "_cmd_doc_checkgames": "Überprüft Rechte für Spiele",
        "_cmd_doc_switchembed": "Schaltet Rechte für Vorschau von Links um",
        "_cmd_doc_checkembed": "Überprüft Rechte für Vorschau von Links",
        "_cmd_doc_switchpolls": "Schaltet Rechte für Umfragen um",
        "_cmd_doc_checkpolls": "Überprüft Rechte für Umfragen",
        "_cmd_doc_switchinfo": "Schaltet Rechte für Info-Änderungen um",
        "_cmd_doc_checkinfo": "Überprüft Rechte für Info-Änderungen",
        "_cmd_doc_switchinvite": "Schaltet Rechte für Einladungen um",
        "_cmd_doc_checkinvite": "Überprüft Rechte für Einladungen",
        "_cmd_doc_switchpin": "Schaltet Rechte für das Anheften von Nachrichten um",
        "_cmd_doc_checkpin": "Überprüft Rechte für das Anheften von Nachrichten",
        "_cmd_doc_checkall": "Sendet eine List von alle Rechte des Benutzers",
        "_cmd_doc_checkadmins": "Sendet eine Liste von allen Admins",
        'ib-right': 'Inline-Bots verwenden',
        'media-right': 'Medien senden',
        'stickers-right': 'Sticker senden',
        'gifs-right': 'GIF senden',
        'games-right': 'Spiele senden',
        'embed-right': 'Vorschau von Links senden',
        'polls-right': 'Umfragen senden',
        'info-right': 'Gruppeninformationen ändern',
        'invite-right': 'Benutzer einladen',
        'pin-right': 'Nachrichten anheften',
        'addadmin-right': 'Admins hinzufügen',
        'anonymous-right': 'Anonyme Nachrichten senden',
        'ban-right': 'Benutzer bannen',
        'delete-right': 'Nachrichten löschen',
        'edit-right': 'Nachrichten bearbeiten',
        'call-management-right': 'Anrufe verwalten',
        'is-banned': '🚫 <b>Benutzer ist gebannt.</b>',
        'is-left': '🚫 <b>Benutzer hat den Chat verlassen.</b>',
        'is-admin': '👤 <b>Benutzer ist ein Admin.</b>',
        'is-creator': '👤 <b>Benutzer ist der Inhaber.</b>',
        'default': '⭕ <b>Benutzer hat Standardrechte.</b>',
    }

    async def switchibcmd(self, m: Message):
        """Switches inline bots using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_inline:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_inline=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('ib-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_inline=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('ib-right')))

    async def checkibcmd(self, m: Message):
        """Checks inline bots using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_inline:
            return await utils.answer(m, self.strings('status-off').format(self.strings('ib-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('ib-right')))

    async def switchsendcmd(self, m: Message):
        """Switches sending messages rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_messages:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_messages=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('send-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_messages=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('send-right')))

    async def checksendcmd(self, m: Message):
        """Checks sending messages rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_messages:
            return await utils.answer(m, self.strings('status-off').format(self.strings('send-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('send-right')))

    async def switchmediacmd(self, m: Message):
        """Switches media using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_media:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_media=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on'))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_media=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off'))

    async def checkmediacmd(self, m: Message):
        """Checks media using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_media:
            return await utils.answer(m, self.strings('status-off').format(self.strings('media-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('media-right')))

    async def switchstickerscmd(self, m: Message):
        """Switches stickers using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_stickers:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_stickers=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('stickers-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_stickers=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('stickers-right')))

    async def checkstickerscmd(self, m: Message):
        """Checks stickers using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_stickers:
            return await utils.answer(m, self.strings('status-off').format(self.strings('stickers-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('stickers-right')))

    async def switchgifscmd(self, m: Message):
        """Switches gifs using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_gifs:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_gifs=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('gifs-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_gifs=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('gifs-right')))

    async def checkgifscmd(self, m: Message):
        """Checks gifs using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_gifs:
            return await utils.answer(m, self.strings('status-off').format(self.strings('gifs-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('gifs-right')))

    async def switchgamescmd(self, m: Message):
        """Switches games using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_games:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_games=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('games-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_games=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('games-right')))

    async def checkgamescmd(self, m: Message):
        """Checks games using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_games:
            return await utils.answer(m, self.strings('status-off').format(self.strings('games-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('games-right')))

    async def switchembedcmd(self, m: Message):
        """Switches links preview using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).embed_links:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), embed_links=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('embed-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), embed_links=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('embed-right')))

    async def checkembedcmd(self, m: Message):
        """Checks links preview using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).embed_links:
            return await utils.answer(m, self.strings('status-off').format(self.strings('embed-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('embed-right')))

    async def switchpollscmd(self, m: Message):
        """Switches polls using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_polls:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_polls=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('polls-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), send_polls=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('polls-right')))

    async def checkpollscmd(self, m: Message):
        """Checks polls using rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).send_polls:
            return await utils.answer(m, self.strings('status-off').format(self.strings('polls-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('polls-right')))

    async def switchinfocmd(self, m: Message):
        """Switches info changing rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).change_info:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), change_info=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('info-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), check_info=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('info-right')))

    async def checkinfocmd(self, m: Message):
        """Checks info changing rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).change_info:
            return await utils.answer(m, self.strings('status-off').format(self.strings('info-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('info-right')))

    async def switchinvitecmd(self, m: Message):
        """Switches invite rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).invite_users:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), invite_users=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('invite-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), invite_users=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('invite-right')))

    async def checkinvitecmd(self, m: Message):
        """Checks invite rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).invite_users:
            return await utils.answer(m, self.strings('status-off').format(self.strings('invite-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('invite-right')))

    async def switchpincmd(self, m: Message):
        """Switches pin message rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).pin_messages:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), pin_messages=False)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('on').format(self.strings('pin-right')))

        else:
            try:
                await m.client.edit_permissions(utils.get_chat_id(m), pin_messages=True)
            except Exception as e:
                return await utils.answer(m, self.strings('rights?!').format(e))
            return await utils.answer(m, self.strings('off').format(self.strings('pin-right')))

    async def checkpincmd(self, m: Message):
        """Checks pin message rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))

        if not (await m.client.get_permissions(utils.get_chat_id(m))).pin_messages:
            return await utils.answer(m, self.strings('status-off').format(self.strings('pin-right')))

        else:
            return await utils.answer(m, self.strings('status-on').format(self.strings('pin-right')))

    async def checkallcmd(self, m: Message):
        """Shows all rights."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))
        await utils.answer(m, self.strings('loading'))
        listr = f"{self.strings('rightslist')}\n\n"
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_messages != True:
            listr += '<i>' + self.strings('send-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('send-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_media != True:
            listr += '<i>' + self.strings('media-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('media-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_stickers != True:
            listr += '<i>' + self.strings('stickers-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('stickers-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_gifs != True:
            listr += '<i>' + self.strings('gifs-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('gifs-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_games != True:
            listr += '<i>' + self.strings('games-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('games-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_inline != True:
            listr += '<i>' + self.strings('ib-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('ib-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).embed_links != True:
            listr += '<i>' + self.strings('embed-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('embed-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).send_polls != True:
            listr += '<i>' + self.strings('polls-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('polls-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).change_info != True:
            listr += '<i>' + self.strings('info-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('info-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).invite_users != True:
            listr += '<i>' + self.strings('invite-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('invite-right').capitalize() + '</i>: ❌\n'
        if (await m.client.get_permissions(utils.get_chat_id(m))).pin_messages != True:
            listr += '<i>' + self.strings('pin-right').capitalize() + '</i>: ✅\n'
        else:
            listr += '<i>' + self.strings('pin-right').capitalize() + '</i>: ❌\n'
        return await utils.answer(m, listr)

    async def checkadminscmd(self, m: Message):
        """Shows admins."""
        if not isinstance(m.peer_id, PeerChannel):
            return await utils.answer(m, self.strings('group?!'))
        await utils.answer(m, self.strings('loading'))
        listr = f"{self.strings('adminslist')}\n"
        async for user in m.client.iter_participants(utils.get_chat_id(m), filter=ChannelParticipantsAdmins):
            listr += f"\n<b>{user.first_name} {user.last_name if user.last_name is not None else ''} ({user.id})</b>\n"
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).is_creator == True:
                listr += self.strings('is-creator') + '\n'
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).add_admins == True:
                listr += '<i>' + self.strings('addadmin-right').capitalize() + '</i>: ✅\n'
            else:
                listr += '<i>' + self.strings('addadmin-right').capitalize() + '</i>: ❌\n'
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).ban_users == True:
                listr += '<i>' + self.strings('ban-right').capitalize() + '</i>: ✅\n'
            else:
                listr += '<i>' + self.strings('ban-right').capitalize() + '</i>: ❌\n'
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).delete_messages == True:
                listr += '<i>' + self.strings('delete-right').capitalize() + '</i>: ✅\n'
            else:
                listr += '<i>' + self.strings('delete-right').capitalize() + '</i>: ❌\n'
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).anonymous == True:
                listr += '<i>' + self.strings('anonymous-right').capitalize() + '</i>: ✅\n'
            else:
                listr += '<i>' + self.strings('anonymous-right').capitalize() + '</i>: ❌\n'
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).manage_call == True:
                listr += '<i>' + self.strings('call-management-right').capitalize() + '</i>: ✅\n'
            else:
                listr += '<i>' + self.strings('call-management-right').capitalize() + '</i>: ❌\n'
            if (await m.client.get_permissions(utils.get_chat_id(m), user.id)).pin_messages == True:
                listr += '<i>' + self.strings('pin-right').capitalize() + '</i>: ✅\n'
            else:
                listr += '<i>' + self.strings('pin-right').capitalize() + '</i>: ❌\n'
        return await utils.answer(m, listr)
