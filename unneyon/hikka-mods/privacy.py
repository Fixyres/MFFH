__version__ = (1, 0, 0)
#          █▄▀ ▄▀█ █▀▄▀█ █▀▀ █▄▀ █  █ █▀█ █▀█
#          █ █ █▀█ █ ▀ █ ██▄ █ █ ▀▄▄▀ █▀▄ █▄█ ▄
#                © Copyright 2025
#            ✈ https://t.me/kamekuro

# 🔒 Licensed under CC-BY-NC-ND 4.0 unless otherwise specified.
# 🌐 https://creativecommons.org/licenses/by-nc-nd/4.0
# + attribution
# + non-commercial
# + no-derivatives

# You CANNOT edit, distribute or redistribute this file without direct permission from the author.

# meta banner: https://raw.githubusercontent.com/kamekuro/hikka-mods/main/banners/privacy.png
# meta pic: https://raw.githubusercontent.com/kamekuro/hikka-mods/main/icons/privacy.png
# meta developer: @kamekuro_hmods
# scope: heroku_only
# scope: hikka_min 1.6.3

import logging
import re
import typing

import telethon
from telethon import types

from .. import loader, utils, inline


logger = logging.getLogger(__name__)


@loader.tds
class PrivacyMod(loader.Module):
    """Module for fastly changing privacy settings"""

    _privacy_types = {
        "phone": types.InputPrivacyKeyPhoneNumber,
        "add_by_phone": types.InputPrivacyKeyAddedByPhone,
        "online": types.InputPrivacyKeyStatusTimestamp,
        "photos": types.InputPrivacyKeyProfilePhoto,
        "forwards": types.InputPrivacyKeyForwards,
        "calls": types.InputPrivacyKeyPhoneCall,
        "p2p": types.InputPrivacyKeyPhoneP2P,
        "voices": types.InputPrivacyKeyVoiceMessages,
        # "messages": None,
        "birthdate": getattr(types, "InputPrivacyKeyBirthday", None),
        "gifts": getattr(types, "InputPrivacyKeyStarGiftsAutoSave", None),
        "bio": getattr(types, "InputPrivacyKeyAbout", None),
        "invites": types.InputPrivacyKeyChatInvite
    }
    _privacy_rules = {
        types.PrivacyValueAllowAll: types.InputPrivacyValueAllowAll,
        getattr(types, "PrivacyValueAllowBots", None): getattr(types, "InputPrivacyValueAllowBots", None),
        types.PrivacyValueAllowChatParticipants: types.InputPrivacyValueAllowChatParticipants,
        getattr(types, "PrivacyValueAllowCloseFriends", None): getattr(types, "InputPrivacyValueAllowCloseFriends", None),
        types.PrivacyValueAllowContacts: types.InputPrivacyValueAllowContacts,
        getattr(types, "PrivacyValueAllowPremium", None): getattr(types, "InputPrivacyValueAllowPremium", None),
        types.PrivacyValueAllowUsers: types.InputPrivacyValueAllowUsers,
        types.PrivacyValueDisallowAll: types.InputPrivacyValueDisallowAll,
        getattr(types, "PrivacyValueDisallowBots", None): getattr(types, "InputPrivacyValueDisallowBots", None),
        types.PrivacyValueDisallowChatParticipants: types.InputPrivacyValueDisallowChatParticipants,
        types.PrivacyValueDisallowContacts: types.InputPrivacyValueDisallowContacts,
        types.PrivacyValueDisallowUsers: types.InputPrivacyValueDisallowUsers
    }


    strings = {
        "name": "Privacy",
        "privacy_types": (
            "<emoji document_id=5974492756494519709>🔗</emoji> <b>Types of privacy settings:</b>\n"
        ),
        "no_user": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>You haven't specified user</b>",
        "u_silly": (
            "<emoji document_id=5449682572223194186>🥺</emoji> <b>You can't set privacy settings "
            "exceptions for yourself, silly.</b>"
        ),
        "choose_type": "🔑 <b>Select the type of settings to set exceptions</b>",
        "not_supported_type": (
            "<emoji document_id=5312383351217201533>⚠️</emoji> <b>It is not possible to set exceptions "
            "for the [{}] type of settings</b>"
        ),
        "allowed": (
            "<emoji document_id=5298609004551887592>💕</emoji> <b>{user} was added to the allowed "
            "users for the [{pr}] type of settings</b>"
        ),
        "disallowed": (
            "<emoji document_id=5224379368242965520>💔</emoji> <b>{user} was added to the disallowed "
            "users for the [{pr}] type of settings</b>"
        ),
        "privacy": {
            "phone": "Phone Number",
            "add_by_phone": "Who can find you by your number",
            "p2p": "Using Peer-to-Peer in calls",
            "online": "Last Seen & Online",
            "photos": "Profile Photos",
            "forwards": "Forwarded Messages",
            "calls": "Calls",
            "voices": "Voice Messages",
            # "messages": "Messages" if _privacy_types.get("messages") else None,
            "birthdate": "Date of Birth" if _privacy_types.get("birthdate") else None,
            "gifts": "Gifts" if _privacy_types.get("gifts") else None,
            "bio": "Bio" if _privacy_types.get("bio") else None,
            "invites": "Invites"
        }
    }

    strings_ru = {
        "_cls_doc": "Модуль для быстрого изменения настроек конфиденциальности",
        "privacy_types": (
            "<emoji document_id=5974492756494519709>🔗</emoji> <b>Типы настроек приватности:</b>\n"
        ),
        "no_user": "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Вы не указали пользователя</b>",
        "u_silly": (
            "<emoji document_id=5449682572223194186>🥺</emoji> <b>Ты не можешь выставить исключения "
            "настроек приватности для самого себя, глупенький</b>"
        ),
        "choose_type": "🔑 <b>Выберите тип настроек для выставления исключений</b>",
        "not_supported_type": (
            "<emoji document_id=5312383351217201533>⚠️</emoji> <b>Для типа настроек [{}] "
            "невозможно выставить исключения</b>"
        ),
        "allowed": (
            "<emoji document_id=5298609004551887592>💕</emoji> <b>{user} добавлен в разрешённых "
            "пользователей для настройки [{pr}]</b>"
        ),
        "disallowed": (
            "<emoji document_id=5224379368242965520>💔</emoji> <b>{user} добавлен в запрещённых "
            "пользователей для настройки [{pr}]</b>"
        ),
        "privacy": {
            "phone": "Номер телефона",
            "add_by_phone": "Кто может найти Вас по номеру",
            "p2p": "Использование peer-to-peer в звонках",
            "online": "Время захода",
            "photos": "Фотографии профиля",
            "forwards": "Пересылка сообщений",
            "calls": "Звонки",
            "voices": "Голосовые сообщения",
            # "messages": "Сообщения" if _privacy_types.get("messages") else None,
            "birthdate": "Дата рождения" if _privacy_types.get("birthdate") else None,
            "gifts": "Подарки" if _privacy_types.get("gifts") else None,
            "bio": "О себе" if _privacy_types.get("bio") else None,
            "invites": "Приглашения"
        }
    }


    async def client_ready(self, client, db):
        self._client: telethon.TelegramClient = client
        self._db = db


    @loader.command(
        ru_doc="👉 Список типов настроек для указания их в командах",
        alias="ptypes"
    )
    async def privacytypescmd(self, message: types.Message):
        """👉 List of setting types to pass it in commands"""

        out = self.strings("privacy_types")
        for key, item in self.strings("privacy").items():
            if not item: continue
            out += f"  <code>{key}</code> — {item}\n"
        await utils.answer(
            message, out
        )


    @loader.command(
        ru_doc="<пользователь> [настройка (необязательно)] 👉 Добавить пользователя в разрешённых для какой-либо настройки"
    )
    async def allowusercmd(self, message: types.Message):
        """<user> [setting (optional)] 👉 Add user to includes for some setting"""

        uid = await self.getID(message)
        if (not uid) or (uid < 0):
            return await utils.answer(message, self.strings("no_user"))
        elif uid == (await self._client.get_me()).id:
            return await utils.answer(message, self.strings("u_silly"))
        args = utils.get_args(message)[(0 if message.is_reply else 1):]
        new_allow_user: types.User = await self._client.get_entity(uid)

        if (len(args) < 1) or (not self._privacy_types.get(args[0])):
            return await self.inline.form(
                message=message,
                text=self.strings("choose_type"),
                reply_markup=self.gen_kb_action(new_allow_user, "allow")
            )

        pr = self.strings('privacy').get(args[0])
        if args[0] == "add_by_phone":
            return await utils.answer(
                message, self.strings("not_supported_type").format(pr)
            )
        key: types.TypeInputPrivacyKey = self._privacy_types.get(args[0])
        rules = (await self._client(telethon.functions.account.GetPrivacyRequest(
            key=key()
        ))).rules

        await self.allow_user(new_allow_user, key, rules, "allow")
        await utils.answer(
            message, self.strings("allowed").format(
                user=telethon.utils.get_display_name(new_allow_user), pr=pr
            )
        )


    @loader.command(
        ru_doc="<пользователь> [настройка (необязательно)] 👉 Добавить пользователя в запрещённых для какой-либо настройки"
    )
    async def disallowusercmd(self, message: types.Message):
        """<user> [setting (optional)] 👉 Add user to excludes for some setting"""

        uid = await self.getID(message)
        if (not uid) or (uid < 0):
            return await utils.answer(message, self.strings("no_user"))
        elif uid == (await self._client.get_me()).id:
            return await utils.answer(message, self.strings("u_silly"))
        args = utils.get_args(message)[(0 if message.is_reply else 1):]
        new_allow_user: types.User = await self._client.get_entity(uid)

        if (len(args) < 1) or (not self._privacy_types.get(args[0])):
            return await self.inline.form(
                message=message,
                text=self.strings("choose_type"),
                reply_markup=self.gen_kb_action(new_allow_user, "disallow")
            )

        pr = self.strings('privacy').get(args[0])
        if args[0] == "add_by_phone":
            return await utils.answer(
                message, self.strings("not_supported_type").format(pr)
            )
        key: types.TypeInputPrivacyKey = self._privacy_types.get(args[0])
        rules = (await self._client(telethon.functions.account.GetPrivacyRequest(
            key=key()
        ))).rules

        await self.allow_user(new_allow_user, key, rules, "disallow")
        await utils.answer(
            message, self.strings("disallowed").format(
                user=telethon.utils.get_display_name(new_allow_user), pr=pr
            )
        )


    async def allow_by_kb(
        self,
        call: inline.types.InlineCall,
        new_user: types.User,
        key: types.TypeInputPrivacyKey
    ):
        pr = "[Unknown]"
        for i in self._privacy_types.keys():
            if self._privacy_types[i] == key:
                pr = self.strings('privacy').get(i); break
        rules = (await self._client(telethon.functions.account.GetPrivacyRequest(
            key=key()
        ))).rules

        await self.allow_user(new_user, key, rules, "allow")
        await call.edit(
            text=self.strings("allowed").format(
                user=telethon.utils.get_display_name(new_user), pr=pr
            )
        )


    async def disallow_by_kb(
        self,
        call: inline.types.InlineCall,
        new_user: types.User,
        key: types.TypeInputPrivacyKey
    ):
        pr = "[Unknown]"
        for i in self._privacy_types.keys():
            if self._privacy_types[i] == key:
                pr = self.strings('privacy').get(i); break
        rules = (await self._client(telethon.functions.account.GetPrivacyRequest(
            key=key()
        ))).rules

        await self.allow_user(new_user, key, rules, "disallow")
        await call.edit(
            text=self.strings("disallowed").format(
                user=telethon.utils.get_display_name(new_user), pr=pr
            )
        )


    async def allow_user(
        self,
        new_allow_user: types.User,
        key: types.TypeInputPrivacyKey,
        rules: list,
        action: str = "allow" # allow/disallow
    ):
        new_rules = []
        f_all = [x for x in rules if type(x) in [types.PrivacyValueAllowAll, types.PrivacyValueDisallowAll]]
        f_all = f_all[0] if f_all else None
        allow_users, disallow_users = [], []
        allow_chats, disallow_chats = [], []
        if (action == "allow") and (type(f_all) != types.PrivacyValueAllowAll):
            allow_users.append(types.InputUser(new_allow_user.id, new_allow_user.access_hash))
        elif (action == "disallow") and (type(f_all) != types.PrivacyValueDisallowAll):
            disallow_users.append(types.InputUser(new_allow_user.id, new_allow_user.access_hash))
        need_to_set = True

        for rule in rules:
            rule_type = type(rule)
            if rule_type == types.PrivacyValueAllowUsers:
                for user in rule.users:
                    if (user == new_allow_user.id) and (action == "allow"):
                        need_to_set = False; break
                    if (user == new_allow_user.id) and (action == "disallow"):
                        continue
                    us: types.User = await self._client.get_entity(user)
                    allow_users.append(types.InputUser(us.id, us.access_hash))
            elif rule_type == types.PrivacyValueDisallowUsers:
                for user in rule.users:
                    if (user == new_allow_user.id) and (action == "disallow"):
                        need_to_set = False; break
                    if (user == new_allow_user.id) and (action == "allow"): continue
                    us: types.User = await self._client.get_entity(user)
                    disallow_users.append(types.InputUser(us.id, us.access_hash))
            elif rule_type == types.PrivacyValueAllowChatParticipants:
                for chat in rule.chats:
                    allow_chats.append(chat)
            elif rule_type == types.PrivacyValueDisallowChatParticipants:
                for chat in rule.chats:
                    disallow_chats.append(chat)
            else:
                new_rules.append(self._privacy_rules[rule_type]())

        if allow_users:
            new_rules.append(types.InputPrivacyValueAllowUsers(allow_users))
        if disallow_users:
            new_rules.append(types.InputPrivacyValueDisallowUsers(disallow_users))
        if allow_chats:
            new_rules.append(types.InputPrivacyValueAllowChatParticipants(allow_chats))
        if disallow_chats:
            new_rules.append(types.InputPrivacyValueDisallowChatParticipants(disallow_chats))

        if need_to_set:
            await self._client(telethon.functions.account.SetPrivacyRequest(
                key=key(), rules=new_rules
            ))


    def gen_kb_action(
        self,
        new_user: types.User,
        action: str # allow/disallow
    ):
        return self.split_list([
            {
                "text": self.strings("privacy").get(key),
                "callback": self.allow_by_kb if action == "allow" else self.disallow_by_kb,
                "args": (new_user, item)
            } for key, item in self._privacy_types.items() if item
        ], 2)


    async def getID(self, message: types.Message):
        reply: types.Message = await message.get_reply_message()
        if reply:
            return reply.sender_id

        args: list = utils.get_args(message)
        if not args: return None
        username = args[0] if args else ""

        match = re.search(r"(?:t\.me/|@|^(\w+)\.t\.me$)([a-zA-Z0-9_\.]+)", username)
        if match:
            username = match.group(1) or match.group(2)

        try:
            response = await self._client(telethon.functions.contacts.ResolveUsernameRequest(username))
        except telethon.errors.rpcbaseerrors.RPCError:
            response = None

        try:
            user_entity = await self._client.get_entity(username)
        except Exception:
            user_entity = None

        if response and response.users:
            return response.users[0].id
        if user_entity:
            return getattr(user_entity, "user_id", None)

        return None
    
    def split_list(self, input_list: typing.List, chunk_size: int):
        return [input_list[i:i+chunk_size] for i in range(0, len(input_list), chunk_size)]