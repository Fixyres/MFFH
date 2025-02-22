# ------------------------------------------------------------
# Module: Telegraph
# Description: Module for creating articles on telegra.ph
# Author: kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands:
# scope: hikka_only
# meta developer: @kmodules
# ------------------------------------------------------------

from .. import loader, utils
import requests
import json

__version__ = (1, 0, 2)

@loader.tds
class TelegraphMod(loader.Module):
    """Create article using telegra.ph"""
    
    strings = {
        "name": "Telegraph",
        "args_error": "Use: .telegraph <title> | <description>",
        "making": "<emoji document_id=5325792861885570739>🫥</emoji> <b>Making article...</b>",
        "acc_error": "<emoji document_id=5440381017825716886>❌</emoji> Error occurred while creating account.",
        "page_error": "<emoji document_id=5440381017825716886>❌</emoji> Error occurred while creating article.", 
        "success": "<emoji document_id=5463144094945516339>👍</emoji> <b>Article created!</b>\n\n<emoji document_id=5217890643321300022>✈️</emoji> <a href='{}'><b>Article</b></a>\n<emoji document_id=5219943216781995020>⚡</emoji> <b>URL</b>: {}"
    }
    
    strings_ru = {
        "name": "Telegraph",
        "args_error": "Использование: .telegraph <заголовок> | <описание>",
        "making": "<emoji document_id=5325792861885570739>🫥</emoji> <b>Создаю статью...</b>",
        "acc_error": "<emoji document_id=5440381017825716886>❌</emoji> Произошла ошибка при создании аккаунта.",
        "page_error": "<emoji document_id=5440381017825716886>❌</emoji> Произошла ошибка при создании статьи.",
        "success": "<emoji document_id=5463144094945516339>👍</emoji> <b>Статья создана!</b>\n\n<emoji document_id=5217890643321300022>✈️</emoji> <a href='{}'><b>Статья</b></a>\n<emoji document_id=5219943216781995020>⚡</emoji> <b>URL</b>: {}"
    }
    
    async def telegraphcmd(self, message):
        """Create article. Use: .telegraph <title> | <description>"""
        
        args = utils.get_args_raw(message)
        if not args or '|' not in args:
            return await message.edit(self.strings["args_error"])
            
        title, description = args.split('|', 1)
        title = title.strip()
        description = description.strip()
        
        await message.edit(self.strings["making"])
        
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
            return await message.edit(self.strings["acc_error"])
            
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
            return await message.edit(self.strings["page_error"])
            
        url = result["result"]["url"]
        
        await message.edit(
            self.strings["success"].format(url, url)
        )
