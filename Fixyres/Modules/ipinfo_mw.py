# meta developer: @mwmodules
# meta desc:  🌍 IP Info - Get detailed information about any IP address
# by @mwmodules
# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
# meta link: .dlm http://mwmodules.ftp.sh/ipinfo.py


import logging
import aiohttp
from .. import loader, utils
import json

logger = logging.getLogger(__name__)

@loader.tds
class IPInfoMod(loader.Module):
    """Получает подробную информацию об IP-адресе, включая хост, дополнительные данные, ссылку на Google Maps и 20 полей."""

    strings = {
        "name": "IPInfo",
        "no_ip": "⚠️ Укажите IP-адрес после команды `.ip`",
        "invalid_ip": "❌ Некорректный IP-адрес.",
        "fetching": "🔎 Получение информации...",
        "error": "❌ Произошла ошибка: {}",
        "not_host": "🚫 IP-адрес не является хостом.",
        "info": (
            "<b>Разработчик:</b> <a href='https://t.me/mwoffice'>@mwoffice</a>\n\n"
            "<b>Информация об IP:</b>\n"
            "<b>IP:</b> <code>{ip}</code>\n"
            "<b>Страна:</b> <code>{country}</code>\n"
            "<b>Регион:</b> <code>{region}</code>\n"
            "<b>Город:</b> <code>{city}</code>\n"
            "<b>Организация:</b> <code>{org}</code>\n"
            "<b>Почтовый индекс:</b> <code>{postal}</code>\n"
            "<b>Широта:</b> <code>{latitude}</code>\n"
            "<b>Долгота:</b> <code>{longitude}</code>\n"
            "<b>Часовой пояс:</b> <code>{timezone}</code>\n"
            "<b>Хост:</b> <code>{is_host}</code>\n"
            "<b>Хостнейм:</b> <code>{hostname}</code>\n"
            "<b>Тип:</b> <code>{type}</code>\n"
            "<b>AS номер:</b> <code>{as_number}</code>\n"
            "<b>AS имя:</b> <code>{as_name}</code>\n"
            "<b>Мобильный:</b> <code>{mobile}</code>\n"
            "<b>Прокси:</b> <code>{proxy}</code>\n"
            "<b>VPN:</b> <code>{vpn}</code>\n"
            "<b>Спутник:</b> <code>{satellite}</code>\n"
             "<b>Континент:</b> <code>{continent}</code>\n"
            "<b>Код страны:</b> <code>{countryCode}</code>\n"
            "<b>Код региона:</b> <code>{regionCode}</code>\n"
            "<b>Валюта:</b> <code>{currency}</code>\n"
            "<b>Язык:</b> <code>{languages}</code>\n"
            "<b>Почтовый индекс:</b> <code>{zipCode}</code>\n"
            "<b>Примерное местоположение:</b> <a href='{google_maps_link}'>Google Maps</a>\n"
        ),
    }

    async def ipcmd(self, message):
        """Получает подробную информацию об IP-адресе и определяет хост.
        .ip <ip_address>
        """

        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_ip"])
            return

        ip = args
        try:
            import ipaddress
            ipaddress.ip_address(ip)
        except ValueError:
            await utils.answer(message, self.strings["invalid_ip"])
            return

        await utils.answer(message, self.strings["fetching"])

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,org,zip,lat,lon,timezone,hosting,query,type,as,mobile,proxy,vpn,satellite,continent,countryCode,regionCode,currency,languages") as response:
                    if response.status == 200:
                        data = await response.json()
                        if data["status"] == "success":
                            is_host = data.get("hosting", False)
                            if is_host:
                                is_host = "Да"
                            else:
                                is_host = "Нет"
                            latitude = data.get("lat", "N/A")
                            longitude = data.get("lon", "N/A")
                            google_maps_link = f"https://www.google.com/maps/place/{latitude},{longitude}" if latitude != "N/A" and longitude != "N/A" else "N/A"

                            info_message = self.strings["info"].format(
                                ip=ip,
                                country=data.get("country", "N/A"),
                                region=data.get("regionName", "N/A"),
                                city=data.get("city", "N/A"),
                                org=data.get("org", "N/A"),
                                postal=data.get("zip", "N/A"),
                                latitude=latitude,
                                longitude=longitude,
                                timezone=data.get("timezone", "N/A"),
                                is_host=is_host,
                                hostname=data.get("query", "N/A"),
                                type=data.get("type", "N/A"),
                                as_number=data.get("as", "N/A").split(' ', 1)[0] if data.get("as") else "N/A",
                                as_name=data.get("as", "N/A").split(' ', 1)[1] if data.get("as") and len(data.get("as").split(' ', 1)) > 1 else "N/A",
                                mobile= "Да" if data.get("mobile", False) else "Нет",
                                proxy="Да" if data.get("proxy", False) else "Нет",
                                vpn="Да" if data.get("vpn", False) else "Нет",
                                satellite="Да" if data.get("satellite", False) else "Нет",
                                continent=data.get("continent", "N/A"),
                                countryCode=data.get("countryCode", "N/A"),
                                regionCode=data.get("regionCode", "N/A"),
                                currency=data.get("currency", "N/A"),
                                languages=data.get("languages", "N/A"),
                                zipCode=data.get("zip", "N/A"),
                                google_maps_link=google_maps_link,
                            )
                            await utils.answer(message, info_message)
                        else:
                            await utils.answer(message, self.strings["error"].format(data["message"]))
                    else:
                        await utils.answer(message, self.strings["error"].format(f"HTTP Error: {response.status}"))
        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
            logger.error(str(e))
    
    async def on_dlmod(self):
      try:
          import aiohttp
      except ImportError:
         await self.download_lib("aiohttp")

    async def download_lib(self, lib_name):
        try:
            await utils.run_sync(lambda: __import__("pip").main(["install", lib_name]))
            return True
        except Exception:
            return False