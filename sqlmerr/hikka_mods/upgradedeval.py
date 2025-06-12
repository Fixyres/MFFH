import datetime
import io
import contextlib
import logging
import sys
import typing
import aiohttp

from enum import Enum
from meval import meval
from dataclasses import dataclass, field

from hikkatl.errors.rpcerrorlist import MessageIdInvalidError
from hikkatl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall
from ..log import HikkaException
try:
    from ..types import HikkaReplyMarkup
except ImportError:
    from ..types import HerokuReplyMarkup as HikkaReplyMarkup


# meta banner: https://github.com/sqlmerr/hikka_mods/blob/main/assets/banners/upgradedeval.png?raw=true
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/upgradedeval.png?raw=true
# meta developer: @sqlmerr_m

ITEMS_PER_PAGE = 6
EMOJIS = {
    "python": "<emoji document_id=5197646705813634076>🐍</emoji>",
    "kotlin": "<emoji document_id=5278725341785889330>👩‍💻</emoji>",
    "rust": "<emoji document_id=5278586051701514918>🦀</emoji>",
    "go": "<emoji document_id=5278401118999682984>🐹</emoji>",
}


class LanguageEnum(str, Enum):
    python = "python"
    rust = "rust"
    kotlin = "kotlin"
    go = "go"

@dataclass(frozen=True)
class EvaluationInfo:
    code: str
    language: LanguageEnum = field(default=LanguageEnum.python)
    result: typing.Optional[str] = field(default=None)
    error: typing.Optional[typing.Union[HikkaException, str]] = field(default=None)
    is_error: bool = field(default=False)
    date: datetime.datetime = field(default_factory=datetime.datetime.now)


@loader.tds
class UpgradedEval(loader.Module):
    """Just eval with customizable text and stdout"""

    strings = {
        "name": "UpgradedEval",
        "_cfg_text_result": "Text for result",
        "_cfg_text_error": "Text for error",
        "_cfg_text_result_and_error": "Text containing both error and result",
        "_cfg_mode": "Code run mode. stdout is when print works. return, this is standard .e; auto is just a mode that automatically selects stdout or return",
    }

    strings_ru = {
        "_cfg_text_result": "Текст результата",
        "_cfg_text_error": "Текст ошибки",
        "_cfg_text_result_and_error": "Текст содержащий и ошибку и результат",
        "_cfg_mode": "Режим запуска кода. stdout, это когда работает print. return, это стандартный .e; auto - это просто режим, который автоматически выбирает stdout или return",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text_result",
                (
                    "<b><i>Language:</i></b> <code>{lang}</code>\n"
                    "{emoji} <b><i>Code:</i></b>\n"
                    "<code><pre class='language-{lang}'>{code}</pre></code>\n\n"
                    "<emoji document_id=5895231943955451762>✅</emoji> <b><i>Result:</i></b>\n"
                    "<code><pre class='language-{lang}'>{result}</pre></code>"
                ),
                lambda: self.strings("_cfg_text_result"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "text_error",
                (
                    "<b><i>Language:</i></b> <code>{lang}</code>\n"
                    "{emoji} <b><i>Code:</i></b>\n"
                    "<code><pre>{code}</pre></code>\n\n"
                    "<emoji document_id=5465665476971471368>❌</emoji> <b><i>Error:</i></b>\n"
                    "<code><pre class='language-{lang}'>{error}</pre></code>"
                ),
                lambda: self.strings("_cfg_text_error"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "text_result_and_error",
                (
                    "<b><i>Language:</i></b> <code>{lang}</code>\n"
                    "{emoji} <b><i>Code:</i></b>\n"
                    "<code><pre>{code}</pre></code>\n\n"
                    "<emoji document_id=5895231943955451762>✅</emoji> <b><i>Result:</i></b>\n"
                    "<code><pre class='language-{lang}'>{result}</pre></code>\n\n"
                    "<emoji document_id=5465665476971471368>❌</emoji> <b><i>Error:</i></b>\n"
                    "<code><pre class='language-{lang}'>{error}</pre></code>"
                ),
                lambda: self.strings("_cfg_text_result_and_error"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "mode",
                "auto",
                lambda: self.strings("_cfg_mode"),
                validator=loader.validators.Choice(["stdout", "return", "auto"]),
            ),
        )
        self._evals: typing.List[EvaluationInfo] = []


    async def __inline_open_eval(self, call: InlineCall, eval_info: EvaluationInfo, current_page: int):
        if not eval_info.is_error:
            text = self.config["text_result"].format(
                emoji=EMOJIS[eval_info.language.lower()],
                lang=eval_info.language.lower(),
                code=utils.escape_html(eval_info.code) if eval_info.code else "None",
                result=eval_info.result if eval_info.result else "None",
            )
        else:
            if eval_info.language == LanguageEnum.python and isinstance(eval_info.error, HikkaException):
                error = (
                    self.lookup("Evaluator").censor(
                        (
                                "\n".join(eval_info.error.full_stack.splitlines()[:-1])
                                + "\n\n"
                                + "🚫 "
                                + eval_info.error.full_stack.splitlines()[-1]
                        )
                    ),
                )
                text = self.config["text_error"].format(
                    emoji=EMOJIS["python"], lang="python", code=utils.escape_html(eval_info.code), error=error[0]
                )
            else:
                error = eval_info.error
                text = self.config["text_result_and_error"].format(
                    lang=eval_info.language.lower(), code=utils.escape_html(eval_info.code), result=eval_info.result, error=error
                )
            


        await call.edit(
            text=text,
            reply_markup={
                "text": "←",
                "callback": self.__inline_open,
                "args": (current_page,)
            }
        )

    async def __inline_open(self, call: InlineCall, page: int = 0):
        await call.edit(
            text="📋 <b>Evaluation history</b>",
            reply_markup=self.__inline_generate_keyboard(self._evals, page),
        )

    def __inline_generate_keyboard(self, evals: typing.List[EvaluationInfo], page: int = 0):
        if len(evals) == 0:
            return []

        # Sort evals in descending order based on date to ensure newest first
        sorted_evals = sorted(evals, key=lambda x: x.date, reverse=True)

        offset = page * ITEMS_PER_PAGE
        if offset < 0 or offset >= len(sorted_evals):
            page = 0
            offset = 0

        # Slice evaluations for the current page
        page_evals = sorted_evals[offset:offset + ITEMS_PER_PAGE]
        buttons = []

        # Generate buttons for evaluations on current page (no reverse)
        for e in page_evals:
            buttons.append(
                [{
                    "text": f"{e.date.strftime('%Y-%m-%d %H:%M:%S')} {'✅' if not e.is_error else '❌'} {e.language.capitalize()}",
                    "callback": self.__inline_open_eval,
                    "args": (e, page)
                }]
            )

        # Navigation buttons
        nav_buttons = []
        if offset > 0:
            nav_buttons.append({
                "text": "<",
                "callback": self.__inline_open,
                "args": (page - 1,)
            })
        else:
            nav_buttons.append({
                "text": "X",
                "data": "empty"
            })

        nav_buttons.append({
            "text": f"{page + 1}/{(len(evals) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE}",
            "data": "empty"
        })

        if offset + ITEMS_PER_PAGE < len(sorted_evals):
            nav_buttons.append({
                "text": ">",
                "callback": self.__inline_open,
                "args": (page + 1,)
            })
        else:
            nav_buttons.append({
                "text": "X",
                "data": "empty"
            })

        if nav_buttons:
            buttons.append(nav_buttons)

        return buttons

    @loader.command(ru_doc="Получить историю (с рестарта юзербота)")
    async def ehistory(self, message: Message):
        """Get history (since userbot restart)"""

        await self.inline.form(
            text="📋 <b>Evaluation history</b>",
            message=message,
            reply_markup=self.__inline_generate_keyboard(self._evals),
        )

    @loader.command(ru_doc="Улучшенный eval")
    async def ie(self, message: Message):
        """Upgraded eval"""
        args = utils.get_args_raw(message)

        try:
            attrs = await self.lookup("Evaluator").getattrs(message)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                result = await meval(
                    utils.escape_html(args),
                    globals(),
                    **attrs,
                )
            output = stdout.getvalue()

        except Exception:
            item = HikkaException.from_exc_info(*sys.exc_info())
            error = (
                self.lookup("Evaluator").censor(
                    (
                        "\n".join(item.full_stack.splitlines()[:-1])
                        + "\n\n"
                        + "🚫 "
                        + item.full_stack.splitlines()[-1]
                    )
                ),
            )

            await utils.answer(
                message,
                self.config["text_error"].format(
                    emoji=EMOJIS["python"],
                    lang="python",
                    code=utils.escape_html(utils.get_args_raw(message)), error=error[0]
                ),
            )

            self._evals.append(EvaluationInfo(
                args,
                error=item,
                is_error=True,
            ))
            return

        mode = self.config["mode"]
        if mode == "stdout":
            result = output
        elif mode == "auto" and output.strip():
            result = output


        if callable(getattr(result, "stringify", None)):
            with contextlib.suppress(Exception):
                result = str(result.stringify())

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.config["text_result"].format(
                    emoji=EMOJIS["python"],
                    lang="python",
                    code=utils.escape_html(args) if args else "None",
                    result=result if result else "None",
                ),
            )

        self._evals.append(EvaluationInfo(
            args,
            result=result,
        ))


    @loader.command(ru_doc="Запустить код на Rust")
    async def erust(self, message: Message):
        """Evaluate Rust code"""
        code = utils.get_args_raw(message)
        url = "https://play.rust-lang.org/execute"
        payload = {
            "channel": "stable",
            "mode": "debug",
            "edition": "2024",
            "crateType": "bin",
            "tests": False,
            "code": code
        }
        
        headers = {"Content-Type": "application/json"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=10) as response:
                response.raise_for_status()
                result = await response.json()
        
        output = result.get("stdout", "")
        errors = result.get("stderr", "")
        
        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.config["text_result_and_error"].format(
                    emoji=EMOJIS["rust"],
                    lang="rust",
                    code=utils.escape_html(code) if code else "None",
                    result=output,
                    error=errors,
                ),
            )

        self._evals.append(EvaluationInfo(code, LanguageEnum.rust, result=output, error=errors, is_error=errors!=""))


    @loader.command(ru_doc="Запустить код на Go")
    async def ego(self, message: Message):
        """Evaluate Go code"""
        code = utils.get_args_raw(message)
        url = "https://play.golang.org/compile"
        payload = {
            "version": 2,
            "body": code,
            "withVet": False
        }
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload, headers=headers, timeout=10) as response:
                response.raise_for_status()
                result = await response.json()
        
        output = ""
        if result.get("Events"):
            for event in result["Events"]:
                if event.get("Kind") == "stdout":
                    output += event.get("Message", "")
        errors = result.get("Errors", "")
        
        if errors:
            with contextlib.suppress(MessageIdInvalidError):
                await utils.answer(
                    message,
                    self.config["text_result_and_error"].format(
                        emoji=EMOJIS["go"],
                        lang="go",
                        code=utils.escape_html(code) if code else "None",
                        result=output,
                        error=errors,
                    ),
                )
        else:
            with contextlib.suppress(MessageIdInvalidError):
                await utils.answer(
                    message,
                    self.config["text_result"].format(
                        emoji=EMOJIS["go"],
                        lang="go",
                        code=utils.escape_html(code) if code else "None",
                        result=output,
                    ),
                )

        self._evals.append(EvaluationInfo(code, LanguageEnum.go, result=output, error=errors, is_error=errors!=""))


    @loader.command(ru_doc="Запустить код на Kotlin")
    async def ekt(self, message: Message):
        """Evaluate Kotlin code"""
        code = utils.get_args_raw(message)
        url = "https://api.kotlinlang.org/api/2.1.20/compiler/run"
        payload = {
            "args": "",
            "conftype": "java",
            "files": [
                {
                    "name": "Main.kt",
                    "publicId": "",
                    "text": code
                }
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=10) as response:
                response.raise_for_status()
                result = await response.json()
        
        output = result.get("text", "")
        errors = result.get("errors", {}).get("Main.kt", [])
        error = ""
        for err in errors:
            error += f"- {err.get('message')}\n"
        
        if errors:
            with contextlib.suppress(MessageIdInvalidError):
                await utils.answer(
                    message,
                    self.config["text_result_and_error"].format(
                        emoji=EMOJIS["kotlin"],
                        lang="kotlin",
                        code=utils.escape_html(code) if code else "None",
                        result=output,
                        error=error,
                    ),
                )
        else:
            with contextlib.suppress(MessageIdInvalidError):
                await utils.answer(
                    message,
                    self.config["text_result"].format(
                        emoji=EMOJIS["kotlin"],
                        lang="kotlin",
                        code=utils.escape_html(code) if code else "None",
                        result=output,
                    ),
                )

        self._evals.append(EvaluationInfo(code, LanguageEnum.kotlin, result=output, error=errors, is_error=errors!=[]))
