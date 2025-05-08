# meta developer: @xdesai

from .. import loader, utils
import socket
import aiohttp
import aiodns
import os

@loader.tds
class URLMod(loader.Module):
    """A module for parsing URLs."""
    strings = {"name": "URLModule"}

    async def scrapecmd(self, message):
        """Extracts and processes data from the specified URL asynchronously."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Please provide a URL to parse.</b>")
            return
        url = args.strip()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    response_text = await response.text()
                    
                    if len(response_text) > 4096:
                        # Если длина ответа больше 4096 символов, сохраняем его в файл и отправляем.
                        with open("response.txt", "w", encoding="utf-8") as file:
                            file.write(response_text)
                        await message.client.send_file(message.chat_id, "response.txt", caption="<b>Response is too long, sent as a file</b>")
                        os.remove("response.txt")
                        await message.delete()
                    else:
                        await utils.answer(message, f"<b>Response:</b>\n<pre>{response_text}</pre>")
        except aiohttp.ClientError as e:
            await utils.answer(message, f"<b>An error occurred:</b> {e}")

    async def expandurlcmd(self, message):
        """Expands the given shortened URL."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Please provide a shortened URL to expand.</b>")
            return
        short_url = args.strip()
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(short_url, allow_redirects=True) as response:
                    response.raise_for_status()
                    expanded_url = str(response.url)
                    await utils.answer(message, f"<b>Expanded URL:</b> <a href='{expanded_url}'>{expanded_url}</a>")
        except aiohttp.ClientError as e:
            await utils.answer(message, f"<b>An error occurred:</b> {e}")

    async def ipurlcmd(self, message):
        """Gets the IP address of the given URL asynchronously."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Please provide a URL to get the IP address.</b>")
            return
        url = args.strip()
        resolver = aiodns.DNSResolver()

        try:
            hostname = url.split("//")[-1].split("/")[0]
            response = await resolver.gethostbyname(hostname, socket.AF_INET)
            ip_address = response.addresses[0]
            await utils.answer(message, f"<b>IP address of {url}:</b> <code>{ip_address}</code>")
        except aiodns.error.DNSError as e:
            await utils.answer(message, f"<b>An error occurred:</b> {e}")
