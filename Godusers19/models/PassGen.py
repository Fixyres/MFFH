# meta developer: @Goduser18
from hikkatl.types import Message
from .. import loader, utils
import random
import string
import hashlib
from cryptography.fernet import Fernet
import urllib.parse

@loader.tds
class PassGenMod(loader.Module):
    """Генератор паролей"""

    strings = {
        "name": "PassGen",
        "gen_help": "🔐 <b>Использование:</b>\n<code>.genpwd site.com</code> - сгенерировать пароль\n<code>.genpwdN</code> - случайный пароль",
        "list_help": "📋 <b>Список паролей:</b>\n<code>.listpwd</code> - показать все пароли",
        "pwd_generated": "✅ <b>Пароль для {}:</b>\n<code>{}</code>\n🔗 {}",
        "random_pwd": "🎲 <b>Случайный пароль:</b>\n<code>{}</code>",
        "pwd_list": "📋 <b>Сохранённые пароли:</b>\n{}\n\n🔗 Быстрые ссылки:\n{}",
        "no_pwds": "ℹ️ Нет сохранённых паролей",
        "key_error": "🔑 Ошибка: Сначала сгенерируйте хотя бы один пароль"
    }

    def __init__(self):
        self._passwords = {}
        self._key = None

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        if "passgen" not in self._db:
            self._db["passgen"] = {}
        self._load_passwords()

    def _load_passwords(self):
        """Загрузка паролей из базы"""
        if "passwords" in self._db["passgen"]:
            self._passwords = self._db["passgen"]["passwords"]
        if "key" in self._db["passgen"]:
            self._key = self._db["passgen"]["key"]

    def _save_passwords(self):
        """Сохранение паролей в базу"""
        self._db["passgen"] = {
            "passwords": self._passwords,
            "key": self._key
        }

    def _generate_password(self, length=12):
        """Генерация сложного пароля"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        while True:
            pwd = ''.join(random.choice(chars) for _ in range(length))
            if (any(c.islower() for c in pwd) and
                any(c.isupper() for c in pwd) and
                any(c.isdigit() for c in pwd) and
                any(c in "!@#$%^&*()" for c in pwd)):
                return pwd

    def _encrypt_password(self, password: str) -> str:
        """Шифрование пароля"""
        if not self._key:
            self._key = Fernet.generate_key().decode()
        cipher = Fernet(self._key.encode())
        return cipher.encrypt(password.encode()).decode()

    def _decrypt_password(self, encrypted: str) -> str:
        """Дешифровка пароля"""
        if not self._key:
            raise ValueError("No encryption key")
        cipher = Fernet(self._key.encode())
        return cipher.decrypt(encrypted.encode()).decode()

    def _generate_login_link(self, site: str) -> str:
        """Генерация ссылки для входа"""
        if site.startswith(('http://', 'https://')):
            domain = urllib.parse.urlparse(site).netloc
        else:
            domain = site.split('/')[0]
        
        return f"https://{domain}/login" if domain else ""

    @loader.command()
    async def genpwd(self, message: Message):
        """Сгенерировать пароль для сайта"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["gen_help"])
            return

        site = args.split()[0].lower()
        password = self._generate_password()
        login_link = self._generate_login_link(site)

        
        encrypted = self._encrypt_password(password)
        self._passwords[site] = encrypted
        self._save_passwords()

        response = self.strings["pwd_generated"].format(site, password, login_link)
        await utils.answer(message, response)

    @loader.command()
    async def genpwdN(self, message: Message):
        """Сгенерировать случайный пароль без привязки к сайту"""
        password = self._generate_password()
        await utils.answer(
            message,
            self.strings["random_pwd"].format(password)
        )

    @loader.command()
    async def listpwd(self, message: Message):
        """Показать все сохранённые пароли с ссылками"""
        if not self._passwords:
            await utils.answer(message, self.strings["no_pwds"])
            return

        try:
            pwd_list = []
            links = []
            for site, encrypted in self._passwords.items():
                decrypted = self._decrypt_password(encrypted)
                pwd_list.append(f"• {site}: <code>{decrypted}</code>")
                login_link = self._generate_login_link(site)
                if login_link:
                    links.append(f"🔗 {site}: {login_link}")

            response = self.strings["pwd_list"].format(
                "\n".join(pwd_list),
                "\n".join(links) if links else "ℹ️ Нет доступных ссылок"
            )
            await utils.answer(message, response)
        except Exception as e:
            await utils.answer(message, self.strings["key_error"])
            self._passwords = {}
            self._save_passwords()

    @loader.command()
    async def delpwd(self, message: Message):
        """Удалить пароль для сайта"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Укажите сайт: <code>.delpwd site.com</code>")
            return

        site = args.lower()
        if site in self._passwords:
            del self._passwords[site]
            self._save_passwords()
            await utils.answer(message, f"🗑️ Пароль для <code>{site}</code> удалён")
        else:
            await utils.answer(message, f"❌ Пароль для <code>{site}</code> не найден")