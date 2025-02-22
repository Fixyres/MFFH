# meta developer: @codeer_kot
from .. import loader, utils
import asyncio

@loader.tds
class KotBioWarsModule(loader.Module):
    "модуль который отправляет боту @KOTBioWarsBot запрос и получает ответ."
    strings = {
        "name": "KotBioWars",
        "no_text": "❌ Пожалуйста, укажите текст после команды.",
        "timeout": "⏱️ Ответ от @KotBioWarsBot не получен в течение 5 секунд.",
    }

    @loader.command()
    async def кcmd(self, message):
        " - отправить запрос боту"
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_text"))
            return

        bot_username = "@KotBioWarsBot"
        await utils.answer(message, f"⏳ Отправляем запрос боту {bot_username}...")

        try:
            async with message.client.conversation(bot_username, timeout=5) as conv:
                await conv.send_message(args)
                response = await conv.get_response()
                await utils.answer(
                    message,
                    f"<b>Запрос:</b>\n<code>{utils.escape_html(args)}</code>\n\n"
                    f"<b>Ответ бота:</b>\n<pre>{utils.escape_html(response.text)}</pre>",
                )
        except asyncio.TimeoutError:
            await utils.answer(message, self.strings("timeout"))
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {str(e)}")
