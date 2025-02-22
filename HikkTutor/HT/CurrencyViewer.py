__version__ = (1, 0, 4)
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ© Copyright 2024
#ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤhttps://t.me/unnic
# 🔒ㅤㅤㅤㅤㅤLicensed under the GNU AGPLv3
# 🌐ㅤㅤhttps://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: @unnic
# name: Currency
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#██╗░░░██╗███╗░░██╗███╗░░██╗██╗░█████╗░
#██║░░░██║████╗░██║████╗░██║██║██╔══██╗
#██║░░░██║██╔██╗██║██╔██╗██║██║██║░░╚═╝
#██║░░░██║██║╚████║██║╚████║██║██║░░██╗
#╚██████╔╝██║░╚███║██║░╚███║██║╚█████╔╝
#░╚═════╝░╚═╝░░╚══╝╚═╝░░╚══╝╚═╝░╚════╝
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

from .. import loader, utils
from telethon.tl.types import Message  # type: ignore
import requests # type: ignore

# ---------------------Module-----------------------
class CurrencyMod(loader.Module):
    """Модуль для сравнения курсов"""

    strings = {
        "name": "Currency",
        "inc_args": "ℹ️ <b>Неправильные аргументы</b>",
        "keyerror": "ℹ️ <b>Возможно, валюта отсутствует в базе данных сайта или вы ввели неправильное название.</b>",
        "currency_not_supported": "ℹ️ <b>Данная валюта не поддерживается. Пожалуйста, проверьте правильность названия.</b>"
    }

# ---------------Tagged functionality----------------
    async def cvcmd(self, message: Message):
        """Используйте .cv <число> <название валюты>."""
        args = utils.get_args_raw(message)
        tray = "RUB"
        if not args:
            args = "1 " + tray

        args_list = args.split()
        try:
            if len(args_list) == 1 and isinstance(float(args_list[0]), float):
                args_list.append(str(tray))
        except Exception:
            args_list = ["1", args_list[0]]

        currency = args_list[1].upper()
        api_url = f"https://min-api.cryptocompare.com/data/price?fsym={currency}&tsyms=USD,RUB,UAH,KZT,EUR,BYN,GBP,CHF,JPY,TON,NOT"
        api_response = requests.get(api_url).json()

        user = await message.get_sender()
        is_premium = user.premium

        if 'Response' in api_response and api_response['Response'] == 'Error':
            await utils.answer(message, self.strings("currency_not_supported"))
            return

        try:
            count = float(args_list[0])

            currency_symbols = {
                "USD": "🇺🇸", "RUB": "🇷🇺", "UAH": "🇺🇦", "KZT": "🇰🇿", "EUR": "🇪🇺", 
                "BYN": "🇧🇾", "GBP": "🇬🇧", "CHF": "🇨🇭", "JPY": "🇯🇵", "TON": "🔵", 
                "NOT": "⚫️"
            }

            emoji_symbols = {
                "USD": "<emoji document_id=5202021044105257611>🇺🇸</emoji>", 
                "RUB": "<emoji document_id=5449408995691341691>🇷🇺</emoji>",
                "UAH": "<emoji document_id=5447309366568953338>🇺🇦</emoji>", 
                "KZT": "<emoji document_id=5228718354658769982>🇰🇿</emoji>",
                "EUR": "<emoji document_id=5228784522924930237>🇪🇺</emoji>", 
                "BYN": "<emoji document_id=5382219601054544127>🇧🇾</emoji>",
                "GBP": "<emoji document_id=5202196682497859879>🇬🇧</emoji>", 
                "CHF": "<emoji document_id=5442703336266543270>🇨🇭</emoji>",
                "JPY": "<emoji document_id=5456261908069885892>🇯🇵</emoji>", 
                "TON": "<emoji document_id=5253691721174234015>💎</emoji>",
                "NOT": "<emoji document_id=5379965911455256722>💎</emoji>"
            }

            form = f"<b>Поиск по курсу: {count} {currency}</b>\n<b>Свежие результаты:</b>\n\n"

            for curr, symbol in currency_symbols.items():
                if curr == currency:
                    continue

                value = api_response.get(curr, 0) * count
                value_str = "{:,.2f}".format(value).replace(",", " ").replace(".", ",")

                if is_premium:
                    flag = emoji_symbols.get(curr, "")
                else:
                    flag = symbol

                form += f"{flag} <code>{value_str}</code> {curr}\n"

            await utils.answer(message, form)

        except KeyError:
            await utils.answer(message, self.strings("keyerror"))

        except ValueError:
            await utils.answer(message, self.strings("inc_args"))

#-------Functionality with list and with tags-------
    async def cvicmd(self, message: Message):
        """Список доступных валют"""
    
        user = await message.get_sender()
        is_premium = user.premium
        instruction = (
           "<b>Список валют</b>\n\n"
           f"{'🇺🇸' if not is_premium else '<emoji document_id=5202021044105257611>🇺🇸</emoji>'}"
           "<code>USD</code><b>(Доллар)</b>\n"
           f"{'🇷🇺' if not is_premium else '<emoji document_id=5449408995691341691>🇷🇺</emoji>'}"
           "<code>RUB</code> <b>(Рубль)</b>\n"
           f"{'🇺🇦' if not is_premium else '<emoji document_id=5447309366568953338>🇺🇦</emoji>'}"
           "<code>UAH</code> <b>(Гривна)</b>\n"
           f"{'🇰🇿' if not is_premium else '<emoji document_id=5228718354658769982>🇰🇿</emoji>'}"
           "<code>KZT</code> <b>(Тенге)</b>\n"
           f"{'🇪🇺' if not is_premium else '<emoji document_id=5228784522924930237>🇪🇺</emoji>'}"
           "<code>EUR</code> <b>(Евро)</b>\n"
           f"{'🇧🇾' if not is_premium else '<emoji document_id=5382219601054544127>🇧🇾</emoji>'}"
           "<code>BYN</code> <b>(Бун)</b>\n"
           f"{'🇬🇧' if not is_premium else '<emoji document_id=5202196682497859879>🇬🇧</emoji>'}"
           "<code>GBP</code> <b>(Фунт)</b>\n"
           f"{'🇨🇭' if not is_premium else '<emoji document_id=5442703336266543270>🇨🇭</emoji>'}"
           "<code>CHF</code> <b>(Франк)</b>\n"
           f"{'🇯🇵' if not is_premium else '<emoji document_id=5456261908069885892>🇯🇵</emoji>'}"
           "<code>JPY</code> <b>(Йена)</b>\n"
           f"{'🔵' if not is_premium else '<emoji document_id=5253691721174234015>💎</emoji>'}"
           "<code>TON</code> <b>(Тонкоин)</b>\n"
           f"{'⚫️' if not is_premium else '<emoji document_id=5379965911455256722>💎</emoji>'}"
           "<code>NOT</code> <b>(Ноткоин)</b>\n\n"
           "<b>Использовать через:</b> <code>.cv</code><число> <название>"
        )
        await message.edit(instruction, parse_mode='html')

        # Хер # Херня # Хератень # Нахер # Захер # Похер
        # Может быть                     # Не может быть
        # Идея Александра              # Кодер Александр 
        # Авторы     модуля    Александр    и     Всякое
        # Код не пиздием и не меняйте иначе засужу нахуй
        # Автор не несёт ответ за твои последствия падла
        # Не    будь    ебланом   не    лезь   в  скрипт
