# `7MMM.     ,MMF'`7MMM.     ,MMF'   `7MMM.     ,MMF'              `7MM
# MMMb    dPMM    MMMb    dPMM       MMMb    dPMM                  MM
# M YM   ,M MM    M YM   ,M MM       M YM   ,M MM  ,pW"Wq.    ,M""bMM  ,pP"Ybd
# M  Mb  M' MM    M  Mb  M' MM       M  Mb  M' MM 6W'   `Wb ,AP    MM  8I   `"
# M  YM.P'  MM    M  YM.P'  MM mmmmm M  YM.P'  MM 8M     M8 8MI    MM  `YMMMa.
# M  `YM'   MM    M  `YM'   MM       M  `YM'   MM YA.   ,A9 `Mb    MM  L.   I8
# .JML. `'  .JMML..JML. `'  .JMML.   .JML. `'  .JMML.`Ybmd9'   `Wbmd"MML.M9mmmP'
#
# (c) 2023 — licensed under Apache 2.0 — https://www.apache.org/licenses/LICENSE-2.0

# meta pic: https://img.icons8.com/stickers/344/block.png
# meta developer: @mm_mods

__version__ = "1.0.0"

from hikka import loader, utils
from telethon.tl.patched import Message
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


# noinspection PyCallingNonCallable
@loader.tds
class ASAPMod(loader.Module):
    """Advanced Sending Automatisation Program"""

    strings = {
        'name': 'ASAP',
        'args?!': '🟥 <b>Arguments needed!</b>',
        'incorrecttime': '🟥 <b>Incorrect time!</b>\n{example}',
        'taskslist': '📄 <b>Tasks list:</b>\n\n',
        'task': '<i>Task <code>{x}</code>:</i> send <code>{text}</code> to <code>{address}</code> ({at_time}).\n',
        'tasklistempty': '🟨 <b>Tasks list is empty!</b>',
        'taskadded': '🟩 <b>Task added!</b>\nNext execution: <code>{at_time}</code>, task number: <code>{x}</code>',
        'taskremoved': '🟩 <b>Task removed!</b>',
        'tasknotfound': '🟥 <b>Task not found!</b>',
        'tasklistcleared': '🟩 <b>Tasks list cleared!</b>',
        'taskpaused': '🟩 <b>Task paused!</b>',
        'allpaused': '🟩 <b>All tasks paused!</b>',
        'taskresumed': '🟩 <b>Task resumed!</b>',
        'taskpretimeexecuted': '🟩 <b>Task executed!</b>\nNext execution: <code>{at_time}</code>',
        'taskreplanned': '🟩 <b>Task replanned!</b>\nNext execution: <code>{at_time}</code>',
        'defaultintervalset': '🟩 <b>Default interval set!</b>\n{example}',
        'incorrectinterval': '🟥 <b>Incorrect interval!</b>',
        'timeformatexample': '🟦 <i>Time format example:</i> <code>2h</code> — 2 hours, '
                             '<code>1d 2h 30m</code> — 1 day, 2 hours and 30 minutes, '
                             '<code>20s</code> — 20 seconds.',
        'tzset': '🟩 <b>Timezone set!</b>',
        'incorrecttz': '🟥 <b>Incorrect timezone!</b>',
        'safetyreasonerror': '🟨 <b>For safety reasons, you can\'t set such short interval!</b>',
    }

    strings_ru = {
        'name': 'ASAP',
        '_cls_doc': 'Продвинутая программа автоматизации отправки сообщений',
        'args?!': '🟥 <b>Нужны аргументы!</b>',
        'incorrecttime': '🟥 <b>Неверное время!</b>\n{example}',
        'taskslist': '📄 <b>Список задач:</b>\n\n',
        'task': '<i>Задача <code>{x}</code>:</i> отправить <code>{text}</code> на <code>{address}</code> ({at_time}).'
                '\n',
        'tasklistempty': '🟨 <b>Список задач пуст!</b>',
        'taskadded': '🟩 <b>Задача добавлена!</b>\nСледующее выполнение: <code>{at_time}</code>, номер задачи: <code>{'
                     'x}</code>',
        'taskremoved': '🟩 <b>Задача удалена!</b>',
        'tasknotfound': '🟩 <b>Задача не найдена!</b>',
        'tasklistcleared': '🟩 <b>Список задач очищен!</b>',
        'taskpaused': '🟩 <b>Задача приостановлена!</b>',
        'allpaused': '🟩 <b>Все задачи приостановлены!</b>',
        'taskresumed': '🟩 <b>Задача возобновлена!</b>',
        'taskpretimeexecuted': '🟩 <b>Задача выполнена!</b>\nСледующее выполнение: <code>{at_time}</code>',
        'taskreplanned': '🟩 <b>Задача перепланирована!</b>\nСледующее выполнение: <code>{at_time}</code>',
        'defaultintervalset': '🟩 <b>Интервал по умолчанию установлен!</b>',
        'incorrectinterval': '🟥 <b>Неверный интервал!</b>\n{example}',
        'timeformatexample': '🟦 <i>Пример формата времени:</i> <code>2h</code> — 2 часа, '
                             '<code>1d 2h 30m</code> — 1 день, 2 часа и 30 минут, '
                             '<code>20s</code> — 20 секунд.',
        'tzset': '🟩 <b>Часовой пояс установлен!</b>',
        'incorrecttz': '🟥 <b>Неверный часовой пояс!</b>',
        'safetyreasonerror': '🟨 <b>По соображениям безопасности вы не можете установить такой короткий интервал!</b>',
    }

    strings_de = {
        'name': 'ASAP',
        '_cls_doc': 'Fortgeschrittenes Programm zur Automatisierung des Nachrichtenversands',
        'args?!': '🟥 <b>Argumente benötigt!</b>',
        'incorrecttime': '🟥 <b>Falsche Zeit!</b>\n{example}',
        'taskslist': '📄 <b>Aufgabenliste:</b>\n\n',
        'task': '<i>Aufgabe <code>{x}</code>:</i> senden <code>{text}</code> zu <code>{address}</code> ({at_time}).\n',
        'tasklistempty': '🟨 <b>Aufgabenliste ist leer!</b>',
        'taskadded': '🟩 <b>Aufgabe hinzugefügt!</b>\nNächste Ausführung: <code>{at_time}</code>, '
                     'Aufgabennummer: <code>{x}</code>',
        'taskremoved': '🟩 <b>Aufgabe entfernt!</b>',
        'tasknotfound': '🟩 <b>Aufgabe nicht gefunden!</b>',
        'tasklistcleared': '🟩 <b>Aufgabenliste gelöscht!</b>',
        'taskpaused': '🟩 <b>Aufgabe pausiert!</b>',
        'allpaused': '🟩 <b>Alle Aufgaben pausiert!</b>',
        'taskresumed': '🟩 <b>Aufgabe fortgesetzt!</b>',
        'taskpretimeexecuted': '🟩 <b>Aufgabe ausgeführt!</b>\nNächste Ausführung: <code>{at_time}</code>',
        'taskreplanned': '🟩 <b>Aufgabe neu geplant!</b>\nNächste Ausführung: <code>{at_time}</code>',
        'defaultintervalset': '🟩 <b>Standardintervall gesetzt!</b>',
        'incorrectinterval': '🟥 <b>Falsches Intervall!</b>\n{example}',
        'timeformatexample': '🟦 <i>Beispiel für das Zeitformat:</i> <code>2h</code> — 2 Stunden, '
                             '<code>1d 2h 30m</code> — 1 Tag, 2 Stunden und 30 Minuten, '
                             '<code>20s</code> — 20 Sekunden.',
        'tzset': '🟩 <b>Zeitzone gesetzt!</b>',
        'incorrecttz': '🟥 <b>Falsche Zeitzone!</b>',
        'safetyreasonerror': '🟨 <b>Aus Sicherheitsgründen können Sie kein so kurzes Intervall festlegen!</b>',
    }

    async def client_ready(self):
        if not self.get('default_interval'):
            self.set('default_interval', '2h')

        if not self.get('tasks'):
            self.set('tasks', {})

        if not self.get('tz'):
            self.set('tz', 0)

    @loader.loop(interval=1, autostart=True)
    async def _run_tasks(self):
        tasks = self.get('tasks')
        if not tasks:
            return

        for k, task in tasks.items():
            if datetime.strptime(task['next_execution'], '%d.%m.%Y %H:%M:%S') <= datetime.now():
                await self._run_task(task, k)

    @staticmethod
    def validate_time(time: str) -> bool:
        """
        Validates the time.
        :param time: time to validate.
        :return: if time is valid or not.
        """
        if not time:
            return False

        args = time.split()

        for arg in args:
            if not arg[:-1].isdigit():
                return False

            if arg[-1] not in ['s', 'm', 'h', 'd']:
                return False

        return True

    @staticmethod
    def convert_time(time: str) -> timedelta:
        """
        Converts time to timedelta.
        :param time: time to convert.
        :return: timedelta.
        """
        args = time.split()
        res = timedelta()

        for arg in args:
            try:
                if arg[-1] == 's':
                    res += timedelta(seconds=int(arg[:-1]))
                elif arg[-1] == 'm':
                    res += timedelta(minutes=int(arg[:-1]))
                elif arg[-1] == 'h':
                    res += timedelta(hours=int(arg[:-1]))
                elif arg[-1] == 'd':
                    res += timedelta(days=int(arg[:-1]))
            except ValueError:
                pass

        return res

    @loader.command(
        'ataskadd',
        ru_doc='Добавить задачу в список задач.\nИспользование: .ataskadd <текст>\n[время]\n[адресат]',
        de_doc='Fügen Sie eine Aufgabe zur Aufgabenliste hinzu.\nVerwendung: .ataskadd <Text>\n[Zeit]\n[Empfänger]',
    )
    async def ataskaddcmd(self, m: Message):
        """Add a task to the list of tasks.
        Usage: .ataskadd <text>
        [time]
        [target]"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        args = args.split('\n')

        if len(args) == 2:
            interval = args[1]
            address = m.chat_id
        elif len(args) == 3:
            interval = args[1]
            address = args[2]
        else:
            interval = self.get('default_interval')
            address = m.chat_id

        if not self.validate_time(interval):
            return await utils.answer(m, self.strings('incorrecttime'))

        if self.convert_time(interval) < timedelta(seconds=10):
            return await utils.answer(m, self.strings('safetyreasonerror'))

        task = {
            'text': args[0],
            'interval': interval,
            'address': address,
            'paused': False,
            'next_execution': (datetime.now() + self.convert_time(interval)).strftime('%d.%m.%Y %H:%M:%S'),
        }

        tasks = self.get('tasks')
        x = len(tasks) + 1
        tasks[str(x)] = task

        self.set('tasks', tasks)

        await utils.answer(
            m, self.strings('taskadded').format(
                at_time=task['next_execution'],
                x=x
            )
        )

    @loader.command(
        'ataskremove',
        ru_doc='Удалить задачу из списка задач.\nИспользование: .ataskremove <номер>',
        de_doc='Entfernen Sie eine Aufgabe aus der Aufgabenliste.\nVerwendung: .ataskremove <Nummer>',
    )
    async def ataskremovecmd(self, m: Message):
        """Remove a task from the list of tasks.
        Usage: .ataskremove <number>"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        try:
            x = int(args)
        except ValueError:
            return await utils.answer(m, self.strings('args?!'))

        x = str(x)

        tasks = self.get('tasks')

        if x not in tasks:
            return await utils.answer(m, self.strings('tasknotfound'))

        del tasks[x]
        self.set('tasks', tasks)

        await utils.answer(m, self.strings('taskremoved'))

    @loader.command(
        'atasklist',
        ru_doc='Показать список задач.',
        de_doc='Zeigt die Liste der Aufgaben an.',
    )
    async def atasklistcmd(self, m: Message):
        """Show the list of tasks."""
        tasks = self.get('tasks')

        if not tasks:
            return await utils.answer(m, self.strings('tasklistempty'))

        res = self.strings('taskslist')

        for k, task in tasks.items():
            res += self.strings('task').format(
                x=k if not task['paused'] else f'</code><b><s>{k}</s></b><code>',
                text=task['text'],
                address=task['address'],
                at_time=datetime.strptime(task['next_execution'], '%d.%m.%Y %H:%M:%S') + timedelta(hours=self.get('tz'))
            )

        await utils.answer(m, res)

    @loader.command(
        'ataskclear',
        ru_doc='Очистить список задач.',
        de_doc='Löschen Sie die Liste der Aufgaben.',
    )
    async def ataskclearcmd(self, m: Message):
        """Clear the list of tasks."""
        self.set('tasks', {})
        await utils.answer(m, self.strings('tasklistcleared'))

    @loader.command(
        'ataskpause',
        ru_doc='Приостановить задачу.\nИспользование: .ataskpause <номер>\nБез аргументов — приостановить все задачи.',
        de_doc='Aufgabe pausieren.\nVerwendung: .ataskpause <Nummer>\nOhne Argumente - alle Aufgaben pausieren.',
    )
    async def ataskpausecmd(self, m: Message):
        """Pause a task.
        Usage: .ataskpause <number>
        If no arguments — pause all tasks."""
        args = utils.get_args_raw(m)

        if not args:
            tasks = self.get('tasks')

            for k, task in tasks.items():
                task['paused'] = True
                tasks[k] = task

            self.set('tasks', tasks)

            return await utils.answer(m, self.strings('taskpaused'))

        try:
            x = int(args)
        except ValueError:
            return await utils.answer(m, self.strings('args?!'))

        x = str(x)

        tasks = self.get('tasks')

        if x not in tasks:
            return await utils.answer(m, self.strings('tasknotfound'))

        tasks[x]['paused'] = True
        self.set('tasks', tasks)

        await utils.answer(m, self.strings('taskpaused'))

    @loader.command(
        'ataskresume',
        ru_doc='Возобновить задачу.\nИспользование: .ataskresume <номер>',
        de_doc='Aufgabe fortsetzen.\nVerwendung: .ataskresume <Nummer>',
    )
    async def ataskresumecmd(self, m: Message):
        """Resume a task.
        Usage: .ataskresume <number>"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        try:
            x = int(args)
        except ValueError:
            return await utils.answer(m, self.strings('args?!'))

        tasks = self.get('tasks')

        if x > len(tasks):
            return await utils.answer(m, self.strings('tasknotfound'))

        tasks[x - 1]['paused'] = False
        self.set('tasks', tasks)

        await utils.answer(m, self.strings('taskresumed'))

    @loader.command(
        'ataskexec',
        ru_doc='Выполнить задачу сейчас и перепланировать согласно интервалу.\nИспользование: .ataskexec <номер>',
        de_doc='Führen Sie die Aufgabe jetzt aus und planen Sie sie entsprechend dem Intervall neu.\nVerwendung: '
               '.ataskexec <Nummer>',
    )
    async def ataskexeccmd(self, m: Message):
        """Execute a task right now and replan according to the interval.
        Usage: .ataskexec <number>"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        try:
            x = int(args)
        except ValueError:
            return await utils.answer(m, self.strings('args?!'))

        x = str(x)

        tasks = self.get('tasks')

        if x not in tasks:
            return await utils.answer(m, self.strings('tasknotfound'))

        task = tasks[x]

        if task['paused']:
            return await utils.answer(m, self.strings('taskpaused'))

        task['next_execution'] = datetime.now() + self.convert_time(task['interval'])
        self.set('tasks', tasks)

        await utils.answer(
            m, self.strings('taskpretimeexecuted').format(
                at_time=datetime.strptime(task['next_execution'], '%d.%m.%Y %H:%M:%S') + timedelta(hours=self.get('tz'))
            )
        )

        await self._run_task(task, x)

    @loader.command(
        'ataskreplan',
        ru_doc='Изменить интервал задачи.\nИспользование: .ataskreplan <номер> <время>',
        de_doc='Ändern Sie das Intervall der Aufgabe.\nVerwendung: .ataskreplan <Nummer> <Zeit>',
    )
    async def ataskreplancmd(self, m: Message):
        """Change the interval of the task.
        Usage: .ataskreplan <number>"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        args = args.split(maxsplit=1)
        x, time = args[0], args[1]

        tasks = self.get('tasks')

        if x not in tasks:
            return await utils.answer(m, self.strings('tasknotfound'))

        task = tasks[x]

        if not self.validate_time(time):
            return await utils.answer(m, self.strings('incorrecttime'))

        task['interval'] = time

        if task['paused']:
            return await utils.answer(m, self.strings('taskpaused'))

        task['next_execution'] = (datetime.now() + self.convert_time(task['interval'])).strftime('%d.%m.%Y %H:%M:%S')

        tasks[x] = task
        self.set('tasks', tasks)

        await utils.answer(
            m, self.strings('taskreplanned').format(
                at_time=datetime.strptime(task['next_execution'], '%d.%m.%Y %H:%M:%S') + timedelta(hours=self.get('tz'))
            )
        )

    @loader.command(
        'adeftint',
        ru_doc='Установить интервал по умолчанию.\nИспользование: .adeftint <время>',
        de_doc='Setzen Sie das Standardintervall.\nVerwendung: .adeftint <Zeit>',
    )
    async def adeftintcmd(self, m: Message):
        """Set the default interval.
        Usage: .ataskdeftint <time>"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        if not self.validate_time(args):
            return await utils.answer(m, self.strings('incorrectinterval'))

        self.set('default_interval', args)
        await utils.answer(
            m, self.strings('defaultintervalset').format(
                example=self.strings('timeformatexample')
            )
        )

    @loader.command(
        'atz',
        ru_doc='Явно установить часовой пояс, если время отображается неверно.\nИспользование: .atz <часовой пояс>',
        de_doc='Legen Sie die Zeitzone explizit fest, wenn die Zeit falsch angezeigt wird.\nVerwendung: '
               '.atz <Zeitzone>',
    )
    async def atzcmd(self, m: Message):
        """Set the timezone explicitly if time displayed wrong.
        Usage: .atz <timezone>"""
        args = utils.get_args_raw(m)

        if not args:
            return await utils.answer(m, self.strings('args?!'))

        try:
            tz = int(args)
        except ValueError:
            try:
                tz = float(args)
            except ValueError:
                return await utils.answer(m, self.strings('incorrecttz'))

        if tz < -12 or tz > 12:
            return await utils.answer(m, self.strings('incorrecttz'))

        self.set('tz', tz)
        await utils.answer(m, self.strings('tzset'))

    async def _run_task(self, task: dict, index: str):
        if task['paused']:
            return

        await self.client.send_message(task['address'], task['text'])

        tasks = self.get('tasks')
        this = tasks[index]

        this['next_execution'] = (datetime.now() + self.convert_time(this['interval'])).strftime('%d.%m.%Y %H:%M:%S')

        tasks[index] = this
        self.set('tasks', tasks)
