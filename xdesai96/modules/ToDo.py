#             █ █ ▀ █▄▀ ▄▀█ █▀█ ▀
#             █▀█ █ █ █ █▀█ █▀▄ █
#              © Copyright 2022
#           https://t.me/hikariatama
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# scope: hikka_min 1.2.10

# meta pic: https://img.icons8.com/stickers/500/000000/todo-list.png
# meta banner: https://mods.hikariatama.ru/badges/todo.jpg
# meta developer: @hikarimods
# scope: hikka_only
# edited by: @xdesai

from random import randint

from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class TodoMod(loader.Module):
    """ToDo List"""

    strings = {
        "name": "ToDo",
        "task_removed": "<blockquote><b>✅ Task removed</b></blockquote>",
        "task_not_found": "<blockquote><b>🚫 Task not found</b></blockquote>",
        "new_task": "<b>Task </b><code>#{}</code>:\n<blockquote>{}</blockquote>\n{}",
    }

    strings_ru = {
        "task_removed": "<blockquote><b>✅ Задача удалена</b></blockquote>",
        "task_not_found": "<b>🚫 Задача не найдена</b",
        "new_task": "<b>Задача </b><code>#{}</code>:\n<blockquote>{}</blockquote>\n{}",
    }

    async def client_ready(self, client, db):
        self.todolist = self.get("todo", {})

        self.imp_levels = [
            "🌌 Watchlist",
            "💻 Proging",
            "⌚️ Work",
            "🎒 Family",
            "🚫 Private",
        ]

    async def tdcmd(self, message: Message):
        """[importance:int] <item> - Add task"""

        args = utils.get_args_raw(message)
        try:
            importance = int(args.split()[0])
            task = args.split(maxsplit=1)[1]
        except Exception:
            importance = 0
            task = args

        try:
            importance = int(task) if task != "" else 0
            reply = await message.get_reply_message()
            if reply:
                task = reply.text
        except Exception:
            pass

        if importance >= len(self.imp_levels):
            importance = 0

        random_id = str(randint(10000, 99999))

        self.todolist[random_id] = [task, importance]

        self.set("todo", self.todolist)
        await utils.answer(
            message,
            self.strings["new_task"].format(
                random_id,
                task,
                self.imp_levels[importance],
            ),
        )

    async def tdlcmd(self, message: Message):
        """Show active tasks"""
        res = "<blockquote><b>#ToDo</b></blockquote>\n"
        items = {len(self.imp_levels) - i - 1: [] for i in range(len(self.imp_levels))}
        for item_id, item in self.todolist.items():
            items[item[1]].append(
                f" <code>{self._client.loader.get_prefix()}utd {item_id}</code>: <code>{item[0]}</code>"
            )

        for importance, strings in items.items():
            if len(strings) == 0:
                continue
            res += "\n<blockquote> -{ " + self.imp_levels[importance][2:] + " }-\n"
            res += (
                self.imp_levels[importance][0]
                + ("\n" + self.imp_levels[importance][0]).join(strings)
                + "</blockquote>\n"
            )

        await utils.answer(message, res)

    async def utdcmd(self, message: Message):
        """<id> - Remove task from todo"""
        args = utils.get_args_raw(message)
        if args.startswith("#"):
            args = args[1:]

        if args not in self.todolist:
            await utils.answer(message, self.strings["task_not_found"])
            return

        del self.todolist[args]
        self.set("todo", self.todolist)
        await utils.answer(message, self.strings["task_removed"])
