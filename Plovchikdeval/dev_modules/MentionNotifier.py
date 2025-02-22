"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P"
                                                                     
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

# meta developer: @kshmods

from .. import loader, utils
from telethon.tl.types import Message
import html

@loader.tds
class MentionNotifierMod(loader.Module):
    """Notifies you when you are mentioned in groups and channels"""
    strings = {"name": "MentionNotifier"}
    def __init__(self):
        self.name = self.strings["name"]
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "BLACKLIST", [], validator=loader.validators.Series(),
            ),
            loader.ConfigValue(
                "WHITELIST", [], validator=loader.validators.Series(),
            ),
        )
        

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def mnblockcmd(self, message):
        """Adds a user to the blacklist"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user_id = (
            int(args) if args.isdigit() else (await self.client.get_entity(args)).id
        ) if args else reply.sender_id
        blacklist = self.config["BLACKLIST"]
        if user_id not in blacklist:
            blacklist.append(user_id)
            self.set("BLACKLIST", blacklist)
            await utils.answer(message, f"Added {user_id} to the blacklist")
        else:
            await utils.answer(message, f"{user_id} is already in the blacklist")

    async def mnwlcmd(self, message):
        """Adds a chat to the whitelist"""
        args = utils.get_args_raw(message)
        args = args[3:] if args.startswith("-46") else args[4:] if args.startswith("-100") else args
        chat_id = (
            int(args) if args.isdigit() or args.startswith("-") else (await self.client.get_entity(args)).id
        ) if args else int(str(message.chat_id)[3:]) if str(message.chat_id).startswith("-46") else int(str(message.chat_id)[4:]) if str(message.chat_id).startswith("-100") else message.chat_id
        whitelist = self.config["WHITELIST"]
        if chat_id not in whitelist:
            whitelist.append(chat_id)
            self.set("WHITELIST", whitelist)
            await utils.answer(message, f"Added {chat_id} to the whitelist")
        else:
            whitelist.remove(chat_id)
            self.set("WHITELIST", whitelist)
            await utils.answer(message, f"Removed {chat_id} from the whitelist")

    async def mnunblockcmd(self, message):
        """Removes a user from the blacklist"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        user_id = (
            int(args) if args.isdigit() else (await self.client.get_entity(args)).id
        ) if args else reply.sender_id
        blacklist = self.config["BLACKLIST"]
        if user_id in blacklist:
            blacklist.remove(user_id)
            self.set("BLACKLIST", blacklist)
            await utils.answer(message, f"Removed {user_id} from the blacklist")
        else:
            await utils.answer(message, f"{user_id} is not in the blacklist")

    async def mnlistcmd(self, message):
        """Lists the users to ignore mentions from and chats to notify mentions from"""
        blacklist = self.config["BLACKLIST"]
        whitelist = self.config["WHITELIST"]
        output = "Users to ignore mentions from:\n"
        if blacklist:
            for user in blacklist:
                try:
                    user_entity = await self.client.get_entity(user)
                    output += f"<emoji document_id=4974551780743447211>🛑</emoji> {user_entity.first_name} ({user})\n"
                except:
                    output += f"<emoji document_id=4974551780743447211>🛑</emoji> {user}\n"
        else:
            output += "No users to ignore mentions from"
        output += "\n\nChats to notify mentions from:\n"
        if whitelist:
            for chat in whitelist:
                try:
                    chat_entity = await self.client.get_entity(chat)
                    output += f"<emoji document_id=4974608010455286340>🛑</emoji> {chat_entity.title} ({chat})\n"
                except:
                    output += f"<emoji document_id=4974608010455286340>🛑</emoji> {chat}\n"
        else:
            output += "No chats to notify mentions from"
        await utils.answer(message, output)

    async def watcher(self, message : Message):
        if isinstance(message, Message):
            if message.mentioned and (message.is_group or message.is_channel):
                chat = await message.get_chat()
                sender = await message.get_sender()
                me = await self.client.get_me()
                if sender.id == me.id or sender.bot or sender.id in self.config["BLACKLIST"]:
                    return
                if chat.id in self.config["WHITELIST"]:
                    if chat.username:
                        chat_link = f"https://t.me/{chat.username}/{message.id}"
                    else:
                        chat_link = f"https://t.me/c/{chat.id}/{message.id}"
                    if sender.username:
                        notification = f"You were mentioned by @{sender.username} in <b>{chat.title}</b>.\nLink: {chat_link}"
                    else:
                        notification = f"You were mentioned by <i><b>{html.escape(sender.first_name)} </b></i>in <b>{chat.title}</b>.\nLink: {chat_link}"
                    await self.inline.bot.send_message(me.id, notification, parse_mode="html")
