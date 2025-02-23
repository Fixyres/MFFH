"""

    █▀▀ ▄▀█ █▄▀ █▀▀ █▀ ▀█▀ █░█░█ █ ▀▄▀
    █▄▄ █▀█ █░█ ██▄ ▄█ ░█░ ▀▄▀▄▀ █ █░█

    Copyleft 2022 t.me/CakesTwix
    This program is free software; you can redistribute it and/or modify

"""

__version__ = (1, 0, 0)

# meta pic: https://allvpn.ru/assets/upload/t-200x200-7439447981535195421.png
# meta developer: @cakestwix_mods
# requires: httpx bs4
# scope: inline

import logging
import xml.etree.ElementTree as ET
from typing import Union

import httpx
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           InlineQueryResultArticle, InputTextMessageContent)
from bs4 import BeautifulSoup

from .. import loader, utils
from ..inline import GeekInlineQuery, rand

logger = logging.getLogger(__name__)

# From Hikka https://github.com/hikariatama/Hikka/blob/master/hikka/utils.py#L459-L461
def chunks(_list: Union[list, tuple, set], n: int, /) -> list:
    """Split provided `_list` into chunks of `n`"""
    return [_list[i : i + n] for i in range(0, len(_list), n)]

async def search_book(query=None):
    books_list = []
    async with httpx.AsyncClient() as client:
        if query:
            xml_ = (await client.get(f"http://flibusta.is/opds/opensearch?searchTerm={query}&searchType=books&pageNumber=1"))
        else:
            xml_ = await client.get("http://flibusta.is/opds/opensearch?searchType=books&pageNumber=1")

        myroot = ET.fromstring(xml_.text)

        for book in myroot.findall('.//{http://www.w3.org/2005/Atom}entry'):
            books_dict = {"Books": {}, "Name": book.find('./{http://www.w3.org/2005/Atom}title').text, "Author": ""}


            for item in book.findall('./{http://www.w3.org/2005/Atom}author'):
                books_dict["Author"] += item.find('./{http://www.w3.org/2005/Atom}name').text + " "

            # Links and Formats
            for item in book.findall('./{http://www.w3.org/2005/Atom}link'):
                if "application/" in item.attrib["type"] and "related" not in item.attrib["rel"]:
                    books_dict["Books"][item.attrib["type"].split("/")[1].replace("+zip", "").replace("x-mobipocket-ebook", "mobi")] = item.attrib["href"]

                # Read
                if "title" in item.attrib:
                    books_dict["Read"] = [item.attrib["title"], item.attrib["href"]]

            if books_dict["Books"] != {}:
                books_list.append(books_dict)

        return books_list

@loader.tds
class FlibustaMod(loader.Module):
    """Get books from flibusta"""

    strings = {
        "name": "Flibusta",
        "no_args": "🎞 <b>You need to specify book name</b>",
        "no_book": "🎞 <b>No books by your query :(</b>",
    }

    # Just commands

    async def bookcmd(self, message):
        """🔎 Sending the form with the books. Send message with args if you want to find a book by title"""
        # Get args from message
        if args:= utils.get_args_raw(message):
            books = await search_book(args)
        else:
            books = await search_book()

        # No books ((
        if books == []:
            return await utils.answer(message, self.strings["no_book"])

        string = f'📙 <b>{books[0]["Name"]}</b>'
        string += f"\n<b>Author:</b> {books[0]['Author']}"

        # epub pdf fb2 mobi / Read
        reply_keyboard = [[{"text": file_, "url": f"http://flibusta.is{books[0]['Books'][file_]}"} for file_ in books[0]["Books"]], [{"text": "Read", "url": f"http://flibusta.is{books[0]['Read'][1]}"}]]

        btn_buff = [{"text": str(i), "callback": self.change_book__callback, "args": (book, args or None)} for i, book in enumerate(books, start=1)]

        reply_keyboard.extend(iter(chunks(btn_buff, 5)))
        try:
            reply_keyboard.remove([])
        except ValueError:
            pass

        await self.inline.form(
            text=string,
            message=message,
            reply_markup=reply_keyboard,
        )

    # Just callbacks

    async def change_book__callback(self, call, book, search=None):
        books = await search_book(search)

        string = f'📙 <b>{book["Name"]}</b>'
        string += f"\n<b>Author:</b> {book['Author']}"

        # epub pdf fb2 mobi / Read
        reply_keyboard = [[{"text": file_, "url": f"http://flibusta.is{book['Books'][file_]}"} for file_ in book["Books"]], [{"text": "Read", "url": f"http://flibusta.is{book['Read'][1]}"}]]

        btn_buff = [{"text": str(i), "callback": self.change_book__callback, "args": (book, search or None)} for i, book in enumerate(books, start=1)]

        reply_keyboard.extend(iter(chunks(btn_buff, 5)))
        try:
            reply_keyboard.remove([])
        except ValueError:
            pass
        await call.edit(text=string, reply_markup=reply_keyboard)

    # Just Inline

    async def book_inline_handler(self, query: GeekInlineQuery) -> None:
        """
        🔎 Sending the form with the books. Send message with args if you want to find a book by title (Inline)
        """
        if text := query.args:
            books = await search_book(text)
        else:
            books = await search_book()
        
        # No books ((
        if books == []:
            return await query.e404()

        InlineQueryResult = []
        for book in books:
            markup = InlineKeyboardMarkup(row_width=3)
            for file_ in book["Books"]:
                markup.insert(InlineKeyboardButton(file_, f"http://flibusta.is{book['Books'][file_]}"))
            InlineQueryResult.append(
                InlineQueryResultArticle(
                id=utils.rand(50),
                title=book["Name"],
                description=book["Author"],
                input_message_content=InputTextMessageContent(
                    f'📙 <b>{book["Name"]}</b>\n<b>Author:</b> {book["Author"]}',
                    "HTML",
                    disable_web_page_preview=True,
                    ),
                reply_markup=markup,
                )
            )
        
        await query.answer(InlineQueryResult, cache_time=0)


    