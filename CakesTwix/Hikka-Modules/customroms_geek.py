"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix                                                       
    This program is free software; you can redistribute it and/or modify 

"""

__version__ = (1, 4, 1)

# requires: requests bs4 lxml
# scope: inline
# scope: geektg_only
# scope: geektg_min 3.1.15
# meta pic: https://styles.redditmedia.com/t5_3htpk/styles/communityIcon_vlbulj1gn8l11.png
# meta developer: @cakestwix_mods

import asyncio
import logging

import aiohttp
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.markdown import hlink
from bs4 import BeautifulSoup
from requests import get

from .. import loader, utils
from ..inline import GeekInlineQuery, rand

logger = logging.getLogger(__name__)


@loader.unrestricted
@loader.ratelimit
@loader.tds
class CustomRomsMod(loader.Module):
    """Miscellaneous stuff for custom ROMs"""

    strings = {
        "name": "InlineROMs",
        "download": "⬇️ <b>Download</b> :",
        "no_device": "<b>No device.</b>",
        "no_device_info": "ℹ Please check the correct codename or availability of the site",
        "no_codename": "<b>Pls codename((</b>",
        "write_codename": "Write the code name of your device",
        "latest_releases": "ℹ Latest {} releases",
        "latest_releases_no_format": "ℹ Latest ROM releases",
        "latest_releases_device": "ℹ Latest {} {} releases for {}",
        "gapps_version": "GApps version",
        "vanilla_version": "Vanilla version",
        "general_info": "General info about {} builds",
        "general_info_description": "ℹ Maintainer, latest version, etc",
        "not_updating": "❌ : There will be no updates at this time",
        "updated": "✅ : Updated",
        "magisk_latest": "𝗟𝗮𝘁𝗲𝘀𝘁 𝗠𝗮𝗴𝗶𝘀𝗸 𝗥𝗲𝗹𝗲𝗮𝘀𝗲𝘀:",
        "app_by": "👤 by {}",
        "Stable": "⦁ 𝗦𝘁𝗮𝗯𝗹𝗲",
        "Beta": "⦁ 𝗕𝗲𝘁𝗮",
        "Canary": "⦁ 𝗖𝗮𝗻𝗮𝗿𝘆",
        "md5": "<b>MD5: </b>",
        "count": "<b>Downloads count: </b>",
        "customAvbSupported": "<b>Custom Avb Supported:</b> ",
    }

    strings_ru = {
        "download": "⬇️ <b>Скачать</b> :",
        "no_device": "<b>Нет устройства.</b>",
        "no_device_info": "ℹ Пожалуйста, проверьте правильное кодовое имя или доступность сайта",
        "no_codename": "<b>Пжл коднейм((</b>",
        "write_codename": "Напишите кодовое имя вашего устройства",
        "latest_releases": "ℹ Последние {} релизы",
        "latest_releases_no_format": "ℹ Последние релизы ПЗУ",
        "latest_releases_device": "ℹ Последние релизы {} {} для {}",
        "gapps_version": "GApps version",
        "vanilla_version": "Ванила",
        "general_info": "Общая информация о сборках {}",
        "general_info_description": "ℹ Сопровождающий, последняя версия и т. д.",
        "not_updating": "❌ : На данный момент обновлений не будет",
        "updated": "✅ : Обновлено",
        "magisk_latest": "<b>Последние релизы Magisk</b>:",
        "app_by": "👤 от {}",
        "Stable": "⦁ <b>Cтабильный</b>",
        "Beta": "⦁ <b>Бета</b>",
        "Canary": "⦁ <b>Канарейка</b>",
        "md5": "<b>MD5: </b>",
        "count": "<b>Количество загрузок: </b>",
        "customAvbSupported": "<b>Поддерживается пользовательский Avb:</b> ",
    }

    magisk_dict = {
        "topjohnwu": [
            {
                "Stable": "master/stable.json",
                "Beta": "master/stable.json",
                "Canary": "master/stable.json",
            },
            "https://raw.githubusercontent.com/topjohnwu/magisk-files/",
        ],
        "vvb2060": [
            {"Stable": "master/lite.json", "Canary": "alpha/alpha.json"},
            "https://raw.githubusercontent.com/vvb2060/magisk_files/",
        ],
        "TheHitMan7": [
            {"Stable": "stable.json", "Beta": "beta.json", "Canary": "canary.json"},
            "https://raw.githubusercontent.com/TheHitMan7/Magisk-Files/master/configs/",
        ],
    }

    twrp_api = "https://dl.twrp.me/"
    no_codename = [
        InlineQueryResultArticle(
            id=rand(20),
            title=strings["write_codename"],
            description=strings["latest_releases_no_format"],
            input_message_content=InputTextMessageContent(
                strings["no_codename"], "HTML", disable_web_page_preview=True
            ),
            thumb_url="https://img.icons8.com/android/128/26e07f/android.png",
            thumb_width=128,
            thumb_height=128,
        )
    ]
    # ROMs
    @loader.unrestricted
    @loader.ratelimit
    async def sakuracmd(self, message):
        """Project Sakura"""

        if args := utils.get_args(message):
            device = args[0].lower()
            data = get(
                "https://raw.githubusercontent.com/ProjectSakura/OTA/11/devices.json"
            ).json()
            for item in data:
                if item["codename"] == device:
                    releases = f"Latest Project Sakura for {item['name']} ({item['codename']}) \n"
                    releases += f"👤 by {item['maintainer_name']} \n"
                    releases += f"{self.strings['download']} (https://projectsakura.xyz/download/#/{item['codename']}) \n"
                    await utils.answer(message, releases)
                    return
            await utils.answer(message, f"{self.strings['no_device']}")
        else:
            await utils.answer(message, f"{self.strings['no_codename']}")
        await asyncio.sleep(5)
        await message.delete()

    @loader.unrestricted
    @loader.ratelimit
    async def dotoscmd(self, message):
        """DotOS"""
        if args := utils.get_args(message):
            device = args[0].lower()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.droidontime.com/api/ota/{device}"
                ) as get:
                    if get.ok:
                        data = await get.json()
                    else:
                        await utils.answer(message, f"{self.strings['no_device']}")
                        await asyncio.sleep(5)
                        await message.delete()
                    await session.close()

            releases = f"<b>Latest DotOS for {data['brandName']} {data['deviceName']}</b> (<code>{data['codename']}</code>) \n"
            releases += f"👤 : {data['maintainerInfo']['name']} \n"
            releases += f"🆚 : {data['latestVersion']} \n"
            releases += f"{self.strings['download']} "
            releases += f"<a href={data['releases'][0]['url']}>{data['releases'][1]['type'].capitalize()}<a/>"
            releases += f" / <a href={data['releases'][1]['url']}>{data['releases'][1]['type'].capitalize()}<a/>"
            await utils.answer(message, releases)
        else:
            await utils.answer(message, f"{self.strings['no_codename']}")
            await asyncio.sleep(5)
            await message.delete()

    # Recovery
    @loader.unrestricted
    @loader.ratelimit
    async def twrpcmd(self, message):
        """TWRP Devices"""
        if args := utils.get_args(message):
            device = args[0].lower()
            url = get(f"{self.twrp_api}{device}/")

            if url.status_code == 404:
                reply = f"`Couldn't find twrp downloads for {device}!`\n"
                await utils.answer(message, reply)
                await asyncio.sleep(5)
                await message.delete()
                return

            page = BeautifulSoup(url.content, "lxml")
            download = page.find("table").find_all("tr")
            reply = f"『 Team Win Recovery Project for {device}: 』\n"
            for item in download:
                dl_link = f"{self.twrp_api}{item.find('a')['href']}"
                dl_file = item.find("td").text
                size = item.find("span", {"class": "filesize"}).text
                reply += f"⦁ <a href={dl_link}>{dl_file}</a> - <tt>{size}</tt>\n"

                await utils.answer(message, reply)

    @loader.unrestricted
    @loader.ratelimit
    async def shrpcmd(self, message):
        """SHRP Devices"""

        if args := utils.get_args(message):
            device = args[0].lower()
            data = get(
                "https://raw.githubusercontent.com/SHRP-Devices/device_data/master/deviceData.json"
            ).json()
            for item in data[:-1]:
                if item["codeName"] == device:
                    releases = f"『 SkyHawk Recovery Project for {item['model']} ({device}): 』\n"
                    releases += f"👤 <b>by<b> {item['maintainer']} \n"
                    releases += f"ℹ️ <b>Version<b> : {item['currentVersion']} \n"
                    releases += f"{self.strings['download']} : <a href={item['latestBuild']}>SourceForge</a> \n"
                    await utils.answer(message, releases)
                    return
            await utils.answer(message, f"{self.strings['no_device']}")
            await asyncio.sleep(5)
            await message.delete()

    @loader.unrestricted
    @loader.ratelimit
    async def pbrpcmd(self, message):
        """PBRP Devices"""
        if args := utils.get_args(message):
            device = args[0].lower()
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://pitchblackrecovery.com/{device}/"
                ) as get:
                    pbrp_page = await get.text()
                    await session.close()

            page = BeautifulSoup(pbrp_page, "lxml")
            status_error = page.find("h1", class_="error-code")
            if status_error is not None:
                return  # No device

            main_info = page.find_all(
                "h3", class_="elementor-heading-title elementor-size-default"
            )
            download_info = page.find(
                "section",
                class_="has_eae_slider elementor-section elementor-inner-section elementor-element elementor-element-714ebe14 elementor-section-boxed elementor-section-height-default elementor-section-height-default",
            )

            version = main_info[0].text
            date = main_info[2].text
            status = main_info[4].text
            maintainer = main_info[6].text
            file_size = download_info.find_all(
                "div", class_="elementor-text-editor elementor-clearfix"
            )[1].text[10:]
            md5 = download_info.find_all(
                "div", class_="elementor-text-editor elementor-clearfix"
            )[2].text[4:]
            sourceforge = download_info.find_all(
                "a", class_="elementor-button-link elementor-button elementor-size-md"
            )[0]["href"]
            github = download_info.find_all(
                "a", class_="elementor-button-link elementor-button elementor-size-md"
            )[1]["href"]

            releases = f"『 Pitch Black Recovery Project for ({device}): 』\n"
            releases += f"👤 <b>by</b> {maintainer} \n"
            releases += f"ℹ️ <b>Status</b> : {status} \n"
            releases += f"ℹ️ <b>Version</b> : {version} \n"
            releases += f"ℹ️ <b>Date</b> : {date} \n"
            releases += f"ℹ️ <b>MD5</b> : {md5} \n"
            releases += f"ℹ️ <b>Size</b> : {file_size} \n"
            releases += f"{self.strings['download']} : <a href={sourceforge}>SourceForge</a> | <a href={github}>GitHub</a>\n"

            await utils.answer(message, releases)

    # Other
    @loader.unrestricted
    @loader.ratelimit
    async def magiskcmd(self, message):
        """Magisk by topjohnwu"""
        magisk_repo = "https://raw.githubusercontent.com/topjohnwu/magisk-files/"
        magisk_dict = {
            "⦁ 𝗦𝘁𝗮𝗯𝗹𝗲": magisk_repo + "master/stable.json",
            "⦁ 𝗕𝗲𝘁𝗮": magisk_repo + "master/beta.json",
            "⦁ 𝗖𝗮𝗻𝗮𝗿𝘆": magisk_repo + "master/canary.json",
        }
        releases = f"<code><i>{self.strings['magisk_latest']}</i></code>\n\n"
        for name, release_url in magisk_dict.items():
            data = get(release_url).json()

            releases += f'{name}: <a href={data["magisk"]["link"]}>APK v{data["magisk"]["version"]}</a> | <a href={data["magisk"]["note"]}>Changelog</a>\n'
        await utils.answer(message, releases)

    # Inline commands
    async def opengapps_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        OpenGApps (Inline)
        @allow: all
        """
        text = query.args

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.opengapps.org/list") as get:
                opengapps_list = await get.json()
                await session.close()

        arch_dict = {}
        version_text = "<b>Avilable versions</b> :\n"
        for arch in opengapps_list["archs"]:
            apis_list = [str(apis) for apis in opengapps_list["archs"][arch]["apis"]]
            arch_dict[arch] = apis_list
            version_text += f"<b>{arch}</b> : {', '.join(apis_list)}\n"

        if not text:
            await query.answer(
                [
                    InlineQueryResultArticle(
                        id=rand(20),
                        title="Select android version for your device",
                        description="ℹ For example : 10.0. Click for more versions",
                        input_message_content=InputTextMessageContent(
                            version_text, "HTML", disable_web_page_preview=True
                        ),
                        thumb_url="https://img.icons8.com/android/128/26e07f/android.png",
                        thumb_width=128,
                        thumb_height=128,
                    )
                ],
                cache_time=0,
            )
            return

        if len(text.split()) == 1:

            archs_inline = []
            archs_photo = {
                "arm": "https://img.icons8.com/android/128/26e07f/32bit.png",
                "arm64": "https://img.icons8.com/android/128/26e07f/64bit.png",
                "x86": "https://img.icons8.com/android/128/26e07f/x86.png",
                "x86_64": "https://img.icons8.com/android/128/26e07f/x64.png",
            }

            for arch in opengapps_list["archs"]:  # arm arm64 x86 etc
                if text in arch_dict[arch]:
                    markup = InlineKeyboardMarkup(row_width=3)
                    for variant in opengapps_list["archs"][arch]["apis"][text][
                        "variants"
                    ]:  # pico nano etc
                        markup.insert(
                            InlineKeyboardButton(variant["name"], url=variant["zip"])
                        )

                    archs_inline.append(
                        InlineQueryResultArticle(
                            id=rand(20),
                            title=arch,
                            description="ℹ Select arch for your device",
                            input_message_content=InputTextMessageContent(
                                f"OpenGApps for Android {text} {arch}",
                                "HTML",
                                disable_web_page_preview=True,
                            ),
                            thumb_url=archs_photo[arch],
                            thumb_width=128,
                            thumb_height=128,
                            reply_markup=markup,
                        )
                    )
                    markup = None
            await query.answer(archs_inline, cache_time=0)

    # https://img.icons8.com/fluency/48/26e07f/android-os.png
    async def aex_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        AOSP Extended (Inline)
        @allow: all
        """
        device_codename = query.args

        if not device_codename:
            await query.answer(self.no_codename, cache_time=0)
            return

        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.aospextended.com/devices/") as get:
                devices_json = await get.json()

            for device in devices_json:
                if device["codename"] == device_codename:
                    inline_query = []
                    for version in device["supported_versions"]:
                        releases = f"Latest AOSP Extended for {device['brand']} {device['name']} ({device['codename']}) \n"
                        async with session.get(
                            f"https://api.aospextended.com/builds/{device_codename}/{version['version_code']}"
                        ) as get:
                            version_json = await get.json()
                        if "error" not in version_json:

                            releases += f"{self.strings['app_by'].format(version['maintainer_name'])} \n"
                            releases += f"💬 {hlink('Telegram Chat', version['tg_link'])} | {hlink('XDA', version['xda_thread'])} | {hlink('XDA Maintainer', version['maintainer_url'])} \n"
                            releases += f"{self.strings['download']} {hlink(version_json[0]['file_name'], version_json[0]['download_link'])} \n\n"

                            releases += (
                                f"{self.strings['md5']}{version_json[0]['md5']} \n"
                            )
                            releases += f"{self.strings['count']}{version_json[0]['downloads_count']} \n"
                            releases += f"{self.strings['customAvbSupported']} {'Yes' if version_json[0]['isCustomAvbSupported'] else 'No'}"

                            inline_query.append(
                                InlineQueryResultArticle(
                                    id=rand(50),
                                    title=version["version_name"],
                                    description=self.strings["app_by"].format(
                                        version["maintainer_name"]
                                    ),
                                    input_message_content=InputTextMessageContent(
                                        releases,
                                        "HTML",
                                        disable_web_page_preview=True,
                                    ),
                                )
                            )
                    await session.close()
                    await query.answer(inline_query, cache_time=0)

    async def dotos_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        DotOS (Inline)
        @allow: all
        """
        text = query.args

        if not text:
            await query.answer(self.no_codename, cache_time=0)
            return

        if len(text.split()) == 1:
            device = text
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.droidontime.com/api/ota/{device}"
                ) as get:
                    if get.ok:
                        data = await get.json()
                    else:
                        await query.answer(
                            [
                                InlineQueryResultArticle(
                                    id=rand(20),
                                    title=self.strings["no_device"],
                                    description=self.strings["no_device_info"],
                                    input_message_content=InputTextMessageContent(
                                        self.strings["no_device_info"],
                                        "HTML",
                                        disable_web_page_preview=True,
                                    ),
                                    thumb_url="https://img.icons8.com/android/128/fa314a/cancel-2.png",
                                    thumb_width=128,
                                    thumb_height=128,
                                )
                            ],
                            cache_time=0,
                        )
                        await session.close()
                        return
                    await session.close()

            vanilla_markup = InlineKeyboardMarkup(row_width=3)
            gapps_markup = InlineKeyboardMarkup(row_width=3)
            for releases in data["releases"]:
                if releases["type"] == "vanilla":
                    vanilla_markup.insert(
                        InlineKeyboardButton(releases["version"], url=releases["url"])
                    )
                else:
                    gapps_markup.insert(
                        InlineKeyboardButton(releases["version"], url=releases["url"])
                    )

            about_info = f"<b>DotOS for {data['brandName']} {data['deviceName']}</b> (<code>{data['codename']}</code>) \n"
            about_info += f"👤 : {hlink(data['maintainerInfo']['name'], data['maintainerInfo']['profileURL'])} \n"
            about_info += f"🆚 : {data['latestVersion']} \n"
            about_info += (
                self.strings["not_updating"]
                if data["discontinued"]
                else self.strings["updated"]
            )
            about_info += f"\n🔗 : {hlink('XDA',data['links']['xda'])} / {hlink('Telegram',data['links']['telegram'])} \n"

            await query.answer(  # About, Vanilla, Gapps
                [
                    InlineQueryResultArticle(
                        id=rand(20),
                        title=self.strings["general_info"].format("DotOS"),
                        description=self.strings["general_info_description"],
                        input_message_content=InputTextMessageContent(
                            about_info,
                            "HTML",
                            disable_web_page_preview=True,
                        ),
                        thumb_url="https://img.icons8.com/android/128/26e07f/info.png",
                        thumb_width=128,
                        thumb_height=128,
                    ),
                    InlineQueryResultArticle(
                        id=rand(20),
                        title=self.strings["vanilla_version"],
                        description=self.strings["latest_releases"].format("DotOS"),
                        input_message_content=InputTextMessageContent(
                            self.strings["latest_releases_device"].format(
                                "DotOS", "Vanilla", device
                            ),
                            "HTML",
                            disable_web_page_preview=True,
                        ),
                        thumb_url="https://img.icons8.com/android/128/26e07f/forward.png",
                        thumb_width=128,
                        thumb_height=128,
                        reply_markup=vanilla_markup,
                    ),
                    InlineQueryResultArticle(
                        id=rand(20),
                        title=self.strings["gapps_version"],
                        description=self.strings["latest_releases"].format("DotOS"),
                        input_message_content=InputTextMessageContent(
                            self.strings["latest_releases_device"].format(
                                "DotOS", "GApps", device
                            ),
                            "HTML",
                            disable_web_page_preview=True,
                        ),
                        thumb_url="https://img.icons8.com/android/128/26e07f/forward.png",
                        thumb_width=128,
                        thumb_height=128,
                        reply_markup=gapps_markup,
                    ),
                ],
                cache_time=0,
            )

    async def magisk_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        Magisk (Inline)
        @allow: all
        """
        inline_query = []
        latest_releases = f"<code><i>{self.strings['magisk_latest']}</i></code>\n\n"

        for magisk_author in self.magisk_dict:  # topjohnwu vvb2060
            text_type = ""
            for magisk_type in self.magisk_dict[magisk_author][
                0
            ]:  # List(Stable, Beta, etc) by author

                base_url = self.magisk_dict[magisk_author][1]
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        base_url + self.magisk_dict[magisk_author][0][magisk_type]
                    ) as get:
                        data = await get.json(content_type=None)

                text_type += f'{self.strings[magisk_type]}: {hlink("APK v" + data["magisk"]["version"], data["magisk"]["link"])} | {hlink("Changelog", data["magisk"]["note"])} \n'
            text_type += f'\n{self.strings["app_by"].format(magisk_author)}'
            inline_query.append(
                InlineQueryResultArticle(
                    id=rand(20),
                    title=self.strings["magisk_latest"],
                    description=self.strings["app_by"].format(magisk_author),
                    input_message_content=InputTextMessageContent(
                        latest_releases + text_type,
                        "HTML",
                        disable_web_page_preview=True,
                    ),
                    thumb_url="https://upload.wikimedia.org/wikipedia/commons/b/b8/Magisk_Logo.png",
                    thumb_width=128,
                    thumb_height=128,
                )
            )

        await query.answer(inline_query, cache_time=0)
