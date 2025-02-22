# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель модуля.
from .. import loader, utils
import asyncio
from telethon.errors import FloodWaitError
from telethon.tl.types import Document, DocumentAttributeSticker, DocumentAttributeImageSize, DocumentAttributeFilename, InputStickerSetID

@loader.tds
class KOTFLModMod(loader.Module):
    """Модуль для проверки на флуд-вейты"""
    strings = {"name": "KOTFLMod"}

    async def client_ready(self, client, db):
        self.client = client

    async def flcmd(self, message):
        """Проверить флуд-вейты"""
        await message.edit("<b>Запускаю проверку на флуд-вейты...</b>")
        delay = 0.1
        errors = []
        test_messages = []

        try:
            for i in range(10):
                try:
                    test_msg = await self.client.send_message(
                        "me", f"Test message {i + 1}"
                    )
                    test_messages.append(test_msg)
                    await asyncio.sleep(delay)
                except FloodWaitError as e:
                    errors.append(f"Отправка сообщений: {str(e)}")
                    break

            try:
                test_photo = await self.client.send_file(
                    "me",
                    file="https://via.placeholder.com/300.png",
                    caption="Test Photo"
                )
                test_messages.append(test_photo)
                await asyncio.sleep(delay)
            except FloodWaitError as e:
                errors.append(f"Отправка фото: {str(e)}")

            try:
                test_gif = await self.client.send_file(
                    "me",
                    file="https://media.giphy.com/media/3o7aD6ZXaa5R3o2C7u/giphy.gif",
                    caption="Test GIF"
                )
                test_messages.append(test_gif)
                await asyncio.sleep(delay)
            except FloodWaitError as e:
                errors.append(f"Отправка GIF: {str(e)}")

            try:
                test_sticker = await self.client.send_file(
                    "me",
                    file=Document(
                        id=773947703670341889,
                        access_hash=3811948230390824482,
                        file_reference=b'\x01\x00\x03r\x01gm\xdd\xe2\n\x82\xe2cc\x11!\xc5t\xd9\x1a\xcf\xee\xb8\xb3h',
                        date=None,
                        mime_type='application/x-tgsticker',
                        size=7269,
                        dc_id=2,
                        attributes=[
                            DocumentAttributeImageSize(w=512, h=512),
                            DocumentAttributeSticker(
                                alt='👋',
                                stickerset=InputStickerSetID(
                                    id=773947703670341644,
                                    access_hash=-585463735839216136
                                ),
                                mask=False
                            ),
                            DocumentAttributeFilename(file_name='AnimatedSticker.tgs')
                        ]
                    ),
                    caption="Test Sticker"
                )
                test_messages.append(test_sticker)
                await asyncio.sleep(delay)
            except FloodWaitError as e:
                errors.append(f"Отправка стикера: {str(e)}")

            try:
                with open("test.txt", "w") as f:
                    f.write("Test file content")
                test_file = await self.client.send_file(
                    "me",
                    file="test.txt",
                    caption="Test File"
                )
                test_messages.append(test_file)
                await asyncio.sleep(delay)
            except FloodWaitError as e:
                errors.append(f"Отправка текстового файла: {str(e)}")
            finally:
                try:
                    import os
                    os.remove("test.txt")
                except Exception:
                    pass

            for msg in test_messages:
                try:
                    await msg.delete()
                except Exception:
                    pass

            if errors:
                await message.edit(
                    f"<b>Обнаружены флуд-вейты:</b>\n\n" + "\n".join(errors)
                )
            else:
                await message.edit("<b>Флуд-вейты не обнаружены.</b>")
        except Exception as e:
            await message.edit(f"Произошла ошибка: {e}")
