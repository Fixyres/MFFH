# meta developer: @Enceth
import asyncio
from telethon import events
from telethon.tl.functions.messages import SendMessageRequest
from .. import loader, utils

class pososihui(loader.Module):
    """Модуль для автоматической рассылки сообщений"""

    strings = {
        "name": "AutoSend",
        "job_added": "'Авторассылка {name}' добавлена с интервалом {interval} секунд",
        "job_removed": "Авторассылка '{name}' успешно удалена",
        "no_jobs": "Нет активной авторассылки",
        "job_list": "Активная авторассылка:\n{jobs}",
        "invalid_command": ""
    }

    def __init__(self):
        self.jobs = {}
        self.running_jobs = {}

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        saved_jobs = self.db.get("AutoSend", "jobs", {})
        self.jobs.update(saved_jobs)
        await self._restart_jobs()

    async def _restart_jobs(self):
        for name, job in self.jobs.items():
            await self._start_job(name, job['interval'], job['chats'], job['text'])

    async def _start_job(self, name, interval, chats, text):
        async def job_loop():
            while name in self.running_jobs:
                for chat_id in chats:
                    try:
                        await self.client(SendMessageRequest(int(chat_id), text))
                    except Exception as e:
                        print(f"Ошибка при отправке в {chat_id}: {e}")
                await asyncio.sleep(interval)

        self.running_jobs[name] = self.client.loop.create_task(job_loop())

    @loader.command()
    async def addafcmd(self, message):
        """<название> <интервал> <список чатов через запятую без пробелов> <сообщение> - добавить авторассылку"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["invalid_command"])
            return

        try:
            name, interval, chats, *text = args.split(" ", 3)
            interval = int(interval)
            chats = chats.split(",")
            text = " ".join(text)
        except ValueError:
            await utils.answer(message, self.strings["invalid_command"])
            return

        self.jobs[name] = {"interval": interval, "chats": chats, "text": text}
        self.db.set("AutoSend", "jobs", self.jobs)
        await self._start_job(name, interval, chats, text)
        await utils.answer(message, self.strings["job_added"].format(name=name, interval=interval))

    @loader.command()
    async def rmafcmd(self, message):
        """<название> - удалить задачу"""
        args = utils.get_args_raw(message)
        if args not in self.jobs:
            await utils.answer(message, self.strings["invalid_command"])
            return

        self.jobs.pop(args)
        self.db.set("AutoSend", "jobs", self.jobs)

        if args in self.running_jobs:
            self.running_jobs[args].cancel()
            self.running_jobs.pop(args)

        await utils.answer(message, self.strings["job_removed"].format(name=args))

    @loader.command()
    async def listafscmd(self, message):
        """Выводит список активных задач."""
        if not self.jobs:
            await utils.answer(message, self.strings["no_jobs"])
            return

        job_list = "\n".join([f"{name}: {job['interval']} секунд, чаты: {', '.join(job['chats'])}" for name, job in self.jobs.items()])
        await utils.answer(message, self.strings["job_list"].format(jobs=job_list))
