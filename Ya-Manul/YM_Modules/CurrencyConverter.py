#meta developer: @ManulMods

from hikkatl.types import Message
from hikkatl.errors import RPCError
from .. import loader, utils
import requests
import logging
import time

logger = logging.getLogger(__name__)

@loader.tds
class CurrencyConverterMod(loader.Module):
    """Модуль для просмотра и конвертации валют (USD, RUB, EUR, TON)"""
    strings = {
        "name": "CurrencyConverter",
        "rates": "📊 <b>Текущие курсы ({} {}):</b>\n{}",
        "converted": "💱 <b>Результат:</b> {} {} = {} {}",
        "error": "🚫 <b>Ошибка:</b> {}",
        "updating": "🔄 Обновляю курсы валют...",
        "updated": "✅ Курсы успешно обновлены!",
        "available_currencies": "Доступные валюты: доллар/USD, руб/RUB, евро/EUR, ton/TON",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "base_currency",
                "USD",
                "Базовая валюта для отображения курсов",
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "cache_time",
                3600,
                "Время кэширования курсов (в секундах)",
                validator=loader.validators.Integer(minimum=60),
            ),
        )
        self.rates = {
            "доллар": 1.0,
            "usd": 1.0,
            "руб": 80.0,
            "rub": 80.0,
            "евро": 0.92,
            "eur": 0.92,
            "ton": 1/3.3,  # 1 TON = 3.3 USD → 1 USD = 1/3.3 TON
            "toncoin": 1/3.3,
        }
        self.last_update = 0

    async def update_rates(self):
        """Обновление курсов валют"""
        try:
            # Получаем курсы фиатных валют
            response = await utils.run_sync(
                requests.get,
                f"https://api.exchangerate-api.com/v4/latest/{self.config['base_currency']}"
            )
            data = response.json()
            
            # Получаем курс TON в USD
            ton_response = await utils.run_sync(
                requests.get,
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "the-open-network",
                    "vs_currencies": "usd",
                    "precision": 8
                }
            )
            ton_data = ton_response.json()
            ton_price = ton_data["the-open-network"]["usd"]
            
            # Правильное соотношение: 1 TON = X USD → 1 USD = 1/X TON
            self.rates.update({
                "доллар": 1.0,
                "usd": 1.0,
                "руб": data["rates"]["RUB"],
                "rub": data["rates"]["RUB"],
                "евро": data["rates"]["EUR"],
                "eur": data["rates"]["EUR"],
                "ton": 1/ton_price,  # Фиксируем правильное соотношение
                "toncoin": 1/ton_price,
            })
            self.last_update = time.time()
            return True
            
        except Exception as e:
            logger.exception("Ошибка при обновлении курсов")
            return False

    def format_value(self, value):
        """Форматирование числового значения"""
        if abs(value - round(value)) < 0.0001:
            return str(round(value))
        return f"{value:.8f}".replace(".", ",").rstrip("0").rstrip(",")

    @loader.command()
    async def kurs(self, message: Message):
        """Показать текущие курсы валют"""
        args = utils.get_args_raw(message)
        amount = float(args.replace(",", ".")) if args and args.replace(",", "").replace(".", "").isdigit() else 1.0
        
        if time.time() - self.last_update > self.config["cache_time"]:
            if not await self.update_rates():
                await utils.answer(
                    message,
                    self.strings("error").format("Не удалось обновить курсы (используются кэшированные)")
                )
        
        formatted = []
        for currency in ["доллар", "руб", "евро", "ton"]:
            value = self.rates[currency] * amount
            formatted.append(f"{currency} {self.format_value(value)}")
        
        await utils.answer(
            message,
            self.strings("rates").format(
                self.format_value(amount),
                self.config["base_currency"],
                "\n".join(formatted)
            )
        )

    @loader.command()
    async def convert(self, message: Message):
        """Конвертировать валюту"""
        args = utils.get_args_raw(message).lower().split()
        if len(args) != 3:
            await utils.answer(
                message,
                self.strings("error").format(
                    f"Неверный формат команды. Используйте: .convert <amount> <from> <to>\n"
                    f"{self.strings['available_currencies']}"
                )
            )
            return
        
        try:
            amount = float(args[0].replace(",", "."))
            from_cur = args[1].replace("toncoin", "ton")
            to_cur = args[2].replace("toncoin", "ton")
            
            valid_currencies = ["доллар", "usd", "руб", "rub", "евро", "eur", "ton", "toncoin"]
            if from_cur not in valid_currencies or to_cur not in valid_currencies:
                await utils.answer(
                    message,
                    self.strings("error").format(
                        f"Неизвестная валюта. {self.strings['available_currencies']}"
                    )
                )
                return
            
            if time.time() - self.last_update > self.config["cache_time"]:
                if not await self.update_rates():
                    await utils.answer(
                        message,
                        self.strings("error").format("Не удалось обновить курсы (используются кэшированные)")
                    )
            
            # Правильная конвертация через USD
            if from_cur in ["ton", "toncoin"]:
                usd_amount = amount * (1 / self.rates["ton"])  # TON → USD
            else:
                usd_amount = amount / self.rates[from_cur]    # Фиат → USD
                
            if to_cur in ["ton", "toncoin"]:
                result = usd_amount * self.rates["ton"]      # USD → TON
            else:
                result = usd_amount * self.rates[to_cur]     # USD → Фиат
            
            await utils.answer(
                message,
                self.strings("converted").format(
                    self.format_value(amount),
                    from_cur,
                    self.format_value(result),
                    to_cur
                )
            )
        except ValueError:
            await utils.answer(
                message,
                self.strings("error").format("Неверный формат числа")
            )
        except Exception as e:
            await utils.answer(
                message,
                self.strings("error").format(f"Ошибка: {str(e)}")
            )

    @loader.command()
    async def updatekurs(self, message: Message):
        """Обновить курсы валют вручную"""
        await utils.answer(message, self.strings("updating"))
        if await self.update_rates():
            await utils.answer(message, self.strings("updated"))
        else:
            await utils.answer(
                message,
                self.strings("error").format("Не удалось обновить курсы")
            ) 
