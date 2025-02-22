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

import tempfile

from .. import loader, utils


class MembersListMod(loader.Module):
    """Module to create a list of users."""
    strings = {"name": "MembersList"}

    async def client_ready(self, client, db):
        self.client = client

    async def mlistcmd(self, message):
        """Get the members list of multiple chats and send it as a txt file."""
        args = utils.get_args_raw(message)
        await message.delete()
        if not args:
            return await utils.answer(message, "Please specify chat IDs separated by spaces.")
        
        chat_ids = args.split()
        all_members_list = []

        for chat_id in chat_ids:
            try:
                members_list = await self.get_members_list(int(chat_id))
                all_members_list.extend(members_list)
            except ValueError:
                await utils.answer(message, f"Invalid chat ID: {chat_id}")
                return
            except Exception as e:
                await utils.answer(message, f"Error fetching members from chat {chat_id}: {e}")
                return

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=".txt", encoding="utf-8") as temp_file:
            for member in all_members_list:
                temp_file.write(member + '\n')
            temp_file_path = temp_file.name

        await self.client.send_file(
            message.chat_id,
            temp_file_path,
            caption=f"Here is the members list. Total users: {len(all_members_list)}",
            reply_to=message.reply_to_msg_id,
        )

    async def get_members_list(self, chat_id):
        members = await self.client.get_participants(chat_id)
        members_list = []

        for member in members:
            user_id = member.id
            first_name = member.first_name or ''
            last_name = member.last_name or ''
            username = member.username or ''
            phone = member.phone if member.id != (await self.client.get_me()).id and member.phone else ''
            members_list.append(f"{user_id}, {first_name}, {last_name}, {username}, {phone}")

        return members_list
