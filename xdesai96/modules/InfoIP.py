# meta developer: @xdesai

import requests
from .. import loader, utils

@loader.tds
class InfoIPMod(loader.Module):

    strings = {
        "name": "InfoIP",
        "invalid_ip": "❌ <b>Specify IP address</b>",
        "no_data": "😢 <b>No data available</b>",
        "data": """
<blockquote><emoji document_id=5447410659077661506>🌐</emoji><b> Information about IP</b></blockquote>
<blockquote><emoji document_id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>
<blockquote><emoji document_id=5235794253149394263>🗺</emoji><b> Country: {country}</b></blockquote>
<blockquote><emoji document_id=5247209275494769660>🕓</emoji><b> Timezone: {timezone}</b></blockquote>
<blockquote><emoji document_id=5330371855368866588>🌇</emoji><b> City: {city}</b></blockquote>
<blockquote><emoji document_id=5308028293033764449>⚡️</emoji><b> Region: {region}</b></blockquote>
<blockquote><emoji document_id=5391032818111363540>📍</emoji><b> Coordinates: <code>{coordinates}</code></b></blockquote>
"""
    }
    strings_ru = {
        "name": "InfoIP",
        "invalid_ip": "❌ <b>Укажите ip адрес</b>",
        "no_data": "😢 <b>Нет данных</b>",
        "data": """
<blockquote><emoji document_id=5447410659077661506>🌐</emoji><b> Информация об IP</b></blockquote>
<blockquote><emoji document_id=6334617384782923882>📟</emoji><b> IP: <code>{ip}</code></b></blockquote>
<blockquote><emoji document_id=5235794253149394263>🗺</emoji><b> Страна: {country}</b></blockquote>
<blockquote><emoji document_id=5247209275494769660>🕓</emoji><b> Часовой пояс: {timezone}</b></blockquote>
<blockquote><emoji document_id=5330371855368866588>🌇</emoji><b> Город: {city}</b></blockquote>
<blockquote><emoji document_id=5308028293033764449>⚡️</emoji><b> Регион: {region}</b></blockquote>
<blockquote><emoji document_id=5391032818111363540>📍</emoji><b> Координаты: <code>{coordinates}</code></b></blockquote>
"""
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command(
        ru_doc="<ip> | Информация об IP"
    )
    async def ipi(self, message):
        """<ip> | Information about IP."""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "❌ Specify IP address.")
            return

        ip = args[0] if isinstance(args, list) else args
        await self.get_location_by_ip(message, ip)

    async def get_location_by_ip(self, message, ip_address):
        url = f'http://ip-api.com/json/{ip_address}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'fail':
                return utils.answer(message, self.strings('no_data'))
            else:
                return utils.answer(message, self.strings('data').format(
                    ip=data.get('query', 'no ip available'),
                    country=data.get('country', 'no country available'),
                    timezone=data.get('timezone', 'no timezone available'),
                    city=data.get('city', 'no city available'),
                    region=data.get('regionName', 'no region available'),
                    coordinates=f'{data.get('lat', 'no latitude available')}, {data.get('lon', 'no longitude available')}'
                ))
