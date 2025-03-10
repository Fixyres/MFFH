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

# meta developer: @kshmods
# requires: requests pyshorteners

from .. import loader, utils
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import socket
import pyshorteners
import os

@loader.tds
class URLMod(loader.Module):
    """A module for parsing URLs."""
    strings = {"name": "URLModule"}

    async def scrapecmd(self, message):
        """Extracts and processes data from the specified URL."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Please provide a URL to parse.</b>")
            return
        url = args.strip()
        try:
            response = requests.get(url)
            response.raise_for_status()
            response_text = response.text
            if len(response_text) > 4096:
                with open("response.txt", "w", encoding="utf-8") as file:
                    file.write(response_text)
                await message.client.send_file(message.chat_id, "response.txt", caption="<b>Response is too long, sent as a file:</b>")
                os.remove("response.txt")
                await message.delete()
            else:
                await utils.answer(message, f"<b>Response:</b>\n<pre>{response_text}</pre>")
        except requests.exceptions.RequestException as e:
            await utils.answer(message, f"<b>An error occurred:</b> {e}")

    async def shurlcmd(self, message):
        """Shortens the given URL."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Please provide a URL to shorten.</b>")
            return
        url = args.strip()
        try:
            shortener = pyshorteners.Shortener().tinyurl
            short_url = shortener.short(url)
            await utils.answer(message, f"<b>Shortened URL:</b> <a href='{short_url}'>{short_url}</a>")
        except Exception as e:
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
            session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            session.mount("http://", HTTPAdapter(max_retries=retries))
            session.mount("https://", HTTPAdapter(max_retries=retries))
            response = session.get(short_url, headers=headers, allow_redirects=True)
            response.raise_for_status()
            expanded_url = response.url
            await utils.answer(message, f"<b>Expanded URL:</b> <a href='{expanded_url}'>{expanded_url}</a>")
        except requests.exceptions.RequestException as e:
            await utils.answer(message, f"<b>An error occurred:</b> {e}")

    async def ipurlcmd(self, message):
        """Gets the IP address of the given URL."""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<b>Please provide a URL to get the IP address.</b>")
            return
        url = args.strip()
        try:
            hostname = url.split("//")[-1].split("/")[0]
            ip_address = socket.gethostbyname(hostname)
            await utils.answer(message, f"<b>IP address of {url}:</b> {ip_address}")
        except socket.gaierror as e:
            await utils.answer(message, f"<b>An error occurred:</b> {e}")