# @Sekai_Yoney

﻿from .. import loader, utils


def register(cb):
    cb(TikTokMod())

class TikTokMod(loader.Module):
    """Качаем видео без водяного знака в Тик Ток."""
    strings = {'name': 'TikTok'}

    async def tikcmd(self, message):
        """.tik ссылка на видео."""
        await utils.answer(message, 'Ща...')
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "А где ссылка?")
            return
        r = await message.client.inline_query('tikdobot', args)
        await message.client.send_file(message.to_id, r[1].result.content.url)
        await message.delete()
