from .. import loader, utils
from telethon.tl.types import Message
import random
import json
from io import BytesIO
from ..inline.types import InlineCall

# meta developer: @kmodules
__version__ = (1, 0, 0)

@loader.tds
class HowMuchMod(loader.Module):
    """Модуль для проверки насколько вы ..."""
    
    strings = {
        "name": "HowMuch",
        "no_template": "<emoji document_id=5219901967916084166>💥</emoji> <b>Шаблон {} не найден.</b>",
        "template_exists": "<emoji document_id=5220070652756635426>👀</emoji> <b>Шаблон уже существует.</b>",
        "template_added": "<emoji document_id=5219899949281453881>✅</emoji> <b>Шаблон был добавлен.</b>",
        "template_deleted": "<emoji document_id=5260424249914435335>♨️</emoji> <b>Шаблон {} был удалён.</b>",
        "templates": "<emoji document_id=5420239291508868251>⭐️</emoji> <b>Шаблоны:</b>\n\n{}\n\n<emoji document_id=5116368680279606270>♥️</emoji><b> Используйте шаблоны через .howmuch &lt;шаблон&gt;.\n</b><emoji document_id=5085022089103016925>⚡️</emoji><b> Создайте шаблон через</b> <b>.addtemplate &lt;title&gt; &lt;emoji&gt;</b>",
        "backup_done": "<emoji document_id=5251429849662243654>🦋</emoji> <b>Бэкап шаблонов.</b>",
        "restore_done": "<emoji document_id=5251333384696776743>⚡️</emoji> <b>Шаблоны были вставлены.</b>",
        "no_reply": "<emoji document_id=5219901967916084166>💥</emoji> <b>Ответьте на файл с шаблонами.</b>"
    }

    def __init__(self):
        self.default_templates = {
            "крутой": "😎",
            "гей": "🏳️‍🌈", 
            "умный": "🤓",
            "смелый": "🥱",
            "быстрый": "😶‍🌫️",
            "секретный": "🔑",
            "свободный": "🗻",
            "сильный": "🏋️‍♂️",
            "программист": "👨‍💻",
            "учитель": "👨‍🏫",
            "робот": "🤖",
            "удачный": "🍀"
        }
        
        self.config = loader.ModuleConfig(
            "templates",
            self.default_templates.copy(),
            "Конфиг шаблонов",
            "buttons",
            False,
            "Включить/выключить кнопку Перепройти"
        )

    def get_result(self, emoji, template, percent):
        return f"<b>{emoji} Вы {template} на <i>{percent}%</i> процентов!</b>"

    def get_template(self, query: str):
        query = query.lower()
        for template in self.config["templates"]:
            if template.lower() == query:
                return template
        return None

    @loader.command() 
    async def howmuch(self, message: Message):
        """Проверить насколько вы подходите под шаблон"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_template"].format(""))
            return
            
        template = self.get_template(args)
        if not template:
            await utils.answer(message, self.strings["no_template"].format(args))
            return

        percent = random.randint(0, 100)
        emoji = self.config["templates"][template]
        result_text = self.get_result(emoji, template, percent)
        
        if self.config["buttons"]:
            await self.inline.form(
                message=message,
                text=result_text,
                reply_markup=[
                    [{"text": f"{emoji} Перепройти", "callback": self.retry_callback, "args": (template,)}]
                ]
            )
        else:
            await utils.answer(message, result_text)

    async def retry_callback(self, call: InlineCall, template: str):
        percent = random.randint(0, 100)
        emoji = self.config["templates"][template]
        await call.edit(
            text=self.get_result(emoji, template, percent),
            reply_markup=[
                [{"text": f"{emoji} Перепройти", "callback": self.retry_callback, "args": (template,)}]
            ]
        )

    @loader.command()
    async def templates(self, message: Message):
        """Показать список доступных шаблонов"""
        templates_text = ""
        for i, (template, emoji) in enumerate(self.config["templates"].items(), 1):
            templates_text += f"{i}. {template} -> {emoji}\n"
            
        await utils.answer(
            message,
            self.strings["templates"].format(f"<b>{templates_text}</b>")
        )

    @loader.command()
    async def addtemplate(self, message: Message):
        """Добавить новый шаблон"""
        args = utils.get_args_raw(message)
        if not args or len(args.split()) != 2:
            await utils.answer(message, self.strings["no_template"].format(""))
            return

        title, emoji = args.split()
        title_lower = title.lower()
        
        for template in self.config["templates"]:
            if template.lower() == title_lower:
                await utils.answer(message, self.strings["template_exists"])
                return

        self.config["templates"][title] = emoji
        await utils.answer(message, self.strings["template_added"])

    @loader.command()
    async def deltemplate(self, message: Message):
        """Удалить пользовательский шаблон"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_template"].format(""))
            return

        template = self.get_template(args)
        if not template:
            await utils.answer(message, self.strings["no_template"].format(args))
            return

        if template in self.default_templates:
            await utils.answer(message, self.strings["no_template"].format(args))
            return

        del self.config["templates"][template]
        await utils.answer(message, self.strings["template_deleted"].format(template))

    @loader.command()
    async def backupts(self, message: Message):
        """Сделать бэкап пользовательских шаблонов"""
        user_templates = {}
        for template, emoji in self.config["templates"].items():
            if template not in self.default_templates:
                user_templates[template] = emoji
                
        backup = json.dumps(user_templates, indent=2, ensure_ascii=False)
        file = BytesIO(backup.encode())
        file.name = "templates_backup.json"
        
        await message.respond(
            self.strings["backup_done"],
            file=file
        )

    @loader.command()
    async def restorets(self, message: Message):
        """Восстановить шаблоны из бэкапа"""
        reply = await message.get_reply_message()
        if not reply or not reply.document:
            await utils.answer(message, self.strings["no_reply"])
            return

        try:
            data = json.loads((await reply.download_media(bytes)).decode())
            templates = self.config["templates"].copy()
            templates.update(data)
            self.config["templates"] = templates
            await utils.answer(message, self.strings["restore_done"])
        except Exception:
            await utils.answer(message, self.strings["no_reply"])
