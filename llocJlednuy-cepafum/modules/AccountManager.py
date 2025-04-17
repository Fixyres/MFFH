__version__ = (2, 3, 3)

# -------------------------------------------------------------------------------- 
#                                                                                  
# Name: AccountManager                                                             
# Description: нᴀстᴘойкᴀ конфидᴇнциᴀльности в ᴛᴇʟᴇɢʀᴀᴍ                          
# meta developer: @ManulMods                                             
# authors: @ManulMods
# version: 2.3.3                                                                                 
#
# █▀▀ █▀▀ █▀█ ▄▀▄ █▀▀ █ █ █▄ ▄█
# █▄▄ ██▄ █▀▀ █▀█ █▀  █▄█ █ ▀ █
#
# ▀▄▀ █▄ ▄█ █▄ ▄█ █▀█ █▀▄ █ █ █   █▀▀ █▀▀ 
#  █  █ ▀ █ █ ▀ █ █▄█ █▄▀ █▄█ █▄▄ ██▄ ▄██ 
#
# -------------------------------------------------------------------------------- 

from telethon import functions, types
from .. import loader, utils

@loader.tds
class AccountManager(loader.Module):
    """нᴀстᴘойкᴀ конфидᴇнциᴀльности в ᴛᴇʟᴇɢʀᴀᴍ"""

    strings = {
        "name": "AccountManager",
        "description": "нᴀстᴘойкᴀ конфидᴇнциᴀльности в ᴛᴇʟᴇɢʀᴀᴍ",
        "authors": "@ManulMods",
        "versions": "2.3.3",
        "error": "<emoji document_id=5237814653010076467>🗓</emoji> нᴇ ʏдᴀлось совᴇᴘшить кᴀкиᴇ-лиҕо вᴀши дᴇйствия...",
        "bio_success": "<emoji document_id=5229132514060167056>🗓</emoji> <b>ҕио ʏспᴇшно оҕновлᴇно!</b>\n<b><emoji document_id=5237814653010076467>🗓</emoji> новоᴇ ҕио:</b> <code>{}</code>",
        "name_success": "<emoji document_id=5233429444156223307>🗓</emoji> <b>имя ʏспᴇшно измᴇнᴇно!</b>\n<b><emoji document_id=5237814653010076467>🗓</emoji> новоᴇ имя:</b> <code>{}</code>",
        "user_success": "<emoji document_id=5235875883297824772>🗓</emoji> <b>юзᴇᴘнᴇйм измᴇнᴇн!</b>\n<b><emoji document_id=5237814653010076467>🗓</emoji> новый юзᴇᴘнᴇйм:</b> @{}",
        "user_removed": "<emoji document_id=5235875883297824772>🗓</emoji> <b>юзᴇᴘнᴇйм ʏдᴀлᴇн!</b>",
        "user_taken": "<emoji document_id=5237814653010076467>🗓</emoji> <b>юзᴇᴘнᴇйм @{} ʏжᴇ зᴀнят!</b>",
        "avatar_success": "<emoji document_id=5228764435362900200>🗓</emoji> <b>вᴀшᴀ ᴀвᴀтᴀᴘкᴀ оҕновлᴇнᴀ!</b>",
        "avatar_error": "<emoji document_id=5237814653010076467>🗓</emoji> <b>отвᴇтьтᴇ нᴀ фото сооҕщᴇниᴇ!</b>",
        "privacy_settings": "<emoji document_id=5237814653010076467>🗓</emoji> <b>нᴀстᴘойки конфидᴇнциᴀльности:</b>\n\n{}",
        "arg_missing": "<emoji document_id=5237814653010076467>🗓</emoji> <b>ʏкᴀжитᴇ ᴀᴘгʏмᴇнт!</b>",
        "check_true": "<emoji document_id=5229132514060167056>🗓</emoji> <b>юзᴇᴘнᴇйм:</b> @{} <b>(достʏпᴇн!)</b>",
        "check_false": "<emoji document_id=5235875883297824772>🗓</emoji> <b>юзᴇᴘнᴇйм:</b> @{} <b>(нᴇ достʏпᴇн!)</b>",
        "check_false_args": "<emoji document_id=5237814653010076467>🗓</emoji> <b>пожᴀлʏйстᴀ впишитᴇ юзᴇᴘнᴇйм котоᴘый вы хотитᴇ пᴘовᴇᴘить...</b>",
        "privacy_everybody": "<emoji document_id=5235875883297824772>🗓</emoji> Все",
        "privacy_contacts": "<emoji document_id=5233429444156223307>🗓</emoji> Контакты",
        "privacy_nobody": "<emoji document_id=5237814653010076467>🗓</emoji> Никто"
    }

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.command()
    async def setbio(self, message):
        """<описание> - измᴇнить ҕио"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["arg_missing"])
            return

        try:
            await self._client(functions.account.UpdateProfileRequest(about=args))
            await utils.answer(message, self.strings["bio_success"].format(args))
        except Exception:
            await utils.answer(message, self.strings["error"])

    @loader.command()
    async def setname(self, message):
        """<имя> - измᴇнить имя"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["arg_missing"])
            return

        try:
            await self._client(functions.account.UpdateProfileRequest(first_name=args))
            await utils.answer(message, self.strings["name_success"].format(args))
        except Exception:
            await utils.answer(message, self.strings["error"])

    @loader.command()
    async def setuser(self, message):
        """<юзернейм> - измᴇнить юзᴇᴘнᴇйм (остᴀвьтᴇ пʏстым для ʏдᴀлᴇния)"""
        args = utils.get_args_raw(message)

        try:
            await self._client(functions.account.UpdateUsernameRequest(username=args or ""))
            if args:
                await utils.answer(message, self.strings["user_success"].format(args))
            else:
                await utils.answer(message, self.strings["user_removed"])
        except Exception as e:
            if "USERNAME_OCCUPIED" in str(e):
                await utils.answer(message, self.strings["user_taken"].format(args))
            else:
                await utils.answer(message, self.strings["error"])

    @loader.command()
    async def setavatar(self, message):
        """<реплай на фото> - ʏстᴀновить новый ᴀвᴀтᴀᴘ"""
        reply = await message.get_reply_message()
        if not reply or not reply.photo:
            await utils.answer(message, self.strings["avatar_error"])
            return

        try:
            file = await reply.download_media(bytes)
            await self._client(functions.photos.UploadProfilePhotoRequest(
                file=await self._client.upload_file(file)))
            await utils.answer(message, self.strings["avatar_success"])
        except Exception:
            await utils.answer(message, self.strings["error"])

    @loader.command()
    async def checkuser(self, message):
        """<юзернейм> - пᴘовᴇᴘяᴇт достʏпность юзᴇᴘнᴇймᴀ"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["check_false_args"])
            return
        
        username = args.strip()

        result = await self.check_username(self._client, username)

        if result:
            await utils.answer(message, self.strings["check_false"].format(username))
        else:
            await utils.answer(message, self.strings["check_true"].format(username))
    
    async def check_username(self, message, username: str) -> bool:
        request = functions.account.CheckUsernameRequest(username=username)
        result = await self._client(request)
        return result

    @loader.command()
    async def getprivacy(self, message):
        """- покᴀзᴀть тᴇкʏщиᴇ нᴀстᴘойки конфидᴇнциᴀльности"""
        last_seen = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyStatusTimestamp()
        ))
        phone = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneNumber()
        ))
        profile_photo = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyProfilePhoto()
        ))
        forwards = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyForwards()
        ))
        groups = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyChatInvite()
        ))
        call = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneCall()
        ))
        voice = await self._client(functions.account.GetPrivacyRequest(
            key=types.InputPrivacyKeyVoiceMessages()
        ))

        global_settings = await self._client(functions.account.GetGlobalPrivacySettingsRequest())
        
        privacy_info = (
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>вᴘᴇмя послᴇднᴇго посᴇщᴇния:</b> {self._format_privacy(last_seen.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>номᴇᴘ тᴇлᴇфонᴀ:</b> {self._format_privacy(phone.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>фото пᴘофиля:</b> {self._format_privacy(profile_photo.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>пᴇᴘᴇсылкᴀ сооҕщᴇний:</b> {self._format_privacy(forwards.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>пᴘиглᴀшᴇния в гᴘʏппы:</b> {self._format_privacy(groups.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>кᴘʏжки/голосовыᴇ:</b> {self._format_privacy(voice.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>звонки:</b> {self._format_privacy(call.rules)}",
            f"<emoji document_id=5231112502573555738>🗓</emoji> <b>ᴀᴘхив и новыᴇ чᴀты:</b> {'<emoji document_id=5237814653010076467>🗓</emoji> Скрыто' if global_settings.archive_and_mute_new_noncontact_peers else '<emoji document_id=5229132514060167056>🗓</emoji> Не скрыто'}"
        )

        await utils.answer(
            message,
            self.strings["privacy_settings"].format("\n".join(privacy_info))
            )    

    def _format_privacy(self, rules):
        """Форматирует правила приватности"""
        if any(isinstance(rule, types.PrivacyValueAllowAll) for rule in rules):
            return "<emoji document_id=5235875883297824772>🗓</emoji> Все"
        elif any(isinstance(rule, types.PrivacyValueAllowContacts) for rule in rules):
            return "<emoji document_id=5233429444156223307>🗓</emoji> Контакты"
        elif any(isinstance(rule, types.PrivacyValueDisallowContacts) for rule in rules):
            return "<emoji document_id=5229132514060167056>🗓</emoji> Близкие друзья"
        else:
            return "<emoji document_id=5237814653010076467>🗓</emoji> Никто"
