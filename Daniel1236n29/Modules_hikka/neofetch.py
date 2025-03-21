
# meta developer: @shrimp_mod
from telethon import events
from .. import loader, utils
import asyncio
import subprocess

@loader.tds
class NeofetchMod(loader.Module):
    """Модуль для отправки результата команды neofetch"""
    strings = {"name": "Neofetch",
               "neofetch_not_installed": "❌ Neofetch не установлен на этой системе."}

    async def neofcmd(self, message):
        """Отправляет результат выполнения команды neofetch"""
        try:
            process = await asyncio.create_subprocess_shell(
                "neofetch --stdout",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if stdout:
                await utils.answer(message, f"<code>{stdout.decode()}</code>")
            elif stderr:
                await utils.answer(message, self.strings["neofetch_not_installed"])
        except FileNotFoundError:
            await utils.answer(message, self.strings["neofetch_not_installed"])
