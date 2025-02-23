# ------------------------------------------------------------
# Module: Telegraph
# Description: Module for creating articles on telegra.ph,
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https://www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands:
# scope: hikka_only
# meta developer: @kmodules
# ------------------------------------------------------------

from .. import loader, utils
import requests
import json

__version__ = (1, 0, 0)

@loader.tds
class TelegraphMod(loader.Module):
    """Create article using telegra.ph"""
    
    strings = {"name": "Telegraph"}
    
    async def telegraphcmd(self, message):
        """Create article. Use:
        	.telegraph <title> <description>"""
        
        args = utils.get_args_raw(message)
        if not args or len(args.split(' ', 1)) < 2:
            return await message.edit("Use: telegraph <title> <description>")
            
        title, description = args.split(' ', 1)
        
        await message.edit("<emoji document_id=5325792861885570739>🫥</emoji> <b>Making article...</b>")
        

        user = await message.client.get_me()
        author = user.first_name
        
        acc_data = requests.get(
            "https://api.telegra.ph/createAccount",
            params={
                "short_name": "Sandbox",
                "author_name": author
            }
        ).json()
        
        if not acc_data["ok"]:
            return await message.edit("❌ Error occured while creating account.")
            
        token = acc_data["result"]["access_token"]
        
        content = [{"tag": "p", "children": [description]}]
        
        page_data = {
            'access_token': token,
            'title': title,
            'content': json.dumps(content),
            'return_content': 'false'
        }
    
        response = requests.get('https://api.telegra.ph/createPage', params=page_data)
        result = response.json()
        
        if not result["ok"]:
            return await message.edit("❌ Error occured while creating article.")
            
        url = result["result"]["url"]
        
        await message.edit(
            f"<emoji document_id=5463144094945516339>👍</emoji> <b>Article created!</b>\n\n"
            f"<emoji document_id=5217890643321300022>✈️</emoji> <a href='{url}'><b>Article</b></a>\n"
            f"<emoji document_id=5219943216781995020>⚡</emoji> <b>URL</b>: {url}"
        )
      