# @Sekai_Yoneya

from .. import loader, utils
import datetime, time
from telethon import functions, types

@loader.tds
class AntiPMMod(loader.Module):

    strings = {"name": "Anti-PM", "pm_off": "<b>Теперь вы принимаете сообщения от всех пользователей.</b>",
               "pm_on": "<b>Вы перестали принимать сообщения от пользователей.</b>",
               "pm_go_away": "Здравствуй! К сожалению, я не принимаю личные сообщения."
                             "\n\nСвяжитесь со мной в @sekai_pmbot, или ожидайте пока я одобрю вас.",
               "pm_allowed": "<b>Я разрешил {} писать мне.</b>",
               "pm_deny": "<b>Я запретил {} писать мне.</b>",
               "blocked": "<b>{} был(-а) занесен(-а) в Черный Список.</b>",
               "unblocked": "<b>{} удален(-а) из Черного Списка.</b>",
               "addcontact": "<b>{} был(-а) добавлен(-а) в контакты.</b>",
               "delcontact": "<b>{} был(-а) удален(-а) из контактов.</b>",
               "who_to_allow": "<b>Кому разрешить писать в личку ?</b>",
               "who_to_deny": "<b>Кому запретить писать в личку ?</b>",
               "who_to_block": "<b>Укажите, кого блокировать.</b>",
               "who_to_unblock": "<b>Укажите, кого разблокировать.</b>",
               "who_to_contact": "<b>Укажите, кого добавить в контакт.</b>",
               "who_to_delcontact": "<b>Укажите, кого удалить из контактов.</b>"}

    def __init__(self):
        self.me = None

    async def client_ready(self, message, db):
        self.db=db
        self.client = client
        self.me = await client.get_me(True)

    async def pmcmd(self, message):
        """Используй: .pm : чтобы включить/отключить авто ответ на личные сообщения."""
        pm = self.db.get("Anti-PM", "pm")
        if pm is not True:
            await utils.answer(message, self.strings["pm_off"])
            self.db.set("Anti-PM", "pm", True)
        else:
            await utils.answer(message, self.strings["pm_on"])
            self.db.set("Anti-PM", "pm", False)

    async def allowcmd(self, message):
        """Используй: .allow чтобы разрешить этому пользователю писать вам в личку."""
        try:
            if message.is_private:
                user = await message.client.get_entity(message.chat_id)
            else:
                return
        except: return await message.edit("<b>Это не лс.</b>")
        self.db.set("Anti-PM", "allowed", list(set(self.db.get("Anti-PM", "allowed", [])).union({user.id})))
        await utils.answer(message, self.strings["pm_allowed"].format(user.first_name))

    async def denycmd(self, message):
        """Используй: .deny чтобы запретить этому пользователю писать вам в личку."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args and not reply:
            return await message.edit("<b>Нет аргументов или реплая.</b>")
        try:
            if message.is_private:
                user = await message.client.get_entity(message.chat_id) 
            if args:
                if args.isnumeric(): user = await message.client.get_entity(int(args))
                else: user = await message.client.get_entity(args)
            else: user = await message.client.get_entity(reply.sender_id)
        except: return await message.edit("<b>Взлом жопы.</b>")
        self.db.set("Anti-PM", "allowed", list(set(self.db.get("Anti-PM", "allowed", [])).difference({user.id})))
        await utils.answer(message, self.strings["pm_deny"].format(user.first_name))

    async def allowedcmd(self, message):
        """Используй: .allowed : чтобы посмотреть список пользователей которым вы разрешили писать в личку."""
        await message.edit("ща покажу")
        allowed = self.db.get("Anti-PM", "allowed", [])
        number = 0
        users = ""
        try:
            for _ in allowed:
                number += 1
                try:
                    user = await message.client.get_entity(int(_))
                except: pass
                if not user.deleted:
                    users += f"{number}. <a href=tg://user?id={user.id}>{user.first_name}</a> | [<code>{user.id}</code>]\n"
                else:
                    users += f"{number} • Удалённый аккаунт ID: [<code>{user.id}</code>]\n"
            await utils.answer(message, "<b>Список пользователей которым я разрешил писать в личку:</b>\n" + users)
        except: return await message.edit("<b>Какой то айди из списка не правильный :/</b>")

    async def blockcmd(self, message):
        """Используй: .block чтобы заблокировать этого пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_block"])
                return
        await message.client(functions.contacts.BlockRequest(user))
        await utils.answer(message, self.strings["blocked"].format(user.first_name))

    async def unblockcmd(self, message):
        """Используй: .unblock чтобы разблокировать этого пользователя."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_unblock"])
                return
        await message.client(functions.contacts.UnblockRequest(user))
        await utils.answer(message, self.strings["unblocked"].format(user.first_name))

    async def addcontcmd(self, message):
        """Используй: .addcont чтобы добавить пользователя в свои контакты."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_contact"])
                return
        await message.client(functions.contacts.AddContactRequest(id=user.id, first_name=user.first_name, last_name=' ', phone='seen', add_phone_privacy_exception=False))
        await utils.answer(message, self.strings["addcontact"].format(user.first_name))

    async def delcontcmd(self, message):
        """Используй: .delcont чтобы удалить пользователя из своих контактов."""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if message.is_private:
            user = await message.client.get_entity(message.chat_id)
        else:
            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                user = await message.client.get_entity(int(args) if args.isnumeric() else args)
            if not user:
                await utils.answer(message, self.strings["who_to_delcontact"])
                return
        await message.client(functions.contacts.DeleteContactsRequest(id=[user.id]))
        await utils.answer(message, self.strings["delcontact"].format(user.first_name))

    async def renamecmd(self, message): 
        args = utils.get_args_raw(message) 
        reply = await message.get_reply_message() 
        if not args: 
            return await message.edit("<b>Нету аргументов.</b>") 
        if not reply: 
            return await message.edit("<b>Где реплай?</b>") 
        else: 
            user = await message.client.get_entity(reply.sender_id) 
        try: 
            await message.client(functions.contacts.AddContactRequest(id=user.id,  
                                                                      first_name=args, 
                                                                      last_name=' ', 
                                                                      phone='мобила', 
                                                                      add_phone_privacy_exception=False)) 
            await message.edit(f"<code>{user.id}</code> <b>переименован(-а) на</b> <code>{args}</code>") 
        except: return await message.edit("<b>Что то пошло не так...</b>")

    async def watcher(self, message): 
        try: 
            user = await utils.get_user(message) 
            pm = self.db.get("Anti-PM", "pm") 
            if message.sender_id == (await message.client.get_me()).id: return 
            if pm is not True: 
                if message.is_private: 
                    if not self.get_allowed(message.from_id): 
                        if user.bot or user.verified: 
                            return 
                        await utils.answer(message, self.strings["pm_go_away"]) 
        except: pass 
 
    def get_allowed(self, id): 
        return id in self.db.get("Anti-PM", "allowed", [])
