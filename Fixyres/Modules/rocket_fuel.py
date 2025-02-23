from .. import loader
from telethon.tl.types import Message
from telethon.tl.custom import Button
import asyncio

@loader.tds
class RocketFuelModule(loader.Module):
    """Модуль для автоматизації дій з кнопками у @coloniZERObot з кількістю повторів"""
    strings = {"name": "RocketFuel"}

    async def rocketauto_cmd(self, message: Message):
        """Автоматизує дії з кнопками: .rocketauto <кількість повторів>"""
        # Витягуємо аргумент з кількістю повторів
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            repeat_count = int(args[1])  # Кількість повторів
        else:
            repeat_count = 1  # За замовчуванням повторюємо один раз

        # Початок циклу
        for i in range(repeat_count):
            await message.edit(f"🚀 Виконую цикл {i + 1}/{repeat_count}...")

            # Крок 1: Відправляємо "юз карта"
            await message.client.send_message(message.chat_id, "юз карта")
            await asyncio.sleep(2)  # Невелика затримка

            # Крок 2: Відправляємо /rocket
            bot_username = "coloniZERObot"  # Юзернейм бота
            await message.client.send_message(message.chat_id, "/rocket")

            try:
                # Крок 3: Чекаємо появи кнопок
                response = await message.client.wait_for_message(
                    from_user=bot_username,  # Очікуємо відповідь від бота
                    chat_id=message.chat_id,  # У тому самому чаті
                    timeout=30  # Максимальний час очікування (30 секунд)
                )

                # Знаходимо кнопку "поповнити паливо"
                fuel_button = self.find_button(response, "поповнити паливо")
                if fuel_button:
                    await message.respond(f"⛽ Натискаю 'поповнити паливо' (цикл {i + 1})...")
                    await response.click(fuel_button)

                    # Крок 4: Чекаємо, поки бот завершить дію
                    await asyncio.sleep(5)  # Невелика затримка

                    # Чекаємо на оновлення кнопок
                    updated_response = await message.client.wait_for_message(
                        from_user=bot_username,
                        chat_id=message.chat_id,
                        timeout=30
                    )

                    # Знаходимо кнопку "запуск"
                    launch_button = self.find_button(updated_response, "запуск")
                    if launch_button:
                        await message.respond(f"🚀 Натискаю 'запуск' (цикл {i + 1})...")
                        await updated_response.click(launch_button)
                        await message.respond(f"✅ Ракета запущена (цикл {i + 1})!")
                    else:
                        await message.respond(f"❌ Не вдалося знайти кнопку 'запуск' (цикл {i + 1}).")
                else:
                    await message.respond(f"❌ Не вдалося знайти кнопку 'поповнити паливо' (цикл {i + 1}).")
            except asyncio.TimeoutError:
                await message.respond(f"❌ Час очікування відповіді від бота закінчився (цикл {i + 1}).")

        await message.respond(f"✅ Цикли виконано {repeat_count} разів!")

    def find_button(self, message: Message, button_text: str):
        """Шукає кнопку за текстом у повідомленні"""
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if isinstance(button, Button) and button_text in button.text.lower():
                        return button
        return None
