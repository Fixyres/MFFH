# meta developer: @xdesai

from hikkatl.types import Message
from .. import loader, utils

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
        args = utils.get_args_raw(message).split(", ", maxsplit=2)
        btn_text, btn_link, text = args

        await self.inline.form(
            text=text,
            message=message,
            reply_markup=[
                [
                    {
                        "text": btn_text,
                        "url": btn_link
                    }
                ]
            ]
        )

    @loader.command(
        ru_doc=" [Ссылка на изображение] [Текст кнопки] [Ссылка в кнопке] [Текст] - Создать инлайн кнопку",
    )
    async def cinlinephoto(self, message: Message):
        """ [Image link] [Button text] [Button link] [Text] - Create inline button"""
        args = utils.get_args_raw(message).split(", ", maxsplit=3)
        image_link, btn_text, btn_link, text = args

        await self.inline.form(
            text=text,
            message=message,
            photo=image_link,
            mime_type="photo/jpeg" if args[0].endswith('.jpg') else "photo/png",
            reply_markup=[
                [
                    {
                        "text": btn_text,
                        "url": btn_link
                    }
                ]
            ]
        )

    @loader.command(
        ru_doc=" [Ссылка на видео] [Текст кнопки] [Ссылка в кнопке] [Текст] - Создать инлайн кнопку",
    )
    async def cinlinevideo(self, message: Message):
        """ [Video link] [Button text] [Button link] [Text] - Create inline button"""
        args = utils.get_args_raw(message).split(", ", maxsplit=3)
        video_link, btn_text, btn_link, text = args

        await self.inline.form(
            text=text,
            message=message,
            video=video_link,
            mime_type="video/mp4",
            reply_markup=[
                [
                    {
                        "text": btn_text,
                        "url": btn_link
                    }
                ]
            ]
        )

    @loader.command(
        ru_doc=" [Ссылка на GIF] [Текст кнопки] [Ссылка в кнопке] [Текст] - Создать инлайн кнопку",
    )
    async def cinlinegif(self, message: Message):
        """ [GIF link] [Button text] [Button link] [Text] - Create inline button"""
        args = utils.get_args_raw(message).split(", ", maxsplit=3)
        gif_link, btn_text, btn_link, text = args

        await self.inline.form(
            text=text,
            message=message,
            gif=gif_link,
            mime_type="video/mp4",
            reply_markup=[
                [
                    {
                        "text": btn_text,
                        "url": btn_link
                    }
                ]
            ]
        )
