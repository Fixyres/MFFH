from hikkatl.types import Message
from .. import loader, utils
import genshin
from genshin.models.hoyolab import GenshinAccount
from .. import main
import logging
import random

"""
    ███    ███ ██    ██ ██████  ██    ██ ██       ██████  ███████ ███████
    ████  ████ ██    ██ ██   ██ ██    ██ ██      ██    ██ ██      ██  
    ██ ████ ██ ██    ██ ██████  ██    ██ ██      ██    ██ ███████ █████
    ██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██    ██      ██ ██  
    ██      ██  ██████  ██   ██  ██████  ███████  ██████  ███████ ███████ 


    Module name
    📜 Licensed under the GNU AGPLv3	
"""

# meta banner: link
# meta desc: desc
# meta developer: @BruhHikkaModules

# requires: genshin

logger = logging.getLogger(__name__)


@loader.tds
class Genshin(loader.Module):
    """Module for Genshin"""

    strings = {"name": "Genshin"}
    strings_ru = {
        "_cls_doc": "Модуль для геншина",
        "wait_auth": "<emoji document_id=5213452215527677338>⏳</emoji> <b>Идёт повторная авторизация...</b>",
        "wait_promo": "<emoji document_id=5213452215527677338>⏳</emoji> <b>Идёт получение промокода...</b>",
        "game_accounts_template": "<b><emoji document_id=5301050457236445678>👀</emoji> Genshin:</b>"
                         "\n<b>UID:</b> <code>{uid}</code>"
                         "\n<b>Ранг приключений:</b> <code>{level}</code>"
                         "\n<b>Ник:</b> <code>{nickname}</code>",
        "authed": "<emoji document_id=5361962439342563894>✅</emoji> <b>Авторизован!</b>",
        "promo_activated": "<emoji document_id=5361962439342563894>✅</emoji> <b><code>{promocode}</code> Активирован!</b>"
    }

    async def client_ready(self, db, client):
        self.hoyo_client = genshin.Client(
            {
                "cookie_token": self.config["cookie_token"],
                "ltuid_v2": int(self.config["ltuid"]), 
                "ltoken_v2": self.config["ltoken"]
            }
        )

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ltoken",
                "v2_UGA879KPhsRM18g23GMCXV80913nbMXOALZGOurfv",
                "Set your ltoken in Hoyoverse to login",
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "ltuid",
                "123456789",
                "Set your ltuid in Hoyoverse to login",
                validator=loader.validators.Hidden(loader.validators.Integer()),
            ),
            loader.ConfigValue(
                "cookie_token",
                "None",
                "Set your cookie token for promocodes",
                validator=loader.validators.Hidden()
            )
        )

    @loader.command(
        ru_doc=" - Поменяли данные для входа или хотите авторизироваться? Вам нужно перезагрузить модуль",
    )
    async def greload(self, message: Message):
        """- You change credentials or want auth? You need to reload module"""

        await utils.answer(message, self.strings["wait_auth"])
        self.hoyo_client = genshin.Client(
            {
                "cookie_token": self.config["cookie_token"],
                "ltuid_v2": int(self.config["ltuid"]), 
                "ltoken_v2": self.config["ltoken"]
            }
        )
        await utils.answer(message, self.strings["authed"])

    @loader.command(
        ru_doc=" - Показывает все аккаунты в Genshin"
    )
    async def hoyoaccounts(self, message: Message):
        ''' - Shows all accounts in Genshin'''
        accounts = await self.hoyo_client.get_game_accounts()
        genshin = []
        for account in accounts:
            if isinstance(account, GenshinAccount):
                genshin.append(account.dict())
        output = ""
        for account in genshin:
            output += self.strings["game_accounts_template"].format(**account)

        
        await utils.answer(
            message, 
            output
        )

    @loader.command(
        ru_doc=" [Промокод] - Активирует промокод"
    )
    async def activatepromo(self, message: Message):
        args = utils.get_args_raw(message)

        await self.hoyo_client.redeem_code(args, game="genshin")

        await utils.answer(
            message, 
            self.strings["promo_activated"].format(
                promocode=args
            )
        )
        

