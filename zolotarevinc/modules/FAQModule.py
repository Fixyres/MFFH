# meta pic: https://static.whypodg.me/mods!faqmodule.png
# meta banner: https://mods.whypodg.me/badges/faqmodule.jpg
# meta developer: @zolotarevxc
# scope: hikka_only
# scope: hikka_min 1.2.10

from .. import loader, utils

@loader.tds
class FAQModule(loader.Module):
    """Модуль FAQ для удобного общения с участниками"""

    strings = {
        "name": "FAQModule",
        "description": "Модуль для управления FAQ.",
        "developer": "Разработчик: @zolotarevxc 🌟",
        "helpfaq": """
📝 <b>Как использовать FAQ модуль:</b>

▫️ <b>.setfaq <вопрос>=<ответ></b> — Установите или обновите вопрос и ответ в FAQ.  
  Пример: .setfaq Как установить бота?=Для установки скачайте файл и следуйте инструкциям.

▫️ <b>.faq <вопрос></b> — Получите ответ на заданный вопрос из FAQ.  
  Пример: .faq Как установить бота?

▫️ <b>.helpfaq</b> — Показать помощь по использованию модуля FAQ.

💬 <b>FAQ поможет быстро отвечать на часто задаваемые вопросы и упростит взаимодействие с участниками.</b>
""",
    }

    def __init__(self):
        self.faq = {}  # Словарь для хранения вопросов и ответов

    async def setfaqcmd(self, message):
        """Добавление или обновление вопроса и ответа в FAQ."""
        args = utils.get_args_raw(message)

        if "=" not in args:
            return await message.edit(
                "<b>❌ Ошибка: Нужно указать вопрос и ответ через знак '='.</b>"
            )

        question, answer = args.split("=", 1)

        if question in self.faq:
            return await message.edit(f"<b>❌ Вопрос '{question}' уже существует.</b>")

        # Добавляем вопрос и ответ в словарь FAQ
        self.faq[question] = answer
        await message.edit(f"<b>✅ Вопрос и ответ успешно добавлены в FAQ:</b>\n<b>{question}</b>\n{answer}")

    async def faqcmd(self, message):
        """Получение ответа на вопрос из FAQ."""
        args = utils.get_args_raw(message)

        if not args:
            return await message.edit("<b>❌ Ошибка: Укажите вопрос.</b>")

        question = args
        answer = self.faq.get(question)

        if not answer:
            return await message.edit(f"<b>❌ Ответ на вопрос '{question}' не найден.</b>")

        await message.edit(f"<b>Ответ на вопрос '{question}':</b>\n{answer}")

    async def helpfaqcmd(self, message):
        """Показать информацию о том, как пользоваться FAQ модулем."""
        await message.edit(self.strings["helpfaq"])

    async def on_load(self):
        """При загрузке модуля выводим описание и информацию о разработчике"""
        await utils.answer(
            message,
            f"{self.strings['description']}\n{self.strings['developer']}\n\n{self.strings['helpfaq']}",
        )
