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
    """Модуль для просмотра и конвертации валют с эмодзи"""
    strings = {
        "name": "CurrencyConverter",
        "rates": "<emoji document_id=5431577498364158238>📊</emoji> <b>Текущие курсы ({} {}):</b>\n{}",
        "converted": "<emoji document_id=5283232570660634549>🪙</emoji> <b>Результат:</b> {} {} = {} {}",
        "error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ошибка:</b> {}",
        "updating": "<emoji document_id=5292226786229236118>🔄</emoji> Обновляю курсы...",
        "updated": "<emoji document_id=5220219696711736568>✔️</emoji> Курсы успешно обновлены!",
        "available_currencies": (
            "Доступные валюты:\n"
            "<emoji document_id=5375129692380607677>💰</emoji> доллар/USD\n"
            "<emoji document_id=5375069159111537380>💰</emoji> евро/EUR\n"
            "<emoji document_id=5375606180347393942>💰</emoji> рубль/RUB\n"
            "<emoji document_id=5375281137222433818>💰</emoji> гривна/UAH\n"
            "<emoji document_id=5375328755524843717>💰</emoji> тенге/KZT\n"
            "<emoji document_id=5375173294888598829>💰</emoji> юань/CNY\n"
            "<emoji document_id=5372795957475820830>💰</emoji> злотый/PLN\n"
            "<emoji document_id=5289519973285257969>💰</emoji> BTC\n"
            "<emoji document_id=5289648693455119919>💰</emoji> TON\n"
            "<emoji document_id=5289904548951911168>💰</emoji> USDT"
        ),
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
        
        # Словарь эмодзи для валют (используем ваши точные эмодзи)
        self.currency_emojis = {
            "доллар": "<emoji document_id=5375129692380607677>💰</emoji>",
            "usd": "<emoji document_id=5375129692380607677>💰</emoji>",
            "руб": "<emoji document_id=5375606180347393942>💰</emoji>",
            "rub": "<emoji document_id=5375606180347393942>💰</emoji>",
            "евро": "<emoji document_id=5375069159111537380>💰</emoji>",
            "eur": "<emoji document_id=5375069159111537380>💰</emoji>",
            "гривна": "<emoji document_id=5375281137222433818>💰</emoji>",
            "uah": "<emoji document_id=5375281137222433818>💰</emoji>",
            "тенге": "<emoji document_id=5375328755524843717>💰</emoji>",
            "kzt": "<emoji document_id=5375328755524843717>💰</emoji>",
            "юань": "<emoji document_id=5375173294888598829>💰</emoji>",
            "cny": "<emoji document_id=5375173294888598829>💰</emoji>",
            "злотый": "<emoji document_id=5372795957475820830>💰</emoji>",
            "pln": "<emoji document_id=5372795957475820830>💰</emoji>",
            "btc": "<emoji document_id=5289519973285257969>💰</emoji>",
            "bitcoin": "<emoji document_id=5289519973285257969>💰</emoji>",
            "ton": "<emoji document_id=5289648693455119919>💰</emoji>",
            "toncoin": "<emoji document_id=5289648693455119919>💰</emoji>",
            "usdt": "<emoji document_id=5289904548951911168>💰</emoji>",
            "tether": "<emoji document_id=5289904548951911168>💰</emoji>",
        }
        
        # Словарь склонений валют
        self.currency_forms = {
            "доллар": ["доллар", "доллара", "долларов"],
            "руб": ["рубль", "рубля", "рублей"],
            "евро": ["евро", "евро", "евро"],
            "гривна": ["гривна", "гривны", "гривен"],
            "тенге": ["тенге", "тенге", "тенге"],
            "юань": ["юань", "юаня", "юаней"],
            "злотый": ["злотый", "злотых", "злотых"],
            "bitcoin": ["биткоин", "биткоина", "биткоинов"],
            "toncoin": ["тон", "тона", "тонов"],
            "tether": ["тезер", "тезера", "тезеров"],
        }
        
        self.rates = {
            # Фиатные валюты
            "доллар": 1.0, "usd": 1.0,
            "руб": 80.0, "rub": 80.0,
            "евро": 0.92, "eur": 0.92,
            "гривна": 38.0, "uah": 38.0,
            "тенге": 450.0, "kzt": 450.0,
            "юань": 7.2, "cny": 7.2,
            "злотый": 4.0, "pln": 4.0,
            
            # Криптовалюты
            "btc": 30000.0,
            "ton": 3.3, "toncoin": 3.3,
            "usdt": 1.0, "tether": 1.0,
        }
        self.last_update = 0

    def get_currency_display(self, currency: str, amount: float) -> str:
        """Возвращает валюту с эмодзи и правильным склонением"""
        amount = abs(amount)
        emoji = self.currency_emojis.get(currency, "")
        
        # Для криптовалют используем короткие названия
        if currency in ["btc", "ton", "usdt"]:
            return f"{emoji} {currency.upper()}"
            
        # Для фиатных валют определяем склонение
        forms = self.currency_forms.get(currency, [currency]*3)
        if amount % 10 == 1 and amount % 100 != 11:
            return f"{emoji} {forms[0]}"
        elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
            return f"{emoji} {forms[1]}"
        else:
            return f"{emoji} {forms[2]}"

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
            
            # Получаем курсы криптовалют
            crypto_response = await utils.run_sync(
                requests.get,
                "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": "bitcoin,the-open-network,tether",
                    "vs_currencies": "usd",
                    "precision": 8
                }
            )
            crypto_data = crypto_response.json()
            
            # Обновляем курсы
            self.rates.update({
                # Фиатные валюты
                "доллар": 1.0, "usd": 1.0,
                "руб": data["rates"]["RUB"], "rub": data["rates"]["RUB"],
                "евро": data["rates"]["EUR"], "eur": data["rates"]["EUR"],
                "гривна": data["rates"]["UAH"], "uah": data["rates"]["UAH"],
                "тенге": data["rates"]["KZT"], "kzt": data["rates"]["KZT"],
                "юань": data["rates"]["CNY"], "cny": data["rates"]["CNY"],
                "злотый": data["rates"]["PLN"], "pln": data["rates"]["PLN"],
                
                # Криптовалюты
                "btc": crypto_data["bitcoin"]["usd"],
                "ton": crypto_data["the-open-network"]["usd"],
                "toncoin": crypto_data["the-open-network"]["usd"],
                "usdt": crypto_data["tether"]["usd"],
                "tether": crypto_data["tether"]["usd"],
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
        
        # Группировка валют для вывода
        fiat_currencies = ["доллар", "евро", "руб", "гривна", "тенге", "юань", "злотый"]
        crypto_currencies = ["btc", "ton", "usdt"]
        
        formatted = []
        
        # Фиатные валюты
        formatted.append("\n<b>Фиатные валюты:</b>")
        for currency in fiat_currencies:
            value = self.rates[currency] * amount
            display = self.get_currency_display(currency, value)
            formatted.append(f"{display} {self.format_value(value)}")
        
        # Криптовалюты
        formatted.append("\n<b>Криптовалюты:</b>")
        for currency in crypto_currencies:
            value = self.rates[currency]  # Прямой курс (1 UNIT = X USD)
            display = self.get_currency_display(currency, value)
            formatted.append(f"{display} {self.format_value(value)}")
        
        await utils.answer(
            message,
            self.strings("rates").format(
                self.format_value(amount),
                self.get_currency_display(self.config["base_currency"].lower(), amount),
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
            from_cur = args[1]
            to_cur = args[2]
            
            # Нормализация названий
            currency_map = {
                # Фиатные валюты
                "доллар": "доллар", "доллара": "доллар", "долларов": "доллар", "доллар": "доллары",
                "usd": "доллар",
                "рубль": "руб", "рубля": "руб", "рублей": "руб", "руб": "руб", "рубли": "руб",
                "rub": "руб",
                "евро": "евро", "eur": "евро",
                "гривна": "гривна", "гривны": "гривна", "гривен": "гривна",
                "uah": "гривна",
                "тенге": "тенге", "kzt": "тенге",
                "юань": "юань", "юаня": "юань", "юань": "юани", "юаней": "юань", "cny": "юань", "юани": "юань",
                "злотый": "злотый", "злотый": "злотые", "злотых": "злотый", "pln": "злотый",
                
                # Криптовалюты
                "btc": "btc", "bitcoin": "btc", "биткоин": "btc", "биткоина": "btc", "биткоинов": "btc",
                "ton": "ton", "toncoin": "ton", "тон": "ton", "тона": "ton", "тонов": "ton",
                "usdt": "usdt", "tether": "usdt", "тезер": "usdt", "тезера": "usdt", "тезеров": "usdt",
            }
            
            from_cur = currency_map.get(from_cur, from_cur)
            to_cur = currency_map.get(to_cur, to_cur)
            
            valid_currencies = list(set(currency_map.values()))
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
            
            # Конвертация через USD
            if from_cur == to_cur:
                result = amount
            elif from_cur in ["btc", "ton", "usdt"]:
                # Крипто -> Любая валюта
                usd_amount = amount * self.rates[from_cur]
                if to_cur == "доллар":
                    result = usd_amount
                else:
                    result = usd_amount * self.rates[to_cur]
            elif to_cur in ["btc", "ton", "usdt"]:
                # Любая валюта -> Крипто
                if from_cur == "доллар":
                    usd_amount = amount
                else:
                    usd_amount = amount / self.rates[from_cur]
                result = usd_amount / self.rates[to_cur]
            else:
                # Фиат -> Фиат
                usd_amount = amount / self.rates[from_cur]
                result = usd_amount * self.rates[to_cur]
            
            # Получаем отформатированные названия с эмодзи
            from_display = self.get_currency_display(from_cur, amount)
            to_display = self.get_currency_display(to_cur, result)
            
            await utils.answer(
                message,
                self.strings("converted").format(
                    self.format_value(amount),
                    from_display,
                    self.format_value(result),
                    to_display
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
        """Обновить курсы вручную"""
        await utils.answer(message, self.strings("updating"))
        if await self.update_rates():
            await utils.answer(message, self.strings("updated"))
        else:
            await utils.answer(
                message,
                self.strings("error").format("Не удалось обновить курсы")
            ) 
