# meta developer: @codeer_kot
# не меняйте мой код, пожалуйста, указывая что вы создатель модуля.
import datetime
from .. import loader, utils

class KOTNewYear(loader.Module):
    """модуль, который выводит сколько осталось дней до нг."""
    
    strings = {"name": "KOTNewYear"}

    async def зимаcmd(self, message):
        """- вывести сообщение сколько осталось до нг."""
        now = datetime.datetime.now()
        closing_date = datetime.datetime(now.year, 12, 31)
        if now.month == 1 and now.day > 1:
            closing_date = closing_date.replace(year=now.year + 1)
            
        time_left = closing_date - now
        await message.delete()
        await message.respond(f"""<emoji document_id=5240125736257337767>🤍</emoji><emoji document_id=5238187773998937670>🤍</emoji><emoji document_id=5239947014078216067>🤍</emoji><emoji document_id=5238065509164922044>🤍</emoji><emoji document_id=5309994572011559027>🤩</emoji><emoji document_id=5240059387602548836>🤍</emoji><emoji document_id=5240164421027771528>🤍</emoji><emoji document_id=5237778579579745454>🤍</emoji><emoji document_id=5240308684684276572>🤍</emoji>
        𝚝𝚘 𝚗𝚎𝚠 𝚢𝚎𝚊𝚛: {time_left.days} 𝚍𝚊𝚢𝚜.
<emoji document_id=5237913149495064630>🤍</emoji><emoji document_id=5237967154413845397>🤍</emoji><emoji document_id=5238225951963233391>🤍</emoji><emoji document_id=5240316922431554469>🤍</emoji><emoji document_id=5341752281752690298>❄️</emoji><emoji document_id=5240047361694118762>🤍</emoji><emoji document_id=5240310183627864086>🤍</emoji><emoji document_id=5240438628919817791>🤍</emoji><emoji document_id=5240457183178538786>🤍</emoji>""")
