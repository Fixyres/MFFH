from .. import loader, utils
import random
import asyncio
import os
import string
import subprocess
from telethon.tl.functions.account import UpdateProfileRequest

# meta developer: @kmodules
__version__ = (1, 0, 3)

@loader.tds
class RussianRouletteModule(loader.Module):
    """Русская рулетка. Немного ИСПОЛЬЗУЙТЕ НА СВОЙ СТРАХ И РИСК."""

    strings = {
        "name": "RussianRoulette", 
        "loaded": "🔫 <b>You loaded the gun.\n\n🔗 Bullet: {}/5</b>\n\n👁️‍🗨️ <b>Shoot?</b>",
        "lucky": "🙂 <b>You got lucky!\n\n🔗 The dangerous bullet was: {}\n👁️‍🗨️ Bullet: {}/5</b>",
        "unlucky": "🫨 <b>BANG! The bullet hit.\n\n😵‍💫 Punishment: {}</b>", 
        "module_deleted": "🗑 Deleted module: {}",
        "changed_name": "👤 Changed name to: {}",
        "tagging": "🏷 Tagging users...",
        "deleting_userbot": "🗑 Deleting userbot...",
        "deleting_modules": "🗑 Deleting modules..."
    }

    strings_ru = {
        "name": "RussianRoulette",
        "loaded": "🔫 <b>Вы зарядили пистолет.\n\n🔗 Пуля: {}/5</b>\n\n👁️‍🗨️ <b>Стрелять?</b>",
        "lucky": "🙂 <b>Вам повезло!\n\n🔗 Опасной пулей была: {}\n👁️‍🗨️ Пуля: {}/5</b>",
        "unlucky": "🫨 <b>БАМ! Пуля попала.\n\n😵‍💫 Наказание: {}</b>",
        "module_deleted": "🗑 Удален модуль: {}",
        "changed_name": "👤 Имя изменено на: {}",
        "tagging": "🏷 Тегаю пользователей...",
        "deleting_userbot": "🗑 Удаление юзербота...",
        "deleting_modules": "🗑 Удаление модулей..."
    }

    async def _get_modules_path(self):
        process = subprocess.run("pwd", shell=True, capture_output=True, text=True)
        current_path = process.stdout.strip()
        
        if "Hikka" in current_path:
            return "Hikka"
        elif "Heroku" in current_path:
            return "Heroku"
        return None
        
    async def _generate_random_prefix(self):
        symbols = string.ascii_letters + string.punctuation
        return random.choice(symbols)
        
    async def _change_name(self):
        names = ["Доксер", "Пубертат", "Веном","ыыы крутой чел","офиц дев хикка","взломан школьником","ананас ы лучшиц доксер","фiжма стон стон"]
        new_name = random.choice(names)
        await self.client(UpdateProfileRequest(
            first_name=new_name,
            last_name=""
        ))
        return new_name
        
    async def _tag_users(self, message):
        chat = await message.get_chat()
        if hasattr(chat, "participants"):
            participants = await self.client.get_participants(chat)
            users_to_tag = random.sample([user for user in participants if user.username], min(3, len(participants)))
            tags = " ".join([f"@{user.username}" for user in users_to_tag])
            await message.respond(tags)

    async def roulettecmd(self, message):
        """Начать игру в русскую рулетку"""
        self.bullet = random.randint(1, 5)
        current = random.randint(1, 5)

        buttons = [
            [
                {
                    "text": "🔫 Стрелять",
                    "callback": self.shoot_callback,
                    "args": (current,),
                },
                {
                    "text": "🔗 Реролл",
                    "callback": self.reroll_callback,
                    "args": (current,),
                },
            ]
        ]

        await self.inline.form(
            text=self.strings["loaded"].format(current),
            message=message,
            reply_markup=buttons,
        )

    async def shoot_callback(self, call, current):
        if current == self.bullet:
            punishments = [
                "Оставление юзербота", 
                "Перезапуск юзербота",
                "Рандомный префикс",
                "Ничего, повезло!",
                "Тегание пользователей"
            ]
            punishment = random.choice(punishments)
            
            await call.edit(
                self.strings["unlucky"].format(punishment)
            )

            if punishment == "Оставление юзербота":
                await asyncio.sleep(1)
                suspend_time = random.randint(30, 60)
                await self.invoke("suspend", f"{suspend_time}", message=call.form["message"])
            elif punishment == "Удаление модулей":
                await call.edit(
                    self.strings["unlucky"].format(punishment) + "\n\n" + 
                    self.strings["deleting_modules"]
                )
                await self._delete_modules()
                await asyncio.sleep(1)
                await self.invoke("restart", "-f", message=call.form["message"])
            elif punishment == "Перезапуск юзербота":
                await asyncio.sleep(1)
                await self.invoke("restart", "-f", message=call.form["message"])
            elif punishment == "Рандомный префикс":
                new_prefix = await self._generate_random_prefix()
                await self.invoke("setprefix", new_prefix, message=call.form["message"])
            elif punishment == "Ничего, повезло!":
                new_name = await self._change_name()
                await call.edit(
                    self.strings["unlucky"].format(punishment) + "\n\n" + 
                    self.strings["changed_name"].format(new_name)
                )
            elif punishment == "Тегание пользователей":
                await call.edit(self.strings["tagging"])
                await self._tag_users(call.form["message"])
            else:  # Удаление юзербота
                await call.edit(
                    self.strings["unlucky"].format(punishment) + "\n\n" + 
                    self.strings["deleting_userbot"]
                )
                await self._delete_userbot()
                await asyncio.sleep(1)
                await self.invoke("restart", "-f", message=call.form["message"])

        else:
            new_current = random.randint(1, 5)
            new_bullet = random.randint(1, 5)
            self.bullet = new_bullet
            
            buttons = [
                [
                    {
                        "text": "🔫 Стрелять",
                        "callback": self.shoot_callback,
                        "args": (new_current,),
                    },
                    {
                        "text": "🔗 Реролл",
                        "callback": self.reroll_callback,
                        "args": (new_current,),
                    },
                ]
            ]
            await call.edit(
                self.strings["lucky"].format(new_bullet, new_current),
                reply_markup=buttons,
            )

    async def reroll_callback(self, call, current):
        self.bullet = random.randint(1, 5)
        new_current = random.randint(1, 5)
        
        buttons = [
            [
                {
                    "text": "🔫 Стрелять",
                    "callback": self.shoot_callback,
                    "args": (new_current,),
                },
                {
                    "text": "🔗 Реролл",
                    "callback": self.reroll_callback,
                    "args": (new_current,),
                },
            ]
        ]

        await call.edit(
            self.strings["loaded"].format(new_current),
            reply_markup=buttons,
        )
