from hikkatl.types import Message
from .. import loader, utils

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 

                                   
    Module Name
"""

# scopes:

# 🔒      Licensed under the GNU AGPLv3

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules


@loader.tds
class MyModule(loader.Module):
    """My module"""

    strings = {"name": "MyModule", "hello": "Hello world!"}
    strings_ru = {"hello": "Привет мир!"}
    strings_es = {"hello": "¡Hola mundo!"}
    strings_de = {"hello": "Hallo Welt!"}

    @loader.command(
        ru_doc="Привет мир!",
        es_doc="¡Hola mundo!",
        de_doc="Hallo Welt!",
        # ...
    )
    async def helloworld(self, message: Message):
        """Hello world"""
        await utils.answer(message, self.strings("hello"))
