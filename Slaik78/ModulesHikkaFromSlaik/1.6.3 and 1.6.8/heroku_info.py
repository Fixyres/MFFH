# ©️ Dan Gazizullin, 2021-2023
# This file is a part of Hikka Userbot
# 🌐 https://github.com/hikariatama/Hikka
# You can redistribute it and/or modify it under the terms of the GNU AGPLv3
# 🔑 https://www.gnu.org/licenses/agpl-3.0.html

# Module is still in test, there may be bugs
# Modified by @Hicota

import re
import emoji
import git
from bs4 import BeautifulSoup
from typing import Optional
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from hikkatl.tl.types import Message
from hikkatl.utils import get_display_name
import requests
import os
import glob

from .. import loader, utils, version
from ..inline.types import InlineQuery
import platform as lib_platform
import getpass

@loader.tds
class HerokuInfoMod(loader.Module):
    """Show userbot info"""

    strings = {"name": "HerokuInfo"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "custom_message",
                doc=lambda: self.strings("_cfg_cst_msg"),
            ),

            loader.ConfigValue(
                "bannerUrl",
                "https://imgur.com/a/7LBPJiq.png",
                lambda: self.strings("_cfg_banner"),
            ),
            
            loader.ConfigValue(
                "pp_to_banner",
                False,
                validator=loader.validators.Boolean(),
            ),

            loader.ConfigValue(
                "show_heroku",
                True,
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "switchInfo",
                False,
                "Switch info to mode photo",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "imgSettings",
                ["Лапокапканот", 30, '#000', '0|0', "mm", 0, '#000'],
                "Image settings\n1. Дополнительный ник (если прежний ник не отображается)\n2. Размер шрифта\n3. Цвет шрифта в HEX формате '#000'\n4. Координаты текста '100|100', по умолчания в центре фотографии\n5. Якорь текста -> https://pillow.readthedocs.io/en/stable/_images/anchor_horizontal.svg\n6. Размер обводки, по умолчанию 0\n7. Цвет обводки в HEX формате '#000'",
                validator=loader.validators.Series(
                    fixed_len=7,
                ),
            ),
        )

    def remove_emoji_and_html(self, text: str) -> str:
        reg = r'<[^<]+?>'
        text = f"{re.sub(reg, '', text)}"
        allchars = [str for str in text]
        emoji_list = [c for c in allchars if c in emoji.EMOJI_DATA]
        clean_text = ''.join([str for str in text if not any(i in str for i in emoji_list)])
        return clean_text
    
    def imgurpidor(self, url: str) -> str:
        page = requests.get(url, stream=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
        soup = BeautifulSoup(page.text, 'html.parser')
        metatag = soup.find("meta", property="og:image")
        return metatag['content']

    def _render_info(self) -> str:
        try:
            repo = git.Repo(search_parent_directories=True)
            diff = repo.git.log([f"HEAD..origin/{version.branch}", "--oneline"])
            upd = (
                self.strings("update_required") if diff else self.strings("up-to-date")
            )
        except Exception:
            upd = ""

        me = self.config['imgSettings'][0] if (self.config['imgSettings'][0] != "Лапокапканот") and self.config['switchInfo'] else '<b><a href="tg://user?id={}">{}</a></b>'.format(
            self._client.hikka_me.id,
            utils.escape_html(get_display_name(self._client.hikka_me)),
        )
        build = utils.get_commit_url()
        _version = f'<i>{".".join(list(map(str, list(version.__version__))))}</i>'
        prefix = f"«<code>{utils.escape_html(self.get_prefix())}</code>»"

        platform = utils.get_named_platform()

        for emoji, icon in [
            ("🍊", "<emoji document_id=5449599833973203438>🧡</emoji>"),
            ("🍇", "<emoji document_id=5449468596952507859>💜</emoji>"),
            ("😶‍🌫️", "<emoji document_id=5370547013815376328>😶‍🌫️</emoji>"),
            ("❓", "<emoji document_id=5407025283456835913>📱</emoji>"),
            ("🍀", "<emoji document_id=5395325195542078574>🍀</emoji>"),
            ("🦾", "<emoji document_id=5386766919154016047>🦾</emoji>"),
            ("🚂", "<emoji document_id=5359595190807962128>🚂</emoji>"),
            ("🐳", "<emoji document_id=5431815452437257407>🐳</emoji>"),
            ("🕶", "<emoji document_id=5407025283456835913>📱</emoji>"),
            ("🐈‍⬛", "<emoji document_id=6334750507294262724>🐈‍⬛</emoji>"),
            ("✌️", "<emoji document_id=5469986291380657759>✌️</emoji>"),
            ("💎", "<emoji document_id=5471952986970267163>💎</emoji>"),
            ("🛡", "<emoji document_id=5282731554135615450>🌩</emoji>"),
            ("💘", "<emoji document_id=5452140079495518256>💘</emoji>"),
            ("🌼", "<emoji document_id=5224219153077914783>❤️</emoji>"),
            ("🎡", "<emoji document_id=5226711870492126219>🎡</emoji>"),
            ("🐧", "<emoji document_id=5361541227604878624>🐧</emoji>")
        ]:
            platform = platform.replace(emoji, icon)
        return (
            (
                "<b>🪐 Heroku</b>\n"
                if self.config["show_heroku"]
                else ""
            )
            + self.config["custom_message"].format(
                me=me,
                version=_version,
                build=build,
                prefix=prefix,
                platform=platform,
                upd=upd,
                uptime=utils.formatted_uptime(),
                cpu_usage=utils.get_cpu_usage(),
                ram_usage=f"{utils.get_ram_usage()} MB",
                branch=version.branch,
                hostname=lib_platform.node(),
                user=getpass.getuser(),
            )
            if self.config["custom_message"]
            else (
                f'<b>{{}}</b>\n\n<b>{{}} {self.strings("owner")}:</b> {me}\n\n<b>{{}}'
                f' {self.strings("version")}:</b> {_version} {build}\n<b>{{}}'
                f' {self.strings("branch")}:'
                f"</b> <code>{version.branch}</code>\n{upd}\n\n<b>{{}}"
                f' {self.strings("prefix")}:</b> {prefix}\n<b>{{}}'
                f' {self.strings("uptime")}:'
                f"</b> {utils.formatted_uptime()}\n\n<b>{{}}"
                f' {self.strings("cpu_usage")}:'
                f"</b> <i>~{utils.get_cpu_usage()} %</i>\n<b>{{}}"
                f' {self.strings("ram_usage")}:'
                f"</b> <i>~{utils.get_ram_usage()} MB</i>\n<b>{{}}</b>"
            ).format(
                (
                    utils.get_platform_emoji()
                    if self._client.hikka_me.premium and self.config["show_heroku"]
                    else ""
                ),
                "<emoji document_id=5373141891321699086>😎</emoji>",
                "<emoji document_id=5469741319330996757>💫</emoji>",
                "<emoji document_id=5449918202718985124>🌳</emoji>",
                "<emoji document_id=5472111548572900003>⌨️</emoji>",
                "<emoji document_id=5451646226975955576>⌛️</emoji>",
                "<emoji document_id=5431449001532594346>⚡️</emoji>",
                "<emoji document_id=5359785904535774578>💼</emoji>",
                platform,
            )
        )

    async def upload_pp_to_oxo(self, photo):
        save_path = "profile_photo.jpg"
        await self._client.download_media(photo, file=save_path)

        try:
            with open(save_path, 'rb') as file:
                oxo = await utils.run_sync(
                    requests.post,
                    "https://0x0.st",
                    files={"file": file},
                    data={"secret": True},
                )

            if oxo.status_code == 200:
                return oxo.text.strip()
            else:
                return "https://imgur.com/a/7LBPJiq.png"

        except Exception:
            return "https://imgur.com/H56KRbM"

        finally:
            if os.path.exists(save_path):
                os.remove(save_path)

    async def get_pp_for_banner(self):
        photos = await self._client.get_profile_photos('me')
        if photos:
            return await self.upload_pp_to_oxo(photos[0])
        return "https://imgur.com/a/7LBPJiq.png"
    
    def _get_info_photo(self) -> Optional[Path]:
        imgform = self.config['bannerUrl'].split('.')[-1]
        imgset = self.config['imgSettings']
        if imgform in ['jpg', 'jpeg', 'png', 'bmp', 'webp']:
            response = requests.get(self.config['bannerUrl'] if not self.config['bannerUrl'].startswith('https://imgur') else self.imgurpidor(self.config['bannerUrl']), stream=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
            img = Image.open(BytesIO(response.content))
            font = ImageFont.truetype(
                glob.glob(f'{os.getcwd()}/assets/font.*')[0], 
                size=int(imgset[1]), 
                encoding='unic'
            )
            w, h = img.size
            draw = ImageDraw.Draw(img)
            draw.text(
                (int(w/2), int(h/2)) if imgset[3] == '0|0' else tuple([int(i) for i in imgset[3].split('|')]),
                f"{self.remove_emoji_and_html(self._render_info())}", 
                anchor=imgset[4],
                font=font,
                fill=imgset[2] if imgset[2].startswith('#') else '#000',
                stroke_width=int(imgset[5]),
                stroke_fill=imgset[6] if imgset[6].startswith('#') else '#000',
                embedded_color=True
            )
            path = f'{os.getcwd()}/assets/imginfo.{imgform}'
            img.save(path)
            return Path(path).absolute()
        return None
    
    @loader.command()
    async def insfont(self, message: Message):
        "<Url|Reply to font> - Install font"
        if message.is_reply:
            reply = await message.get_reply_message()
            fontform = reply.document.mime_type.split("/")[1]
            if not fontform in ['ttf', 'otf']:
                await utils.answer(
                    message,
                    '<b>Incorrect font format</b>\n<blockquote>Поддерживаемые форматы -> otf, ttf</blockquote>'
                )
                return
            origpath = glob.glob(f'{os.getcwd()}/assets/font.*')[0]
            ptf = f'{os.getcwd()}/font.{fontform}'
            os.rename(origpath, ptf)
            photo = await reply.download_media(origpath)
            if photo is None:
                os.rename(ptf, origpath)
                await utils.answer(
                    message,
                    'Reply to font!'
                )
                return
            os.remove(ptf)
        elif utils.check_url(utils.get_args_raw(message)):
            fontform = utils.get_args_raw(message).split('.')[-1]
            if not fontform in ['ttf', 'otf']:
                await utils.answer(
                    message,
                    '<b>Incorrect font format</b>\n<blockquote>Поддерживаемые форматы -> otf, ttf</blockquote>'
                )
                return
            response = requests.get(utils.get_args_raw(message), stream=True)
            os.remove(glob.glob(f'{os.getcwd()}/assets/font.*')[0])
            with open(f'{os.getcwd()}/assets/font.{fontform}', 'wb') as file:
                file.write(response.content)
        else:
            await utils.answer(
                message,
                '<b>Reply to font or </b>'
            )
        await utils.answer(
            message,
            '<b>Font installed</b><emoji document_id=5436040291507247633>🎉</emoji>\nТеперь вы с удовольствием можете пользоваться им'
        )

    @loader.command()
    async def infocmd(self, message: Message):
        if self.config.get('pp_to_banner', True):
            print(self.config['bannerUrl'])
            try:
                new_bannerUrl = await self.get_pp_for_banner()
                if new_bannerUrl:
                    self.config['bannerUrl'] = new_bannerUrl
                    await self._db.set("Config", "bannerUrl", new_bannerUrl)
            except Exception:
                pass
        if self.config['switchInfo']:
            if self._get_info_photo() is None:
                await utils.answer(
                    message, 
                    '<b>Incorrect image format</b>\n<blockquote>Поддерживаемые форматы -> jpg, jpeg, png, bmp, webp</blockquote>'
                )
                return
            await utils.answer_file(
                message,
                f'{utils.os.getcwd()}/assets/imginfo.{self.config["bannerUrl"].split(".")[-1]}'
            )
        else:
            await utils.answer_file(
                message,
                self.config["bannerUrl"],
                self._render_info(False),
            )

    @loader.command()
    async def herokuinfo(self, message: Message):
        await utils.answer(message, self.strings("desc"))

    @loader.command()
    async def setinfo(self, message: Message):
        if not (args := utils.get_args_html(message)):
            return await utils.answer(message, self.strings("setinfo_no_args"))

        self.config["custom_message"] = args
        await utils.answer(message, self.strings("setinfo_success"))

