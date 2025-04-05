__version__ = (1,0,1)
#░░░░░░░░░░░░░░░░░░░░░░
#░░░░░░░░░░██░░██░░░░░░
#░░░░░░░░░████████░░░░░
#░░░░░░░░░████████░░░░░
#░░░░░░░░░░██████░░░░░░
#░░░░░░░░░░░░██░░░░░░░░
#░░░░░░░░░░░░░░░░░░░░░░
#░░░░░░░░░█▔█░░█░█░░░░░
#░░░░░░░░░██░░░░█░░░░░░
#░░░░░░░░░█▁█░░░█░░░░░░
#░░░░░░░░░░░░░░░░░░░░░░
#░░░███░███░███░███░███
#░░░░░█░█░░░░█░░█░░░█░█
#░░░░█░░███░░█░░█░█░█░█
#░░░█░░░█░░░░█░░█░█░█░█
#░░░███░███░░█░░███░███

# Team: 'H:Mods'
# meta developer: @nullmod


from .. import loader, utils
import re
import asyncio
from datetime import datetime, timedelta


@loader.tds
class ScheduledMessagesPlusMod(loader.Module):
    """Планирование периодичных сообщений"""
    strings = {"name": "ScheduledMessagesPlus"}

    @loader.command()
    async def sch(self, message):
        """Используй .sch <периодичность в секундах> <количество отправок> <текст>

Проф. режим: .sch 15 3 test{x=1;x*2}/{y=0;y+1}
Запланирует три сообщения: test2/1, test4/2, test8/3"""
        args = utils.get_args_raw(message).split(' ', 2)
        if len(args) < 3 or not args[0].isdigit() or not args[1].isdigit():
            return await message.edit("Неверные аргументы")

        interval, count, text = int(args[0]), int(args[1]), args[2]
        if count > 100:
            return await message.edit("Максимальное число отложенных сообщений - 100.")

        chat_id = message.chat_id
        forum_topic_id = message.reply_to.reply_to_msg_id if message.reply_to else None  # Forum(!!!!!!!!!!!)
        await message.edit("Сообщения будут запланированы")

        variables = {}

        for i in range(count):
            send_time = datetime.utcnow() + timedelta(seconds=interval * i)
            formatted_text = self.process_text(text, variables)
            await self.client.send_message(chat_id, formatted_text, schedule=send_time, reply_to=forum_topic_id)

    def process_text(self, text, variables):
        """Process text okay?"""
        def replace_match(match):
            return self.eval_expr(match.group(1), variables)
        
        return re.sub(r"\{(.*?)\}", replace_match, text)

    def eval_expr(self, expr, variables):
        """eval()"""
        parts = expr.split(";")
        last_value = None
        var_name = None
        for part in parts:
            part = part.strip()
            if "=" in part and part.count("=") == 1:
                var, value = part.split("=")
                var = var.strip()
                if var not in variables:
                    variables[var] = eval(value, {"__builtins__": {}}, variables)
                last_value = variables[var]
                var_name = var
            else:
                last_value = eval(part, {"__builtins__": {}}, variables)

                if var_name is not None:
                    variables[var_name] = last_value
        return str(last_value)
