__version__ = (2, 7, 1)
#            © Copyright 2024
#           https://t.me/HikkTutor 
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: dushnometr

from .. import loader, utils
import random
from telethon.tl.functions.users import GetFullUserRequest
import asyncio

@loader.tds
class PoiskMod(loader.Module):
    """Модуль для поиска главной душнилы чата
    
    Это шуточный модуль, автор ни в коем случае не пытался вас обидеть """
    strings = {'name': 'dushnometr'}

    async def dncmd(self, message):
        """- найти душнилу"""
        await message.edit("<b>Запуск душнометра...</b>")
        await asyncio.sleep(2)

        progress_steps = [4, 23, 40, 57, 90]
        for step in progress_steps:
            await message.edit(f"Распознаю душнил... [{'■' * (step // 10)}{'□' * (10 - step // 10)}] {step}%")
            await asyncio.sleep(1)

        await message.edit("Сравниваю душнил...")
        for _ in range(3):
            await asyncio.sleep(0.5)
            await message.edit("Сравниваю душнил" + "." * (_ + 1))
        
        users = await message.client.get_participants(message.chat_id)
        dusno = random.choice(users)

        greetings = [
            f'<b>Похоже, что главный душнила в чате</b> <a href="tg://user?id={dusno.id}">{dusno.first_name}<b>. Откройте окно!</b></a>',
            f'<b>Ухты, душнометр зашкаливает! Царь душнил - </b> <a href="tg://user?id={dusno.id}">{dusno.first_name}</a>',
            f'<b>Даже открытое окно не спасает... </b> <a href="tg://user?id={dusno.id}">{dusno.first_name} <b>,таких душнил я ещё не встречал</b> </a>!',
        ]

        selected_greeting = random.choice(greetings)
        await message.edit(selected_greeting)
