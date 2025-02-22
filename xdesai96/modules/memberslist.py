# meta developer: @xdesai

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
