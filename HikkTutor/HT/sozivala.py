__version__ = (1, 0, 0)

#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: @AmdFx6100
# name: sozivala

from .. import loader, utils
from telethon.errors import ChatAdminRequiredError
import json
import os
import random

emoji = """😀😃😄😁😆🥹😅😂🤣🥲☺️😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🥸🤩🥳🙂‍↕️😏😒🙂‍↔️😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😶‍🌫️😱😨😰😥😓🤗🤔🫣🤭🫢🫡🤫🫠🤥😶🫥😐🫤😑🫨😬🙄😯😦😧😮😲🥱😴🤤😪😮‍💨😵😵‍💫🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😹😻😼😽🙀😿😾🫶🤲👐🙌👏🤝👍👎👊✊🤛🤜🫷🫸🤞✌️🫰🤟🤘👌🤌🤏🫳🫴👈👉👆👇☝️✋🤚🖐🖖👋🤙🫲🫱💪🦾🖕✍🙏🫵🦶🦵🦿💄💋👄🫦🦷👅👂🦻👃👣👁👀🫀🫁🧠🗣👤👥🫂👶👧🧒👦👩🧑👨👩‍🦱🧑‍🦱👨‍🦱👩‍🦰🧑‍🦰👨‍🦰👱‍♀️👱👱‍♂️🧔‍♂️👩‍🦳👵🧑‍🦳🧓👨‍🦳👴👩‍🦲👲🧑‍🦲👳‍♀️👨‍🦲👳🧔‍♀️👳‍♂️🧔🧕👮‍♀️🕵‍♀️👮🕵👮‍♂️🕵‍♂️👷‍♀️👩‍⚕️👷🧑‍⚕️👷‍♂️👨‍⚕️💂‍♀️👩‍🌾💂🧑‍🌾💂‍♂️👨‍🌾👩‍🍳👩‍🏫🧑‍🍳🧑‍🏫👨‍🍳👨‍🏫👩‍🎓👩‍🏭🧑‍🎓🧑‍🏭👨‍🎓👨‍🏭👩‍🎤👩‍💻🧑‍🎤🧑‍💻👨‍🎤👨‍💻👩‍🏫👩‍💼🧑‍🏫🧑‍💼👨‍🏫👨‍💼👩‍🏭👩‍🔧🧑‍🏭🧑‍🔧👨‍🏭👨‍🔧👩‍💻👩‍🔬🧑‍💻🧑‍🔬👨‍💻👨‍🔬👩‍🎨👩‍🚀🤵‍♀️🧑‍🎨🧑‍🚀🤵👨‍🎨👨‍🚀🤵‍♂️👩‍🚒👩‍⚖️👸🧑‍🚒🧑‍⚖️🫅👨‍🚒👨‍⚖️🤴👩‍✈️👰‍♀️🥷🧑‍✈️👰🦸‍♀️👨‍✈️👰‍♂️🦸🦸‍♂️🧙‍♂️🧟🦹‍♀️🧝‍♀️🧟‍♂️🦹🧝🧞‍♀️🦹‍♂️🧝‍♂️🧞🤶🧌🧞‍♂️🧑‍🎄🧛‍♀️🧜‍♀️🎅🧛🧜🧙‍♀️🧛‍♂️🧜‍♂️🧙🧟‍♀️🧚‍♀️🧚👨‍🍼🙅‍♂️🧏‍♂️🧚‍♂️🙇‍♀️🙆‍♀️🤦‍♀️👼🙇🙆🤦🤰🙇‍♂️🙆‍♂️🤦‍♂️🫄💁‍♀️🙋‍♀️🤷‍♀️🫃💁🙋🤷🤱💁‍♂️🙋‍♂️🤷‍♂️👩‍🍼🙅‍♀️🧏‍♀️🙎‍♀️🧑‍🍼🙅🧏🙎🙎‍♂️💆‍♂️👯👩‍🦼🙍‍♀️🧖‍♀️👯‍♂️🧑‍🦼🙍🧖🕴👨‍🦼🙍‍♂️🧖‍♂️👩‍🦽👩‍🦼‍➡️💇‍♀️💅🧑‍🦼‍➡️🧑‍🦽💇🤳👨‍🦽👨‍🦼‍➡️💇‍♂️💃👩‍🦽‍➡️🚶‍♀️💆‍♀️🕺🧑‍🦽‍➡️🚶💆👯‍♀️👨‍🦽‍➡️🚶‍♂️🚶‍♀️‍➡️🧎‍♀️🧎‍♀️‍➡️🚶‍➡️🧎🧎‍➡️🚶‍♂️‍➡️🧎‍♂️🧎‍♂️‍➡️👩‍🦯🏃‍♀️🧍‍♀️🧑‍🦯🏃🧍👨‍🦯🏃‍♂️🧍‍♂️👩‍🦯‍➡️🏃‍♀️‍➡️👫🧑‍🦯‍➡️🏃‍➡️👭👨‍🦯‍➡️🏃‍♂️‍➡️👬👩‍❤️‍👨🧶👩‍❤️‍👩🧵💑🪡👨‍❤️‍👨🧥👩‍❤️‍💋‍👨🥼👩‍❤️‍💋‍👩🦺💏👚👨‍❤️‍💋‍👨👕🪢👖🩲🥿🩳👠👔👡👗👢👙👞🩱👟👘🥾🥻🧦🩴🧤🧣👝🌂🎩👛🧢👜👒💼🎓🎒⛑🧳🪖👓👑🕶💍🥽🌂"""
emoji_list = list(emoji)

def chunks(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]

@loader.tds
class sozivala(loader.Module):
    """Модуль для массового упоминания участников группы с возможностью исключения определенных пользователей"""
    strings = {"name": "sozivala"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "EXCLUDED_USERS_FILE", "excluded_users.json", "Файл для хранения списка исключенных пользователей"
        )
        self.excluded_users = self.load_excluded_users()

    def load_excluded_users(self):
        if os.path.exists(self.config["EXCLUDED_USERS_FILE"]):
            with open(self.config["EXCLUDED_USERS_FILE"], "r") as f:
                return json.load(f)
        return {}

    def save_excluded_users(self):
        with open(self.config["EXCLUDED_USERS_FILE"], "w") as f:
            json.dump(self.excluded_users, f)

    async def client_ready(self, client, db):
        self.client = client

    async def is_admin(self, chat_id):
        try:
            permissions = await self.client.get_permissions(chat_id, 'me')
            return permissions.is_admin
        except ChatAdminRequiredError:
            return False
            
    @loader.command()
    async def all(self, message):
        """- Запустить/остановить созыв"""
        chat = await message.get_chat()
        if not chat:
            await message.edit("Не удалось получить информацию о чате.")
            return

        if not getattr(chat, 'megagroup', False):
            await message.edit("Эта команда доступна только в супергруппах.")
            return

        if not await self.is_admin(chat.id):
            await message.edit("У вас нет прав администратора в этом чате.")
            return

        if hasattr(self, "mention_task") and not self.mention_task.done():
            self.mention_task.cancel()
            await message.edit("Массовое упоминание остановлено.")
            return
        self.mention_task = self.client.loop.create_task(self.mention_all_members(message))
        await message.delete()

    async def mention_all_members(self, message):
        args = utils.get_args_raw(message)
        tag = args or ""
        tags = []
        chat = await message.get_chat()
        async for user in self.client.iter_participants(chat.id):
          if user.bot == False:
            if str(user.id) not in self.excluded_users.get(str(chat.id), []) or str(user.id) == 'me':
                print(str(user)+'\n')
                tags.append(f"<a href='tg://user?id={user.id}'>{random.choice(emoji_list)}</a>")  
        chunkss = list(chunks(tags, 20))
        for chunk in chunkss:
            await message.client.send_message(message.to_id, tag + ' '.join(chunk))

    @loader.command()
    async def remove(self, message):
        """<chat_id> <user_id/username> - Исключить пользователя из упоминания"""
        args = utils.get_args(message)
        if len(args) != 2:
            await message.edit("Использование: .remove <chat_id> <user_id|username>")
            return

        chat_id = args[0]
        if not str(chat_id).startswith('-100'):
            chat_id = '-100' + str(chat_id)
        user_identifier = args[1]

        try:
            if user_identifier.isdigit():
                user_id = int(user_identifier)
                user = await self.client.get_entity(user_identifier)
                if user.bot == True:
                    await message.edit('Боты и так не учавствуют в созыве')
                    return
            else:
                user = await self.client.get_entity(user_identifier)
                if user.bot == True:
                    await message.edit('Боты и так не учавствуют в созыве')
                    return
                user_id = user.id
            
            if chat_id not in self.excluded_users:
                self.excluded_users[chat_id] = []

            if user_id not in self.excluded_users[chat_id]:
                self.excluded_users[chat_id].append(user_id)
                self.save_excluded_users()

                await message.edit(
                f"Пользователь <a href='tg://user?id={user.id}'>{user.first_name}</a> исключен из массового упоминания в чате \"{chat_id}\" "
            )
            else:
                await message.edit(
                f"Пользователь <a href='tg://user?id={user.id}'>{user.first_name}</a> уже исключен из массового упоминания в чате \"{chat.title}\" (ID: {chat_id})."
            )
        except Exception as e:
            await message.edit(f"Не удалось получить информацию о пользователе или чате: {e}")
            return


    @loader.command()
    async def unremove(self, message):
        """<chat_id> <user_id/username> - Вернуть исключенного пользователя в упоминания"""
        args = utils.get_args(message)
        if len(args) != 2:
            await message.edit("Использование: .unremove <chat_id> <user_id|username>")
            return
        chat_id = args[0]
        if not str(chat_id).startswith('-100'):
            chat_id = '-100' + str(chat_id)
        user_identifier = args[1]

        try:
            if user_identifier.isdigit():
                user_id = int(user_identifier)
            else:
                user = await self.client.get_entity(user_identifier)
                user_id = user.id
            if chat_id in self.excluded_users and user_id in self.excluded_users[chat_id]:
                self.excluded_users[chat_id].remove(user_id)
                if not self.excluded_users[chat_id]:
                    del self.excluded_users[chat_id]
                self.save_excluded_users()

                await message.edit(
                f"Пользователь <a href='tg://user?id={user.id}'>{user.first_name}</a> восстановлен для массового упоминания в чате (ID: {chat_id})."
            )
            else:
                await message.edit(
                f"Пользователь не был исключен из массового упоминания в чате (ID: {chat_id})."
            )
        except Exception as e:
            await message.edit(f"Не удалось получить информацию о пользователе: {e}")
            return
    @loader.command()
    async def check(self, message):
        """<chat_id> - Показать пользователей, исключенных из упоминания в чате"""
        args = utils.get_args(message)
        if len(args) != 1:
            await message.edit("Использование: .check <chat_id>")
            return

        chat_id = args[0]
        if not str(chat_id).startswith('-100'):
            chat_id = '-100' + str(chat_id)

        if chat_id not in self.excluded_users or not self.excluded_users[chat_id]:
            await message.edit(f"В чате с ID {chat_id} нет исключенных пользователей.")
            return

        excluded_ids = self.excluded_users[chat_id]
        excluded_users_info = []

        try:
            for user_id in excluded_ids:
                try:
                    user = await self.client.get_entity(user_id)
                    excluded_users_info.append(f"<a href='tg://user?id={user.id}'>{user.first_name}</a> ({user.id})")
                except Exception as e:
                    excluded_users_info.append(f"Не удалось получить информацию о пользователе с ID {user_id}: {e}")

            excluded_users_list = "\n".join(excluded_users_info)
            await message.edit(f"Исключенные пользователи в чате с ID {chat_id}:\n{excluded_users_list}")
        except Exception as e:
            await message.edit(f"Ошибка при получении списка исключенных пользователей: {e}")