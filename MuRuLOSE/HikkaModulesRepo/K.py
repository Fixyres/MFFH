from hikkatl.types import Message
from .. import loader, utils
import logging

logger = logging.getLogger(__name__)

@loader.tds
class K(loader.Module):
    """K"""

    strings = {"name": "K", "K": "K"}
    
    async def client_ready(self, client, db):
        self._log_lib = await self.import_lib(
            "https://raw.githubusercontent.com/MuRuLOSE/HikkaModulesRepo/main/libaries/logs.py",
            suspend_on_error=True
        )
        self._log_handler = self._log_lib._log_handler
        logger.addHandler(self._log_handler)
        
    @loader.command()
    async def k(self, message: Message):
        """K"""
        raise Exception("Testing error handling")
        await utils.answer(message, "K")
        # why