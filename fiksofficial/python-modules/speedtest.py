# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule
# requires: speedtest-cli

import speedtest
from .. import loader

class SpeedTestMod(loader.Module):
    """Модуль для проверки скорости интернета"""

    strings = {"name": "SpeedTest"}

    async def speedcmd(self, message):
        """Запускает тест скорости интернета"""
        msg = await message.edit("Запускаем Speedtest... 🏁")

        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000  # Мбит/с
            upload = st.upload() / 1_000_000      # Мбит/с
            ping = st.results.ping

            await msg.edit(
                f"<emoji document_id=5325547803936572038>✨</emoji> <b>Speedtest завершён!</b> <emoji document_id=5325547803936572038>✨</emoji>\n\n"
                f"<b>Ping:</b> <i>{ping:.2f} ms</i>\n"
                f"<emoji document_id=6041730074376410123>📥</emoji> <b>Загрузка:</b> <i>{download:.2f} Mbps</i>\n"
                f"<emoji document_id=6041730074376410123>📤</emoji> <b>Отдача:</b> <i>{upload:.2f} Mbps</i>",
                parse_mode="HTML"
            )
        except Exception as e:
            await msg.edit(f"<b>Ошибка при выполнении Speedtest:</b>\n<code>{e}</code>")
