# ---------------------------------------------------------------------------------
#  /\_/\  
# ( o.o )  🔓 Module for Hikka userbot
#  > ^ <   
# ---------------------------------------------------------------------------------
# Name: CurrencyConverter
# Description: Конвертер валют (криптовалюты пока что не поддерживаются)
# Author: @OS7NT
# Commands:
# .con
# ---------------------------------------------------------------------------------

import aiohttp
from datetime import datetime
from .. import loader, utils

class CurrencyConverterMod(loader.Module):
    """Конвертер валют и криптовалют с актуальными курсами"""
    
    strings = {
        "name": "CurrencyConverter",
        "processing": "<b>📊 Получаю курсы валют...</b>",
        "error": "<b>❌ Ошибка при получении данных</b>",
        "invalid_args": "<b>❌ Неверный формат! Используйте: .con [сумма] [валюта]</b>\nПример: .con 1000 USD",
        "not_found": "<b>❌ Валюта не найдена!</b>"
    }

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        
    def __init__(self):
        self.currencies = {
            "USD": "🇺🇸", "EUR": "🇪🇺", "RUB": "🇷🇺",
            "UAH": "🇺🇦", "BYN": "🇧🇾", "KZT": "🇰🇿"
        }
        
        self.crypto = {
            "BTC": "₿", "ETH": "⟠", "TON": "💎",
            "USDT": "₮", "BNB": "🟡"
        }
        
    async def get_rates(self, base_currency: str):
        """Получение курсов валют через API"""
        try:
            # Используем API для фиатных валют
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.exchangerate-api.com/v4/latest/{base_currency}") as resp:
                    if resp.status == 200:
                        return await resp.json()
                        
            # Для крипты можно использовать например Coingecko API
            if base_currency in self.crypto:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"https://api.coingecko.com/api/v3/simple/price?ids={base_currency.lower()}&vs_currencies=usd,rub,byn") as resp:
                        if resp.status == 200:
                            return await resp.json()
                            
        except Exception:
            return None

    async def concmd(self, message):
        """Конвертирует валюту
        Использование: .con [сумма] [валюта]
        Пример: .con 1000 USD"""
        
        args = utils.get_args(message)
        if len(args) != 2:
            await message.edit(self.strings["invalid_args"])
            return

        try:
            amount = float(args[0])
            currency = args[1].upper()
        except ValueError:
            await message.edit(self.strings["invalid_args"])
            return

        await message.edit(self.strings["processing"])
        
        if currency not in self.currencies and currency not in self.crypto:
            await message.edit(self.strings["not_found"])
            return

        rates = await self.get_rates(currency)
        if not rates:
            await message.edit(self.strings["error"])
            return

        result = "<b>💱 Конвертация валют</b>\n\n"
        result += f"<b>Исходная сумма:</b> {amount:,.2f} {currency}\n\n"

        if currency in self.currencies:
            # Конвертация фиатных валют
            for target, flag in self.currencies.items():
                if target != currency:
                    converted = amount * rates['rates'].get(target, 0)
                    result += f"{flag} <b>{target}:</b> {converted:,.2f}\n"
                    
        elif currency in self.crypto:
            # Конвертация криптовалют
            crypto_prices = rates.get(currency.lower(), {})
            converted_usd = amount * crypto_prices.get('usd', 0)
            converted_rub = amount * crypto_prices.get('rub', 0)
            converted_byn = amount * crypto_prices.get('byn', 0)
            
            result += f"🇺🇸 <b>USD:</b> {converted_usd:,.2f}\n"
            result += f"🇷🇺 <b>RUB:</b> {converted_rub:,.2f}\n"
            result += f"🇧🇾 <b>BYN:</b> {converted_byn:,.2f}\n"

        result += f"\n<i>Обновлено: {datetime.now().strftime('%H:%M:%S')}</i>"
        
        await message.edit(result)