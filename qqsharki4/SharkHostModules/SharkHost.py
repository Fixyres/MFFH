# ©️ EXPERT_CATPON, 2025
# 🌐 https://github.com/qqsharki4/SharkHostModules/blob/main/SharkHost.py
# Licensed under GNU AGPL v3.0
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# meta developer: @EXPERT_CATPON && @SharkHostBot

import aiohttp
import asyncio
from herokutl.tl.types import Message
from .. import loader, utils
import datetime

def parse_ps_etime_to_human(etime: str) -> str:
    etime = etime.strip()
    days, hours, minutes = 0, 0, 0
    if '-' in etime:
        try:
            days_part, time_part = etime.split('-', 1)
            days = int(days_part)
        except ValueError:
            time_part = etime
    else:
        time_part = etime
    
    parts = time_part.split(':')
    try:
        if len(parts) == 3:
            hours, minutes, _ = map(int, parts)
        elif len(parts) == 2:
            minutes, _ = map(int, parts)
            if minutes >= 60:
                hours, minutes = divmod(minutes, 60)
        elif len(parts) == 1:
            minutes = int(parts[0])
            if minutes >= 60:
                hours, minutes = divmod(minutes, 60)
    except (ValueError, IndexError):
        pass

    result = [f"{days}д" if days else "", f"{hours}ч" if hours else "", f"{minutes}м" if minutes else ""]
    return ' '.join(filter(None, result)) or '~1м'

def days_ago_text(dt_str: str) -> str:
    if not dt_str:
        return "Неизвестно"
    try:
        dt = datetime.datetime.fromisoformat(dt_str)
        now = datetime.datetime.now(dt.tzinfo)
        days = (now.date() - dt.date()).days
        if days < 0:
            days = 0
        if days % 10 == 1 and days % 100 != 11:
            word = 'день'
        elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
            word = 'дня'
        else:
            word = 'дней'
        return f"{days} {word} назад"
    except (ValueError, TypeError):
        return dt_str

@loader.tds
class SharkHostMod(loader.Module):
    strings = {
        "name": "SharkHost",
        "config_api_url": "URL API SharkHost.",
        "config_api_token": "Ваш API токен. @SharkHostBot.",
        "token_not_set": "🚫 <b>API токен не установлен!</b>",
        "getting_info": "🔄 <b>Узнаю информацию ...</b>",
        "no_ub": "🚫 <b>У вас нет активных юзерботов.</b>",
        "no_ub_name": "🚫 <b>Ошибка, не найдено имя юзербота.</b>",
        "started": "✅ Started",
        "stopped": "❌ Stopped",
        "restarted": "🔄 Restarted",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_url",
                "https://api.sharkhost.space",
                lambda: self.strings("config_api_url"),
                validator=loader.validators.Link(),
            ),
            loader.ConfigValue(
                "api_token",
                None,
                lambda: self.strings("config_api_token"),
                validator=loader.validators.Hidden(),
            ),
        )

    async def _request(self, method: str, path: str, **kwargs):
        if not self.config["api_token"]:
            return self.strings("token_not_set")
        headers = {"X-API-Token": self.config["api_token"]}
        url = f"{self.config['api_url'].strip('/')}/api/v1/{path}"
        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                async with session.request(method, url, **kwargs) as resp:
                    if resp.status == 429:
                        return "⏳ <b>Не флуди!</b>\n<blockquote>Вы отправляете запросы слишком часто.</blockquote>"
                    data = await resp.json()
                    if data.get("success"):
                        return data.get("data")
                    error = data.get("error", {})
                    error_message = error.get("message", "Нет деталей")
                    return (f"🚫 <b>API Ошибка:</b> <code>{error.get('code', 'UNKNOWN')}</code>\n"
                            f"<blockquote>🗒️ <b>Сообщение:</b> {utils.escape_html(error_message)}</blockquote>")
            except aiohttp.ClientError as e:
                return f"🚫 <b>Ошибка сети:</b> <blockquote>{e}</blockquote>"

    async def _get_my_userbot(self):
        response = await self._request("GET", "userbots")
        if isinstance(response, str):
            return response
        userbots = response.get("userbots", [])
        if not userbots:
            return self.strings("no_ub")
        return userbots[0]

    @loader.command(ru_doc="[код] - Показать статус серверов")
    async def sstatuscmd(self, message: Message):
        await utils.answer(message, "🔄 <b>Запрашиваю статусы...</b>")
        args = utils.get_args_raw(message)
        params = {"code": args} if args else {}
        response = await self._request("GET", "servers/status", params=params)
        if isinstance(response, str):
            return await utils.answer(message, response)
        servers = response.get("servers", [])
        if not servers:
            return await utils.answer(message, "✅ <b>Серверы не найдены.</b>")
        result = "📡 <b>Статус серверов SharkHost:</b>\n"
        for server in servers:
            result += (f"\n<blockquote>{server['flag']} <b>{server['name']}</b> (<code>{server['code']}</code>)\n\n"
                       f"📍 <b>Локация:</b> <i>{server['location']}</i>\n"
                       f"🚦 <b>Статус:</b> <code>{server['status']}</code>\n"
                       f"⚙️ <b>CPU:</b> {server['cpu_usage']} | <b>RAM:</b> {server['ram_usage']}\n"
                       f"💾 <b>Диск:</b> {server['disk_usage']}\n"
                       f"🤖 <b>Юзерботы:</b> {server['slots']}</blockquote>")
        await utils.answer(message, result)

    @loader.command(ru_doc="<reply/ID/юзернейм> - Показать информацию о пользователе")
    async def scheckcmd(self, message: Message):
        identifier = utils.get_args_raw(message)
        if not identifier:
            if message.is_reply:
                reply = await message.get_reply_message()
                identifier = str(reply.sender_id)
            else:
                return await utils.answer(message, "🚫 <b>Укажите ID/юзернейм или ответьте на сообщение.</b>")
        
        await utils.answer(message, "🔄 <b>Запрашиваю информацию...</b>")
        response = await self._request("GET", f"users/{identifier}")
        if isinstance(response, str):
            return await utils.answer(message, response)
        
        owner = response.get('owner', {})
        userbot = response.get('userbot')
        owner_username = owner.get('username') or owner.get('id', 'N/A')
        
        result = (f"👤 <b>Инфо о пользователе</b> <a href=\"tg://user?id={owner.get('id')}\">{utils.escape_html(str(owner_username))}</a>:\n\n"
                  f"<blockquote><b> • ID:</b> <code>{owner.get('id', 'N/A')}</code>\n"
                  f"<b> • Полное имя:</b> <i>{utils.escape_html(owner.get('full_name') or 'Не указано')}</i>\n"
                  f"<b> • Зарегистрирован:</b> <i>{days_ago_text(owner.get('registered_at'))}</i></blockquote>\n")
        
        if userbot:
            result += ("\n🤖 <b>Инфо о юзерботе:</b>\n<blockquote>"
                       f"<b> • Системное имя:</b> <code>{userbot.get('ub_username')}</code>\n"
                       f"<b> • Тип:</b> <code>{userbot.get('ub_type')}</code>\n"
                       f"<b> • Статус:</b> <code>{userbot.get('status')}</code>\n"
                       f"<b> • Сервер:</b> <code>{userbot.get('server_code')}</code>\n"
                       f"<b> • Создан:</b> <i>{days_ago_text(userbot.get('created_at'))}</i>")
            if uptime := userbot.get('uptime'):
                result += f"\n<b> • Аптайм:</b> <code>{utils.escape_html(parse_ps_etime_to_human(uptime))}</code>"
            result += "</blockquote>"
        else:
            result += "<blockquote>ℹ️ <i>У этого пользователя нет активного юзербота.</i></blockquote>"
        await utils.answer(message, result)
    
    @loader.command(ru_doc="Открыть меню управления юзерботом")
    async def smanagecmd(self, message: Message):
        status_message = await utils.answer(message, self.strings("getting_info"))
        userbot_data = await self._get_my_userbot()
        if isinstance(userbot_data, str):
            return await utils.answer(status_message, userbot_data)
        ub_username = userbot_data.get("ub_username")
        ub_status = userbot_data.get("status")
        if not ub_username or not ub_status:
            return await utils.answer(status_message, self.strings("no_ub_name"))
        await self.inline.form(message=status_message, **self._get_manage_menu_content(ub_username, ub_status))

    def _get_manage_menu_content(self, ub_username: str, status: str) -> dict:
        text = (f"🕹️ <b>Управление юзерботом</b> <code>{utils.escape_html(ub_username)}</code>\n"
                f"<b>Текущий статус:</b> <code>{status}</code>\n\nВыберите действие:")
        markup = []
        row = []
        if status == "running":
            row.append({"text": "🛑 Остановить", "callback": self._manage_callback, "args": (ub_username, "stop")})
            row.append({"text": "🔄 Перезапустить", "callback": self._manage_callback, "args": (ub_username, "restart")})
        else: 
            row.append({"text": "🚀 Запустить", "callback": self._manage_callback, "args": (ub_username, "start")})
            row.append({"text": "🔄 Перезапустить", "callback": self._manage_callback, "args": (ub_username, "restart")})
        markup.append(row)
        markup.append([{"text": "❌ Закрыть", "action": "close"}])
        return {"text": text, "reply_markup": markup}

    async def _manage_callback(self, call, ub_username: str, action: str):
        feedback = {"start": self.strings("started"), "stop": self.strings("stopped"), "restart": self.strings("restarted")}
        await call.edit(feedback.get(action, "✅ Готово!"))
        
        asyncio.create_task(self._request("POST", f"userbots/{ub_username}/manage", json={"action": action}))
        
        await asyncio.sleep(2) 
        new_info_response = await self._get_my_userbot()
        if isinstance(new_info_response, str) or not new_info_response.get("ub_username"):
            return await call.edit("🚫 Не удалось обновить статус меню.", reply_markup=None)
        
        new_status = new_info_response.get("status")
        await call.edit(**self._get_manage_menu_content(ub_username, new_status))
    
    async def _direct_manage_action(self, message: Message, action: str):
        status_message = await utils.answer(message, self.strings("getting_info"))
        userbot_data = await self._get_my_userbot()
        if isinstance(userbot_data, str):
            return await utils.answer(status_message, userbot_data)
        ub_username = userbot_data.get("ub_username")
        if not ub_username:
            return await utils.answer(status_message, self.strings("no_ub_name"))
        feedback = {"start": self.strings("started"), "stop": self.strings("stopped"), "restart": self.strings("restarted")}
        await utils.answer(status_message, feedback.get(action))
        
        asyncio.create_task(self._request("POST", f"userbots/{ub_username}/manage", json={"action": action}))

    @loader.command(ru_doc="Запустить юзербота")
    async def sstartcmd(self, message: Message):
        await self._direct_manage_action(message, "start")

    @loader.command(ru_doc="Остановить юзербота")
    async def sstopcmd(self, message: Message):
        await self._direct_manage_action(message, "stop")

    @loader.command(ru_doc="Перезапустить юзербота")
    async def srestartcmd(self, message: Message):
        await self._direct_manage_action(message, "restart")
