# meta developer: @YA_ManuI

import requests
from hikkatl.types import Message
from hikkatl.tl.types import DocumentAttributeVideo
from .. import loader, utils

@loader.tds
class ImgurVideoUploaderMod(loader.Module):
    """Загружает видео в Imgur по реплаю и возвращает ссылку. Не забудьте зайти в cfg"""
    strings = {"name": "ImgurVideoUploader"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "client_id",
                "",
                lambda: "Client-ID от Imgur API (регистрация: https://api.imgur.com/oauth2/addclient)",
                validator=loader.validators.Hidden(),
            ),
        )
        super().__init__()

    @loader.command()
    async def ivup(self, message: Message):
        """- загрузить видео из реплая"""
        try:
            if not self.config["client_id"]:
                await utils.answer(message, "❌ Установи Client-ID через: .cfg ImgurVideoUploader. Гайд по быстрому получению @GaidImgur")
                return

            reply = await message.get_reply_message()
            if not reply or not reply.media:
                await utils.answer(message, "❌ Ответь на видео!")
                return

            if not reply.document or not any(
                isinstance(a, DocumentAttributeVideo)
                for a in reply.document.attributes
            ):
                await utils.answer(message, "❌ Это не видео!")
                return

            video = await reply.download_media(bytes)
            if len(video) > 200 * 1024 * 1024:
                await utils.answer(message, "❌ Максимальный размер 200MB!")
                return

            await utils.answer(message, "⏳ Загружаю на Imgur...")

            response = requests.post(
                "https://api.imgur.com/3/upload",
                headers={"Authorization": f"Client-ID {self.config['client_id']}"},
                files={"video": video},
                timeout=15
            )

            if response.status_code == 503:
                raise requests.RequestException("Imgur временно недоступен (503)")

            try:
                data = response.json()
            except Exception as e:
                error_text = f"Ошибка JSON: {e}\nОтвет: {response.text[:150]}"
                raise requests.RequestException(error_text)

            if data.get("success", False) and response.status_code == 200:
                await utils.answer(message, f"✅ Ссылка: {data['data']['link']}")
            else:
                error_msg = data.get("data", {}).get("error", "Неизвестная ошибка")
                await utils.answer(message, f"❌ Ошибка: {error_msg}")

        except requests.RequestException as e:
            await utils.answer(message, f"🌐 Ошибка сети: {str(e)}")
        except Exception as e:
            await utils.answer(message, f"🔥 Ошибка: {repr(e)}")