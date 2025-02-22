# meta pic: https://static.whypodg.me/mods!animetools.png
# meta banner: https://mods.whypodg.me/badges/animetools.jpg
# meta developer: @idiotcoders
# scope: hikka_only
# scope: hikka_min 1.2.10

from deep_translator import GoogleTranslator
from typing import Optional

import mimetypes
import os
import requests
from io import BytesIO

from telethon.tl.types import Message

from .. import loader, utils



@loader.tds
class animetoolsMod(loader.Module):
    """AnimeTools"""

    strings = {
        "name": "AnimeTools",
        "no_results": "<emoji document_id=5210952531676504517>❌</emoji> No results found!",
        "character": "\n<emoji document_id=5370765563226236970>👤</emoji> <b>Character:</b> <i>{}</i>",
        "quote": "\n<emoji document_id=5465300082628763143>💬</emoji> <b>Quote:</b> <i>{}</i>",
        "anime": "\n<emoji document_id=6334664298710697689>🍿</emoji> <b>Anime:</b> <i>{}</i>",
        "enter_name": "<emoji document_id=5467928559664242360>❗</emoji> <b>You must specify a character name!</b>",
        "description": "\n<emoji document_id=5818865088970362886>ℹ️</emoji> <b>Description:</b> <i>{}</i>",
        "genres": "\n<emoji document_id=5359441070201513074>🎭 </emoji> <b>Genres:</b>  <i>{}</i>",
        "reply": "<emoji document_id=5215273032553078755>❌</emoji> You must reply to a some media or add it on your message!",
        "loading": "<emoji document_id=5213452215527677338>⏳</emoji> Loading...",
        "findanime": "<emoji document_id=5215644719022874555>ℹ️</emoji> <b>Anime:</b> <code>{}</code>\n<emoji document_id=6032602169360780718>🤨</emoji> <b>Similar to:</b> <code>{}%</code>\n<emoji document_id=6334664298710697689>🍿</emoji> <b>Episode:</b> <code>{}</code>",
        "error": "<emoji document_id=5215273032553078755>❎</emoji> An error has occurred, please try again",
        "no_desc": "❌ No description!",
        "no_photo": "<emoji document_id=5215273032553078755>❎</emoji> Need a picture"
    }

    strings_ru = {
        "name": "AnimeTools",
        "no_results": "<emoji document_id=5210952531676504517>❌</emoji> Результатов не найдено!",
        "character": "\n<emoji document_id=5370765563226236970>👤</emoji> <b>Персонаж:</b> <i>{}</i>",
        "quote": "\n<emoji document_id=5465300082628763143>💬</emoji> <b>Цитата:</b> <i>{}</i>",
        "anime": "\n<emoji document_id=6334664298710697689>🍿</emoji> <b>Аниме:</b> <i>{}</i>",
        "description": "\n<emoji document_id=5818865088970362886>ℹ️</emoji> <b>Описание:</b>  <i>{}</i>",
        "genres": "\n<emoji document_id=5359441070201513074>🎭 </emoji> <b>Жанры:</b>  <i>{}</i>",
        "enter_name": "<emoji document_id=5467928559664242360>❗</emoji> <b>Вы должны указать имя персонажа!</b>",
        "loading": "<emoji document_id=5213452215527677338>⏳</emoji> Загрузка ...",
        "error": "<emoji document_id=5215273032553078755>❎</emoji> Произошла ошибка, попробуйте снова",
        "reply": "<emoji document_id=5215273032553078755>❌</emoji> Нужно ответить на фото/видео или прикрепить его!",
        "findanime": "<emoji document_id=5215644719022874555>ℹ️</emoji> <b>Аниме:</b> <code>{}</code>\n<emoji document_id=6032602169360780718>🤨</emoji> <b>Похоже на:</b> <code>{}%</code>\n<emoji document_id=6334664298710697689>🍿</emoji> <b>Эпизод:</b> <code>{}</code>",
        "_cmd_doc_findanime": "Ищет по картинке что за аниме",
        "_cmd_doc_animequote": "Отправляет аниме цитатки",
        "_cmd_doc_animechar": "Отправляет аниме цитатки определенного персонажа",
        "_cmd_doc_animeavailable": "Отправляет список всех доступных аниме на данный момент",
        "_cmd_doc_randomanime": "Отправляет случайное аниме",
        "_cmd_doc_characteravailable": "Отправляет список всех доступных персонажей на данный момент",
        "no_desc": "❌ Без описания!"    
    }


    @loader.command(alias="fa")
    async def findanimecmd(self, message):
        """Search by picture for what anime"""
        loading = await utils.answer(message, self.strings["loading"])
        reply_msg = await message.get_reply_message()
        msg = reply_msg or message
        media = msg.media
        if media:
            if msg.photo:
                filename = "photo.png"
            elif msg.video:
                filename = "video.mp4"
            elif msg.gif:
                filename = "gif.gif"
            else:
                filename = "photo.png"

            filename = await self.client.download_media(media, file=filename)
            typem, encoding = mimetypes.guess_type(filename)
            r = requests.post(
                "https://api.trace.moe/search",
                data=open(filename, "rb"),
                headers={"Content-Type": typem}
            ).json()

            res = r['result'][0]
            episode = res['episode']
            video = res['video']
            name = res['filename'].split('.')[0]
            simil = res['similarity']
            await loading.delete()
            await utils.answer_file(
                message,
                file=video,
                caption=self.strings["findanime"].format(name, simil*100, episode)
            )
            os.remove(filename)
        else:
            await utils.answer(message, self.strings['reply'])


    @loader.command(alias="aq")
    async def animequotecmd(self, message: Message):
        """Sends anime quotes"""
        args = utils.get_args_raw(message)
        link = "https://animechan.vercel.app/api/random"
        if args:
            link += "/anime?title={args}"
        qdata = (await utils.run_sync(requests.get, link)).json()

        try:
            qdata["quote"] = GoogleTranslator(source="auto", target="ru").translate(qdata["quote"])
        except KeyError:
            qdata = {"quote": "no_results", "character": "no_results", "anime": "no_results"}

        quote, chr, anime = qdata["quote"], qdata["character"], qdata["anime"]

        if not qdata.get("quote") or "no_results" in [qdata.get("quote"), qdata.get("character"), qdata.get("anime")]:
            await utils.answer(message, self.strings["no_results"])
            return

        quote = (
            self.strings['quote'].format(quote) +
            self.strings['character'].format(chr) +
            self.strings['anime'].format(anime)
        )
        await utils.answer(message, quote)


    @loader.command(alias="ac")
    async def animechar(self, message):
        """Sends anime quotes for specific character"""
        character_name = utils.get_args_raw(message)
        if not character_name:
            await utils.answer(message, self.strings['enter_name'])
            return
        link = f"https://animechan.vercel.app/api/random/character?name={character_name}"
        qdata = (await utils.run_sync(requests.get, link)).json()

        try:
            qdata["quote"] = GoogleTranslator(source="auto", target="ru").translate(qdata["quote"])
        except KeyError:
            qdata = {"quote": "no_results", "character": "no_results", "anime": "no_results"}

        quote, chr, anime = qdata["quote"], qdata["character"], qdata["anime"]

        if not qdata.get("quote") or "no_results" in [qdata.get("quote"), qdata.get("character"), qdata.get("anime")]:
            await utils.answer(message, self.strings["no_results"])
            return

        quote = (
            self.strings['quote'].format(quote) +
            self.strings['character'].format(chr) +
            self.strings['anime'].format(anime)
        )
        await utils.answer(message, quote)


    @loader.command(alias="aa")
    async def animeavailable(self, message: Message):
        """Sends a list of available anime"""
        args = utils.get_args_raw(message)
        link = "https://animechan.vercel.app/api/available/anime"
        response = await utils.run_sync(requests.get, link)
        available_anime = response.json()
        if args:
            matching_anime = [anime for anime in available_anime if args.lower() in anime.lower()]
            if matching_anime:
                anime_message = "\n".join(matching_anime)
            else:
                await utils.answer(message, self.strings["no_results"])
                return
        else:
            anime_message = "\n".join(available_anime)
        await utils.answer(message, anime_message)    


    @loader.command(alias="ca")
    async def characteravailable(self, message: Message):
        """Sends a list of available characters"""
        args = utils.get_args_raw(message)
        link = "https://animechan.vercel.app/api/available/character"
        response = await utils.run_sync(requests.get, link)
        available_anime = response.json()
        if args:
            matching_anime = [anime for anime in available_anime if args.lower() in anime.lower()]
            if matching_anime:
                anime_message = "\n".join(matching_anime)
            else:
                await utils.answer(message, self.strings["no_results"])
                return
        else:
            anime_message = "\n".join(available_anime)
        await utils.answer(message, anime_message)


    @loader.command(alias="ra")
    async def randomanime(self, message: Message):
        """Sends a random anime"""
        a = await utils.answer(message, self.strings["loading"])
        try:
            link = "https://anime777.ru/api/rand"
            adata = (await utils.run_sync(requests.get, link)).json()

            anime_kind = adata["material_data"]["anime_kind"]
            if anime_kind == "ova":
                return await self.randomanime(message)

            title = adata["title"]
            genres = ", ".join(adata["material_data"]["anime_genres"])
            description = adata["material_data"]["description"]
            screenshots = adata["material_data"]["screenshots"]

            anime_message = (
                self.strings['anime'].format(title) +
                self.strings['genres'].format(genres) +
                self.strings['description'].format(description)
            )
            await a.delete() 
            await utils.answer_file(message, screenshots[0], anime_message)

        except:
            await utils.answer(message, "error")