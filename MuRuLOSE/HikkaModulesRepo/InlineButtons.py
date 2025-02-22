from hikkatl.types import Message
from .. import loader, utils

'''
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    InlineButtons
    📜 Licensed under the GNU AGPLv3	
'''

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class InlineButtons(loader.Module):
    """Create inline buttons easily"""

    strings = {"name": "InlineButtons"}
    strings_ru = {"_cls_doc": "Создайте инлайн кнопки легко"}

    @loader.command(
        ru_doc=" [Текст кнопки] [Ссылка в кнопке] [Текст] - Создать инлайн кнопку",
    )
    async def cinline(self, message: Message):
        """ [Button text] [Button link] [Text] - Create inline button"""
        args = utils.get_args_raw(message).split()

        await self.inline.form(
            text=' '.join(args[2:]),
            message=message,
            reply_markup=[
                [
                    {
                        "text": args[0],
                        "url": args[1]
                    }
                ]
            ]
        )


