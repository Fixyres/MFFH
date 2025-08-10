#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                  

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule
# requires: asyncio

from .. import loader, utils
import asyncio


@loader.tds
class MultiUnloadModule(loader.Module):
    """Unloads several modules at once with one command"""

    strings = {
        "name": "MultiUnloadModule",
        "processing": "<b>Выгружаю модули...</b>",
        "done": "<b>Выгрузка завершена.</b>",
        "no_modules": "<b>Укажите хотя бы один модуль.</b>",
        "progress": "<b>Выгружаю ({current}/{total}):</b> <code>{module}</code>",
        "error": "<b>Ошибка при выгрузке {mod}:</b> {e}",
    }

    strings_ru = {
        "processing": "<b>Выгружаю модули...</b>",
        "done": "<b>Выгрузка завершена.</b>",
        "no_modules": "<b>Укажите хотя бы один модуль.</b>",
        "progress": "<b>Выгружаю ({current}/{total}):</b> <code>{module}</code>",
        "error": "<b>Error unloading {mod}:</b> {e}",
    }

    @loader.command(ru_doc="{модули через запятую} — выгрузить несколько модулей")
    async def mulm(self, message):
        """{modules separated by commas} - unload multiple modules"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_modules"))
            return

        modules = [m.strip() for m in args.split(",") if m.strip()]
        if not modules:
            await utils.answer(message, self.strings("no_modules"))
            return

        total = len(modules)

        for i, mod in enumerate(modules, start=1):
            await message.edit(self.strings("progress").format(
                current=i,
                total=total,
                module=mod
            ))
            try:
                await self.invoke("unloadmod", mod, message=message)
            except ValueError as e:
                await message.edit(self.strings("error").format(mod=mod, e=e))
                await asyncio.sleep(1)

        await message.edit(self.strings("done"))