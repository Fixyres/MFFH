# meta developer: @codermasochist

from telethon.tl.types import Message
from ..inline.types import InlineCall
from .. import loader, utils
import asyncio

@loader.tds
class Bfgim(loader.Module):
    """инлайн менеджер для бфг. by @codermasochist"""

    strings = {"name": "Bfgim"}
    _bot = "@bforgame_bot"

    @loader.command()
    async def infcmd(self, message: Message):
        """— <reply> открыть меню."""
        args = utils.get_args(message)
        user_id = None

        if not args:
            if message.is_reply:
                reply = await message.get_reply_message()
                user_id = reply.sender_id
            else:
                await message.reply("укажи ид или реплай")
                return
        else:
            user = args[0]
            if user.isdigit():
                user_id = int(user)
            else:
                try:
                    user = await self.client.get_entity(user)
                    user_id = user.id
                except Exception:
                    await message.reply("ошибочке.")
                    return

        await self.show_main_menu(message, user_id, is_inline=False)

    async def show_main_menu(self, call, user_id, is_inline=True):
        buttons = [
            [{"text": "чс", "callback": self.check_chs, "args": (user_id,)}],
            [{"text": "профиль", "callback": self.profile, "args": (user_id,)}],
        ]
        
        text = f"<b>выберите для игрока:</b>\n<code>{user_id} </code>"
        
        if is_inline:
            await call.edit(text, reply_markup=buttons)
        else:
            await self.inline.form(text, message=call, reply_markup=buttons)

    async def execute_command(self, command: str) -> str:
        async with self.client.conversation(self._bot) as conv:
            try:
                await conv.send_message(command)
                return (await conv.get_response(timeout=10)).raw_text
            except asyncio.TimeoutError:
                return "бот не ответил, лох."

    async def check_chs(self, call: InlineCall, user_id):
        result = await self.execute_command(f"информация о чс {user_id}")
        await self.show_result(call, user_id, result)

    async def profile(self, call: InlineCall, user_id):
        result = await self.execute_command(f"профиль {user_id}")
        await self.show_result(call, user_id, result)

    async def show_result(self, call: InlineCall, user_id, result):
        buttons = [[{"text": "назад", "callback": self.show_main_menu, "args": (user_id, True)}]]
        await call.edit(f"<b>Результат:</b>\n\n{result}", reply_markup=buttons)
