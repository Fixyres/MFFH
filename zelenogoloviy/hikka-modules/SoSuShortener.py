#MIT License
#
#Copyright (c) 2025 zelenogoloviy
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ---------------------------------
# ---------------------------------------------------------------------------------
# Name: SoSuShortener
# Description: module for short urls in So.su.
# Author: @zelenogoloviy_m
# ---------------------------------------------------------------------------------
# meta developer: @zelenogoloviy_m
# scope: SoSuShortener
# scope: SoSuShortener 0.0.1
# ---------------------------------------------------------------------------------
__version__ = (0, 0, 1)
from .. import loader, utils
import string
import random
import requests
class Short:
    def __init__(self):
        self.base_url = "https://so.su/shorten.php"
    def generate_random_keyword(self, length=10):
        chars = string.ascii_letters + string.digits * 5
        return ''.join(random.choice(chars) for _ in range(length))
    def shorten_url(self, long_url):
        keyword = self.generate_random_keyword()
        data = {
            "url": long_url,
            "keyword": keyword
        }
        try:
            response = requests.post(self.base_url, data=data)
            if response.status_code == 200:
                return response.text.strip()
            return None
        except Exception as e:
            print(f"Произошла ошибка при запросе: {e}")
            return None
@loader.tds
class Sosumodule(loader.Module):
    """module for short urls in So.su"""
    strings = {
        "name": "SoSuShortener",
        "no_args": "No args",
        "shorten": "<emoji document_id=5769289093221454192>🔗</emoji> <b>Shorten link:</b>"
    }
    @loader.command()
    async def shortcmd(self, message):
        """short the url \n .short <https://your.link>"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message,
                self.strings["no_args"]
            )
            return
        shortener = Short()
        shortened_url = shortener.shorten_url(long_url=args)
        if shortened_url:
            await utils.answer(message, f"{self.strings['shorten']} {shortened_url}")
        else:
            await utils.answer(message, "Failed to shorten URL")