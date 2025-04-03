__version__ = (1, 0, 5)
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

from telethon import types  # type: ignore
from telethon.errors import ChatAdminRequiredError  # type: ignore
from .. import loader, utils
import logging

logger = logging.getLogger(__name__)


@loader.tds
class DelMod(loader.Module):
    """Модуль для очистки удаленных аккаунтов в чате"""

    strings = {
        "name": "Del",
        "author": "@HikkTutor",
        "no_deleted_accounts": "<emoji document_id=5341509066344637610>😎</emoji> <b>Здесь нет ни одного удаленного аккаунта.</b>",
        "deleted_accounts_removed": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Удалено {} удаленных аккаунтов.</b>",
        "no_messages": "<emoji document_id=5341509066344637610>😎</emoji> <b>Здесь нет сообщений от удаленных аккаунтов.</b>",
        "messages_removed": "<emoji document_id=5328302454226298081>🫥</emoji> <b>Удалено {} сообщений от удаленных аккаунтов.</b>",
        "not_admin": "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Недостаточно прав для выполнения этой команды.</b>",
        "not_group": "<emoji document_id=5787313834012184077>😀</emoji> <b>Эта команда предназначена только для групп!</b>",
        "error": "<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Ошибка при удалении аккаунта {}: {}.</b>",
        "searching": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск удаленных аккаунтов..</b>",
        "searching_messages": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск сообщений от удаленных аккаунтов..</b>",
    }

    async def client_ready(self, client, db):
        self._client = client
        self.db = db

    @loader.command()
    async def delete(self, message: types.Message):
        """Удаляет удаленные аккаунты из чата"""
        chat = await message.get_chat()

        if isinstance(chat, types.User):
            await utils.answer(message, self.strings("not_group"))
            return

        if not chat.admin_rights and not chat.creator:
            await utils.answer(message, self.strings("not_admin"))
            return

        removed_count = 0
        edit_message = await utils.answer(message, self.strings("searching"))
        if not edit_message:
            edit_message = message

        async for user in self._client.iter_participants(chat):
            if user.deleted:
                try:
                    await self._client.kick_participant(chat, user)
                    removed_count += 1
                except ChatAdminRequiredError:
                    await utils.answer(message, self.strings("not_admin"))
                    return
                except Exception as e:
                    await utils.answer(message, self.strings("error").format(user.id, str(e)))
                    return

        if removed_count == 0:
            await edit_message.edit(self.strings("no_deleted_accounts"))
        else:
            await edit_message.edit(self.strings("deleted_accounts_removed").format(removed_count))

    @loader.command()
    async def delmsg(self, message: types.Message):
        """Удаляет сообщения от удаленных аккаунтов из чата"""
        chat = await message.get_chat()

        if isinstance(chat, types.User):
            await utils.answer(message, self.strings("not_group"))
            return

        if not chat.admin_rights and not chat.creator:
            await utils.answer(message, self.strings("not_admin"))
            return

        removed_count = 0
        edit_message = await utils.answer(message, self.strings("searching_messages"))
        if not edit_message:
            edit_message = message

        offset_id = None
        while True:
            if offset_id is None:
                offset_id = 0

            logger.debug(f"Fetching messages with offset_id: {offset_id}")
            messages = await self._client.get_messages(chat, offset_id=offset_id, reverse=True, limit=100)
            logger.debug(f"Fetched {len(messages)} messages")

            if not messages:
                break

            for msg in messages:
                if msg.sender and isinstance(msg.sender, types.User) and msg.sender.deleted:
                    try:
                        await msg.delete()
                        removed_count += 1
                    except ChatAdminRequiredError:
                        await utils.answer(message, self.strings("not_admin"))
                        return
                    except Exception as e:
                        await utils.answer(message, self.strings("error").format(msg.sender.id, str(e)))
                        return

            if messages:
                offset_id = messages[-1].id
                logger.debug(f"Updated offset_id to: {offset_id}")
            else:
                break
                
        if removed_count == 0:
            await edit_message.edit(self.strings("no_messages"))
        else:
            await edit_message.edit(self.strings("messages_removed").format(removed_count))
