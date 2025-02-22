# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель модуля.

from .. import loader, utils
import asyncio
import re
from datetime import datetime, timedelta

class KOTIrisTradeModule(loader.Module):
    """Модуль для автоматической торговли на Ирис-бирже"""
    strings = {"name": "KOTIrisTrade"}

    async def client_ready(self, client, db):
        self.client = client
        self.running = False
        self.db = db
        self.current_sell_price = None
        self.current_buy_price = None
        self.waiting_for_notification = False

    async def трдcmd(self, message):
        """Запускает торговый процесс"""
        self.running = True
        target_user_id = 5443619563
        await message.edit("🏁 Торговля запущена.")
        
        while self.running:
            try:
                if self.waiting_for_notification:
                    await asyncio.sleep(3)
                    continue

                await asyncio.sleep(3)
                response = await self.check_exchange(target_user_id)
                if response:
                    min_sell, max_buy = self.parse_exchange_data(response)
                    if min_sell is not None and max_buy is not None:
                        if self.current_sell_price and min_sell < self.current_sell_price:
                            await asyncio.sleep(3)
                            await self.client.send_message(target_user_id, ".биржа отменить все")
                            await asyncio.sleep(3)
                            self.current_sell_price = None
                            self.current_buy_price = None

                        if self.current_buy_price and max_buy > self.current_buy_price:
                            await asyncio.sleep(3)
                            await self.client.send_message(target_user_id, ".биржа отменить все")
                            await asyncio.sleep(3)
                            self.current_sell_price = None
                            self.current_buy_price = None

                        if not self.current_sell_price:
                            await asyncio.sleep(3)
                            new_sell_price = round(min_sell - 0.01, 2)
                            response = await self.send_trade_command(target_user_id, "продать", 999, new_sell_price)
                            if response and "В мешке нет золотых мандаринок" not in response.message:
                                if "⚖️ Ирис-биржа. Заявка на продажу от" in response.message:
                                    self.waiting_for_notification = True
                                    self.current_sell_price = new_sell_price
                                    continue

                        if not self.current_buy_price:
                            await asyncio.sleep(3)
                            new_buy_price = round(max_buy + 0.01, 2)
                            response = await self.send_trade_command(target_user_id, "купить", 999, new_buy_price)
                            if response and "Не удалось купить золотые мандаринки" not in response.message:
                                if "⚖️ Ирис-биржа. Заявка на покупку от" in response.message:
                                    self.waiting_for_notification = True
                                    self.current_buy_price = new_buy_price
                                    continue

                await asyncio.sleep(3)
                
            except Exception as e:
                await message.edit(f"❌ Ошибка: {str(e)}")
                await asyncio.sleep(3)

    async def стрдcmd(self, message):
        """Останавливает торговый процесс"""
        self.running = False
        self.current_sell_price = None
        self.current_buy_price = None
        self.waiting_for_notification = False
        await message.edit("🛑 Торговля остановлена.")

    async def check_exchange(self, user_id):
        """Проверка биржи"""
        try:
            async with self.client.conversation(user_id, timeout=30) as conv:
                await conv.send_message("биржа")
                response = await conv.get_response()
                return response
        except asyncio.TimeoutError:
            return None

    async def send_trade_command(self, user_id, action, amount, price):
        """Отправка торговой команды"""
        try:
            async with self.client.conversation(user_id, timeout=30) as conv:
                command = f".биржа {action} {amount} {price:.2f}"
                await conv.send_message(command)
                response = await conv.get_response()
                return response
        except asyncio.TimeoutError:
            return None

    def parse_exchange_data(self, message):
        """Парсинг данных биржи"""
        text = message.message
        text = text.replace(',', '.').replace('\xa0', ' ')

        sell_section = re.search(r"🔽 Заявки на продажу([\s\S]*?)🔼 Заявки на покупку", text)
        buy_section = re.search(r"🔼 Заявки на покупку([\s\S]*)", text)

        min_sell = None
        max_buy = None

        if sell_section:
            sell_prices = re.findall(r"(\d+\.\d+) мандаринок \|\s*\d+\s+голд", sell_section.group(1))
            sell_prices = [float(price) for price in sell_prices]
            if sell_prices:
                min_sell = min(sell_prices)

        if buy_section:
            buy_prices = re.findall(r"(\d+\.\d+) мандаринок \|\s*\d+\s+голд", buy_section.group(1))
            buy_prices = [float(price) for price in buy_prices]
            if buy_prices:
                max_buy = max(buy_prices)

        return min_sell, max_buy

    async def watcher(self, message):
        """Отслеживание уведомлений о покупке/продаже"""
        if not self.running:
            return
            
        if message.sender_id == 5443619563:
            if "⚖️ Ирис-биржа. Уведомление" in message.text:
                self.waiting_for_notification = False
                self.current_sell_price = None
                self.current_buy_price = None
                await asyncio.sleep(3)
                await self.check_exchange(5443619563)
