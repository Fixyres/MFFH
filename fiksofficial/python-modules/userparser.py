# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# -*- coding: utf-8 -*-
# Name: UserParser
# Description: Данный модуль позволяет копировать ID, Username и Name участников чата при помощи команды .userpars
# meta developer: @PyModule

from .. import loader, utils
import json
import os

class UserIDParserMod(loader.Module):
    """Парсер ID, имени, фамилии и юзернейма пользователей с выбором формата файла"""
    strings = {
        "name": "UserParser",
        "format_set": "<emoji document_id=5206607081334906820>✔️</emoji> <b>Формат файла успешно установлен на: {}</b>",
        "invalid_format": "<emoji document_id=5274099962655816924>❗️</emoji> <b>Неверный формат! Используйте: json, txt или html.</b>",
    }

    def __init__(self):
        self.file_format = "json"

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        saved_format = self.db.get("UserParser", "file_format", None)
        if saved_format:
            self.file_format = saved_format

    async def formatparscmd(self, message):
        """Устанавливает формат файла: json, txt или html"""
        args = utils.get_args_raw(message)
        if args and args.lower() in ["json", "txt", "html"]:
            self.file_format = args.lower()
            self.db.set("UserParser", "file_format", self.file_format)
            await message.edit(self.strings["format_set"].format(self.file_format))
        else:
            await message.edit(self.strings["invalid_format"])

    async def userparscmd(self, message):
        """Собирает информацию о пользователях из чата и сохраняет в файл"""
        chat = message.chat
        if not chat:
            await message.edit("<emoji document_id=5210952531676504517>❌</emoji> <b>Это не чат!</b>")
            return
        user_data = []
        async for user in self.client.iter_participants(chat.id):
            user_info = {
                "id": user.id,
                "username": user.username or "None",
                "first_name": user.first_name or "None",
                "last_name": user.last_name or "None"
            }
            user_data.append(user_info)
        chat_title = chat.title or "Без названия"
        chat_id = chat.id
        chat_info = f"Чат: {chat_title}\nID чата: {chat_id}"
        file_format = self.file_format
        if file_format == "json":
            file_path = "user_data.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
            caption = f"Список пользователей из чата (JSON):\n{chat_info}"
        elif file_format == "txt":
            file_path = "user_data.txt"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{chat_info}\n\n")
                for user in user_data:
                    f.write(
                        f"ID: {user['id']}, "
                        f"Username: {user['username']}, "
                        f"Имя: {user['first_name']}, "
                        f"Фамилия: {user['last_name']}\n"
                    )
            caption = f"Список пользователей из чата (TXT):\n{chat_info}"
        elif file_format == "html":
            file_path = "user_data.html"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Список пользователей</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        h1 {{
            text-align: center;
            color: #333;
        }}
        p {{
            font-size: 16px;
            color: #555;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 16px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }}
        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        tr:hover {{
            background-color: #ddd;
        }}
        .bold {{
            font-weight: bold;
        }}
        .italic {{
            font-style: italic;
        }}
        .underline {{
            text-decoration: underline;
        }}
        .highlight {{
            background-color: yellow;
        }}
    </style>
</head>
<body>
    <h1 class="bold">Список пользователей из чата</h1>
    <p><strong>Чат:</strong> <span class="italic">{chat_title}</span></p>
    <p><strong>ID чата:</strong> <span class="underline">{chat_id}</span></p>
    <table>
        <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Имя</th>
            <th>Фамилия</th>
        </tr>
""")
                for user in user_data:
                    f.write(f"""
        <tr>
            <td class="bold">{user['id']}</td>
            <td class="italic">{user['username']}</td>
            <td class="underline">{user['first_name']}</td>
            <td class="highlight">{user['last_name']}</td>
        </tr>
""")
                f.write("""
    </table>
</body>
</html>
""")
            caption = f"Список пользователей из чата (HTML):\n{chat_info}"
        else:
            await message.edit("<emoji document_id=5274099962655816924>❗️</emoji> <b>Неверный формат файла! Укажите 'json', 'txt' или 'html' с помощью команды .formatpars.</b>")
            return
        await self.client.send_file("me", file_path, caption=caption)
        os.remove(file_path)
        await message.edit("<emoji document_id=5206607081334906820>✔️</emoji> <b>Успешно!</b>")
