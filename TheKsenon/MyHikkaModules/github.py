# ------------------------------------------------------------
# Module: GitHubInfo
# Description: Module for GitHub profile information.
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands: .github
# scope: hikka_only
# meta developer: @kmodules
# ------------------------------------------------------------

import requests
from datetime import datetime
from .. import loader, utils

__version__ = (1, 0, 1)

@loader.tds
class GitHubInfoMod(loader.Module):
    """Module for viewing GitHub profile information"""

    strings = {
        "name": "GitHubInfo",
        "no_username": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Please specify a username!</b>",
        "user_not_found": "<emoji document_id=5210952531676504517>❌</emoji> <b>User not found</b>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Error getting data</b>: <i>{}</i>",
        "loading": "<emoji document_id=5328239124933515868>⚙️</emoji> <b>Loading information...</b>",
        "repos": "repositories",
        "no_data": "No data"
    }

    strings_ru = {
        "name": "GitHubInfo",
        "no_username": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Укажите имя пользователя!</b>",
        "user_not_found": "<emoji document_id=5210952531676504517>❌</emoji> <b>Пользователь не найден</b>",
        "error": "<emoji document_id=5420323339723881652>⚠️</emoji> <b>Ошибка при получении данных</b>: <i>{}</i>",
        "loading": "<emoji document_id=5328239124933515868>⚙️</emoji> <b>Загружаю информацию...</b>",
        "repos": "репозиториев",
        "no_data": "Нет данных"
    }

    async def client_ready(self, client, db):
        self.client = client

    @loader.command(ru_doc="<username> - получить информацию о профиле GitHub",
                   en_doc="<username> - get GitHub profile information")
    async def github(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_username"])
            return

        await utils.answer(message, self.strings["loading"])

        try:
            r = requests.get(f"https://api.github.com/users/{args}")
            if r.status_code == 404:
                await utils.answer(message, self.strings["user_not_found"])
                return
            if r.status_code != 200:
                await utils.answer(message, self.strings["error"].format("Invalid API response"))
                return

            user = r.json()
            
            repos = requests.get(f"https://api.github.com/users/{args}/repos")
            repos_data = repos.json()
            languages = {}
            for repo in repos_data:
                if repo['language'] and not repo['fork']:
                    languages[repo['language']] = languages.get(repo['language'], 0) + 1
            
            top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
            
            if len(top_langs) > 1:
                langs_parts = []
                for i, lang in enumerate(top_langs):
                    prefix = " ┣ " if i < len(top_langs)-1 else " ┗ "
                    langs_parts.append(f"{prefix}<b>{lang[0]}:</b> <i>{lang[1]} {self.strings['repos']}</i>")
                langs_text = "\n".join(langs_parts)
            elif len(top_langs) == 1:
                langs_text = f" ┗ <b>{top_langs[0][0]}:</b> <i>{top_langs[0][1]} {self.strings['repos']}</i>"
            else:
                langs_text = f" ┗ {self.strings['no_data']}"
            
            created = datetime.strptime(user['created_at'], "%Y-%m-%dT%H:%M:%SZ")
            created_date = created.strftime("%d.%m.%Y")
            
            text = (
                f"<emoji document_id=5296237851891998039>😸</emoji> <b>Github profile:</b>\n\n"
                f"<emoji document_id=5879770735999717115>👤</emoji> <b>Main information:</b>\n"
                f" ┣ <b>Github username:</b> <a href='https://github.com/{user['login']}'>{user['login']}</a>\n"
                f" ┣ <b>Company:</b> {user['company'] or '❌'}\n"
                f" ┣ <b>Account created:</b> {created_date}\n"
                f" ┣ <b>Website:</b> {user['blog'] or '❌'}\n"
                f" ┗ <b>Email:</b> {user['email'] or '❌'}\n\n"
                f"<emoji document_id=5305610789717902392>📊</emoji> <b>Statistics:</b>\n"
                f" ┣ <b>Followers:</b> {user['followers']}\n"
                f" ┣ <b>Following:</b> {user['following']}\n"
                f" ┣ <b>Public repositories:</b> {user['public_repos']}\n"
                f" ┗ <b>Public gists:</b> {user['public_gists']}\n\n"
                f"<emoji document_id=5472196174825901368>💡</emoji> <b>Most used languages:</b>\n"
                f"{langs_text}"
            )
            
            await utils.answer(message, text)

        except Exception as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
