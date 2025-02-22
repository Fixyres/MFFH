__version__ = (3, 2, 0)
# _           _            _ _
# | |         | |          (_) |
# | |     ___ | |_ ___  ___ _| | __
# | |    / _ \| __/ _ \/ __| | |/ /
# | |___| (_) | || (_) \__ \ |   <
# \_____/\___/ \__\___/|___/_|_|\_\
#
#              © Copyright 2022
#
#         developed by @lotosiiik, @byateblan

# 🔒 Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta pic: https://static.whypodg.me/mods!bio.png
# meta banner: https://mods.whypodg.me/badges/bio.jpg
# scope: hikka_only
# scope: hikka_min 1.2.10

# developer of basic module: @zeticsce
# developer of Num: @trololo_1
# meta developer: @idiotcoders

from .. import loader, utils  # noqa
import asyncio
import contextlib
import pytz
import re
re._MAXCACHE = 3000
import telethon
from telethon.tl.types import MessageEntityTextUrl, Message
from telethon.tl.functions.users import GetFullUserRequest
import json as JSON
from telethon.errors.rpcerrorlist import FloodWaitError
from datetime import datetime, date, time
import logging
import types
from ..inline.types import InlineCall

import random
import subprocess
import string, pickle

def validate_text(text: str):
    txt = text.replace("<u>", "").replace("</u>", "").replace("<i>", "").replace("</i>", "").replace("<b>", "").replace("</b>", "").replace("<s>", "").replace("</s>", "").replace("<tg-spoiler>", "").replace("</tg-spoiler><s>", "")
    return txt

@loader.tds
class BioMod(loader.Module):
    """
💘
    """
    strings = {
        
        "name": "Bio",
        
        "not_reply": "<emoji document_id=5215273032553078755>💔</emoji> Реплая нет.",
        
        "not_args": "<emoji document_id=5215273032553078755>💔</emoji> Аргументов нет.",
        
        "nolink": "<emoji document_id=5197248832928227386>💔</emoji> Нет ссылки.",

        "hueta": "Ничего не могу понять..💔",

        "r.save":   
            "<emoji document_id=5212932275376759608>💖</emoji> Жертва <b><code>{}</code></b> в зарлисте.\n"
            "<b><emoji document_id=5433635625217563352>💊</emoji> +{}{}</b> био-ресурсов",
        "auto.save":   
            "<emoji document_id=5212932275376759608>💘</emoji> Жертва <b><code>{}</code></b> в зарлисте.\n"
            "<b><emoji document_id=5433635625217563352>💊</emoji> {}+{}</b> био-ресурсов.",        
        "search":
            "<emoji document_id=5212932275376759608>💓</emoji> Жертва <code>{}</code> приносит:\n"
            "<b><emoji document_id=5433635625217563352>💊</emoji> +{} био-ресурсов.</b>\n"
            "<emoji document_id=5766931615737449648>📆</emoji> Дата: <i>{}</i>",
        
        "nf": "<emoji document_id=5215273032553078755>💔</emoji> Не найдено! Скорее всего не бил, давай бей!",
        
        "no_user": "<emoji document_id=5215273032553078755>💔</emoji> Пользователь {} не существует.",

        "nous": "<emoji document_id=5215273032553078755>💔</emoji> Жертва или пользователь не существует.",

        "anf": "<emoji document_id=5215329773366025981>💔</emoji> некого искать..",

        "aicmd":
            "<b>🥷🏻</b> <a href='tg://openmessage?user_id={}'>{}</a>\n"
            "<b>🆔:</b> <code>@{}</code>",
        "myid": "<b>My 🆔:</b> <code>@{}</code>",
        

        "guidedov":    
            "<b>💘 Юзабельность доверки:</b>\n"
            "\n<b>{0}</b>  <code>бей</code> | <code>кус</code>[ьайни] | <code>зарази</code>[тьть] " # 🔽
            "| <code>еб</code>[ниажшь] | <code>уеб</code>[жиаошть] [1-10] (@id|@user|link)/"
            "\n<b>{0}</b>  <code>бей</code> | <code>кус</code>[ьайни] | <code>зарази</code>[тьть] " # 🔽
            "| <code>еб</code>[ниажшь] | <code>уеб</code>[жиаошть] [1-10] ="
            "\n<b>{0}</b>  <code>бей</code> | <code>кус</code>[ьайни] | <code>зарази</code>[тьть] " # 🔽
            "| <code>еб</code>[ниажшь] | <code>уеб</code>[жиаошть] [1-10] +"
            "\n<b>{0}</b>  <code>бей</code> | <code>кус</code>[ьайни] | <code>зарази</code>[тьть] " # 🔽
            "| <code>еб</code>[ниажшь] | <code>уеб</code>[жиаошть] [1-10] -"
            "\n<b>{0}</b>  <code>цен</code>[ау] | <code>вч</code>[ек]  <i>(цена вакцины)</i>"
            "\n<b>{0}</b>  <code>вак</code>[цинау] | <code>леч</code>[ись] | <code>хи</code>[лльсяйинг] | <code>лек</code>[арство]"
            "\n<b>{0}</b>  <code>жертв</code>[ыау] | <code>еж</code>[ау]"
            "\n<b>{0}</b>  <code>бол</code>[езьни]"
            "\n<b>{0}</b>  <code>#лаб</code>[уа] | <code>%лаб</code>[уа] | <code>/лаб</code>[уа]"
            "\n<b>{0}</b>  <code>увед</code>[ыаомления]  <i>(+вирусы)</i>"
            "\n<b>{0}</b>  <code>-вирус</code>[ыа]\n\n"
            "〽️ <b>Апгрейд навыков:</b>\n"
            "<b>{0}  навык (0-5)</b> или\n<b>{0}  чек навык (0-5)</b>\n"
            "<i> Например: <b>{0} квалификация 4</b>\n" 
            "(улучшает квалификацию учённых на 4 ур.)</i>\n\n"    
            "〽️ <b>Доступные навыки:</b>\n"
            "🧪 Патоген (<b>пат</b> [огены])\n👨‍🔬 Квалификация (<b>квал</b> [ификацияула] | <b>разраб</b> [откау])\n"
            "🦠 Заразность (<b>зз</b> | <b>зараз</b> [аностьку])\n🛡 Иммунитет (<b>иммун</b> [итеткау])\n"
            "☠️ Летальность (<b>летал</b> [ьностькау])\n🕵️‍♂️ Безопасность (<b>сб</b> | <b>служб</b> [ау] | <b>безопасно</b> [сть])\n\n"
            "<b>🔎 Поиск жертв в зарлисте:</b>\n"
            "<b>{0}  з [ @id ]</b> или\n"
            "<b>{0}  з [ реплай ]</b>\n"
            "<i>см. <code>{1}config bio</code> для настройки.</i>",

        "dov": 
            "<b>🌘 <code>{5}Дов сет</code> [ id|реплай ]</b> --- <b>Добавить/удалить саппорта.</b>\n"
            "<i>   ✨ Зайки в доверке:</i>\n"
            "{0}\n\n"
            "<b>🌘 <code>{5}Дов ник</code> ник</b> --- <b>Установить ник</b>.\n <i>Например: <b><code>.Дов ник {3}</code></b></i>.\n"
            "<b>   🔰 Ник доверки: <code>{1}</code></b>\n\n"
            "<b>🌘 <code>{5}Дов пуск</code></b> --- <b>Запустить/Остановить</b>.\n"
            "<b>   {2}</b>\n"
            "<i><b>Доступ открыт к:</b></i>\n{4}",

        "zarlistHelp": 
            "<b>Как пользоваться зарлистом:</b>\n\n"
            "<i>По умолчанию, все новые жертвы автоматически заносятся в зарлист,"
            " кроме, когда в сообщении ириса о заражении нету ссылки на жертву.</i>\n\n"
            "Шаблоны для добавления жертвы:\n"
            "{0}зар @id 1.1к\n"
            "жд @id 1.1к\n\n"
            "Чтобы найти жертву используй:\n"
            "{0}зар @id/реплай ф\n"
            "{1} з @id/реплай\n"
            "жл @id/реплай\n\n"
            "Также, инфу о бонусе с жертвы можно увидеть рядом с именем при использовании команды {0}б",

        "user_rm": "<emoji document_id=5404879225737978176>💔</emoji> Помощник <b><code>{}</code></b> туда иго <emoji document_id=5361597229683449359>😡</emoji>.",
        
        "user_add": "<emoji document_id=5212932275376759608>💞</emoji> Помощник <b><code>{}</code></b> добавлен!",
        
        "wrong_nick": "<b>📝 Введите ник.</b>",
        
        "nick_add": "🔰 Ник доверки <b>{}</b> установлен!",
        
        "dov_start": "<b><emoji document_id=5212932275376759608>💓</emoji> Успешно запущено!</b>",
        
        "dov_stop": "<b>💔 Успешно остановлено.</b>",
        
        "dov.wrong_args": 
            "<b><emoji document_id=5215273032553078755>💔</emoji> Неизвестный аргумент.</b>\n"
            "<i>📝 Введите <code>.дов</code> для просмотра команд.</i>",   
        
        "wrong_id": "💔 Правильно 🆔 введи.",
        
        "ex": "💕 Исключение: <code>{}</code>",
        
        "wrong_ot-do": '<emoji document_id=5215273032553078755>💔</emoji> Используй <b>правильно</b> функцию "от-до".',
        
        "no_sargs": "<emoji document_id=5215273032553078755>💔</emoji> Не найдено совпадение в начале строк с аргументами.",
        
        "no_link": "<emoji document_id=5215273032553078755>💔</emoji> Ссылка не найдена.",
        
        "too_much_args": "<emoji document_id=5215273032553078755>💔</emoji> Кол-во аргументов <b>больше</b> одного, либо начинается <b>не</b> со знака <code>@</code>",
        
        "no_zar_reply": "<emoji document_id=5215273032553078755>💔</emoji> Нет реплая на сообщение ириса о заражении.",
        
        "empty_zar": "<emoji document_id=5215273032553078755>💔</emoji> Список заражений пуст.",
        
        "wrong_zar_reply": '<emoji document_id=5215273032553078755>💔</emoji> Реплай <b>не</b> на сообщение ириса о заражении "<b>...подверг заражению...</b>"',
        
        "wrong_cmd": "<emoji document_id=5215273032553078755>💔</emoji> Команда введена некорректно.",
        
        "empty_ex": "<emoji document_id=5215273032553078755>💔</emoji> Cписок исключений пуст.",
        
        "tids": "<b><emoji document_id=5212932275376759608>💞</emoji> Id'ы успешно извлечены.</b>",
        
        "tzar": "<emoji document_id=5212932275376759608>💓</emoji> Заражения завершены.",
        
        "clrex": "<emoji document_id=5404879225737978176>💔</emoji> Список исключений очищен.",
        
        "zar_rm": "<emoji document_id=5404879225737978176>💔</emoji> Жертва <b><code>{0}</code></b> {1}удалена.",
        
        "exadd": "<emoji document_id=5404879225737978176>💔</emoji> Пользователь <code>{}</code> в исключениях.",
        
        "exrm": "<emoji document_id=5404879225737978176>💔</emoji> Пользователь <code>{}</code> удален.",
        
        "clrzar": "<emoji document_id=5404879225737978176>💔</emoji> Зарлист <b>очищен</b>.",
        
        "guide":
            "<b>Помощь по модулю BioHelper:</b>\n\n"
            "<code>{0}biohelp дов</code> 👈 Помощь по доверке\n"
            "<code>{0}biohelp зарлист</code> 👈 Помощь по зарлисту"


    }
    async def client_ready(self, client, db):
        self.db = db
        self.client = client #IDS
        if not self.db.get("NumMod", "exUsers", False):
            self.db.set("NumMod", "exUsers", [])
        if not self.db.get("NumMod", "infList", False):
            self.db.set("NumMod", "infList", {})

    async def айcmd(self, message):
        """
[reply/arg]
Получает айди пользователя.
        """
        reply = await message.get_reply_message()
        args = utils.get_args(message)
        if not reply:
            
            if not args:
                user = await message.client.get_entity(message.sender_id)
                link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)
                return await message.reply(
                    f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                    f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
                )
            user = 0
            if re.fullmatch(r"@\D\w{3,32}", args[0], flags=re.ASCII):
                user = await message.client.get_entity(args[0])
            
            elif re.fullmatch(r"@\d{4,14}", args[0], flags=re.ASCII):
                user = args[0].replace("@", "")
                user = await message.client.get_entity(int(user))

            elif re.fullmatch(r"\d{4,14}", args[0], flags=re.ASCII):
                user = await message.client.get_entity(int(args[0]))
            
            elif re.fullmatch(r"\D\w{3,32}", args[0], flags=re.ASCII):
                user = await message.client.get_entity(args[0])
            
            if not user:
                return await message.reply("ты ввел хуйню реально")

            link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)
            return await message.reply(
                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
            )
        if not args:
            user = await message.client.get_entity(reply.sender_id)
            link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)
            return await message.reply(
                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
            )

        user = 0
        if re.fullmatch(r"@\D\w{3,32}", args[0], flags=re.ASCII):
            user = await message.client.get_entity(args[0])
        
        elif re.fullmatch(r"@\d{4,14}", args[0], flags=re.ASCII):
            user = args[0].replace("@", "")
            user = await message.client.get_entity(int(user))
        elif re.fullmatch(r"\d{4,14}", args[0], flags=re.ASCII):
            user = await message.client.get_entity(int(args[0]))
        
        elif re.fullmatch(r"\D\w{3,32}", args[0], flags=re.ASCII):
            user = await message.client.get_entity(args[0])
        
        if not user:
            return await message.reply("ты ввел хуйню реально")
        link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)
        return await message.reply(
            f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
            f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
        )

### Module Num by trololo_1
    async def зcmd(self, message):
        """
[arg] [arg] [arg]....
В качестве аргументов используй числа или первые символы строки.
(без них бьет по ответу с 10 патов)
        """
        
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        count_st = 0
        count_hf = 0
        
        if not reply or not reply and not args:
            await message.reply(
                self.strings("not_reply")
            )
            return
        
        
        list_args = []
        args = utils.get_args_raw(message)
        if not args:
            vlad = reply.sender_id
            hui = f'<code>/заразить 10 @{vlad}<code>\nспасибки <emoji document_id=5215327827745839526>❤️</emoji>'
            


            await message.client.send_message(message.peer_id, hui)
            return
        for i in args.split(' '):
            if '-' in i:
                ot_do = i.split('-')
                try:
                    list_args.extend(str(x) for x in range(int(ot_do[0]), int(ot_do[1]) + 1))
                except Exception:
                    await message.reply(
                        self.strings("wrong_ot-do")
                    )
                    return
            else:
                list_args.append(i)
        a = reply.text
        lis = a.splitlines()
        for start in list_args:
            for x in lis:
                if x.lower().startswith(str(start.lower())):
                    count_st = 1
                    if 'href="' in x:
                        count_hf = 1
                        del_msg = 0
                        if not del_msg:
                            await message.delete()
                        del_msg += 1
                        b = x.find('href="') + 6
                        c = x.find('">')
                        link = x[b:c]
                        if link.startswith('tg'):
                            users = '@' + link.split('=')[1]
                            if users in exlist:
                                await message.client.send_message(message.peer_id,
                                    self.strings("ex").format(
                                    users
                                    ),
                                    reply_to=reply
                                )
                            else:
                                await message.client.send_message(message.peer_id, 
                                    f'<code>/заразить 5 {users}</code>\n<code></code>',
                                    reply_to=reply)
                        elif link.startswith('https://t.me'):
                            a = '@' + str(link.split('/')[3])
                            if a in exlist:
                                await message.client.send_message(message.peer_id,
                                    self.strings("ex").format(
                                    users
                                    ),
                                    reply_to=reply
                                )
                            else:
                                await message.client.send_message(message.peer_id, 
                                    f'<code>/заразить 5 {a}</code>\n<code></code>',
                                    reply_to=reply)
                        else:
                            await message.reply(
                                self.strings("hueta")
                            )
                        break
            await asyncio.sleep(3.3)   
        if not count_st:
            await message.reply(
                self.strings("no_sargs")
            )
        elif not count_hf:
            await message.reply(
                self.strings("no_link")
            )
        elif len(list_args) >= 5:
            await message.reply(
                self.strings("tzar")
            )
    async def оcmd(self, message):
        """
Заражает всех по реплаю.
Используй ответ на сообщение с @id/@user/link
        """
        
        reply = await message.get_reply_message()
        exlist = self.db.get("NumMod", "exUsers")
        err = "1"
        if not reply:
            await message.reply(
                self.strings("not_reply")
            )
            return
        json = JSON.loads(reply.to_json())
        try:
            for i in range(len(reply.entities)):
                try:
                    link = json["entities"][i]["url"]
                    if link.startswith('tg'):
                        users = '@' + link.split('=')[1]
                        if users in exlist:
                            await message.reply(
                                    self.strings("ex").format(
                                    users
                                    )
                                )
                        else:
                            await message.reply(f'/заразить {users}')
                    elif link.startswith('https://t.me'):
                        a = '@' + str(link.split("/")[3])
                        if a in exlist:
                            await message.reply(
                                    self.strings("ex").format(
                                    a
                                    )
                                )
                        else:
                            await message.reply(f'/заразить {a}')
                    else:
                        await message.reply(
                            self.strings("hueta")
                        )
                except Exception:
                    blayt = reply.raw_text[json["entities"][i]["offset"]:json["entities"][i]["offset"] + json["entities"][i]["length"]]
                    if blayt in exlist:
                        await message.reply(
                            self.strings("ex").format(
                                blayt
                                )
                            )
                    else:
                        await message.reply(f"/заразить {blayt}")
                await asyncio.sleep(3.3)
        
        except TypeError:
            err = "2"
            await message.edit(
                self.strings("hueta")
            )
        if err != "2":
            await message.delete()
    async def искcmd(self, message):
        """
Добавляет исключения для команд .з и .о
Используй: .иск {@user/@id/reply}
        """
        
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        exlistGet = self.db.get("NumMod", "exUsers")
        exlist = exlistGet.copy()
        if not args:
            #if reply:
            #    rid = "@" + str(reply.sender_id)


            if len(exlist) < 1:
                await message.reply(
                    self.strings("empty_zar")
                )
                return
            exsms = ''.join(f'<b>{count}.</b> <code>{i}</code>\n' for count, i in enumerate(exlist, start=1))
            await utils.answer(message, exsms)
            return
        #if reply:
        if args == 'clear':
            exlist.clear()
            self.db.set("NumMod", "exUsers", exlist)
            await message.reply(
                self.strings("clrex")
            )
            return
        if len(args.split(' ')) > 1 or args[0] != '@':
            await message.reply(
                self.strings("too_much_args")
            )
            return
        if args in exlist:
            exlist.remove(args)
            self.db.set("NumMod", "exUsers", exlist)
            await message.edit(
                self.strings("exrm").format(
                    args
                )
            )
            return
        exlist.append(args)
        self.db.set("NumMod", "exUsers", exlist)
        await message.edit(
            self.strings("exadd").format(
                args
            )
        )
    async def зарcmd(self, message):
        """
Список ваших заражений.
.зар {@id} {чис.ло} {арг}
Для удаления: .зар {@id}

Аргументы:
к ->  добавить букву k(тысяч) к числу.
ф/о ->  поиск по ид'у/юзеру.
р ->  добавлению в список по реплаю.

-backup ->  бэкап зарлиста в файл.
-restore ->  добавление жертв из бэкапа в зарлист.
-restore --y ->  полная замена зарлиста на бэкап.
        """
        pref = self.get_prefix()
        norm_args = utils.get_args(message)
        infList = self.db.get("NumMod", "infList")
        file_name = 'zarlistbackup.pickle'
        id = message.to_id
        reply = await message.get_reply_message()        
        args = utils.get_args_raw(message)
        infList = self.db.get("NumMod", "infList")
        timezone = "Europe/Kiev"
        vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
        k = ''
        with contextlib.suppress(Exception):
            args_list = args.split(' ')
        ###
        args_backup, args_restore, args_restore_y = [
            "backup",
            "-backup",
            "-b",
            "--backup",
            "--b"],[
            "restore",
            "-restore",
            "--restore",
            "-r",
            "--r"],[
            "--y"
        ]
        if args in args_backup:
            try:
                await message.delete()
                dict_all = { 'zar': infList}
                with open(file_name, 'wb') as f:
                    pickle.dump(dict_all, f)
                return await message.client.send_file(id, file_name)
            except Exception as e:
                return await utils.answer(message, f"<b>Ошибка:\n</b>{e}")            

        try:
            if norm_args[0] in args_restore:
                backupargs1 = 0
                try:
                    if norm_args[1] in args_restore_y:
                        backupargs1 = 1
                except:
                    pass
                reply_document = ""
                try:
                    reply_document = reply.document
                except AttributeError:
                    pass
    
                try:
                    if not reply:
                        return await message.reply(
                            self.strings("not_reply")
                        )
                    if not reply_document:
                        return await utils.answer(message, f"<b>ебалай, это не файл.</b>")
    
                    await reply.download_media(file_name)
                    with open(file_name, 'rb') as f:
                        data = pickle.load(f)
                    zar = data['zar']
                    result_zar = dict(infList, **zar)
                    if backupargs1:
                        infList.clear()
                    a = "с заменой " if backupargs1 else ""
                    self.db.set("NumMod", "infList", result_zar)
                    
                    return await utils.answer(message, f"<emoji document_id=5212932275376759608>✅</emoji> <b>Бекап зарлиста {a}загружен!</b>")
                except Exception as e:
                    return await utils.answer(message, f"<b>пиздец, Ошибка:\n</b>{e}")
        except IndexError:
            pass
        if not args:
            if not infList:
                return await message.edit(
                    self.strings("empty_zar")
                )
            sms = "<emoji document_id=5382116710817995998>😷</emoji> Список ваших заражений:\n\n"
            sms += ''.join(
                f"• {key}  +{value[0]} [{value[1]}]\n"
                    for key, value in infList.items()
            )
            return await utils.answer(message, sms)
            
        ##
        ###
        if 'р' in args.lower():
            reply = await message.get_reply_message()
            
            if not reply:
                return await message.reply(
                    self.strings("no_zar_reply")
                )
            ##

            trueZ = 'подверг заражению'
            trueZ2 = 'подвергла заражению' # да, я еблан)
            text = reply.text
            if trueZ not in reply.text and trueZ2 not in reply.text:
                await message.reply(
                    self.strings("wrong_zar_reply")
                )
            else:  # ☣
                try:
                    ept = ""
                    text = reply.text
                    x = text.index('☣') + 4
                    count = text[x:].split(' ', maxsplit=1)[0]
                    x = text.index('user?id=') + 8
                    user = '@' + text[x:].split('"', maxsplit=1)[0]
                    infList[user] = [str(count), vremya]
                    self.db.set("NumMod", "infList", infList)
                    await message.reply(
                        self.strings("r.save").format(
                            user, count, ept
                        )
                    )
                except ValueError:
                    await message.reply(
                        self.strings("nolink")
                    )
        elif args_list[0] == "clear84561":
            infList.clear()
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("clrzar")
            )

        elif 'ф' in args.lower() or 'о' in args.lower():
            zhertva = 0
            reply = await message.get_reply_message()

            if not reply:            
                zhertva = 0
                if re.fullmatch(r"@\d{3,10}", args_list[0], flags=re.ASCII):
                    zhertva = args_list[0]

                if re.fullmatch(r"@\D\w{3,32}", args_list[0], flags=re.ASCII):
                    try:
                        get_id = await message.client.get_entity(args_list[0])
                        get_id = get_id.id
                        zhertva = "@" + str(get_id)
                    except ValueError:
                        return await message.reply(
                            self.strings("no_user").format(
                                args_list[0]
                            )
                        ) 
                if not zhertva:
                    return await message.reply(
                        self.strings("wrong_cmd")
                    )
                if zhertva in infList:
                    user = infList[zhertva]
                    await message.reply(
                        self.strings("search").format(
                            zhertva, user[0], user[1]
                        )
                    )
                if zhertva not in infList:   
                    await message.reply(
                        self.strings("nf")
                    )  

            if reply: # <- костыль для фикса UnboundLocalError: local variable 'reply' ...
                rid = '@' + str(reply.sender_id)

                zhertva = "R#C*N("

                if re.fullmatch(r"@\d{3,10}", args_list[0], flags=re.ASCII):
                    zhertva = args_list[0]

                if re.fullmatch(r"@\D\w{3,32}", args_list[0], flags=re.ASCII):
                    try:
                        get_id = await message.client.get_entity(args_list[0])
                        get_id = get_id.id
                        zhertva = "@" + str(get_id)
                    except:
                        return await message.reply(
                            self.strings("no_user").format(
                                args_list
                            )
                        )                
                if zhertva in infList:
                    user = infList[zhertva]
                    await message.reply(
                        self.strings("search").format(
                            zhertva, user[0], user[1]
                        )
                    )                             
                elif rid in infList:
                    user = infList[rid]
                    await message.reply(
                        self.strings("search").format(
                            rid, user[0], user[1]
                        )
                    )              
                        
                elif rid not in infList:
                        await message.reply(
                            self.strings("nf")
                        )
        elif len(args_list) == 1 and args_list[0] in infList:
            del_zar = f"(+{infList[args_list[0]][0]}) "
            infList.pop(args_list[0])
            self.db.set("NumMod", "infList", infList)
            
            await message.reply(
                self.strings("zar_rm").format(
                    args, del_zar
                )
            )

        else:
            k = ''
            pas = 0
            try:
                user, count = str(args_list[0]), float(args_list[1])
            except Exception:
                try:
                    if "к" in args_list[1] or "k" in args_list[1]:
                        user = str(args_list[0])
                        args = str(args_list[1])
                        len_args = len(args_list[1])
                        count = args[:len_args-1]
                        count = float(count)
                        k += 'k'
                        pas = 1
                    else: 
                        return await message.reply(
                            self.strings("wrong_cmd")
                        )
                except: 
                    return await message.reply(
                        self.strings("wrong_cmd")
                    )                
            if re.fullmatch(r"@\D{3,32}\w{3,32}", user, flags=re.ASCII):

                get_id = await message.client.get_entity(user)
                get_id = get_id.id
                user = "@" + str(get_id)

                                  
            if 'к' in args.lower() and pas == 0 or 'k' in args.lower() and pas == 0:
                k += "k"     
            infList[user] = [str(count) + k, vremya]
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("r.save").format(
                            user, count, k
                )
            )


    async def калкcmd(self, message: Message):
        """
        Команда, которая вычисляет сколько 🧬Био-ресурсов или же ic☣️ нужно\nПример: .ic <характеристика> <уровень С> <уровень До>\n
        """
        args = utils.get_args(message)
        if not args or len(args) != 3 or not args[1].isdigit() or not args[2].isdigit() or args[2] == args[1] or int(args[2]) <= int(args[1]):
            await utils.answer(
                message, "🚫| <b>Чтобы использовать калькулятор напишите .ic <навык> <уровень С> <уровень До></b>"
            )
            return

        skill, from_lvl, to_lvl = args
        from_lvl, to_lvl = int(from_lvl), int(to_lvl)
        amount = (
            await self._client.inline_query(
                "@hikkaftgbot", f"{skill}#{from_lvl}#{to_lvl}"
            )
        )[0].title

        if not amount.isdigit():
            await utils.answer(message, amount)
            return

        amount = f"{int(amount):,}".replace(",", " ")

        await utils.answer(
            message,
            f"🍀| Чтобы увеличить навык «{skill}» с {from_lvl} до {to_lvl} уровня"
            f" потребуется: {amount} био-ресурсов🧬 или же ic☣️",
        )

    async def довcmd(self, message):
        """
{args1} {args2 OR reply}
Введи команду для просмотра аргументов.
        """
        
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        filter_and_users = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
        wnik = await self._client(GetFullUserRequest(message.sender_id))
        ent = wnik.users[0]
        a = self.config
        pref = self.get_prefix()
        dovs = ""
        if a["Доступ к лабе"]:
            dovs += "лабе, "
        if a["Доступ к заражениям"]:
            dovs += "заражениям, "
        if a["Доступ к прокачке"]:
            dovs += "прокачкам, "
        if a["Доступ к зарлисту"]:
            dovs += "зарлисту, "        
        if a["Доступ к жертвам"]:
            dovs += "жертвам, "
        if a["Доступ к болезням"]:
            dovs += "болезням, "
        if a["Доступ к вирусам"]:
            dovs += "установке вирусов, "
        if a["Доступ к хиллингу"]:
            dovs += "хиллингу, "
        len_dovs = len(dovs)
        dovs_accept = dovs[:len_dovs-2]

        dov_users = ', '.join(
            f'<code>@{i}</code>' for i in filter_and_users['users']
        )
        if not args:
            return await self.inline.form(
                self.strings("dov").format(
                    dov_users,
                    filter_and_users['filter'] or '❌ Не установлен.',
                    '✅ Запущен' if self.config["Вкл/выкл"] else '❎ Остановлен',
                    ent.first_name if len(ent.first_name) <= 12  else "ник",
                    dovs_accept if dovs_accept != "" else "всё ограничено 👌",
                    pref
                ),
                reply_markup={
                    "text": "Закрыть",
                    "callback": self.inline__close,

                },
                message=message,
                disable_security=False
            )
        args = args.split(' ', maxsplit=1)
        if len(args) == 1 and not reply and args[0] != 'пуск': # 
            return await utils.answer(message, '🤔 Не могу понять, что за хуета?..')
        
        elif args[0] == 'сет':
            try:
                user_id = args[1]
                if not user_id.isdigit():
                    return await message.reply(
                        self.strings("wrong_id")
                    )

            except Exception:
                user_id = str(reply.sender_id)
            
            if user_id in filter_and_users['users']:
                filter_and_users['users'].remove(user_id)
                return await message.reply(
                    self.strings("user_rm").format(
                        user_id
                    )
                )
            elif user_id not in filter_and_users['users']:
                filter_and_users['users'].append(user_id)
                return await message.reply(
                    self.strings("user_add").format(
                        user_id
                    )
                )

            return self.db.set("NumMod", "numfilter", filter_and_users)
        
        elif args[0] == 'ник':
            try:
                filter_and_users['filter'] = args[1].lower().strip()
                self.db.set("NumMod", "numfilter", filter_and_users)
                return await message.reply(
                    self.strings("nick_add").format(
                        args[1]
                    )
                )
            except Exception:
                return await message.reply(
                    self.strings("wrong_nick")
                )

        
        elif args[0] == 'пуск':
            if self.config["Вкл/выкл"]:
                self.config["Вкл/выкл"] = False
                return await message.reply(
                    self.strings("dov_stop")
                )

            else:
                self.config["Вкл/выкл"] = True
                return await message.reply(
                    self.strings("dov_start")
                )

        else:
            return await message.reply(
                self.strings("dov.wrong_args")
            )

    async def message_q( # спизжено из IrisLab
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
    ):
        """Отправляет сообщение и возращает ответ"""
        async with self.client.conversation(user_id, exclusive=False) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if mark_read:
                await conv.mark_read()

            if delete:
                await msg.delete()
                await response.delete()

            return response

    async def watcher(self, message):
        if not isinstance(message, telethon.tl.types.Message): return
        filter_and_users = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
        user_id = str(message.sender_id)
        sndr_id = message.sender_id
        
        nik = filter_and_users["filter"]
        text = message.raw_text.lower()
        reply = await message.get_reply_message()
        infList = self.db.get("NumMod", "infList")
        args = utils.get_args(message)
#############################################################     Авто Зарлист
        get_me = await message.client.get_me()
        timezone = "Europe/Kiev"
        vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
        if re.search(r"подве.{2,4} заражению", text, flags=re.ASCII):
            if not self.config["Автосохранение жертв"]:
                return
            split_text, r_text, msg_text = "", "", ""
            try:
                msg_text = message.text
                split_text = msg_text.splitlines()
                r_text = reply.text
                
            except:
                pass
            irises = [
                5443619563, 
                707693258, 
                5226378684, 
                5137994780, 
                5434504334
            ]
            if message.sender_id not in irises:
                return            
            attempts = "🗓 Отчёт об операции заражения объекта:"
            podverg = split_text[0] if attempts not in msg_text else split_text[3]
            retur = 0
            try:
                if podverg.startswith('🦠 <a href="https://t.me/'):
                    y = podverg.index('https://t.me/') + 13
                    user3 = podverg[y:].split('"', maxsplit=1)[0]
                    if user3.lower() != get_me.username.lower():
                        return
                    retur = 1
                if podverg.startswith('🦠 <a href="tg:'):
                    y = podverg.index('user?id=') + 8  
                    user3 = podverg[y:].split('"', maxsplit=1)[0]    
                    if get_me.id != user3:
                        return 
                    retur = 1
            except ValueError:
                pass
            if sndr_id not in irises:
                return await message.reply("что за хуета")
            if not retur:
                return
            try:
                x = msg_text.index('☣') + 4
                count = msg_text[x:].split(' ', maxsplit=1)[0]
                

                #if count == "1":
                #    return await message.reply("ок")

                x = msg_text.index('user?id=') + 8
                user = '@' + msg_text[x:].split('"', maxsplit=1)[0]
                ept = f"<s>+{infList[user][0]}</s>  " if user in infList else ""
                infList[user] = [str(count), vremya]
                self.db.set("NumMod", "infList", infList)
                await message.reply(self.strings("auto.save").format(user, ept, count))
            except ValueError:
                return
                #await message.reply(
                #    self.strings("nolink")
                #)
############################################################
        if re.fullmatch(r"ид\s@.{,32}", text, flags=re.ASCII):
            if str(sndr_id) != str(get_me.id):
                return
            user = 0
            if re.fullmatch(r"@\D\w{3,32}", args[0], flags=re.ASCII):
                user = await message.client.get_entity(args[0])
            
            elif re.fullmatch(r"@\d{4,14}", args[0], flags=re.ASCII):
                user = args[0].replace("@", "")
                user = await message.client.get_entity(int(user))
            if not user:
                return await message.reply("ты ввел хуйню реально")

            link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)
            return await message.reply(
                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
            )        

        if text == "ид":
            if str(sndr_id).lower() != str(get_me.id).lower():
                return
            reply = await message.get_reply_message()
            args = utils.get_args(message)
            if not reply:
                user = await message.client.get_entity(message.sender_id)
                link = f'<a href="t.me/{user.username}">{user.first_name}</a>' if user.username else f'<a href="tg://openmessage?user_id={user.id}">{user.first_name}</a>'
                return await message.reply(
                    f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                    f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
                )
            user = await message.client.get_entity(reply.sender_id)
            link = f'<a href="t.me/{user.username}">{user.first_name}</a>' if user.username else f'<a href="tg://openmessage?user_id={user.id}">{user.first_name}</a>'
            return await message.reply(
                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
            )
    
            user = 0
            if re.fullmatch(r"@\D\w{3,32}", args[0], flags=re.ASCII):
                user = await message.client.get_entity(args[0])
            
            elif re.fullmatch(r"@\d{4,14}", args[0], flags=re.ASCII):
                user = args[0].replace("@", "")

            if not user:
                return await message.reply("ты ввел хуйню реально")
            link = '<a href="t.me/{}">{}</a>'.format(user.username, user.first_name) if user.username else '<a href="tg://openmessage?user_id={}">{}</a>'.format(user.id, user.first_name)
            return await message.reply(
                f"<emoji document_id=5780683340810030158>✈️</emoji> {link}\n"
                f"<emoji document_id=4918133202012340741>👤</emoji> <code>@{user.id}</code>"
            )
        if text == "жд":
            if str(sndr_id) != str(get_me.id):
                return
            if not reply:
                return await message.reply(
                    self.strings("no_zar_reply")
                )
            trueZ = 'подверг заражению'
            trueZ2 = 'подвергла заражению' # да, я еблан)
            text = reply.text
            if trueZ not in reply.text and trueZ2 not in reply.text:
                return await message.reply(
                    self.strings("wrong_zar_reply")
                )
            try:
                ept = ""
                text = reply.text
                x = text.index('☣') + 4
                count = text[x:].split(' ', maxsplit=1)[0]
                x = text.index('user?id=') + 8
                user = '@' + text[x:].split('"', maxsplit=1)[0]
                infList[user] = [str(count), vremya]
                self.db.set("NumMod", "infList", infList)
                await message.reply(
                    self.strings("r.save").format(
                        user, count, ept
                    )
                )
            except ValueError:
                await message.reply(
                    self.strings("nolink")
                )

        if re.fullmatch(r"жд\s@\d{3,12}.{,10}", text, flags=re.ASCII):
            if str(sndr_id) != str(get_me.id):
                return            
            k = ''
            pas = 0
            try:
                user, count = str(args[0]), float(args[1])
            except Exception:
                try:
                    if "к" in args[1] or "k" in args[1] or "," in args:
                        count = args[1].replace("k", "").replace("к", "").replace(",", ".")
                        count = float(count)
                        user = str(args[0])
                        k += 'k'
                        pas = 1
                    else: 
                        return await message.reply(
                            self.strings("wrong_cmd")
                        )
                except: 
                    return await message.reply(
                        self.strings("wrong_cmd")
                    )                
            if re.fullmatch(r"@\D{3,32}\w{3,32}", user, flags=re.ASCII):
                get_id = await message.client.get_entity(user)
                get_id = get_id.id
                user = "@" + str(get_id)

            if 'к' in args and pas == 0 or 'k' in args and pas == 0:
                k += "k"     
            infList[user] = [str(count) + k, vremya]
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("r.save").format(
                            user, count, k
                )
            )


        if text == "жу":
            if str(sndr_id) != str(get_me.id):
                return
            if not reply:
                return
            user = "@" + str(reply.sender_id)
            if user not in infList:
                return await message.reply(
                    self.strings("nf")
                )
            del_zar = f"(+{infList[user][0]}) "
            infList.pop(user)
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("zar_rm").format(
                    args, del_zar
                )
            )

        if re.fullmatch(r"жу\s@\d{3,12}", text, flags=re.ASCII):
            if str(sndr_id) != str(get_me.id):
                return
            user = "@" + text.split("@", maxsplit=1)[1]
            if user not in infList:
                return await message.reply(
                    self.strings("nf")
                )
            del_zar = f"(+{infList[user][0]}) "
            infList.pop(user)
            self.db.set("NumMod", "infList", infList)
            await message.reply(
                self.strings("zar_rm").format(
                    args, del_zar
                )
            )


        if text == "жл":
            if str(sndr_id) != str(get_me.id):
                return
            if not reply:
                return
            zhertva = "@" + str(reply.sender_id)
            if zhertva in infList:
                user = infList[zhertva]
                await message.reply(
                    self.strings("search").format(
                        zhertva, user[0], user[1]
                    )
                )
            if zhertva not in infList:   
                await message.reply(
                    self.strings("nf")
                )  
        if re.fullmatch(r"жл\s@\d{3,12}", text, flags=re.ASCII):
            if str(sndr_id) != str(get_me.id):
                return
            zhertva = "@" + text.split("@", maxsplit=1)[1]
            
            if zhertva in infList:
                user = infList[zhertva]
                await message.reply(
                    self.strings("search").format(
                        zhertva, user[0], user[1]
                    )
                )
            if zhertva not in infList:   
                await message.reply(
                    self.strings("nf")
                )  

        if not nik or not self.config["Вкл/выкл"] or user_id not in filter_and_users['users']: 
            return
        if not text.startswith(nik): return
        
        if self.config["Доступ к заражениям"] == True:  
            if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}\s|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?(?P<link>@[0-9a-z_]+|(?:https?://)?t\.me/[0-9a-z_]+|tg://openmessage\?user_id=(?P<id>[0-9]+))",
                text, flags=re.ASCII
            ):
                
                send_mesа = send_mesа.groupdict()
                send_mesа['link'], send_mesа['id'] = '@' + send_mesа['id'] if send_mesа['id'] else send_mesа['link'], ''
                send_mesа['z'] = '/заразить '
                send_mesа['lvl'] = send_mesа['lvl'] or ''
                mes = ''.join(send_mesа.values())
                await message.reply(mes)

        if self.config["Доступ к заражениям"] == True:  
            if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}\s|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?([\=])",
                text, flags=re.ASCII
            ):
                
                send_mesа = send_mesа.groupdict()
                send_mesа['ravno'] = '='
                send_mesа['z'] = '/заразить '
                send_mesа['lvl'] = send_mesа['lvl'] or ''
                mes = ''.join(send_mesа.values())
                await message.reply(mes)

        if self.config["Доступ к заражениям"] == True:  
            if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}\s|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?([\-])",
                text, flags=re.ASCII
            ):
                
                send_mesа = send_mesа.groupdict()
                send_mesа['minus'] = '-'
                send_mesа['z'] = '/заразить '
                send_mesа['lvl'] = send_mesа['lvl'] or ''
                mes = ''.join(send_mesа.values())
                await message.reply(mes)

        if self.config["Доступ к заражениям"] == True:  
            if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}\s|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?([\+])",
                text, flags=re.ASCII
            ):
                
                send_mesа = send_mesа.groupdict()
                send_mesа['plus'] = '+'
                send_mesа['z'] = '/заразить '
                send_mesа['lvl'] = send_mesа['lvl'] or ''
                mes = ''.join(send_mesа.values())
                await message.reply(mes)

        if self.config["Доступ к заражениям"] == True:  
            if send_mesа := re.search(
                r"(?P<z>бей\s|кус[ьайни]{,3}\s|зарази[тьть]{,3}\s|еб[ниажшь]{,3}\s|уеб[иаошть]{,3}\s|опуст[и]{,2}\s|организуй горячку\s)(?P<lvl>[1-9]?[0]?\s)?([/^равного])",
                text, flags=re.ASCII
            ):
                
                send_mesа = send_mesа.groupdict()
                send_mesа['ravno1'] = '='
                send_mesа['z'] = '/заразить '
                send_mesа['lvl'] = send_mesа['lvl'] or ''
                mes = ''.join(send_mesа.values())
                await message.reply(mes)

            #if send_mesа := re.search(
            #    r"(?P<eb>бей\s|еб\s)(?P<lvl>[1-9]?[0]?\s)", text):
            #    if text == f"{nik} еб":
            #        if reply:
            #            popusk = reply.sender_id 
            #            send_mesа = send_mesа.groupdict()
            #            send_mesа['z'] = '/зоразить '
            #            send_mesа['lvl'] = send_mesа['lvl'] or ''
            #            send_mesа['id'] = popusk
            #            mes = ''.join(send_mesа.values())
            #            await message.reply(mes)






###### чеки
        if self.config["Доступ к прокачке"] == True:  
            if send_mes := re.search(r"(?P<ch>зараз[куаность]{,5} чек[нутьиай]{,4}\s|чек[айниуть]{,4} зараз[куаность]{,5}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['ch'] = '+заразность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
    
    
            elif send_mes := re.search(r"(?P<pat>пат[огены]{,5} чек[айниуть]\s|чек[айниуть]{,4} пат[огены]{,5}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['pat'] = '+патоген '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<let>летал[каьностьу]{,5} чек[айниуть]{,4}\s|чек[айниуть]{,4} летал[каьностьу]{,5}\s)(?P<lvl>[1-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['let'] = '+летальность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<kvala>квал[лаификацияу]{,8} чек[айниуть]{,4}\s|разраб[откау]{,4} чек[айниуть]{,4}\s|чек[айниуть]{,4} разраб[откау]{,4}\s|чек[айниуть]{,4} квал[улаификация]{,8}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['kvala'] = '+квалификация '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<imun>чек[айниуть]{,4} иммун[еитеткау]{,4}\s|чек[айниуть]{,4} имун[еитеткау]{,4}\s|имун[еитеткау]{,4} чек[айниуть]{,4}\s|иммун[еитеткау]{,4} чек[айниуть]{,4}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['imun'] = '+иммунитет '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<sb>сб чек[айниуть]{,4}\s|безопасно[сть]{,3} чек[айниуть]{,4}\s|служб[ау]{,2} чек[айниуть]{,4}\s|чек[айниуть]{,4} служб[ау]{,2}\s|чек[айниуть]{,4} безопасно[сть]{,3}\s|чек[айниуть]{,4} сб\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['sb'] = '+безопасность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
#### кач    алки
            elif send_mes := re.search(r"(?P<zar>зараз[уканость]{,5}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['zar'] = '++заразность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<pat>пат[огены]{,5}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['pat'] = '++патоген '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<let>летал[укаьность]{,5}\s)(?P<lvl>[1-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['let'] = '++летальность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<kvala>квал[улаификация]{,8}\s|разраб[откау]{,4}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['kvala'] = '++квалификация '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<imun>иммун[уеитетка]{,4}|имун[уеитетка]{,4}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['imun'] = '++иммунитет '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            elif send_mes := re.search(r"(?P<sb>сб\s|безопасно[сть]{,3}\s|служб[ау]{,2}\s)(?P<lvl>[0-5]+)", text, flags=re.ASCII):
                send_mes = send_mes.groupdict()
                send_mes['sb'] = '++безопасность '
                send_mes['lvl'] = send_mes['lvl'] or ''
                mes = ''.join(send_mes.values())
                await message.reply(mes)
            
        if self.config["Доступ к болезням"] == True:  
            if re.search(r"бол[езьни]{,5}\b", text, flags=re.ASCII):
                await message.reply('/мои болезни')
        
        if self.config["Доступ к жертвам"] == True:  
            if re.search(r"жертв[ыау]{,2}|еж[ау]{,2}", text, flags=re.ASCII):
                await message.reply('/мои жертвы')

        if self.config["Доступ к вирусам"] == True:  
            if re.search(r"-вирус[ыа]{,2}", text):
                await message.reply('-вирусы')
            if re.search(r"увед[ыаомления]{,8}", text, flags=re.ASCII):
                await message.reply('+вирусы')
        
        if self.config["Доступ к хиллингу"] == True:    
            if re.search(r"вак[цинау]{,3}|леч[ись]{,2}|хи[лльсяйинг]{,2}|лек[арство]{,2}", text, flags=re.ASCII):
                await message.reply('/купить вакцину')
            if re.search(r"цен[ау]{,2}|вч[ек]{,2}", text):
                await message.reply('<i>купить вакцину</i>')
        toxt = text.replace(f"{nik} ", "")
        if self.config["Доступ к лабе"] == True:
            #if re.search(r"" + nik + "%лаб[уа]{,2}|/лаб[уа]{,2}|#лаб[уа]{,2}", text, flags=re.ASCII):
            #    await message.reply('👇')
            #    await message.respond('/моя лаба')

            if re.fullmatch(r"лаб[ау]{,2}", toxt, flags=re.ASCII): # регулярка
                lab_raw = await self.message_q( # отправляет сообщение боту и возвращает текст
                    f"/лаб",
                    5443619563,
                    mark_read=True,
                    delete=True,
                )
                lab_lines = lab_raw.text.splitlines() # те��ст с лабой, разбитый на строки
                if "🔬 Досье лаборатории" not in lab_lines[0]:
                    return
                sms = ""
                for i in lab_lines: # цикл for по всем строкам в тексте лабы
                    if "🧪 Готовых патогенов:" in i:
                        s = i.replace("🧪 Готовых патогенов:", "")
                        sms += f"<emoji document_id=5783003963179666902>🌊</emoji> Готовые паты: {s}\n"
                    if "⏱ Новый патоген:" in i:
                        s = i.replace("⏱ Новый патоген:", "")
                        sms += f"<emoji document_id=5785371297613614717>🫧</emoji> Новый пат: {s}\n"
                    if "👨‍🔬 Квалификация учёных:" in i:
                        s = i.replace("👨‍🔬 Квалификация учёных:", "")
                        s = s.replace("ур", "lvl")
                        sms += f"\n<emoji document_id=5785349938741251020>🧳</emoji> Квала: {s}\n"
                    if "🦠 Заразность:" in i:
                        s = i.replace("🦠 Заразность:", "")
                        s = s.replace("ур", "lvl")
                        sms += f"<emoji document_id=5785071878263541193>🫂</emoji> Заразность: {s}\n"
                    if "🛡 Иммунитет:" in i:
                        s = i.replace("🛡 Иммунитет:", "")
                        s = s.replace("ур", "lvl")
                        sms += f"<emoji document_id=5783025837448105119>🛡</emoji> Иммунитет: {s}\n"
                    if "☠️ Летальность:" in i:
                        s = i.replace("☠️ Летальность:", "")
                        s = s.replace("ур", "lvl")
                        sms += f"<emoji document_id=5782645294755746292>💀</emoji> Летал: {s}\n"
                    if "🕵️‍♂️ Служба безопасности:" in i:
                        s = i.replace("🕵️‍♂️ Служба безопасности:", "")
                        s = s.replace("ур", "lvl")
                        sms += f"<emoji document_id=5782944641091375551>💥</emoji> Служба безопасности: {s}\n\n"
                    if "☣️ Био-опыт:" in i:
                        s = i.replace("☣️ Био-опыт:", "")
                        sms += f"<emoji document_id=5782890399949396525>☣️</emoji> Опыт: {s}\n"
                    if "🧬 Био-ресурс:" in i:
                        s = i.replace("🧬 Био-ресурс:", "")
                        sms += f"<emoji document_id=5784980159236936164>🧬</emoji> Ресурсы: {s}\n"
                await message.reply(sms) # ответ

#######################################################
        if self.config["Доступ к зарлисту"] == True:
            reply = await message.get_reply_message()
            infList = self.db.get("NumMod", "infList")
            timezone = "Europe/Kiev"
            vremya = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
            with contextlib.suppress(Exception):
                text_list = text.split(' ', maxsplit=2)
            
            if re.search(r"(?P<zarlist>з\s)(?P<link>@[0-9a-z_]+|tg://openmessage\?user_id=[0-9]+)",
                text, flags=re.ASCII):
                if not text.startswith(f"{nik} з") and not text.startswith(f"{nik}з"):
                    return
    
                if text_list[2] in infList:
                    user = infList[text_list[2]]
                    await message.reply(
                        self.strings("search").format(
                            text_list[2], user[0], user[1]
                        )
                    )
                if text_list[2] not in infList:
                    await message.reply(
                        self.strings("nf")
                    )
                else:
                    return
            
            if re.search(r"з", text, flags=re.ASCII):
                if text != f"{nik} з" and text != f"{nik}з":
                    return
                zhertva = '@' + str(reply.sender_id)

                
                if not reply:
                    return
                
                if re.fullmatch(r"@\d{5,11}", reply.text, flags=re.ASCII):
                    zhertva = reply.text

                if re.fullmatch(r".{,5}заразить @\d{5,11}", reply.text.lower(), flags=re.ASCII):
                    zhertva = "@" + str(reply.text.split("@")[1])

                if re.fullmatch(r".{,5}заразить @\d{5,11}", reply.text.lower(), flags=re.ASCII):
                    zhertva = "@" + str(reply.text.split("@")[1])

                if re.fullmatch(r".{,5}зарази[ть\s..]+ @\D\w{3,32}", reply.text.lower(), flags=re.ASCII):
                    user = "@" + str(reply.text.split("@")[1])
                    get_id = await message.client.get_entity(user)
                    get_id = get_id.id
                    zhertva = "@" + str(get_id)

                if re.fullmatch(r".{,5}зарази[ть\s..]+ @\D\w{3,32}", reply.text.lower(), flags=re.ASCII):
                    user = "@" + str(reply.text.split("@")[1])
                    get_id = await message.client.get_entity(user)
                    get_id = get_id.id
                    zhertva = "@" + str(get_id)



                if zhertva in infList:
                    user = infList[zhertva]
                    await message.reply(
                        self.strings("search").format(
                            zhertva, user[0], user[1]
                        )
                    )              
                        
                elif zhertva not in infList:
                        await message.reply(
                            self.strings("nf")
                        )  
                else:
                    return
            
            if re.search(r"сб", text, flags=re.ASCII):
                if text != f"{nik} сб" and text != f"{nik}сб":
                    return
                try:
                    reply = await message.get_reply_message()
                    txxxt = reply.text
                    org = "Организатор"
                    txxt = txxxt.splitlines()
                    zhertva = "none"
                except: 
                    pass
                
                for i in txxt:
                    if i.startswith(org):
                        b = i.find('href="') + 6
                        c = i.find('">')
                        link = i[b:c]                        
                        
                        if link.startswith("tg"):
                            zhertva = '@' + link.split('=')[1]
                        
                        if link.startswith("https://t.me"):
                            try:
                                userk = str(link.split('/')[3])
                                uebok = "@" + str(userk)
                                get_id = await message.client.get_entity(uebok)
                                get_id1 = get_id.id
                                zhertva = "@" + str(get_id1)
                            except:
                                return await message.reply("<b>флудвейт, ищи по айди</b>")

                        if zhertva in infList:
                            user = infList[zhertva]
                            await message.reply(
                                self.strings("search").format(
                                    zhertva, user[0], user[1]
                                )
                            )                             
                        elif zhertva not in infList:
                            await message.reply(
                                self.strings("nf")
                            ) 
            if re.search(r"био", text, flags=re.ASCII):
                if text != f"{nik} био" and text != f"{nik}био":
                    return
                reply = await message.get_reply_message()
                args = utils.get_args_raw(message)
                if not reply:
                    return
                bt, bch, bk, btz, bchz, ezha, bol = "🔬 ТОП ЛАБОРАТОРИЙ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:","🔬 ТОП ЛАБОРАТОРИЙ БЕСЕДЫ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:","🔬 ТОП КОРПОРАЦИЙ ПО ЗАРАЖЕНИЯМ:","🔬 ТОП БОЛЕЗНЕЙ:","🔬 ТОП БОЛЕЗНЕЙ БЕСЕДЫ:","🦠 Список больных вашим патогеном:","🤒 Список ваших болезней:"
                
                infList = self.db.get("NumMod", "infList")

                a = reply.text
                sms = ''
                if "🔬 ТОП ЛАБОРАТОРИЙ БЕСЕДЫ" in a:
                    sms += "🥰 топ вкусняшек чата:\n"
                    
                if "🔬 ТОП ЛАБОРАТОРИЙ ПО" in a:
                    sms += "🔬 ТOП ЛАБОРАТOРИЙ ПО БИO-ОПЫТУ ЗАРAЖЁННЫХ:\n" #ТOП ИММУНОДРОЧЕРОВ:
        
                if bt not in a and bch not in a and bk not in a and btz not in a and bchz not in a and ezha not in a and bol not in a:
                    return 
                b = reply.raw_text.splitlines() 
                b.pop(0)
                hh = []
                for i in b:
                    try:
                        hh.append(i.split('|')[1])
                    except: pass
                json = JSON.loads(reply.to_json())
                
                count = 1
                for i in range(0, len(reply.entities) ):
                    try:
                        exp = hh[i]
                    except:
                        exp = i
                    link = json["entities"][i]["url"]
                    try:
                        if link.startswith('tg'):
                            bla = []
                            for i in link.split('='):
                                bla.append(i)
                            b = await message.client.get_entity(int(bla[1]))
                            
                            b_first_name1 = utils.remove_html(utils.validate_html(utils.escape_html(b.first_name)))
        
                            b_first_name2 = b_first_name1.replace("|", "/")
        
                            b_final = "<a href='tg://openmessage?user_id={0}'>{1}</a>".format(b.id, b_first_name2)
                            
                            
                            zh = ''
                            b_id = "@" + bla[1]
                            if b_id in infList:
                                user = infList[b_id]
                                zh = f"(+{user[0]}) "
        
        
                            sms += f'{str(count)}. {b_final} {zh}| {exp} | <code>@{b.id}</code>\n'
                        
                        elif link.startswith('https://t.me'):
                            a = '@' + str(link.split('/')[3])
                            sms += f'{str(count)}. <code>{a}</code> | <u>{result}</u>\n'
                        else:
                            sms += f'{str(count)}. что за хуе��а?\n'
                    except:
                        if link.startswith('https://t.me'):
                            a ='@' + str(link.split('/')[3])
                            sms += f'{str(count)}. <code>{a}</code> | <u>{exp}</u> \n'
                        elif link.startswith('tg'):
                            bla = []
                            for i in link.split('='):
                                bla.append(i)
                            blya = "<a href='tg://openmessage?user_id={0}'>???</a>".format(bla[1])
                            zh = ''
                            b_id = "@" + bla[1]
                            if b_id in infList:
                                user = infList[b_id]
                                zh = f"(+{user[0]}) "
                            sms += f'{str(count)}. {blya} {zh}| {exp} | <code>@{bla[1]}</code>  \n'
                    count += 1
        
                try:
                    await self.inline.form(
                        sms,
                        reply_markup={
                                        "text": f"🔻 Close",
                                        "callback": self.inline__close,
                        },
                        message=message,
                        disable_security=False
                    )
                except:
                    await message.reply(sms) 
            
#######################################################

###     
    async def гcmd(self, message):
        """
[arg] [arg] [arg]....
Выполняет команду .ид по реплаю.
Аргументом являются числа и первые символы строки.
        """
        
        reply = await message.get_reply_message()
        
        count_st = 0
        count_hf = 0
        if not reply:
            await message.reply(
                self.strings("not_reply")
            )
            return

        args = utils.get_args_raw(message)
        list_args=[]
        if not args:
            await message.reply(
                self.strings("not_args")
            )
            return
        a = reply.text
        for i in args.split(' '):
            if '-' in i:
                ot_do = i.split('-')
                try:
                    for x in range(int(ot_do[0]),int(ot_do[1])+1):
                        list_args.append(str(x))
                except:
                    await message.reply(
                        self.strings("ot_do")
                    )
                    return
            else:
                list_args.append(i)
        lis = []
        for i in a.splitlines():
            lis.append(i)
        for start in list_args:
            for x in lis:
                if x.lower().startswith(str(start.lower())):
                    count_st = 1
                    if 'href="' in x:
                        count_hf = 1
                        b=x.find('href="')+6
                        c=x.find('">')
                        link = x[b:c]
                        if link.startswith('tg'):
                            list = []
                            for i in link.split('='):
                                list.append(i)
                            await message.reply(f'.ид <code>@{list[1]}</code>'
                            )
                            break
                        elif link.startswith('https://t.me'):
                            a ='@' + str(link.split('/')[3])
                            await message.reply(f'.ид <code>{a}</code>'
                            )
                            break
                        else:
                            await message.reply(
                                self.strings("hueta")
                            )
                            break
            await asyncio.sleep(3)
        if not count_st:
            await message.reply(
                self.strings("no_sargs")
            )
        elif not count_hf:
            await message.reply(
                self.strings("nolink")
            )
        elif len(list_args) >= 5:
            await message.respond(
                self.strings("tids")
            )
            await asyncio.sleep(3.3)


    async def иcmd(self, message):
        """
Чекает все айди по реплаю.
Используй ответ на сообщение с @id/@user/link
        """
        reply = await message.get_reply_message()
        if not reply:
            await message.reply(
                self.strings("not_reply")
            )
            return
        json = JSON.loads(reply.to_json())
        for i in range(len(reply.entities)):
            try:
                link = json["entities"][i]["url"]
                if link.startswith('tg'):
                    users = '@' + link.split('=')[1]
                    await message.reply(f'.ид {users}')
                elif link.startswith('https://t.me'):
                    a = '@' + str(link.split("/")[3])
                    await message.reply(f'.ид {a}')
                else:
                    await message.reply(
                        self.strings("hueta")
                    )
            except Exception:
                hueta = validate_text(reply.raw_text)
                
                blayt = hueta[json["entities"][i]["offset"]:json["entities"][i]["offset"] + json["entities"][i]["length"]]
                await message.reply(f".ид <code>{blayt}</code>")
            await message.delete()
            await asyncio.sleep(3.3)
    
    async def бcmd(self, message):
        """
Используй ответом на биотопы/жертвы и т.п
        """
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        infList = self.db.get("NumMod", "infList")
        
        a = reply.text
        b = reply.raw_text.splitlines()
        
        if not reply:
            await message.edit(
                self.strings("not_reply")
               )
            return

        sms = ''
        if "🔬 ТОП ЛАБОРАТОРИЙ БЕСЕДЫ" in a:
            sms += "🥰 топ вкусняшек чата:\n"
            
        if "🔬 ТОП ЛАБОРАТОРИЙ ПО" in a:
            sms += "🔬 ТOП ЛАБОРАТOРИЙ ПО БИO-ОПЫТУ ЗАРAЖЁННЫХ:\n" #ТOП ИММУНОДРОЧЕРОВ:

        not_hueta = [
            "🔬 ТОП ЛАБОРАТОРИЙ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:",
            "🔬 ТОП ЛАБОРАТОРИЙ БЕСЕДЫ ПО БИО-ОПЫТУ ЗАРАЖЁННЫХ:",
            "🔬 ТОП КОРПОРАЦИЙ ПО ЗАРАЖЕНИЯМ:",
            "🔬 ТОП БОЛЕЗНЕЙ:",
            "🔬 ТОП БОЛЕЗНЕЙ БЕСЕДЫ:",
            "🦠 Список больных вашим патогеном:",
            "🤒 Список ваших болезней:"
        ]

        if b[0] not in not_hueta: 
            await message.respond(
                self.strings("hueta")
            )
            return 
        get_me = await message.client.get_me()
        emojis = [
            "<emoji document_id=5219806684066618617>🍎</emoji>",
            "<emoji document_id=5215493819641895305>🚛</emoji>",
            "<emoji document_id=5213452215527677338>⏳</emoji>",
            "<emoji document_id=5213107179329953547>⏰</emoji>",
            "<emoji document_id=5314775862749438888>🔠</emoji>",
            "<emoji document_id=5316939156172053790>🟪</emoji>",
            "<emoji document_id=5314362416312623719>🔝</emoji>",
            "<emoji document_id=5316567190529384159>🤔</emoji>"
        ]
        emoji = f"{random.choices(emojis, k=1)[0]} " if get_me.premium else ""

        hiunya = [
            f"{emoji}<b>щас ебанёт)...</b> {utils.ascii_face()}",
            f"{emoji}<b>взлом пентагона...</b> {utils.ascii_face()}",
            f"{emoji}<b>доза героина поступает в кровь...</b> {utils.ascii_face()}"
        ]
        msg = f"{emoji}<b>Loading... {utils.ascii_face()}<b>"
        if random.randint(1, 100) > 95:
            msg = random.choices(hiunya, k=1)[0]
        await utils.answer(message, msg)
        b.pop(0)
        hh = []
        for i in b:
            try:
                hh.append(i.split('|')[1])
            except: pass
        json = JSON.loads(reply.to_json())
        
        count = 1
        for i in range(0, len(reply.entities) ):
            exp = ""
            try:
                exp = hh[i]
            except:
                exp = i
            link = json["entities"][i]["url"]
            if link.startswith('tg'):
                bla = []
                for i in link.split('='):
                    bla.append(i)   
                b_id = "@" + bla[1]
                zh = f"<b>(✔{infList[b_id][0]}) </b>" if b_id in infList else ""
                
                try:
                    b = await message.client.get_entity(int(bla[1]))
                    name = utils.remove_html(utils.validate_html(b.first_name))
                    name = f"<a href='tg://openmessage?user_id={b.id}'>{name}</a>"
                    sms += f'{str(count)}. {name} {zh}| {exp} | <code>@{b.id}</code>\n'
                except:
                    blya = "<a href='tg://openmessage?user_id={0}'>???</a>".format(bla[1])
                    sms += f'{str(count)}. {blya} {zh}| {exp} | <code>@{bla[1]}</code>\n'
            
            elif link.startswith('https://t.me'):
                a = '@' + str(link.split('/')[3])
                try:    
                    sms += f'{str(count)}. <code>{a}</code> | <u>{result}</u>\n'
                except:
                    sms += f'{str(count)}. <code>{a}</code> | <u>{exp}</u>\n'
            else:
                sms += f'{str(count)}. что за хуета?\n'
            count += 1
        
        await self.inline.form(
            sms,
            reply_markup={
                            "text": f"🔻 Close",
                            "callback": self.inline__close,
            },
            message=message,
            disable_security=False
        )
        

### помощь
    async def biohelpcmd(self, message: Message):
        """
Выдает помощь по модулю
        """
        
        pref = self.get_prefix()
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        args = args.lower()
 
#######################   
        if args == 'дов':
            nnik = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
            nik = nnik['filter'] or 'ник' 
            await self.inline.form(
                self.strings("guidedov").format(
                    nik, pref
                ),
                reply_markup={
                    "text": "Закрыть",
                    "callback": self.inline__close,

                },
                message=message,
                disable_security=False
            )   
        elif args == "зарлист":
            nnik = self.db.get("NumMod", "numfilter", {'users': [], 'filter': None, 'status': False})
            nik = nnik['filter'] or 'ник' 
            await self.inline.form(
                self.strings("zarlistHelp").format(
                    pref, nik
                ),
                reply_markup={
                    "text": "Закрыть",
                    "callback": self.inline__close,

                },
                message=message,
                disable_security=False
            )
        else:
            await self.inline.form(
                self.strings("guide").format(
                        pref
                ),
                reply_markup={
                                "text": "Закрыть",
                                "callback": self.inline__close,
                },
            message=message,
            disable_security=False
            )
    async def inline__close(self, call) -> None:
        await call.delete()

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "Доступ к лабе",
                False,
                "Доступ к лабе через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к заражениям",
                True,
                "Доступ к команде заражения через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к прокачке",
                False,
                "Доступ к прокачке навыков через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к зарлисту",
                False,
                "Доступ к поиску жертв в зарлисте через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к жертвам",
                True,
                "Доступ к жертвам через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к болезням",
                True,
                "Доступ к болезням через доверку",
                validator=loader.validators.Boolean(),
            ),

            loader.ConfigValue(
                "Доступ к вирусам",
                False,
                "Доступ к установке вирусов через доверку",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Доступ к хиллингу",
                True,
                "Доступ к покупке вакцины",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Вкл/выкл",
                False,
                "Включение и отключение доверки"
                "\n❗️ Не влияет на отключение доверки в других Num'модулях.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "Автосохранение жертв",
                True,
                "Вкл/выкл автосохранение жертв в зарлист. \n\nОБЯЗАТЕЛЬНО НУЖЕН ЮЗЕРНЕЙМ ПО ТИПУ @idiotcoders",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "inline bot for б",
                False,
                "[BETA] Использование инлайн бота для команды б",
                validator=loader.validators.Boolean(),
            )
        )
