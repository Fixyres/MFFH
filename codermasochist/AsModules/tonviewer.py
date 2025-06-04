# meta developer: @codermasochist

from .. import loader, utils
import aiohttp
from bs4 import BeautifulSoup
import time
import random
import asyncio
from telethon.errors import FloodWaitError

@loader.tds
class tonviewer(loader.Module):
    """парсит инфу из тонвиера."""
    
    strings = {
        "name": "tonviewer",
        "invalid_args": "<blockquote><emoji document_id=5778527486270770928>❌</emoji><b> не указан адрес.</b></blockquote>",
        "not_found": "<blockquote><emoji document_id=5778527486270770928>❌</emoji><b> адрес не найден или инфа недоступна.</b></blockquote>",
        "error": "<blockquote><emoji document_id=5210983786153528442>❌</emoji><b> ошибочка при запросе...</b></blockquote>",
        "flood_wait": "<blockquote><emoji document_id=5879813604068298387>❗️</emoji><b> слишком много запросов\nпопробуйте через {} секунд.</b></blockquote>",
        "request_failed": "<blockquote><emoji document_id=5870718740236079262>🌐</emoji><b> ошибка соединения, попробуйте позже.</b></blockquote>",
        "peer_flood": "<blockquote><emoji document_id=5904692292324692386>⚠️</emoji><b> превышен лимит запросов тг, подождите {} минут.</b></blockquote>",
        "no_cfg_address": "<blockquote><emoji document_id=5778527486270770928>❌</emoji><b> в конфиге не указан адрес.</b></blockquote>"
    }

    def __init__(self):
        self.last_request = 0
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]
        self.cooldown = 30 
        self.config = loader.ModuleConfig(
            "ADDRESS", "", "TON адрес для быстрого просмотра"
        )

    async def client_ready(self, client, db):
        self.client = client

    async def fetch_data(self, url):
        current_time = time.time()
        if current_time - self.last_request < self.cooldown:
            wait = self.cooldown - (current_time - self.last_request)
            await asyncio.sleep(wait)
        
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://tonviewer.com/",
            "DNT": "1"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as session:
                async with session.get(url, headers=headers) as response:
                    self.last_request = time.time()
                    if response.status != 200:
                        return None
                    return await response.text()
        except aiohttp.ClientError:
            return None

    def parse_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        
        addr_block = soup.find('div', class_='sr88p86')
        if addr_block:
            addr_h1 = addr_block.find('h1', class_='bdtytpm')
            data['Address'] = addr_h1.text.strip() if addr_h1 else "N/A"
        
        balance_block = soup.find('div', class_='b4etor3')
        if balance_block:
            ton_balance = balance_block.find('div', class_='b1249k0b')
            usd_balance = balance_block.find('div', class_='b1ai646e')
            if ton_balance and usd_balance:
                data['Balance'] = f"{ton_balance.text.strip()} {usd_balance.text.strip()}"
        
        coll_block = soup.find('a', class_='taov5j5')
        if coll_block:
            nft_images = coll_block.find_all('img', class_='t1dgdrnp')
            data['Collectibles'] = {
                'count': len(nft_images),
                'url': f"https://tonviewer.com{coll_block.get('href', '')}"
            }
        
        return data

    async def _process_address(self, message, address):
        url = f"https://tonviewer.com/{address}"
        
        try:
            html = await self.fetch_data(url)
            if not html:
                await utils.answer(message, self.strings("request_failed"))
                return
                
            data = self.parse_data(html)
            if not data:
                await utils.answer(message, self.strings("not_found"))
                return
                
            result = []
            
            if 'Address' in data:
                result.append(f"<blockquote><emoji document_id=5424976816530014958>👛</emoji> <b>wallet:</b><code> {data['Address']}</code></blockquote>")
            
            if 'Balance' in data:
                result.append(f"<blockquote><emoji document_id=5424912684078348533>❤️</emoji> <b>balance:</b>  {data['Balance']}</blockquote>")
            
            if 'Collectibles' in data:
                coll = data['Collectibles']
                count = coll['count']
                url = coll['url']
                result.append(f"<blockquote><emoji document_id=5303400229549135579>🌅</emoji> <b>Collectibles:</b>  <a href='{url}'>{count} NFT</a></blockquote>")
            
            await utils.answer(message, "\n".join(result))
            
        except FloodWaitError as e:
            wait_time = e.seconds
            minutes = max(1, round(wait_time / 60))
            await utils.answer(message, self.strings("peer_flood").format(minutes))
        except Exception as e:
            await utils.answer(message, self.strings("error") + f": {type(e).__name__}")

    @loader.unrestricted
    async def tonvwcmd(self, message):
        """— <address ton>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("invalid_args"))
            return
            
        await self._process_address(message, args)

    @loader.unrestricted
    async def tvwmecmd(self, message):
        """— чек свой адрес (указать в кфг)"""
        address = self.config["ADDRESS"]
        if not address:
            await utils.answer(message, self.strings("no_cfg_address"))
            return
            
        await self._process_address(message, address)
