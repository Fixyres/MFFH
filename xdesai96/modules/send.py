# meta developer: @xdesai

from .. import loader, utils

@loader.tds
class SendPmMod(loader.Module):
    """Module for sending private messages"""
    strings = {"name": "SendPm"}

    async def client_ready(self, client, db):
        self.client = client
        self.pmchat : int = None
        self.show_chat_to : int = None
        self.formatted_message = ""
        self.message_to_change_id : int = None

    async def sendcmd(self, message):
        """Send a private message to a user. Usage: .send <message>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Usage: .send <message></b>")
            return
        if isinstance(args, list):
            args = " ".join(args)
        msg = args
        user_id = self.pmchat
        try:
            await self.client.send_message(user_id, msg)
            await message.delete()
        except Exception as e:
            await message.edit(f"<b>Error: {str(e)}</b>")

    async def setpmcmd(self, message):
        """Set a chat to send a message. Usage: .setpm <chat_id>"""
        user_id = utils.get_args_raw(message)
        if isinstance(user_id, list):
            user_id = user_id[0]
        self.message_to_change_id = message.id
        self.formatted_message = ""
        self.pmchat = int(user_id)
        self.show_chat_to = int(message.chat_id)
        await message.edit(f"Chat with {self.pmchat} started!")

    async def stopchatcmd(self, message):
        """Send a private message to a user. Usage: .stopchat <user_id>"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Usage: .stopchat (user_id) </b>")
            return

        if isinstance(args, list):
            args = args[0]
        user_id = args
        try:
            self.pmchat = None
            self.show_chat_to = None
            await message.edit(f'<b>PM with {user_id} stopped!</b>')
        except Exception as e:
            await message.edit(f"<b>Error: {str(e)}</b>")

    async def watcher(self, message):
        if (message.is_private or not message.is_private) and (message.chat_id == self.show_chat_to or message.chat_id == self.pmchat):
            chat_id = message.from_id
            if message.out and (message.chat_id == self.pmchat or message.text[1:].startswith("send")):
                try:
                    self.formatted_message += f"\nme: {message.text.split('send', 1)[1].strip()}"
                except Exception:
                    self.formatted_message += f"\nme: {message.text}"
            else:
                if message.from_id == self.pmchat:
                    self.formatted_message += f"\n{chat_id}: {message.text}"
            await self.client.edit_message(self.show_chat_to, self.message_to_change_id, self.formatted_message)
