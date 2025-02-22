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
# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @kshmods
__version__ = (0, 1, 3)

from .. import loader, utils

import os
import asyncio
import subprocess

@loader.tds
class VoiceChatInstaller(loader.Module):
    '''Module for install HikkaVoicemode(voicechat)'''

    strings = {
        'name': 'VoiceChatInstall',
        'installing_ffmpeg': '<emoji document_id=5307675706283533118>🫥</emoji> <b>Installing FFMPEG...</b>',
        'installing_nodejs': '<emoji document_id=5328239124933515868>⚙️</emoji> <b>Installing NodeJs...</b>',
        'installing_youtubedl': '<emoji document_id=5328311576736833844>🔴</emoji> <b>Installing yt-dlp...</b>',
        'installing_pytgcalls': '<emoji document_id=5325872701032635449>⏳</emoji> <b>Installing hikkalls...</b>',
        'attempting_for_install': (
            '<emoji document_id=5305794398938735107>💭</emoji> <b>'
            'Requirements installed. Trying to install module...</b>'
        ),
        'installed_all': '<emoji document_id=6325696222313055607>😶</emoji> <b>Module seccessfully installed!</b>',
        'егор': '<emoji document_id=5258291768587197831>✖️</emoji> <b>Error! Please, try again</b>'
    }

    strings_ru = {
        'installing_ffmpeg': '<emoji document_id=5307675706283533118>🫥</emoji> <b>Установка FFMPEG...</b>',
        'installing_nodejs': '<emoji document_id=5328239124933515868>⚙️</emoji> <b>Установка NodeJs...</b>',
        'installing_youtubedl': '<emoji document_id=5328311576736833844>🔴</emoji> <b>Установка yt-dlp...</b>',
        'installing_pytgcalls': '<emoji document_id=5325872701032635449>⏳</emoji> <b>Установка hikkalls...</b>',
        'attempting_for_install': (
            '<emoji document_id=5305794398938735107>💭</emoji> <b>'
            'Зависимости установлены. Пробую загрузить модуль...</b>'
        ),
        'installed_all': '<emoji document_id=6325696222313055607>😶</emoji> <b>VoiceChat успешно установлен!</b>',
        'егор': '<emoji document_id=5258291768587197831>✖️</emoji> <b>Произошла ошибка! Прпробуйте снова</b>'
    }

    async def check_module(self):
        return any([True if 'HikkaVoiceMode' else False in mod for mod in self.allmodules.modules])

    @loader.command(ru_doc='- установить voicechat(hikkavoicemode) на Хикку')
    async def install(self, message):
        '''
        - install VoiceMod to Hikka.
        '''

        check_sudo = subprocess.check_output(['whoami']).decode().strip()
        if check_sudo == 'root':
            sudo = False
        else:
            sudo = True
        try:
            subprocess.check_output(['node','-v']).decode().strip()
        except:
            await utils.answer(message, self.strings('installing_nodejs'))
            command_0 = 'curl -sL https://deb.nodesource.com/setup_18.x -o nodesource_setup.sh'
            command_1 = 'bash nodesource_setup.sh'
            command_2 = 'apt-get install -y nodejs'
            if sudo:
                command_0 = f'sudo -S {command_0}' 
                command_1 = f'sudo -S {command_1}' 
                command_2 = f'sudo -S {command_2}' 
            os.system(command_0)
            await asyncio.sleep(0.5)
            os.system(command_1)
            await asyncio.sleep(0.5)
            os.system(command_2)

        b = await utils.answer(message, self.strings('installing_pytgcalls'))
        command = 'pip install hikkalls --no-deps'
        os.system(command)

        d = await utils.answer(b, self.strings('installing_youtubedl'))

        if os.access('/usr/local/bin', os.W_OK):
            install_dir = '/usr/local/bin'
        elif os.access('/usr/bin', os.W_OK):
            install_dir = '/usr/bin'
        else:
            install_dir = os.path.join(os.environ['HOME'], '.local', 'bin')
        os.makedirs(install_dir, exist_ok=True)
        command = f'curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o "{install_dir}/yt-dlp" && chmod a+rx "{install_dir}/yt-dlp"'
        subprocess.run(command, shell=True, check=True)

        checking_sudo = subprocess.check_output(['whoami']).decode().strip()
        if checking_sudo == 'root':
            sudo = False
        else:
            sudo = True
            await utils.answer(message, self.strings('installing_ffmpeg'))
            command_0 = 'apt update -y && apt install ffmpeg libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev -y'
            if sudo:
                command_0 = f'sudo -S {command_0}' 
                command_1 = 'sudo -S apt update && sudo apt install ffmpeg libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev -y'
            os.system(command_0)
            await asyncio.sleep(0.5)
            os.system(command_1)

        attempt = await utils.answer(d, self.strings('attempting_for_install'))
        msg = await self.client.send_message(message.chat_id, '<i>Installing...</i>')
        await self.allmodules.commands["dlmod"](await utils.answer(msg, f"{self.get_prefix()}dlmod https://raw.githubusercontent.com/Plovchikdeval/dev_modules/refs/heads/main/VoiceChat.py"))

        installed = await self.check_module()

        if installed:
            await utils.answer(attempt, self.strings('installed_all'))
        else:
            await utils.answer(attempt, self.strings('егор'))
