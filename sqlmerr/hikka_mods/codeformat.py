"""
░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
"""

# meta developer: @sqlmerr_m
# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_codeformat.png?raw=true

from .. import loader, utils

from hikkatl.tl.types import Message


@loader.tds
class CodeFormat(loader.Module):
    """Format your code!"""

    strings = {"name": "CodeFormat"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "language", "python", validator=loader.validators.String()
            )
        )

    @loader.command()
    async def code(self, message: Message):
        args = utils.get_args_raw(message)
        language = self.config["language"]

        await utils.answer(
            message, f"<pre><code class='language-{language}'>{args}</code></pre>"
        )
