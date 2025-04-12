# Copyright 2025, werpyock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__version__ = (1, 0, 0)
# meta developer: @wmodules

from hikkatl.types import Message
from hikkatl.utils import resolve_id, get_display_name
from .. import loader, utils

@loader.tds
class IDMod(loader.Module):
    """Модуль для получения ID пользователей или чатов"""
    
    strings = {
        "name": "ID",
        "id": "🆔 {name}: <code>{id}</code>",
        "error": "❌ Ошибка: {exception}"
    }

    async def useridcmd(self, message: Message):
        """получить ID пользователя"""
        try:
            user = (await message.get_reply_message()).sender if message.is_reply else message.sender
            name = get_display_name(user)
            
            await utils.answer(
                message,
                self.strings("id").format(name=name, id=user.id)
            )
        except Exception as e:
            await utils.answer(
                message,
                self.strings("error").format(exception=str(e))
            )

    async def chatidcmd(self, message: Message):
        """получить ID текущего чата"""
        try:
            chat = await message.get_chat()
            name = get_display_name(chat)
                
            await utils.answer(
                message,
                self.strings("id").format(name=name, id=resolve_id(chat.id)[0])
            )
        except Exception as e:
            await utils.answer(
                message,
                self.strings("error").format(exception=str(e))
            )
