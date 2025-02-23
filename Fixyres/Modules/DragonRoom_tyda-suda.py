from decimal import Decimal, ROUND_UP
from asyncio import gather, sleep
import asyncio

from .. import loader, utils

vipdata = ['1', '2', '5', '10']
vipbottlesdata = [100, 200, 500, 1000]

class DragonRoomMod(loader.Module):
    """Автокомнаты от дракоши без смс и регистрации)"""

    strings = {"name": "DragonRoom tyda-suda"}
    async def client_ready(self, client, db) -> None:
        if hasattr(self, "hikka"):
            return

        self.db = db
        self.client = client
    _bot = "@bfgbunker_bot"

    async def auroomcmd(self, message):
        """Пример ввода: .auroom <номер комнаты> <количество уровней больше 10>"""
        try:
            args = utils.get_args(message)
            if not args:
                self.db.set(self.strings["name"], "state", False)
                await utils.answer(message, "<emoji document_id=5213150232082130270>💔</emoji><b>DragonRoom выключен успокойся глупыш</b>")
                return
            if int(args[0].strip()) > 18:
                self.db.set(self.strings["name"], "state", False)
                await utils.answer(message, "<emoji document_id=5213150232082130270>💔</emoji><b>Ало нет такой комнаты дебил блять</b>")
                return
            await utils.answer(
                message,
                (
                    "<emoji document_id=5359441070201513074>🎭</emoji><b>УраУра ты смог его запустить, ты не так безнадёжен)\n\n"
                    "Чтобы оффнуть шарманку просто напиши: <code>.offdragon</code></b>"
                ),
            )
            
            levelcount = int(args[1].strip())
            messagecount = 0 
            self.set('BIGmillion', False)
            self.db.set(self.strings["name"], 'roomnumber', int(args[0].strip()))
            self.db.set(self.strings["name"], "state", True)
            async with self._client.conversation(self._bot) as b:
                await asyncio.sleep(1)
                await b.send_message("Б")
                resp = await b.get_response()
                bottles = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Бутылок:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.set('bottles', bottles)
                self.db.set(self.strings["name"], 'oldbottles', bottles)
                await asyncio.sleep(1)
            async with self._client.conversation(self._bot) as b:
                await asyncio.sleep(1)
                await b.send_message("к "+str(self.db.get(self.strings["name"], 'roomnumber')))
                resp = await b.get_response()
                oldlevel = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Уровень:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'oldlevel', oldlevel)
                oldprofit = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Прибыль:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'oldprofit', oldprofit)
                oldhumans = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Макс. человек:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'oldhumans', oldhumans)
                pricenow = int(''.join(map(str,(resp.text.split('Cледующее улучшение стоит:')[1].strip().split(' '))[0].split('.')[0:])))
                if pricenow >= 1000000:
                    self.set('BIGmillion', True)
                await asyncio.sleep(1)
                while self.db.get(self.strings["name"], "state") and levelcount > 0:
                    if messagecount >= 3:
                        await message.respond('починить бункер')
                        await asyncio.sleep(2)
                        messagecount = 0
                    
                    if not self.get("BIGmillion"):
                        levels = int(vipdata[self.config['VIP_level']])-1
                        levelprice = pricenow
                        if self.config['VIP_level'] == 0:
                            pricenow *= 1.007
                            levelprice = pricenow
                        else:
                            while levels != 0: 
                                pricenow = pricenow * 1.007 
                                levelprice = levelprice + pricenow 
                                levels -= 1
                        decimal_num = Decimal(str(levelprice))
                        rounded_decimal_num = decimal_num.quantize(Decimal('1'), rounding=ROUND_UP)
                        levelprice = int(rounded_decimal_num)
                        levelprice /= 10000
                        decimal_num = Decimal(str(levelprice))
                        rounded_decimal_num = decimal_num.quantize(Decimal('1'), rounding=ROUND_UP)
                        changebottles = int(rounded_decimal_num)
                        if changebottles > self.get('bottles'):
                            await message.respond('<emoji document_id=4900350448269001623>🍾</emoji><b>Ало чунга-чанга бутылок нету, жди пополнение)</b>')
                            levelcount = 0
                            self.db.set(self.strings["name"], "state", False)
                            return 0
                        else:
                            bottles = self.get('bottles') - changebottles
                            self.set('bottles', bottles)
                        decimal_num = Decimal(str(pricenow))
                        rounded_decimal_num = decimal_num.quantize(Decimal('1'), rounding=ROUND_UP)
                        pricenow = int(rounded_decimal_num)
                        
                    if pricenow >= 1000000:
                        self.set('BIGmillion', True)
                        changebottles = vipbottlesdata[self.config['VIP_level']]
                        pricenow = 0
                    
                    await message.respond('обменять бутылки '+str(changebottles))
                    await asyncio.sleep(1)
                    await resp.click(data='upgrade_room_'+str(message.from_id)+'_'+str(self.db.get(self.strings["name"], 'roomnumber'))+'_'+vipdata[self.config['VIP_level']])
                    await asyncio.sleep(1)
                    levelcount -= int(vipdata[self.config['VIP_level']])
                    messagecount += 1 
                await b.send_message("к "+str(self.db.get(self.strings["name"], 'roomnumber')))
                resp = await b.get_response()
                newlevel = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Уровень:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'newlevel', newlevel)
                newprofit = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Прибыль:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'newprofit', newprofit)
                newhumans = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Макс. человек:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'newhumans', newhumans)
                await asyncio.sleep(1)
                await b.send_message("Б")
                resp = await b.get_response()
                newbottles = int(
                    "".join(
                        string
                        for string in resp.raw_text.split("Бутылок:")[1].split()[0].strip()
                        if string.isdigit()
                    )
                )
                self.db.set(self.strings["name"], 'newbottles', newbottles)
                await message.respond(f'<emoji document_id=4900350448269001623>🍾</emoji><b>ало DragonRooms закончил прокачивать твою ебаную комнату номер {self.db.get(self.strings["name"], "roomnumber")}</b>\n<emoji document_id=5231200819986047254>📊</emoji>Статистика хуйни:\n<emoji document_id=5244837092042750681>📈</emoji>Прокачено хуйни: {int(self.db.get(self.strings["name"], "newlevel"))-int(self.db.get(self.strings["name"], "oldlevel"))}\n<emoji document_id=5375296873982604963>💰</emoji>Прибыль увеличена на {int(self.db.get(self.strings["name"], "newprofit"))-int(self.db.get(self.strings["name"], "oldprofit"))} кр.\n<emoji document_id=5870994129244131212>👤</emoji>Вместимость людей увеличена на {int(self.db.get(self.strings["name"], "newhumans"))-int(self.db.get(self.strings["name"], "oldhumans"))}\n<emoji document_id=5370900768796711127>🍾</emoji>Потрачено бутылок: {int(self.db.get(self.strings["name"], "oldbottles"))-int(self.db.get(self.strings["name"], "newbottles"))}')
                self.db.set(self.strings["name"], "state", False)

        except Exception as e:
            await utils.answer(message, (e))
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "VIP_level",
                3,
                "Уровень вашего вип статуса",
                validator=loader.validators.Integer(),
            ),
        )
