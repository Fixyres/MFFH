# Sekai_Yoneya

from .. import loader, utils


@loader.tds
class WelcomeLeftMod(loader.Module):
    """Вход и выход пользователей в чате."""
    strings = {'name': 'Welcome & Left'}

    async def client_ready(self, client, db):
        self.db = db
        self.client = client

    async def welcomecmd(self, message):
        """Включить/выключить приветствие новых пользователей в чате. Используй: .welcome <clearall (по желанию)>."""
        welcome = self.db.get("Welcome", "welcome", {})
        chatid = str(message.chat_id)
        args = utils.get_args_raw(message)
        if args == "clearall":
            self.db.set("Welcome", "welcome", {})
            return await message.edit("<b>[Welcome]</b> Все настройки модуля сброшены.")

        if chatid in welcome:
            welcome.pop(chatid)
            self.db.set("Welcome", "welcome", welcome)
            return await message.edit("<b>[Welcome]</b> Отключено!")

        welcome.setdefault(chatid, {})
        welcome[chatid].setdefault("message", "Добро пожаловать в чат!")
        welcome[chatid].setdefault("is_reply", False)
        self.db.set("Welcome", "welcome", welcome)
        await message.edit("<b>[Welcome]</b> Включено!")


    async def setwelcomecmd(self, message):
        """Установить приветствие новых пользователей в чате.\nИспользуй: .setwelcome <текст (можно использовать {name}; {chat})>; ничего."""
        welcome = self.db.get("Welcome", "welcome", {})
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        chatid = str(message.chat_id)
        chat = await message.client.get_entity(int(chatid)) 
        try:
            if not args and not reply:
                return await message.edit(f'<b>[Welcome] Приветствие новых пользователей в "{chat.title}":</b>\n\n'
                                          f'<b>Статус:</b> Включено.\n'
                                          f'<b>Приветствие:</b> {welcome[chatid]["message"]}\n\n'
                                          f'<b>~ Установить новое приветствие можно с помощью команды:</b> .setwelcome <текст>.')
            else:
                if reply:
                    welcome[chatid]["message"] = reply.id
                    welcome[chatid]["is_reply"] = True
                else:
                    welcome[chatid]["message"] = args
                    welcome[chatid]["is_reply"] = False
                self.db.set("Welcome", "welcome", welcome)
                return await message.edit("<b>[Welcome] Новое приветствие установлено успешно!</b>")
        except KeyError: return await message.edit(f'<b>[Welcome] Приветствие новых пользователей в "{chat.title}":</b>\n\n'
                                                   f'<b>Статус:</b> Отключено')


    async def watcher(self, message):
        """Интересно, почему он именно watcher называется... 🤔"""
        try:
            welcome = self.db.get("Welcome", "welcome", {})
            chatid = str(message.chat_id)
            if chatid not in welcome: return
            if message.user_joined or message.user_added:
                user = await message.get_user()
                chat = await message.get_chat()
                if welcome[chatid]["is_reply"] == False:
                    return await message.reply((welcome[chatid]["message"]).format(name=user.first_name, chat=chat.title))
                msg = await self.client.get_messages(int(chatid), ids=welcome[chatid]["message"])
                await message.reply(msg)
        except: pass
        
    async def leftcmd(self, message): 
        """Включить/выключить выход пользователей из чата. Используй: .left <clearall (по желанию)>.""" 
        left = self.db.get("Left", "left", {}) 
        chatid = str(message.chat_id) 
        args = utils.get_args_raw(message) 
        if args == "clearall": 
            self.db.set("Left", "left", {}) 
            return await message.edit("<b>[Left]</b> Все настройки модуля сброшены.") 
 
        if chatid in left: 
            left.pop(chatid) 
            self.db.set("Left", "left", left) 
            return await message.edit("<b>[Left]</b> Отключено!") 
 
        left.setdefault(chatid, {}) 
        left[chatid].setdefault("message", "Пока👋") 
        left[chatid].setdefault("is_reply", False) 
        self.db.set("Left", "left", left) 
        await message.edit("<b>[Left]</b> Включен!") 
 
 
    async def setleftcmd(self, message): 
        """Установить новое сообщение при выходе из чата пользователей.\nИспользуй: .setleft <текст (можно использовать {name}; {chat})>; ничего.""" 
        left = self.db.get("Left", "left", {}) 
        args = utils.get_args_raw(message) 
        reply = await message.get_reply_message() 
        chatid = str(message.chat_id) 
        chat = await message.client.get_entity(int(chatid))  
        try: 
            if not args and not reply: 
                return await message.edit(f'<b>[Left] Выход пользователей в "{chat.title}":</b>\n\n' 
                                          f'<b>Статус:</b> Включено.\n' 
                                          f'<b>Текст:</b> {left[chatid]["message"]}\n\n' 
                                          f'<b>~ Установить новый текст можно с помощью команды:</b> .setleft <текст>.') 
            else: 
                if reply: 
                    left[chatid]["message"] = reply.id 
                    left[chatid]["is_reply"] = True 
                else: 
                    left[chatid]["message"] = args 
                    left[chatid]["is_reply"] = False 
                self.db.set("Left", "left", left) 
                return await message.edit("<b>[Left] Новый текст установлен успешно!</b>") 
        except KeyError: return await message.edit(f'<b>[Left] в "{chat.title}":</b>\n\n' 
                                                   f'<b>Статус:</b> Отключено') 
 
 
    async def watcher(self, message): 
        try: 
            left = self.db.get("Left", "left", {}) 
            chatid = str(message.chat_id) 
            if chatid not in left: return 
            if message.user_left or message.user_kicked: 
                user = await message.get_user() 
                chat = await message.get_chat() 
                if left[chatid]["is_reply"] == False: 
                    return await message.reply((left[chatid]["message"]).format(name=user.first_name, chat=chat.title)) 
                msg = await self.client.get_messages(int(chatid), ids=left[chatid]["message"]) 
                await message.reply(msg) 
        except: pass
