__version__ = (1, 0, 1)
# meta developer: @psyho_Kuznetsov

from .. import loader, utils
from telethon import types
import asyncio
import logging

logger = logging.getLogger(__name__)

@loader.tds
class HeartAnimationMod(loader.Module):
    """❤️ Анимация сердца и эффект печати текста"""

    strings = {
        "name": "Animation",
        "error": "❌ Произошла ошибка: {}"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "ANIMATION_SPEED", 0.5, 
            "ANIMATION_CYCLES", 3,
            "TEXT_SPEED", 0.3,  
        )

    async def client_ready(self, client, db):
        self._db = db
        self._client = client

    @loader.command(ru_doc="Создает анимированное сердце")
    async def h(self, message: types.Message):
        """Создает анимированное сердце"""
        try:
            hearts = ['♥️', '🧡', '💛', '💚', '🩵', '💙', '💜', '🤎', '🖤', '🩶']
            heart_pattern = [
                "🤍🤍🤍🤍🤍🤍🤍🤍🤍",
                "🤍🤍❤️❤️🤍❤️❤️🤍🤍",
                "🤍❤️❤️❤️❤️❤️❤️❤️🤍",
                "🤍❤️❤️❤️❤️❤️❤️❤️🤍",
                "🤍❤️❤️❤️❤️❤️❤️❤️🤍",
                "🤍🤍❤️❤️❤️❤️❤️🤍🤍",
                "🤍🤍🤍❤️❤️❤️🤍🤍🤍",
                "🤍🤍🤍🤍❤️🤍🤍🤍🤍",
                "🤍🤍🤍🤍🤍🤍🤍🤍🤍"
            ]

            msg = await utils.answer(message, "\n".join(heart_pattern))
            if isinstance(msg, (list, tuple, set)):
                msg = msg[0]

            animation_speed = self.config.get("ANIMATION_SPEED", 0.5)
            animation_cycles = self.config.get("ANIMATION_CYCLES", 3) 

            for _ in range(animation_cycles):
                for heart in hearts:
                    new_pattern = [row.replace('❤️', heart) for row in heart_pattern]
                    await msg.edit("\n".join(new_pattern))
                    await asyncio.sleep(animation_speed)

            await asyncio.sleep(0.5)
            await msg.delete()

        except Exception as e:
            logger.exception(e)
            await utils.answer(message, self.strings['error'].format(str(e)))

    @loader.command(ru_doc="Печатает текст с эффектом появления")
    async def p(self, message: types.Message):
        """Печатает текст с эффектом появления"""
        try:
            text = utils.get_args_raw(message)
            if not text:
                await utils.answer(message, "❌ Укажите текст для печати.")
                return

            msg = await utils.answer(message, "█")
            if isinstance(msg, (list, tuple, set)):
                msg = msg[0]

            text_speed = self.config.get("TEXT_SPEED", 0.3)
            if not isinstance(text_speed, (int, float)) or text_speed <= 0:
                text_speed = 0.3

            for i in range(1, len(text) + 1):
                partial_text = text[:i] + "█"
                await msg.edit(partial_text)
                await asyncio.sleep(text_speed)

            await msg.edit(text)

        except Exception as e:
            logger.exception(e)
            await utils.answer(message, self.strings['error'].format(str(e)))