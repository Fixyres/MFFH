__version__ = (1, 0, 0)
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ© Copyright 2024
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤhttps://t.me/unnic
# 🔒ㅤㅤㅤㅤㅤLicensed under the GNU AGPLv3
# 🌐ㅤㅤhttps://www.gnu.org/licenses/agpl-3.0.html
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
# author: @unnic
# name: Del
#██╗░░░██╗███╗░░██╗███╗░░██╗██╗░█████╗░
#██║░░░██║████╗░██║████╗░██║██║██╔══██╗
#██║░░░██║██╔██╗██║██╔██╗██║██║██║░░╚═╝
#██║░░░██║██║╚████║██║╚████║██║██║░░██╗
#╚██████╔╝██║░╚███║██║░╚███║██║╚█████╔╝
#░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚═╝░╚════╝

import asyncio
from telethon import types
from telethon.errors import ChatAdminRequiredError
from .. import loader, utils

@loader.tds
class DelMod(loader.Module):
    """Module for Cleaning Up Deleted Accounts in Chat"""

    strings = {
        "name": "Del",
        "author": "@HikkTutor",
    }

    async def client_ready(self, client, db):
        self._client = client
        self.db = db

    @loader.command()
    async def delete(self, message: types.Message):
        """Удаляет удалённые аккаунты из чата"""
        chat = await message.get_chat()

        if isinstance(chat, types.User):
            await utils.answer(message, "<emoji document_id=5787313834012184077>😀</emoji> <b>Эта команда предназначена только для групп</b>")
            return

        if not chat.admin_rights and not chat.creator:
            await utils.answer(message, "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Недостаточно прав для выполнения этой команды.</b>")
            return

        removed_count = 0
        
        edit_message = await utils.answer(message, "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск удалённых аккаунтов</b>")
        if not edit_message:
            edit_message = message

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except ChatAdminRequiredError:
                    await utils.answer(message, "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Для выполнения команды необходимы права администратора</b>")
                    return
                except Exception as e:
                    await utils.answer(message, f"<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Ошибка при удалении аккаунта {user.id}: {str(e)}</b>")

        if removed_count == 0:
            await edit_message.edit("<emoji document_id=5341509066344637610>😎</emoji> <b>Здесь нет ни одного удалённого аккаунта</b>")
        else:
            await edit_message.edit(f"<emoji document_id=5328302454226298081>🫥</emoji> <b>Удалено {removed_count} удалённых аккаунтов</b>")
