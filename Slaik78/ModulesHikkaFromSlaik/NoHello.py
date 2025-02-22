#------------------------------------------------------------------
#      ___           ___       ___                       ___     
#     /\  \         /\__\     /\  \          ___        /\__\    
#    /::\  \       /:/  /    /::\  \        /\  \      /:/  /    
#   /:/\ \  \     /:/  /    /:/\:\  \       \:\  \    /:/__/     
#  _\:\~\ \  \   /:/  /    /::\~\:\  \      /::\__\  /::\__\____ 
# /\ \:\ \ \__\ /:/__/    /:/\:\ \:\__\  __/:/\/__/ /:/\:::::\__\
# \:\ \:\ \/__/ \:\  \    \/__\:\/:/  / /\/:/  /    \/_|:|~~|~   
#  \:\ \:\__\    \:\  \        \::/  /  \::/__/        |:|  |    
#   \:\/:/  /     \:\  \       /:/  /    \:\__\        |:|  |    
#    \::/  /       \:\__\     /:/  /      \/__/        |:|  |    
#     \/__/         \/__/     \/__/                     \|__|   
#------------------------------------------------------------------ 
# meta developer: @hicota


import re
from .. import loader, utils

@loader.tds
class NoHello(loader.Module):
    """Модуль для неприветов"""

    strings = {"name": "NoHello"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
            "listNoHello",
             ['привет', 'приветик', 'пр', 'здравствуйте', 'здравствуй', 'здрасте', 'здарова', 'здорова', 'здаров', 'здоров', 'даров', 'даров', 'добрый день', 'добрый вечер', 'ку', 'салам', 'салют', 'хай'],
            lambda: "Добавляй текст, который не хочешь видеть.",
            validator=loader.validators.Series()
            ),
        )

    @loader.watcher(only_messages = True)
    async def watcher(self, message):
        if message.is_private:
            msg = re.sub(r'[^\w\s]', '', message.text.lower())
            if msg in self.config['listNoHello']:
                if message.from_id != self.tg_id:
                    await message.client.send_message(message.from_id, '<a href="https://nohello.net/ru">Прочти меня</a>', reply_to=message.id, link_preview=False)