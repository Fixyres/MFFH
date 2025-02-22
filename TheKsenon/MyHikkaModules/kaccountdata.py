from .. import loader, utils
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import asyncio
from datetime import datetime

# meta developer: @kmodules
__version__ = (1, 0, 0)

@loader.tds
class AccountDataMod(loader.Module):
    """Получить информацию об аккаунте, дц, регистрации(нестабильно). 
    
    Функционал как у AyuGram."""
    
    strings = {
        "name": "K:AccountData",
        "searching": "<emoji document_id=5222108309795908493>✨</emoji><i> </i><b>Ищу информацию...</b>",
        "info": "<emoji document_id=5276489300207217985>✅</emoji> <b>Информация о {}</b>:\n\n<emoji document_id=5264892613630111886>💎</emoji> <b>ID:</b> <code>{}</code>\n<emoji document_id=5258466470676940666>✈️</emoji> <b>Дата-центр:</b> <code>{}</code>\n<emoji document_id=5276489300207217985>✅</emoji> <b>Дата регистрации:</b> <code>{}</code>\n<emoji document_id=5235588635885054955>🎲</emoji> <b>Возраст аккаунта:</b> <code>{}</code>",
        "no_args": "<emoji document_id=5248988671855576740>🚫</emoji> <b>Укажите пользователя или ответьте на сообщение!</b>"
    }
    
    async def client_ready(self, client, db):
        self.client = client

    def calculate_age(self, date_str):
        try:
            numbers = ''.join(c for c in date_str if c.isdigit() or c == '.')
            parts = numbers.split('.')
            if len(parts) == 3:
                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                reg_date = datetime(year, month, day)
            else:
                return f"Invalid format: {date_str}"
                
            current_date = datetime.now()
            days_difference = (current_date - reg_date).days
            
            years = days_difference // 365
            remaining_days = days_difference % 365
            months = remaining_days // 30
            days = remaining_days % 30

            def years_str(n):
                if n % 10 == 1 and n % 100 != 11:
                    return "год"
                elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
                    return "года"
                else:
                    return "лет"
                    
            def months_str(n):
                if n % 10 == 1 and n % 100 != 11:
                    return "месяц"
                elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
                    return "месяца"
                else:
                    return "месяцев"
                    
            def days_str(n):
                if n % 10 == 1 and n % 100 != 11:
                    return "день"
                elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
                    return "дня"
                else:
                    return "дней"

            return f"{years} {years_str(years)}, {months} {months_str(months)}, {days} {days_str(days)}"
        except Exception as e:
            return f"Ошибка расчета возраста: {date_str} -> {str(e)}"
        
    @loader.command()
    async def aboutacc(self, message):
        """Получить информацию об аккаунте | .aboutacc <username/reply>"""
        
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        
        if not args and not reply:
            return await message.edit(self.strings["no_args"])
            
        await message.edit(self.strings["searching"])
        
        try:
            if reply:
                user = await self.client.get_entity(reply.sender_id)
                username = reply.sender.username
            else:
                if args.startswith("@"):
                    args = args[1:]
                user = await self.client.get_entity(args)
                username = args
                
            await self.client.send_message("regdatabot", f"/reg @{username}")
            await asyncio.sleep(1)
            
            async for msg in self.client.iter_messages("regdatabot", limit=1):
                reg_info = msg.text
                
            id_match = reg_info.split("\n")[0].split(": ")[1].strip()
            reg_date = reg_info.split("\n")[1].split(": ")[1].strip()
            age_str = self.calculate_age(reg_date)
            
            dc_id = user.photo.dc_id if user.photo else "Error"
            
            await self.client.edit_folder("regdatabot", folder=1)
            
            await message.edit(
                self.strings["info"].format(
                    user.first_name,
                    id_match,
                    dc_id,
                    reg_date,
                    age_str
                )
            )
            
        except Exception as e:
            await message.edit(f"Ошибка: {str(e)}")
