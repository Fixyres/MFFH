#meta developer: @kotcheat

from .. import loader, utils
import random
import string
import qrcode
import io
from faker import Faker

fake = Faker()

class KOTFakeGenMod(loader.Module):
    """Генератор случайных данных"""
    
    strings = {
        "name": "KOTFakeGen",
        "pwd_doc": "Генерация пароля",
        "num_doc": "Генерация номера",
        "id_doc": "Случайное имя",
        "mullvad_doc": "Ключ Mullvad",
        "discord_doc": "Токен Discord",
        "card_doc": "Номер карты",
        "email_doc": "Случайный email",
        "birth_doc": "Дата рождения",
        "uuid_doc": "Генерация UUID",
        "mac_doc": "MAC-адрес",
        "address_doc": "Случайный адрес",
        "username_doc": "Имя пользователя",
        "quote_doc": "Случайная цитата",
        "job_doc": "Должность",
        "license_doc": "Номер лицензии",
        "ssn_doc": "Генерация SSN",
        "qr_doc": "QR-код",
        "coords_doc": "Координаты",
        "news_doc": "Фейковые новости",
        "btcaddr_doc": "Bitcoin-адрес",
        "btckey_doc": "Приватный ключ BTC",
        "stock_doc": "Профиль акции"
    }
    
    def generate_password(self, length=12):
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_number(self, country_code="7"):
        digits = ''.join(random.choice(string.digits) for _ in range(10))
        return f"+{country_code}{digits}"
        
    def generate_btc_address(self):
        # Генерация случайного Bitcoin-адреса
        chars = string.ascii_letters + string.digits
        prefix = random.choice(["1", "3", "bc1"])
        if prefix == "1" or prefix == "3":
            length = random.randint(25, 34)
        else:
            length = random.randint(42, 62)
        return prefix + ''.join(random.choice(chars) for _ in range(length - len(prefix)))

    @loader.command()
    async def pwdcmd(self, message):
        """Генерация пароля"""
        args = utils.get_args_raw(message)
        try:
            length = int(args) if args else 12
            pwd = self.generate_password(length)
            await message.edit(f"🔐 {pwd}")
        except ValueError:
            await message.edit("❌ Укажите корректную длину пароля")

    @loader.command()
    async def numcmd(self, message):
        """Генерация номера телефона"""
        args = utils.get_args_raw(message)
        country_code = args if args else "7"
        num = self.generate_number(country_code)
        await message.edit(f"📱 {num}")

    @loader.command()
    async def idcmd(self, message):
        """Генерация случайной личности"""
        await message.edit(f"👤 {fake.name()}")

    @loader.command()
    async def mullvadcmd(self, message):
        """Генерация ключа Mullvad"""
        key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        await message.edit(f"🔐 {key}")

    @loader.command()
    async def discordcmd(self, message):
        """Генерация токена Discord"""
        token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(59))
        await message.edit(f"🎮 {token}")

    @loader.command()
    async def cardcmd(self, message):
        """Генерация номера банковской карты"""
        card = fake.credit_card_number(card_type=None)
        await message.edit(f"💳 {card}")

    @loader.command()
    async def emailcmd(self, message):
        """Генерация случайного email"""
        email = fake.email()
        await message.edit(f"📧 {email}")

    @loader.command()
    async def birthcmd(self, message):
        """Генерация случайной даты рождения"""
        birth = fake.date_of_birth()
        await message.edit(f"🎂 {birth}")

    @loader.command()
    async def uuidcmd(self, message):
        """Генерация UUID"""
        uuid = fake.uuid4()
        await message.edit(f"🆔 {uuid}")

    @loader.command()
    async def maccmd(self, message):
        """Генерация MAC-адреса"""
        mac = fake.mac_address()
        await message.edit(f"🖥️ {mac}")

    @loader.command()
    async def addresscmd(self, message):
        """Генерация случайного адреса"""
        address = fake.address()
        await message.edit(f"🏠 {address}")

    @loader.command()
    async def usernamecmd(self, message):
        """Генерация имени пользователя"""
        username = fake.user_name()
        await message.edit(f"👤 {username}")

    @loader.command()
    async def quotecmd(self, message):
        """Генерация случайной цитаты"""
        quote = fake.sentence()
        await message.edit(f"💬 {quote}")

    @loader.command()
    async def jobcmd(self, message):
        """Генерация должности"""
        job = fake.job()
        await message.edit(f"💼 {job}")

    @loader.command()
    async def licensecmd(self, message):
        """Генерация номера лицензии"""
        license_plate = fake.license_plate()
        await message.edit(f"🚗 {license_plate}")

    @loader.command()
    async def ssncmd(self, message):
        """Генерация SSN"""
        ssn = fake.ssn()
        await message.edit(f"📝 {ssn}")

    @loader.command()
    async def qrcmd(self, message):
        """Генерация QR-кода"""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("❌ Пожалуйста, укажите текст для QR-кода")
            return
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(args)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        
        await message.delete()
        await self.client.send_file(
            message.chat_id,
            buf,
            caption=f"🔳 {args}"
        )

    @loader.command()
    async def coordscmd(self, message):
        """Генерация случайных координат"""
        latitude = round(random.uniform(-90.0, 90.0), 6)
        longitude = round(random.uniform(-180.0, 180.0), 6)
        await message.edit(f"🗺️ Широта: {latitude}, Долгота: {longitude}")

    @loader.command()
    async def newscmd(self, message):
        """Генерация фейковых новостей"""
        headlines = [
            "Ученые обнаружили новый вид насекомых в Амазонке",
            "Известный актер объявил о своем участии в новом проекте",
            "Исследование показало, что шоколад полезен для здоровья",
            "Новая технология обещает революцию в медицине",
            "Археологи нашли древний артефакт в Египте"
        ]
        
        bodies = [
            "Сегодня утром команда исследователей сообщила о своем открытии.",
            "Событие вызвало бурную реакцию в социальных сетях.",
            "Эксперты предсказывают значительное влияние на индустрию.",
            "Местные жители выражают свою поддержку.",
            "Новость распространилась с невероятной скоростью."
        ]
        
        headline = random.choice(headlines)
        body = random.choice(bodies)
        await message.edit(f"📰 `{headline}`\n\n`{body}`")

    @loader.command()
    async def btcaddrcmd(self, message):
        """Генерация Bitcoin-адреса"""
        btc_address = self.generate_btc_address()
        await message.edit(f"₿ `{btc_address}`")

    @loader.command()
    async def btckeycmd(self, message):
        """Генерация приватного ключа Bitcoin"""
        btc_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
        await message.edit(f"🔑 {btc_key}")

    @loader.command()
    async def stockcmd(self, message):
        """Генерация профиля акции"""
        stock = {
            "company": fake.company(),
            "symbol": ''.join(random.choices(string.ascii_uppercase, k=4)),
            "price": round(random.uniform(10, 1000), 2),
            "volume": random.randint(1000, 1000000)
        }
        
        stock_info = (
            f"🏢 {stock['company']}\n"
            f"🔣 {stock['symbol']}\n"
            f"💰 ${stock['price']}\n"
            f"📊 {stock['volume']}"
        )
        
        await message.edit(stock_info)
