# чатгпт кормит, больные мозги тоже
#
# meta banner: https://0x0.st/s/gJtVZxi43-Zy4q2je-yx-A/8XdP.gif
# meta developer: @HikkaZPM
#
# The module is made as a joke, all coincidences are random :P
# 
#       кот вахуи
#       /\_____/\
#      /  o   o  \
#     ( ==  ^  == )
#      )         (
#     (           )
#    ( (  )   (  ) )
#   (__(__)___(__)__)
# 
# 
#
# based on: https://raw.githubusercontent.com/Fixyres/Modules/main/venom.py
from .. import loader, utils

@loader.tds
class okakMod(loader.Module):
    """окак"""

    strings = {
        "name": "окак"
    }

    async def okakcmd(self, m):
        """окак"""
        await utils.asyncio.sleep(1)
        self.db.set("okak", "on", not self.db.get("okak", "on", False))
        if self.db.get("okak", "on", False):
            await m.edit("<emoji document_id=5211078941153974712>😨</emoji>ACTIVATED")

    async def watcher(self, m):
        if self.db.get("okak", "on", False) and m.out:
            await m.edit("окак")
