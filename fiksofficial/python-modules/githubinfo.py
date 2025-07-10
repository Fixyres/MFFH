#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                 

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule

from .. import loader, utils
import logging
import json
import re
import urllib.request
from datetime import datetime, timedelta

@loader.tds
class GitHubInfoMod(loader.Module):
    """GitHub user info, recent activity and contribution graph"""
    strings = {
        "name": "GitHubInfo",
        "no_username": "❗ Provide a GitHub username.",
        "user_not_found": "🚫 User not found: <b>{}</b>",
        "profile": "Profile",
        "no_activity": "🕸 No recent activity from <b>{}</b>",
        "no_contrib": "📭 No contribution data for <b>{}</b>",
        "info_text": (
            "👤 <b>{name}</b> | <a href=\"{url}\">{profile}</a>\n"
            "🏢 {company} | 📍 {location}\n"
            "📝 {bio}\n\n"
            "📦 Repos: <b>{repos}</b> | "
            "👥 Followers: <b>{followers}</b> | "
            "👣 Following: <b>{following}</b>\n"
            "🕒 Created: <code>{created}</code>"
        ),
        "activity_header": "<b>Recent activity:</b>\n",
        "activity_commit": "🔨 {count} commit(s) → <code>{branch}</code> in {repo}",
        "activity_create": "✨ Created {ref_type} in {repo}",
        "activity_pr": "🔄 {action} PR: {title}",
        "activity_issue": "❗ {action} issue: {title}",
        "activity_star": "⭐ Starred {repo}",
        "activity_fork": "⑂ Forked to {fork}",
        "activity_other": "⚡ {event} in {repo}",
        "contrib_header": "<b>Contribution graph</b> for <a href=\"https://github.com/{username}\">{username}</a>:\n",
        "contrib_footer": "⬛ = 0, 🟩 = 1+ contributions",
    }

    strings_ru = {
        "no_username": "❗ Укажи имя пользователя GitHub.",
        "user_not_found": "🚫 Пользователь не найден: <b>{}</b>",
        "profile": "Профиль",
        "no_activity": "🕸 Нет активности у <b>{}</b>",
        "no_contrib": "📭 Нет данных о вкладах <b>{}</b>",
        "info_text": (
            "👤 <b>{name}</b> | <a href=\"{url}\">{profile}</a>\n"
            "🏢 {company} | 📍 {location}\n"
            "📝 {bio}\n\n"
            "📦 Репозитории: <b>{repos}</b> | "
            "👥 Подписчики: <b>{followers}</b> | "
            "👣 Подписки: <b>{following}</b>\n"
            "🕒 Создан: <code>{created}</code>"
        ),
        "activity_header": "<b>Последняя активность:</b>\n",
        "activity_commit": "🔨 {count} коммит(ов) → <code>{branch}</code> в {repo}",
        "activity_create": "✨ Создан {ref_type} в {repo}",
        "activity_pr": "🔄 {action} PR: {title}",
        "activity_issue": "❗ {action} issue: {title}",
        "activity_star": "⭐ В избранное {repo}",
        "activity_fork": "⑂ Форк в {fork}",
        "activity_other": "⚡ {event} в {repo}",
        "contrib_header": "<b>График активности</b> <a href=\"https://github.com/{username}\">{username}</a>:\n",
        "contrib_footer": "⬛ = 0, 🟩 = 1+ контрибуций",
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def github_api(self, url):
        try:
            with urllib.request.urlopen(url) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            self.logger.warning(f"[GitHub API] {e}")
            return None

    def get_username(self, message):
        args = message.text.split(maxsplit=1)
        return args[1] if len(args) > 1 else None

    @loader.command(doc="Show GitHub user info", ru_doc="Информация о пользователе GitHub")
    async def gh(self, message):
        """Show GitHub user info"""
        username = self.get_username(message)
        if not username:
            return await message.edit(self.strings("no_username"))

        data = self.github_api(f"https://api.github.com/users/{username}")
        if not data:
            return await message.edit(self.strings("user_not_found").format(username))

        await message.edit(self.strings("info_text").format(
            name=data.get("name") or username,
            url=data["html_url"],
            profile=self.strings("profile"),
            company=data.get("company", "N/A"),
            location=data.get("location", "N/A"),
            bio=data.get("bio", "No bio"),
            repos=data.get("public_repos", 0),
            followers=data.get("followers", 0),
            following=data.get("following", 0),
            created=data.get("created_at", "")[:10]
        ))

    @loader.command(doc="Show recent GitHub activity", ru_doc="Последняя активность GitHub")
    async def gha(self, message):
        """Show recent GitHub activity"""
        username = self.get_username(message)
        if not username:
            return await message.edit(self.strings("no_username"))

        events = self.github_api(f"https://api.github.com/users/{username}/events?per_page=5")
        if not events:
            return await message.edit(self.strings("no_activity").format(username))

        lines = []
        for event in events:
            etype = event["type"]
            repo = event["repo"]["name"]
            payload = event.get("payload", {})

            if etype == "PushEvent":
                branch = re.sub(r"refs/heads/", "", payload.get("ref", "main"))
                count = len(payload.get("commits", []))
                lines.append(self.strings("activity_commit").format(count=count, branch=branch, repo=repo))
            elif etype == "CreateEvent":
                lines.append(self.strings("activity_create").format(ref_type=payload.get("ref_type"), repo=repo))
            elif etype == "PullRequestEvent":
                pr = payload.get("pull_request", {})
                lines.append(self.strings("activity_pr").format(action=payload.get("action"), title=pr.get("title")))
            elif etype == "IssuesEvent":
                issue = payload.get("issue", {})
                lines.append(self.strings("activity_issue").format(action=payload.get("action"), title=issue.get("title")))
            elif etype == "WatchEvent":
                lines.append(self.strings("activity_star").format(repo=repo))
            elif etype == "ForkEvent":
                lines.append(self.strings("activity_fork").format(fork=payload.get("forkee", {}).get("full_name")))
            else:
                lines.append(self.strings("activity_other").format(event=etype, repo=repo))

        await message.edit(self.strings("activity_header") + "\n".join(lines))

    @loader.command(doc="Show GitHub contribution graph", ru_doc="Показать график контрибов GitHub")
    async def ghc(self, message):
        """Show GitHub contribution graph"""
        username = self.get_username(message)
        if not username:
            return await message.edit(self.strings("no_username"))

        data = self.github_api(f"https://github-contributions-api.deno.dev/{username}.json")
        contribs = data.get("contributions") if data else None

        if not isinstance(contribs, list):
            return await message.edit(self.strings("no_contrib").format(username))

        today = datetime.utcnow().date()
        start = today - timedelta(days=90)
        matrix = [["⬛" for _ in range(13)] for _ in range(7)]

        for entry in contribs:
            try:
                date = datetime.strptime(entry["date"], "%Y-%m-%d").date()
                if not (start <= date <= today):
                    continue
                day = (date.weekday() + 1) % 7  # Sunday=0
                week = (date - start).days // 7
                if entry.get("contributionCount", 0) > 0:
                    matrix[day][week] = "🟩"
            except:
                continue

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        graph = "\n".join(f"{days[i]} {''.join(matrix[i])}" for i in range(7))

        await message.edit(
            self.strings("contrib_header").format(username=username)
            + f"<pre>{graph}</pre>\n"
            + self.strings("contrib_footer")
        )