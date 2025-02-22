#                █████████████████████████████████████████
#                █────██────█────█────█───█────█────█────█
#                █─██──█─██─█─██─█─██─██─██─██─█─██─█─██─█
#                █─██──█─██─█────█─██─██─██─██─█────█─██─█
#                █─██──█─██─█─█─██─██─██─██─██─█─█─██─██─█
#                █────██────█─█─██────██─██────█─█─██────█
#                █████████████████████████████████████████
#
#
#                     Copyright 2022 t.me/Dorotoro
#             https://www.gnu.org/licenses/agpl-3.0.html
#
# meta banner: https://raw.githubusercontent.com/dorotorothequickend/DorotoroModules/main/banners/Dor%D0%BEtoroSimpleRoleplay.png
# meta developer: @DorotoroMods

from .. import loader, utils
import random

@loader.tds
class SimpleRolePlay(loader.Module):
    """Базовые команды для текстовых ролевых игр."""

    strings = {
        "name": "Simple RolePlay",
        "symbol": "Символ который используется в конце и в начале /me. (например, звезда)",
        "not_args": "<emoji document_id=6325733670132909953>😰</emoji> <b>Вы неправильно вписали действие или же не указали его вовсе. Попробуйте еще раз.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "symbol",
                None,
                doc=lambda: self.strings("symbol")
            ),
        )


    @loader.command()
    async def me(self, message):
        "<действие> - сообщает об исполнителе команды от первого лица. Пример использования: .me открыл браузер. Также есть доп. настройка в .config"
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("not_args"))
        
        me = self.client.hikka_me
        nickname = f'{me.first_name} {me.last_name if me.last_name else ""}'

        cfg = self.config["symbol"]
        
        if cfg:
            await utils.answer(message, f"<emoji document_id=5785175271011259591>🌀</emoji> <b>{cfg}{nickname}</b> <i>{args}</i><b>{cfg}</b>")
        else:
            await utils.answer(message, f"<emoji document_id=5785175271011259591>🌀</emoji> <b>{nickname}</b> <i>{args}</i><b>")
    
    @loader.command()
    async def do(self, message):
        "<действие> - предназначена для описания событий и подробностей игрового мира в настоящем времени, не относящихся конкретно к определённым людям. Пример использования: .do В кармане Дороторо лежит пистолет и пара гранат."
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("not_args"))

        me = self.client.hikka_me
        nickname = f'{me.first_name} {me.last_name if me.last_name else ""}'

        await utils.answer(message, f"<emoji document_id=5785175271011259591>🌀</emoji> <i>{args}</i> - | <b>{nickname}</b>")

    @loader.command()
    async def otry(self, message):
        "<действие> -  предназначена для решения спорных и неоднозначных ситуаций, где события могут развиваться по нескольким сценариям, либо если требуется случайная вероятность удачи того или иного действия. Пример использования: .try завёл машину."
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("not_args"))

        me = self.client.hikka_me
        nickname = f'{me.first_name} {me.last_name if me.last_name else ""}'

        tryr = random.choice([
            "<b><emoji document_id=6334758581832779720>✅</emoji> Удачно </b>", 
            "<b><emoji document_id=6334578700012488415>❌</emoji> Неудачно </b>"
        ])
        
        await utils.answer(message, f"<emoji document_id=5785175271011259591>🌀</emoji> <b>{nickname}</b> <i>{args}</i> - | {tryr}")
    
    @loader.command()
    async def todo(self, message):
        "<действие> <фраза>- совмещает описание окружающей обстановки, действие от 3го лица (см. описание .do) с одновременной фразой своего персонажа. Пример использования: .todo Спокойной ночи. засыпая"
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, self.strings("not_args"))
        arg1, arg2 = args[0], " ".join(args[1:])
        
        me = self.client.hikka_me
        nickname = f'{me.first_name} {me.last_name if me.last_name else ""}'
        
        await utils.answer(message, f"<emoji document_id=5785175271011259591>🌀</emoji> <i>'{arg1}', - сказал </i><b>{nickname}</b>, <i>{arg2}.</i>")
    
