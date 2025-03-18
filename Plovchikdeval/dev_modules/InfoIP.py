# meta developer: @kshmods

"""
888    d8P   .d8888b.  888    888     888b     d888  .d88888b.  8888888b.   .d8888b.  
888   d8P   d88P  Y88b 888    888     8888b   d8888 d88P" "Y88b 888  "Y88b d88P  Y88b 
888  d8P    Y88b.      888    888     88888b.d88888 888     888 888    888 Y88b.      
888d88K      "Y888b.   8888888888 d8b 888Y88888P888 888     888 888    888  "Y888b.   
8888888b        "Y88b. 888    888 Y8P 888 Y888P 888 888     888 888    888     "Y88b. 
888  Y88b         "888 888    888     888  Y8P  888 888     888 888    888       "888 
888   Y88b  Y88b  d88P 888    888 d8b 888   "   888 Y88b. .d88P 888  .d88P Y88b  d88P 
888    Y88b  "Y8888P"  888    888 Y8P 888       888  "Y88888P"  8888888P"   "Y8888P" 
                                                           
(C) 2025 t.me/kshmods
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
"""

import requests
from .. import loader, utils


@loader.tds
class InfoIPMod(loader.Module):

    strings = {
        "name": "InfoIP"
    }

    @loader.owner
    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.command()
    async def ipi(self, message):
        """<ip> | Information about IP."""
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "❌ Specify IP address.")
            return

        ip = args[0] if isinstance(args, list) else args
        data = await get_location_by_ip(ip)
        await utils.answer(message, data)

async def get_location_by_ip(ip_address):
    url = f'http://ip-api.com/json/{ip_address}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'fail':
            return "No data available"
        else:
            return f"""
<blockquote><emoji document_id=5447410659077661506>🌐</emoji><b> Information about IP</b></blockquote>
<blockquote><emoji document_id=6334617384782923882>📟</emoji><b> IP: <code>{data.get('query', 'no ip available')}</code></b></blockquote>
<blockquote><emoji document_id=5235794253149394263>🗺</emoji><b> Country: {data.get('country', 'no country available')}</b></blockquote>
<blockquote><emoji document_id=5247209275494769660>🕓</emoji><b> Timezone: {data.get('timezone', 'no timezone available')}</b></blockquote>
<blockquote><emoji document_id=5330371855368866588>🌇</emoji><b> City: {data.get('city', 'no city available')}</b></blockquote>
<blockquote><emoji document_id=5308028293033764449>⚡️</emoji><b> Region: {data.get('regionName', 'no region available')}</b></blockquote>
<blockquote><emoji document_id=5391032818111363540>📍</emoji><b> Location: <code>{data.get('lat', 'no latitude available')}, {data.get('lon', 'no longitude available')}</code></b></blockquote>
"""
