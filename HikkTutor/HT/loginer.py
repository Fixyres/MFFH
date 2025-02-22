__version__ = (1, 0, 3)

#            © Copyright 2024
#           https://t.me/HikkTutor 
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#┏┓━┏┓━━┏┓━━┏┓━━┏━━━━┓━━━━━┏┓━━━━━━━━━━━━
#┃┃━┃┃━━┃┃━━┃┃━━┃┏┓┏┓┃━━━━┏┛┗┓━━━━━━━━━━━
#┃┗━┛┃┏┓┃┃┏┓┃┃┏┓┗┛┃┃┗┛┏┓┏┓┗┓┏┛┏━━┓┏━┓━━━━
#┃┏━┓┃┣┫┃┗┛┛┃┗┛┛━━┃┃━━┃┃┃┃━┃┃━┃┏┓┃┃┏┛━━━━
#┃┃━┃┃┃┃┃┏┓┓┃┏┓┓━┏┛┗┓━┃┗┛┃━┃┗┓┃┗┛┃┃┃━━━━━
#┗┛━┗┛┗┛┗┛┗┛┗┛┗┛━┗━━┛━┗━━┛━┗━┛┗━━┛┗┛━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# load from: t.me:HikkTutor 
# meta developer:@HikkTutor 
# author: vsakoe
# name: loginer

import requests
from .. import loader, utils
from datetime import datetime
import random
import string
import os
import json
from faker import Faker

fake = Faker()

@loader.tds
class loginer(loader.Module):
    """Генерация аккаунтов с временной почтой для регистрации без личных данных"""

    strings = {"name": "loginer"}
    save_path = "accounts.json" 
    account_cache = {}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "accounts", {}, "Сохраненные аккаунты"
            ),
        )
        self._load_accounts()

    def generate_username(self):
        return fake.user_name()

    def generate_password(self, length=12):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
#часть кода и идея временной почты взяты у @blazeftg из модуля TempMail: https://t.me/blazeftg/18
    def get_temp_email(self):
        try:
            response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox")
            response.raise_for_status()
            return response.json()[0]
        except requests.RequestException as e:
            print(f"Error fetching temp email: {e}")
            return None

    def get_email_messages(self, email):
        if email is None:
            return []
        try:
            name, domain = email.split('@')
            response = requests.get(
                f"https://www.1secmail.com/api/v1/?action=getMessages&login={name}&domain={domain}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching email messages: {e}")
            return []
        except ValueError:
            print("Invalid email format.")
            return []

    def read_email_message(self, email, message_id):
        try:
            name, domain = email.split('@')
            response = requests.get(
                f"https://www.1secmail.com/api/v1/?action=readMessage&login={name}&domain={domain}&id={message_id}"
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error reading email message: {e}")
            return {}
        except ValueError:
            print("Invalid email format.")
            return {}

    def _load_accounts(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r') as f:
                data = json.load(f)
                self.config["accounts"] = data.get("accounts", {})
                self.account_cache = data.get("account_cache", {})

    def _save_accounts(self):
        data = {
            "accounts": self.config["accounts"],
            "account_cache": self.account_cache
        }
        with open(self.save_path, 'w') as f:
            json.dump(data, f)

    def _get_holiday_greeting(self):
        now = datetime.now()
        month, day = now.month, now.day

        if month == 12 and day == 31 or month == 1 and day in {1, 2}:
            return "С Новым годом! 🎉🎇🎆"
        elif month == 2 and day == 14:
            return "С Днем святого Валентина! ❤️"
        elif month == 3 and day == 8:
            return "С Международным женским днем! 🌸"
        elif month == 5 and day == 1:
            return "С Днем труда! 💼"
        elif month == 10 and day == 31:
            return "С Хэллоуином! 🎃"
        elif month == 12 and day == 25:
            return "С Рождеством! 🎄"
        else:
            return ""

    @loader.command()
    async def generate(self, message):
        """Генерация новых данных"""
        username = self.generate_username()
        password = self.generate_password()
        email = self.get_temp_email()

        self.account_cache[email] = {"username": username, "password": password, "saved": False}
        self._save_accounts()

        response = (
            f"🌟 <b>Новый аккаунт создан!</b>\n\n"
            f"👤 <b>Ник:</b> <code>{utils.escape_html(username)}</code>\n"
            f"🔑 <b>Пароль:</b> <code>{utils.escape_html(password)}</code>\n"
            f"📧 <b>Почта:</b> <code>{utils.escape_html(email)}</code>\n"
            "Вы можете проверить почту или сохранить данные ниже."
        )

        buttons = [
            [
                {
                    "text": "📧 Проверить почту",
                    "callback": self.show_email_messages,
                    "args": (email,),
                }
            ],
            [
                {
                    "text": "💾 Сохранить",
                    "callback": self.save_account,
                    "args": (email,),
                }
            ],
        ]

        await self.inline.form(
            text=response,
            message=message,
            reply_markup=buttons
        )

    async def save_account(self, call, email):
        """Сохраняет данные аккаунта"""
        account_info = self.account_cache.get(email)
        if account_info:
            username = account_info["username"]
            password = account_info["password"]
            save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.config["accounts"][username] = {
                "password": password,
                "email": email,
                "date": save_time
            }
            self._save_accounts()
            account_info["saved"] = True

        response = f"✅ Данные для <b>{utils.escape_html(username)}</b> сохранены!"

        buttons = [
            {
                "text": "🔙 Назад",
                "callback": self.back_to_account,
                "args": (email,),
            }
        ]

        await call.edit(
            text=response,
            reply_markup=buttons
        )

    async def show_email_messages(self, call, email):
        """Показывает сообщения на временной почте"""
        account_info = self.account_cache.get(email)
        if not account_info:
            await call.answer("Данные аккаунта недоступны.", show_alert=True)
            return

        messages = self.get_email_messages(email)
        response = (
            f"📧 <b>Почта для:</b> <code>{utils.escape_html(email)}</code>\n"
            f"👤 <b>Ник:</b> <code>{utils.escape_html(account_info['username'])}</code>\n\n"
        )

        if messages:
            for msg in messages:
                content = self.read_email_message(email, msg['id'])
                response += (
                    f"📨 <b>От:</b> <code>{utils.escape_html(msg['from'])}</code>\n"
                    f"💬 <b>Тема:</b> <code>{utils.escape_html(msg['subject'])}</code>\n"
                    f"📝 <b>Содержание:</b> {utils.escape_html(content.get('textBody', ''))}\n\n"
                )
        else:
            response += "📭 Нет новых писем."

        buttons = [
            {
                "text": "🔙 Назад",
                "callback": self.back_to_account,
                "args": (email,),
            },
            {
                "text": "🔄 Обновить",
                "callback": self.refresh_email_messages,
                "args": (email,),
            }
        ]

        await call.edit(
            text=response,
            reply_markup=buttons
        )

    async def refresh_email_messages(self, call, email):
        """Обновляет список сообщений на временной почте"""
        await self.show_email_messages(call, email)

    async def back_to_account(self, call, email):
        """Возвращает к информации об аккаунте"""
        account_info = self.account_cache.get(email)
        if not account_info:
            await call.answer("Данные аккаунта недоступны.", show_alert=True)
            return

        greeting = self._get_holiday_greeting()
        is_saved = account_info["saved"]

        response = (
            ("🔓 <b>Не сохранённый аккаунт:</b>\n\n" if not is_saved else "") +
            f"👤 <b>Ник:</b> <code>{utils.escape_html(account_info['username'])}</code>\n"
            f"🔑 <b>Пароль:</b> <code>{utils.escape_html(account_info['password'])}</code>\n"
            f"📧 <b>Почта:</b> <code>{utils.escape_html(email)}</code>\n\n"
        )

        if is_saved:
            response += f"{greeting}\n"

        buttons = [
            [
                {
                    "text": "📧 Проверить почту",
                    "callback": self.show_email_messages,
                    "args": (email,),
                }
            ],
            [
                {
                    "text": "🗑️ Забыть" if is_saved else "💾 Сохранить",
                    "callback": self.confirm_delete_account if is_saved else self.save_account,
                    "args": (account_info['username'],) if is_saved else (email,),
                }
            ],
            [
                {
                    "text": "❌ Закрыть",
                    "callback": self.close_message,
                }
            ]
        ]

        await call.edit(
            text=response,
            reply_markup=buttons
        )

    async def confirm_delete_account(self, call, username):
        """Подтверждает удаление аккаунта"""
        response = (
            f"❓ <b>Удалить аккаунт</b> <code>{utils.escape_html(username)}</code>?\n"
            "⚠️ Будьте осторожны, вы можете потерять данные."
        )

        buttons = [
            [
                {
                    "text": "✅ Да",
                    "callback": self.delete_account,
                    "args": (username,),
                },
                {
                    "text": "🚫 Нет",
                    "callback": self.close_message,
                }
            ]
        ]

        await call.edit(
            text=response,
            reply_markup=buttons
        )

    async def delete_account(self, call, username):
        """Удаляет аккаунт из сохраненных"""
        self.config["accounts"].pop(username, None)
        self._save_accounts()

        self.account_cache.pop(username, None)
        self._save_accounts()

        response = f"🗑️ Аккаунт <b>{utils.escape_html(username)}</b> удален."

        buttons = [
            {
                "text": "❌ Закрыть",
                "callback": self.close_message,
            }
        ]

        await call.edit(
            text=response,
            reply_markup=buttons
        )

    async def close_message(self, call):
        """Закрывает текущее сообщение"""
        await call.delete()

    @loader.command()
    async def saves(self, message, username=None):
        """ ник или вывести список"""
        if username is None:
            args = utils.get_args_raw(message)
        else:
            args = username

        if args:
            account = self.config["accounts"].get(args)
            if account:
                response = (
                    f"🔐 <b>Аккаунт:</b> <code>{utils.escape_html(args)}</code>\n"
                    f"🔑 <b>Пароль:</b> <code>{utils.escape_html(account['password'])}</code>\n"
                    f"📧 <b>Почта:</b> <code>{utils.escape_html(account['email'])}</code>\n\n"
                    f"{self._get_holiday_greeting()}\n"
                )

                buttons = [
                    [
                        {
                            "text": "📧 Проверить почту",
                            "callback": self.show_email_messages,
                            "args": (account['email'],),
                        }
                    ],
                    [
                        {
                            "text": "🗑️ Забыть",
                            "callback": self.confirm_delete_account,
                            "args": (args,),
                        }
                    ],
                    [
                        {
                            "text": "❌ Закрыть",
                            "callback": self.close_message,
                        }
                    ],
                ]

                await self.inline.form(
                    text=response,
                    message=message,
                    reply_markup=buttons
                )
            else:
                await message.respond(f"❌ Аккаунт <code>{utils.escape_html(args)}</code> не найден.")
        else:
            if not self.config["accounts"]:
                await message.respond("📭 Нет сохраненных аккаунтов.")
            else:
                response = "<b>📜 Сохраненные аккаунты:</b>\n\n"
                for username, details in self.config["accounts"].items():
                    response += (
                        f"👤 <b>Никнейм:</b> <code>{utils.escape_html(username)}</code>\n"
                        f"🗓️ <b>Дата:</b> <code>{utils.escape_html(details['date'])}</code>\n\n"
                    )
                response += f"{self._get_holiday_greeting()}\n"

                await message.respond(response)
