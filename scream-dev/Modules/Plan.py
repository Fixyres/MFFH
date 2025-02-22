#           __..--''``---....___   _..._    __
# /// //_.-'    .-/";  `        ``<._  ``.''_ `. / // /
#///_.-' _..--.'_    \                    `( ) ) // //
#/ (_..-' // (< _     ;_..__               ; `' / ///
# / // // //  `-._,_)' // / ``--...____..-' /// / //
# 🐈 Module writed @ScreamDev 
# 👌 Channel @ScreamModules
# 🧨 Blog: @ScreamDevBlog
# meta developer: @ScreamDev

import datetime
import logging
import asyncio
from telethon.tl.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

class PlanManager(loader.Module):
    strings = {
        "name": "PlanManager",
        "description": "Менеджер планов от @ScreamDev",
        "plans_empty": "❌ <b>Список планов пуст.</b>",
        "plans_list": "📝 <b>Список планов:</b>\n{}",
        "plan_added": "✅ <b>План добавлен:</b> {}",
        "plan_deleted": "🗑️ <b>План удалён:</b> {}",
        "plan_crossed": "✍️ <b>План вычеркнут:</b> {}",
        "invalid_plan_number": "⚠️ <b>Неверный номер плана.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "timezone",
                "0",
                lambda: "Используйте 1, -1, -3 и т. д. для установки смещения времени.",
            ),
        )
        self.plans = []  # Список оригинальных планов
        self.crossed_plans = []  # Список уже вычеркнутых планов
        asyncio.create_task(self.start_cleanup())

    async def start_cleanup(self):
        """Запускает процесс очистки планов"""
        while True:
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=int(self.config["timezone"]))))
            if now.hour == 0 and now.minute == 0:
                self.plans.clear()  # Очистка планов
                self.crossed_plans.clear()  # Очистка списка вычеркнутых планов
                logger.info("Список планов очищен.")
            await asyncio.sleep(60)  # Проверка каждый 60 секунд

    @loader.command(command="makeplan")
    async def makeplan(self, message: Message):
        """Добавляет новый план"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "⚠️ <b>Вы должны указать план.</b>")
            return
        
        self.plans.append(args)  # Новые планы добавляются в оригинальный список
        await utils.answer(message, self.strings["plan_added"].format(args))

    @loader.command(command="plan")
    async def show_plans(self, message: Message):
        """Показывает список планов"""
        if not self.plans and not self.crossed_plans:
            await utils.answer(message, self.strings["plans_empty"])
            return
        
        formatted_plans = "\n".join(
            f"{i + 1}. {plan}" for i, plan in enumerate(self.plans)
        )
        formatted_crossed = "\n".join(
            f"{i + 1 + len(self.plans)}. <s>{plan}</s>" for i, plan in enumerate(self.crossed_plans)
        )
        full_plan_list = formatted_plans + "\n" + formatted_crossed if formatted_crossed else formatted_plans
        await utils.answer(message, self.strings["plans_list"].format(full_plan_list))

    @loader.command(command="cross_plan")
    async def cross_plan(self, message: Message):
        """Вычеркивает план из списка"""
        args = utils.get_args_raw(message)
        if not args.isdigit() or int(args) < 1 or int(args) > len(self.plans):
            await utils.answer(message, self.strings["invalid_plan_number"])
            return
        
        index = int(args) - 1
        crossed_plan = self.plans.pop(index)  # Убираем план из оригинального списка
        self.crossed_plans.append(crossed_plan)  # Добавляем его в список вычеркнутых
        await utils.answer(message, self.strings["plan_crossed"].format(crossed_plan))

    @loader.command(command="delplan")
    async def del_plan(self, message: Message):
        """Удаляет план из списка"""
        args = utils.get_args_raw(message)
        if not args.isdigit() or int(args) < 1 or int(args) > len(self.plans):
            await utils.answer(message, self.strings["invalid_plan_number"])
            return

        index = int(args) - 1
        deleted_plan = self.plans.pop(index)
        await utils.answer(message, self.strings["plan_deleted"].format(deleted_plan))
