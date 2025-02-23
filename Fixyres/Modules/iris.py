# -*- coding: utf-8 -*-
# Hikka Userbot Module
# Модуль для просмотра мешка в Irise by @zhako_o7 xd

from .. import loader, utils
import asyncio  # Для ожидания ответа

class IrisMesh(loader.Module):
    """Модуль для просмотра мешка в Irise by @zhako_o7"""
    strings = {"name": "IrisMesh"}

    async def бcmd(self, message):
        """Используйте .б как ответ на сообщение"""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("❌ Команда должна быть ответом на сообщение!")
            return

        # Получаем информацию о пользователе
        user = reply.sender
        if not user:
            await message.edit("❌ Не удалось получить информацию о пользователе!")
            return

        # Используем username, если есть, иначе ID в формате @ID
        username = f"@{user.username}" if user.username else f"@{user.id}"
        bag_message = f"мешок {username}"
        
        # Изменяем сообщение на "Ожидайте"
        await message.edit("⏳ Ожидайте...")

        # Отправляем сообщение в личку бота
        await message.client.send_message("@iris_black_bot", bag_message)

        # Устанавливаем время ожидания для ответа от бота (10 секунд)
        try:
            for _ in range(10):  # Цикл ожидания, максимум 10 итераций по 1 секунде
                await asyncio.sleep(1)  # Ждем 1 секунду перед следующей проверкой
                messages = await message.client.get_messages("@iris_black_bot", limit=5)

                # Проверяем последние сообщения
                for msg in messages:
                    if msg.sender_id == (await message.client.get_entity("@iris_black_bot")).id:
                        # Убедились, что сообщение от бота
                        if "не разрешал заглядывать" in msg.text.lower():
                            await message.edit("❌ Мешок закрыт!")
                        else:
                            await message.edit(msg.text)
                        return  # Прерываем цикл, так как получили ответ

            # Если бот не ответил в течение времени
            await message.edit("❌ Бот не ответил!")
        except asyncio.TimeoutError:
            # Если тайм-аут, сообщаем, что бот не ответил
            await message.edit("❌ Бот не ответил в течение заданного времени.")


