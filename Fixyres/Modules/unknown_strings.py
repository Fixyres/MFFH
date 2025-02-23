# _  __  ___   ____  _   _ 
# | |/ / | __| |_  / | | | |
# | ' <  | _|   / /  | |_| |
# |_|\_\ |___| /___|  \___/
#
#  __  __    ___    ___    ___ 
# |  \/  |  / _ \  |   \  / __|
# | |\/| | | (_) | | |) | \__ \
# |_|  |_|  \___/  |___/  |___/
#

# meta developer: @dummykezu

from .. import loader, utils

@loader.tds
class UnknownStringsMod(loader.Module):
    strings = {
        "name": "UnknownStrings",
        "cfg_desc": "Enable or disable the UnknownStrings",
    }
    
    strings_ru = {
        "cfg_desc": "Включить или отключить UnknownStrings",
    }
    
    strings_ua = {
        "cfg_desc": "Увімкнути або вимкнути UnknownStrings",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "enabled",
                True,
                "Enable or disable the UnknownStrings mode",
                validator=loader.validators.Boolean(),
            ),
        )

    async def watcher(self, message):
        if not self.config["enabled"]:
            return
        
        if message.out and not message.text.startswith((self.get_prefix())):
            await message.edit("Unknown strings.")