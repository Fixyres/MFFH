# meta developer: @ManulMods

from hikkatl.types import Message
from hikkatl.errors import RPCError
from .. import loader, utils
import requests
import logging
import time

logger = logging.getLogger(__name__)

@loader.tds
class CurrencyConverterMod(loader.Module):
    """Модуль для просмотра и конвертации валют (USD, RUB, EUR, UAH, KZT, CNY, TON)"""
    strings = {
        "name": "CurrencyConverter",
        "rates": "<emoji document_id=5431577498364158238>📊</emoji> <b>Текущие курсы ({} {}):</b>\n{}",
        "converted": "<emoji document_id=5283232570660634549>🪙</emoji> <b>Результат:</b> {} {} = {} {}",
        "error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ошибка:</b> {}",
        "updating": "<emoji document_id=5292226786229236118>🔄</emoji> Обновляю курсы валют...",
        "updated": "<emoji document_id=5220219696711736568>✔️</emoji> Курсы успешно обновлены!",
        "available_currencies": "Доступные валюты: доллар/USD, руб/RUB, евро/EUR, гривна/UAH, тенге/KZT, юань/CNY, ton/TON",
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
            "гривна": 38.0,
            "uah": 38.0,
            "тенге": 450.0,
            "kzt": 450.0,
            "юань": 7.2,
            "cny": 7.2,
            "ton": 3.3,  # 1 TON = 3.3 USD (прямой курс)
            "toncoin": 3.3,
        }
        self.last_update = 0

    async def client_ready(self, client, db):
        self._client = client
        await self.update_rates()

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
            
            # Обновляем курсы
            self.rates.update({
                "доллар": 1.0,
                "usd": 1.0,
                "руб": data["rates"]["RUB"],
                "rub": data["rates"]["RUB"],
                "евро": data["rates"]["EUR"],
                "eur": data["rates"]["EUR"],
                "гривна": data["rates"]["UAH"],
                "uah": data["rates"]["UAH"],
                "тенге": data["rates"]["KZT"],
                "kzt": data["rates"]["KZT"],
                "юань": data["rates"]["CNY"],
                "cny": data["rates"]["CNY"],
                "ton": ton_data["the-open-network"]["usd"],  # Прямой курс 1 TON = X USD
                "toncoin": ton_data["the-open-network"]["usd"],
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
        return f"{value:.4f}".replace(".", ",").rstrip("0").rstrip(",")

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
        
        # Сортируем валюты для красивого вывода
        currencies_order = ["доллар", "евро", "руб", "гривна", "тенге", "юань", "ton"]
        formatted = []
        for currency in currencies_order:
            if currency == "ton":
                value = self.rates[currency]  # Для TON показываем прямой курс (1 TON = X USD)
                formatted.append(f"TON {self.format_value(value)} USD")
            else:
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
            
            valid_currencies = ["доллар", "usd", "руб", "rub", "евро", "eur", 
                              "гривна", "uah", "тенге", "kzt", "юань", "cny",
                              "ton", "toncoin"]
            
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
            
            # Нормализация названий валют
            currency_map = {
                "usd": "доллар",
                "rub": "руб",
                "eur": "евро",
                "uah": "гривна",
                "kzt": "тенге",
                "cny": "юань",
                "toncoin": "ton"
            }
            from_cur = currency_map.get(from_cur, from_cur)
            to_cur = currency_map.get(to_cur, to_cur)
            
            # Логика конвертации
            if from_cur == to_cur:
                result = amount
            elif from_cur == "ton":
                # TON → Любая валюта: TON → USD → Валюта
                usd_amount = amount * self.rates["ton"]
                if to_cur == "доллар":
                    result = usd_amount
                else:
                    result = usd_amount * self.rates[to_cur]
            elif to_cur == "ton":
                # Любая валюта → TON: Валюта → USD → TON
                if from_cur == "доллар":
                    usd_amount = amount
                else:
                    usd_amount = amount / self.rates[from_cur]
                result = usd_amount / self.rates["ton"]
            else:
                # Фиат → Фиат через USD
                usd_amount = amount / self.rates[from_cur]
                result = usd_amount * self.rates[to_cur]
            
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
