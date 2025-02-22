# █▀ █░█ ▄▀█ █▀▄ █▀█ █░█░█
# ▄█ █▀█ █▀█ █▄▀ █▄█ ▀▄▀▄▀

# Copyright 2023 t.me/shadow_modules
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from telethon.tl.types import Message
from .. import loader, utils  # type: ignore

# scope: hikka_only
# meta developer: @shadow_modules, @dan_endy, @hikarimods
# meta banner: https://i.imgur.com/SbLqMlM.jpeg

logger = logging.getLogger(__name__)


@loader.tds
class InlineVizitkaMod(loader.Module):
    """You information in inline vizitka"""

    strings = {
        "name": "InlineVizitka",
        "mysocial": "<b>✨ My social networks</b>",
        "userules": (
            "<b>How this module is used</b>\n1. Links to social networks must be"
            " entered in <code>{prefix}config</code>\n2. Links in the config must start"
            " with https:// otherwise there will be an <b>error</b>"
        ),
    }

    strings_ru = {
        "mysocial": "<b>✨ Мои соцсети</b>",
        "userules": (
            "<b>Как пользоваться данным модулем</b>\n1. Ссылки на соц.сети надо вводить"
            " в <code>{prefix}config</code>\n2. Ссылки в конфиге должны начинаться с"
            " https:// иначе будет <b>ошибка</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                None,
                lambda: "Custom message in .vizitka",
            ),
            loader.ConfigValue(
                "VK",
                "🚫 Link not set",
                lambda: "You VK LINK",
            ),
            loader.ConfigValue(
                "discord",
                "🚫 Link not set",
                lambda: "You discord LINK",
            ),
            loader.ConfigValue(
                "twitter",
                "🚫 Link not set",
                lambda: "You twitter LINK",
            ),
            loader.ConfigValue(
                "inst",
                "🚫 Link not set",
                lambda: "You instagram LINK",
            ),
            loader.ConfigValue(
                "grustno",
                "🚫 Link not set",
                lambda: "You grustnogram LINK",
            ),
            loader.ConfigValue(
                "telegram",
                "🚫 Link not set",
                lambda: "You telegram chanel LINK",
            ),
            loader.ConfigValue(
                "gitlab",
                "🚫 Link not set",
                lambda: "You gitlab account LINK",
            ),
            loader.ConfigValue(
                "github",
                "🚫 Link not set",
                lambda: "You github account LINK",
            ),
            loader.ConfigValue(
                "twitch",
                "🚫 Link not set",
                lambda: "You twitch LINK",
            ),
            loader.ConfigValue(
                "anixart",
                "🚫 Link not set",
                lambda: "You anixart LINK",
            ),
            loader.ConfigValue(
                "xda",
                "🚫 Link not set",
                lambda: "You xda LINK",
            ),
            loader.ConfigValue(
                "4pda",
                "🚫 Link not set",
                lambda: "You 4pda LINK",
            ),
            loader.ConfigValue(
                "tiktok",
                "🚫 Link not set",
                lambda: "You tiktok LINK",
            ),
            loader.ConfigValue(
                "pinterest",
                "🚫 Link not set",
                lambda: "You pinterest LINK",
            ),
            loader.ConfigValue(
                "spotify",
                "🚫 Link not set",
                lambda: "You spotify LINK",
            ),
            loader.ConfigValue(
                "pixiv",
                "🚫 Link not set",
                lambda: "You pixiv LINK",
            ),
        )

    @loader.unrestricted
    async def vizitkacmd(self, message: Message):
        """Command for displaying a business card"""
        await self.inline.form(
            message=message,
            text=self.config["custom_message"] or "<b>✨ Мои соцсети</b>",
            reply_markup=[
                [
                    {"text": "🥱 Discord", "callback": self.inline__callAnswer},
                    {"text": "🦢 VK", "url": self.config["VK"]},
                ],
                [
                    {"text": "❤ Instagram", "url": self.config["inst"]},
                    {"text": "🖤 Grustnogram", "url": self.config["grustno"]},
                ],
                [
                    {"text": "🌐 Twitter", "url": self.config["twitter"]},
                    {"text": "💫 TG Channel", "url": self.config["telegram"]},
                ],
                [
                    {"text": "🌚 GitHub", "url": self.config["github"]},
                    {"text": "☀ GitLab", "url": self.config["gitlab"]},
                ],
                [
                    {"text": "😽 Anixart", "url": self.config["anixart"]},
                    {"text": "📱 4PDA", "url": self.config["4pda"]},
                ],
                [
                    {"text": "📺 Twitch", "url": self.config["twitch"]},
                    {"text": "📴 XDA", "url": self.config["xda"]},
                ],
                [
                    {"text": "🤣 Tik tok", "url": self.config["tiktok"]},
                    {"text": "🎧 Spotify", "url": self.config["spotify"]},
                ],
                [
                    {"text": "🖌 Pixiv", "url": self.config["pixiv"]},
                    {"text": "🖌 Pinterest", "url": self.config["pinterest"]},
                ],
            ],
        )

    async def inline__callAnswer(self, call):
        await call.answer(self.config["discord"], show_alert=True)

    async def vizinfocmd(self, message: Message):
        await utils.answer(
            message,
            self.strings("userules").format(prefix=self.get_prefix()),
        )
