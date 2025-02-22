from hikkatl.types import Message
from .. import loader, utils


@loader.tds
class FirstID(loader.Module):
    """Find the first ID"""

    strings = {
        "name": "firstid",
        "menu": "Use inline menu to interact!",
        "next": "Next",
        "back": "Back",
        "close": "Close",
        "sucsess": "Successfully received profile by ID: <code>{}</code>",
        "failure": "Failed to get profile by ID: <code>{}</code>"
    }

    strings_ru = {
        "menu": "Используй инлайн меню для взаимодействия!",
        "next": "Следующее",
        "back": "Предыдущее",
        "close": "Закрыть",
        "sucsess": "Удачно получен профиль по айди: <code>{}</code>",
        "failure": "Не удалось получить профиль по айди: <code>{}</code>"
    }
        
    def buttons(self, uid):
        markup =  [
                [
                    {
                        "text": f"⏩ {self.strings['next']}",
                        "callback": self._inline_next,
                        "args": (uid, ),
                    }
                ],
                [
                    {
                        "text": f"❌ {self.strings['close']}", 
                        "action": "close"
                    }
                ],
                [
                    {
                        "text": f"⏪ {self.strings['back']}",
                        "callback": self._inline_back,
                        "args": (uid, )
                    }
                ],
            ]
        return markup

    @loader.command()
    async def findid(self, message: Message):
        """- [Число с которого начинать] - Поиск ID"""
        args = utils.get_args_raw(message)
        
        uid = int(args) if args else 0
        uids = []
        # full inline...

        await self.inline.form(
            text=self.strings["menu"],
            message=message,
            reply_markup=self.buttons(uid).copy()
        )
        
    # inline callbacks
    
    async def _inline_next(self, call, uid):
        next_uid = uid+1
        try:
            user = await self.client.get_entity(next_uid)
        except ValueError:
            msg = self.strings["failure"].format(next_uid)
        else:
            msg = self.strings["sucsess"].format(next_uid)
        await call.edit(msg,  reply_markup=self.buttons(next_uid))
            
    async def _inline_back(self, call, uid):
        next_uid = uid-1
        try:
            user = await self.client.get_entity(next_uid)
        except ValueError:
            msg = self.strings["failure"].format(next_uid)
        else:
            msg = self.strings["sucsess"].format(next_uid)
        await call.edit(msg,  reply_markup=self.buttons(next_uid))
