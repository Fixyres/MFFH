# meta developer: @xdesai

from .. import loader, utils
import aiohttp
import logging

logger = logging.getLogger("CurrencyMod")


class Currency(loader.Module):
    strings = {
        "name": "Currency",
        "rate": "<b>Rates for {amount} {currency}:\n<blockquote expandable>{rates}</blockquote></b>",
        "err": "Error: <code>{error}</code>",
        "currency": "{cur}: {converted}",
        "invalid_args": "<emoji document_id=5017058788604117831>❌</emoji> <b>Invalid args</b>",
    }

    strings_ru = {
        "rate": "<b>Курсы для {amount} {currency}:\n<blockquote expandable>{rates}</blockquote></b>",
        "err": "Ошибка: <code>{error}</code>",
        "currency": "{cur}: {converted}",
        "invalid_args": "<emoji document_id=5017058788604117831>❌</emoji> <b>Неверные аргументы</b>",
    }

    strings_jp = {
        "rate": "<b>{amount} {currency} のレート:\n<blockquote expandable>{rates}</blockquote></b>",
        "err": "エラー: <code>{error}</code>",
        "currency": "{cur}: {converted}",
        "invalid_args": "<emoji document_id=5017058788604117831>❌</emoji> <b>無効な引数です</b>",
    }

    api_endpoints = [
        "https://open.er-api.com/v6/latest/{}",
    ]

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "currency",
                ["PLN", "AZN", "USD", "EUR", "RUB", "UAH"],
                lambda: "List of currencies in which you want to show",
                validator=loader.validators.Series(),
            ),
        )

    @loader.command(
        ru_doc="<сумма> <валюта> - Показать курсы валют",
        jp_doc="<amount> <currency> - 為替レートを表示",
    )
    async def cr(self, message):
        """<amount> <currency> - Show Exchange Rates"""
        args = utils.get_args(message)
        if len(args) < 2:
            return await utils.answer(message, self.strings["invalid_args"])

        try:
            amount = float(args[0])
            base_currency = args[1].upper()
        except Exception as e:
            return await utils.answer(message, self.strings["err"].format(error=str(e)))

        async with aiohttp.ClientSession() as session:
            rates = await self.fetch_rates(session, base_currency)
            if not rates:
                return await utils.answer(
                    message, self.strings["err"].format(error="Failed to get rates")
                )

        result_lines = []
        for cur in self.config["currency"]:
            cur_up = cur.upper()
            if cur_up == base_currency:
                continue
            else:
                rate = rates.get(cur_up)
                if rate is None:
                    converted = "N/A"
                else:
                    converted = amount * rate

            if isinstance(converted, float):
                converted_str = f"{converted:.2f}"
            else:
                converted_str = str(converted)

            result_lines.append(
                self.strings["currency"].format(cur=cur_up, converted=converted_str)
            )

        text = self.strings["rate"].format(
            amount=amount, currency=base_currency, rates="\n".join(result_lines)
        )
        await utils.answer(message, text)

    async def fetch_rates(self, session, base_currency):
        for url in self.api_endpoints:
            try:
                async with session.get(
                    url.format(base_currency.upper()), timeout=10
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "rates" in data and data["rates"]:
                            return data["rates"]
                        else:
                            logger.error("No rates in response")
                            return None
                    else:
                        logger.error(f"HTTP {response.status}")
                        return None
            except Exception as e:
                logger.error(f"API error ({url.format(base_currency.upper())}): {e}")
                return None
