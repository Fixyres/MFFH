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
# meta developer: @Hicota
# requires: pillow

import glob
import os
import requests
from .. import loader

@loader.tds
class IIHikkaInfomod(loader.Module):
    '''Install Hikka(Heroku)info with image mode (Beta)'''

    strings = {'name': 'IIHikkaInfo'}

    @loader.command()
    async def inshikkainfo(self, message):
        """ИДИ СЮДА яишко яишко СЕЙЧАС яишко ТЕБЕ БУДЕТ РАЗБИВАТЬ яишко🥚🥚🥚🥚ПОЛУЧАЙ яишко🥚🥚🥚🥚🥚🥚🥚🥚НА🥚НА🥚НА🥚🥚🥚БЕЕЕЙ🥚🥚🥚яишко яишко яишко ТЕБЕ МАЛО????🥚🥚🥚ПОНЯЛ яишко🥚🥚🥚🥚НА ЕШЕ ЯИЧКЭЭЭ🥚🥚🥚ЖРИ яишко🥚🥚🥚яишко БЕЙ🥚🥚🥚🥚ТЫ ПОНИМАЕШЬ ЧТО яишко БЕЙ МЕНЯ🥚🥚🥚🥚🥚🥚НА яишко яишко🥚🥚🥚 яишко. ЗАПОМНИТЕ ТАК БУДЕТ С КАЖДЫМ яишко.🥚🥚🥚бей яичко чур я выиграю🥚"""
        await message.edit('<emoji document_id=5213277341639254218>🖍</emoji><b>Installing</b>')
        path = glob.glob(f'{os.getcwd()}/*/modules/*_info.py')[0]
        if 'heroku' in path:
            os.remove(path)
            response = requests.get('https://raw.githubusercontent.com/Slaik78/ModulesHikkaFromSlaik/refs/heads/main/heroku_info.py')
        elif 'hikka' in path:
            os.remove(path)
            response = requests.get('https://raw.githubusercontent.com/Slaik78/ModulesHikkaFromSlaik/refs/heads/main/hikka_info.py')
        with open(path, 'wb') as file:
            file.write(response.content)
        response = requests.get('https://x0.at/cZdy.ttf')
        if response.status_code != 200:
            await message.edit(f'<emoji document_id=5465665476971471368>❌</emoji><b>Server error {response.status_code}</b>')
            return
        with open(f'{os.getcwd()}/assets/font.ttf', 'wb') as file:
            file.write(response.content)
        await message.edit('<emoji document_id=5370870691140737817>🥳</emoji><b>Installation completed</b>\nДля работы модуля надо перезагрузить юзербота')
        
