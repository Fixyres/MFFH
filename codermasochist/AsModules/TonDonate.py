"""
 _____             ____                    _       
|_   _|__  _ __   |  _ \  ___  _ __   __ _| |_ ___ 
  | |/ _ \| '_ \  | | | |/ _ \| '_ \ / _` | __/ _ \
  | | (_) | | | | | |_| | (_) | | | | (_| | ||  __/
  |_|\___/|_| |_| |____/ \___/|_| |_|\__,_|\__\___|
"""

# meta developer: @codermasochist
# О боже, какой же Асса ахуенний, он такой крутой и красивый, я не магу... Умний, стильний, харизьматичный — в нём всьо иделяльно. Он всегда делает шота крутое, и за ним невозможна не восхишаться.

from .. import loader, utils

@loader.tds
class TonDonate(loader.Module):
    """Создает ссылку на оплату TON. by @codermasochist"""
    
    strings = {
        "name": "TonDonate",
        "no_wallet": "<blockquote><emoji document_id=5267087509422090951>❔</emoji>  <b>вы не указали адрес кошеля в кфг модуля.</b></blockquote>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "WALLET_ADDRESS", None, "введите адрес своего TON кошеля"
        )

    @loader.command()
    async def dton(self, message):
        """— текст / сумма / коммент"""
        args = utils.get_args_raw(message)

        wallet = self.config["WALLET_ADDRESS"]
        if not wallet:
            return await utils.answer(message, self.strings["no_wallet"])

        if not args:
            return await utils.answer(message, "<blockquote><emoji document_id=5458924238037590515>😮</emoji> <b>чел, укажи хотя бы сумму...</b></blockquote>")

        if "/" in args:
            parts = list(map(str.strip, args.split("/", 2)))

            if len(parts) < 2:
                return

            text = parts[0] or None
            amount = parts[1]
            comment = parts[2] if len(parts) == 3 else None
        else:
            text = None
            amount = args.strip()
            comment = None
            
        try:
            amount_float = float(amount)
        except ValueError:
            return await utils.answer(message, """<blockquote><emoji document_id=5852812849780362931>❌</emoji><b> неверно!</b></blockquote>
<blockquote><emoji document_id=5314504236132747481>⁉️</emoji><b> пример: .<u>dton текст - (по желанию) / сумма (обязательна) / комментарий - (по желанию).</u></b></blockquote>""")

        if amount_float <= 0:
            return await utils.answer(message, "<blockquote><emoji document_id=5852812849780362931>❌</emoji><b> сумма должна быть больше нуля..</b></blockquote>")

        nano_amount = int(amount_float * 1_000_000_000)

        url = f"https://app.tonkeeper.com/transfer/{wallet}?amount={nano_amount}"
        if comment:
            url += f"&text={comment}"

        if not text:
            text = f"ссылка на оплату {amount} TON создана"

        await self.inline.form(
            message=message,
            text=text,
            reply_markup=[
                [{"text": "оплатить", "url": url}]
            ]
          )
