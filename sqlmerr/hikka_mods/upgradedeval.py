import io
import contextlib
import sys
from meval import meval

from hikkatl.errors.rpcerrorlist import MessageIdInvalidError

from .. import loader, utils
from ..log import HikkaException


# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_upgradedeval.png?raw=true
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/upgradedeval.png?raw=true
# meta developer: @sqlmerr_m


@loader.tds
class UpgradedEval(loader.Module):
    """Just eval with customizable text and stdout"""

    strings = {
        "name": "UpgradedEval",
        "_cfg_text_result": "Text for result",
        "_cfg_text_error": "Text for error",
        "_cfg_mode": "Code run mode. stdout is when print works. return, this is standard .e",
    }

    strings_ru = {
        "_cfg_text_result": "Текст результата",
        "_cfg_text_error": "Текст ошибки",
        "_cfg_mode": "Режим запуска кода. stdout, это когда работает print. return, это стандартный .e",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text_result",
                "<emoji document_id=5197646705813634076>🐍</emoji> <b><i>Code:</i></b>\n<code>{code}</code>\n\n<emoji document_id=5895231943955451762>✅</emoji> <b><i>Result:</i></b>\n<code>{result}</code>",
                lambda: self.strings("_cfg_text_result"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "text_error",
                "<emoji document_id=5197646705813634076>🐍</emoji> <b><i>Code:</i></b>\n<code>{code}</code>\n\n<emoji document_id=5465665476971471368>❌</emoji> <b><i>Error:</i></b>\n<code>{error}</code>",
                lambda: self.strings("_cfg_text_error"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "mode",
                "stdout",
                lambda: self.strings("_cfg_mode"),
                validator=loader.validators.Choice(["stdout", "return"]),
            ),
        )

    @loader.command(ru_doc="Улучшенный eval")
    async def ie(self, message):
        """Upgraded eval"""
        args = utils.get_args_raw(message)

        try:
            if self.config["mode"] == "stdout":
                stdout = io.StringIO()
                with contextlib.redirect_stdout(stdout):
                    await meval(
                        utils.escape_html(args),
                        globals(),
                        **await self.lookup("Evaluator").getattrs(message),
                    )
                result = stdout.getvalue()
            else:
                result = await meval(
                    utils.escape_html(args),
                    globals(),
                    **await self.lookup("Evaluator").getattrs(message),
                )

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
                    code=utils.escape_html(utils.get_args_raw(message)), error=error[0]
                ),
            )

            return

        if callable(getattr(result, "stringify", None)):
            with contextlib.suppress(Exception):
                result = str(result.stringify())

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.config["text_result"].format(
                    code=utils.escape_html(args) if args else "None",
                    result=result if result else "None",
                ),
            )
