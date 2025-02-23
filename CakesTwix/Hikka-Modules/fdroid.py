"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 1, 0)

# meta pic: https://forum.f-droid.org/uploads/default/original/2X/c/cfb2c14973c28415b0e5b5f7adef9c8288cd8609.png
# meta developer: @cakestwix_mods
# scope: hikka_only
# requires: httpx bs4

import logging

import httpx
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.markdown import hlink
from bs4 import BeautifulSoup

from .. import loader, utils
from ..inline.types import InlineQuery

logger = logging.getLogger(__name__)


async def fdroid_search(search_app = "") -> dict:
    fdroid_main = "https://apt.izzysoft.de/fdroid/index.php?repo=main" # FDroid

    async with httpx.AsyncClient() as client:
        html = (await client.post(fdroid_main, data={"limit": 50, "searchterm": search_app, "doFilter": "Go%21"})).content

    soup = BeautifulSoup(html, "html.parser")
    apps = []

    html_apps = soup.find_all("div", class_="approw")

    for app in html_apps:
        buff = {"Name": app.find("span", class_="boldname").get_text()}
        buff["Desc"] = app.find_all("div", class_="appdetailcell")[-2].get_text()
        buff["Icon"] = app.find("img")["src"] if app.find("img")["src"] != "/shared/images/spacer.gif" else "https://f-droid.org/repo/com.termux.tasker/en-US/icon.png"

        buff["Minor-Details"] = app.find_all("span", class_="minor-details")
        buff["Links"] = app.find_all("a", class_="paddedlink")[1:]
        apps.append(buff)

    return apps
    
def StringBuilder(app):
    return f"<code>{app['Name']}</code> {app['Minor-Details'][0].get_text()} ({app['Minor-Details'][1].get_text()})\n\n{app['Desc']}"

class FDroidMod(loader.Module):
    """Search for android apps from FDroid"""

    strings = {
        "name": "FDroid",
        "no_apps": "🚫 Unfortunately, I couldn't find any applications",
    }

    strings_ru = {
        "name": "FDroid",
        "no_apps": "🚫 К сожалению, не нашел приложений",
    }

    async def fdroidcmd(self, message):
        """Find the app in the FDroid catalog"""
        args = utils.get_args_raw(message)
        if apps := await fdroid_search(args):
            markup = [[{"text": app.get_text(), "url": app["href"]} for app in apps[0]["Links"]]]
            if len(apps) != 1:
                markup.append([{"text":"➡️","callback": self.fdroid_pagination__callback, "args": (apps, 0, "+")}])
            await self.inline.form(
                text=StringBuilder(apps[0]),
                message=message,
                # photo=apps[0]["Icon"],
                reply_markup=markup,
            )
        else:
            await utils.answer(message, self.strings["no_apps"])

    @loader.inline_everyone
    async def fdroid_inline_handler(self, query: InlineQuery) -> None:
        """Find the app in the FDroid catalog (Inline)"""
        query_args = query.args

        if apps := await fdroid_search(query_args):
            InlineQueryResult = []
            for app in apps:
                # Generate button
                markup = InlineKeyboardMarkup()
                for link in app["Links"]:
                    markup.insert(InlineKeyboardButton(link.get_text(), link["href"]))

                # Add InlineQueryResultArticle
                InlineQueryResult.append(
                    InlineQueryResultArticle(
                        id=utils.rand(64),
                        title=f'{app["Name"]} ({app["Minor-Details"][1].get_text()})',
                        description=app["Desc"],
                        input_message_content=InputTextMessageContent(
                            StringBuilder(app),
                            "HTML",
                            disable_web_page_preview=True,
                        ),
                        reply_markup=markup,
                        # thumb_url=app["Icon"],
                    )
                )

            await query.answer(InlineQueryResult, cache_time=0)
        else:
            await query.e404()
    
    # Just callbacks

    async def fdroid_pagination__callback(self, call, apps, index, type_button):
        markup = [[{"text": app.get_text(), "url": app["href"]} for app in apps[index]["Links"]],[]]
        if type_button == "+":
            index += 1
            markup[1].append({"text":"⬅️","callback": self.fdroid_pagination__callback, "args": (apps, index, "-")})
            if index != len(apps) - 1:
                markup[1].append({"text":"➡️","callback": self.fdroid_pagination__callback, "args": (apps, index, "+")})
        else:
            index -= 1
            if index != 0:
                markup[1].append({"text":"⬅️","callback": self.fdroid_pagination__callback, "args": (apps, index, "-")})

            markup[1].append({"text":"➡️","callback": self.fdroid_pagination__callback, "args": (apps, index, "+")})
        await call.edit(text=StringBuilder(apps[index]), reply_markup=markup)
