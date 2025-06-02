#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
#                              
# meta banner: https://envs.sh/Nma.jpg
# meta developer: @Toxano_Modules
# scope: @Toxano_Modules

import aiohttp
import asyncio
import random
from urllib.parse import urlencode, quote
from hikkatl.types import Message
from .. import loader, utils


@loader.tds
class Rule34Module(loader.Module):
    """Rule34 medie"""
    
    strings = {
        "name": "Rule34",
        "searching": "🔍 <b>Ищу изображения...</b>",
        "no_results": "😔 <b>Ничего не найдено по запросу:</b> <code>{}</code>",
        "error": "❌ <b>Ошибка при выполнении запроса:</b> <code>{}</code>",
        "invalid_args": "❌ <b>Укажите теги для поиска!</b>\n<code>{prefix}r34 <теги></code>",
        "gallery_caption": "🖼 <b>Результат #{}</b>\n📝 <b>Теги:</b> <code>{}</code>\n🔗 <b>ID:</b> <code>{}</code>\n🌐 <b>Источник:</b> <code>{}</code>",
        "random_caption": "🎲 <b>Случайное изображение</b>\n📝 <b>Теги:</b> <code>{}</code>\n🔗 <b>ID:</b> <code>{}</code>\n🌐 <b>Источник:</b> <code>{}</code>",
        "loading": "⏳ <b>Загружаю галерею...</b>",
        "searching_random": "🎲 <b>Ищу случайное изображение...</b>",
    }
    
    strings_en = {
        "searching": "🔍 <b>Searching for images...</b>",
        "no_results": "😔 <b>No results found for:</b> <code>{}</code>",
        "error": "❌ <b>Error occurred:</b> <code>{}</code>",
        "invalid_args": "❌ <b>Please specify tags to search!</b>\n<code>{prefix}r34 <tags></code>",
        "gallery_caption": "🖼 <b>Result #{}</b>\n📝 <b>Tags:</b> <code>{}</code>\n🔗 <b>ID:</b> <code>{}</code>\n🌐 <b>Source:</b> <code>{}</code>",
        "random_caption": "🎲 <b>Random image</b>\n📝 <b>Tags:</b> <code>{}</code>\n🔗 <b>ID:</b> <code>{}</code>\n🌐 <b>Source:</b> <code>{}</code>",
        "loading": "⏳ <b>Loading gallery...</b>",
        "searching_random": "🎲 <b>Searching for random image...</b>",
    }

    def __init__(self):

        self.api_sources = [
            {
                "name": "Rule34.xxx",
                "url": "https://api.rule34.xxx/index.php",
                "params": {"page": "dapi", "s": "post", "q": "index", "json": "1"}
            },
            {
                "name": "Gelbooru",
                "url": "https://gelbooru.com/index.php",
                "params": {"page": "dapi", "s": "post", "q": "index", "json": "1"}
            },
            {
                "name": "Danbooru",
                "url": "https://danbooru.donmai.us/posts.json",
                "params": {}
            }
        ]
        
    async def _make_request(self, tags: str = "", limit: int = 50, source_index: int = None) -> tuple:
        """Выполняет запрос к случайному API источнику"""

        if source_index is None:
            source_index = random.randint(0, len(self.api_sources) - 1)
        
        source = self.api_sources[source_index]
        
        try:
            if source["name"] == "Danbooru":

                params = {
                    "limit": limit,
                    "random": "true"
                }
                if tags:
                    params["tags"] = tags
                url = f"{source['url']}?{urlencode(params)}"
            else:

                params = source["params"].copy()
                params.update({
                    "limit": limit
                })
                if tags:
                    params["tags"] = tags
                url = f"{source['url']}?{urlencode(params)}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = data if isinstance(data, list) else []
                        return results, source["name"]
                    else:
                        raise Exception(f"HTTP {response.status}")
                        
        except Exception as e:

            if source_index is None:
                for i, _ in enumerate(self.api_sources):
                    if i != source_index:
                        try:
                            return await self._make_request(tags, limit, i)
                        except:
                            continue
            raise e

    async def _get_image_info(self, post: dict, source_name: str) -> dict:
        """Извлекает информацию об изображении из поста"""
        

        if source_name == "Danbooru":
            return {
                "id": post.get("id", "unknown"),
                "file_url": post.get("file_url", ""),
                "large_file_url": post.get("large_file_url", ""),
                "preview_file_url": post.get("preview_file_url", ""),
                "tags": post.get("tag_string", "").replace(" ", ", "),
                "score": post.get("score", 0),
                "rating": post.get("rating", "unknown"),
                "source": source_name
            }
        else:

            return {
                "id": post.get("id", "unknown"),
                "file_url": post.get("file_url", ""),
                "sample_url": post.get("sample_url", ""),
                "preview_url": post.get("preview_url", ""),
                "tags": post.get("tags", "").replace(" ", ", "),
                "score": post.get("score", 0),
                "rating": post.get("rating", "unknown"),
                "source": source_name
            }

    async def _get_all_sources_results(self, tags: str, limit: int = 20) -> list:
        """Получает результаты со всех источников для разнообразия"""
        all_results = []
        
        for i, source in enumerate(self.api_sources):
            try:
                results, source_name = await self._make_request(tags, limit, i)
                for post in results:
                    info = await self._get_image_info(post, source_name)
                    if info["file_url"] or info.get("large_file_url") or info.get("sample_url"):
                        all_results.append(info)
            except Exception:
                continue  

        random.shuffle(all_results)
        return all_results

    @loader.command(
        ru_doc="<теги> - Поиск ",
        en_doc="<tags> - Search "
    )
    async def r34cmd(self, message: Message):
        """<теги> - Поиск изображений по тегам"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(
                message, 
                self.strings("invalid_args").format(prefix=self.get_prefix())
            )
            return

        loading_msg = await utils.answer(message, self.strings("searching"))
        
        try:

            all_images = await self._get_all_sources_results(args, 30)
            
            if not all_images:
                await utils.answer(
                    loading_msg,
                    self.strings("no_results").format(utils.escape_html(args))
                )
                return

            await utils.answer(loading_msg, self.strings("loading"))
            

            image_urls = []
            captions = []
            
            for i, info in enumerate(all_images[:50]):  
                url = (info.get("file_url") or 
                       info.get("large_file_url") or 
                       info.get("sample_url"))
                
                if url:
                    image_urls.append(url)
                    caption = self.strings("gallery_caption").format(
                        i + 1,
                        utils.escape_html(info["tags"][:100] + "..." if len(info["tags"]) > 100 else info["tags"]),
                        info["id"],
                        info["source"]
                    )
                    captions.append(caption)
            
            if not image_urls:
                await utils.answer(
                    loading_msg,
                    self.strings("no_results").format(utils.escape_html(args))
                )
                return
            

            current_index = [0]   
            
            def get_next_image():
                if current_index[0] >= len(image_urls):
                    current_index[0] = 0
                url = image_urls[current_index[0]]
                current_index[0] += 1
                return url

            def get_caption():
                caption_index = (current_index[0] - 1) % len(captions)
                return captions[caption_index]


            gallery_result = await self.inline.gallery(
                message=loading_msg,
                next_handler=get_next_image,
                caption=get_caption,
                preload=3,
                force_me=False  
            )
            
            if not gallery_result:

                try:
                    await self._client.send_file(
                        message.peer_id,
                        image_urls[0],
                        caption=captions[0],
                        parse_mode="HTML",
                        reply_to=message.reply_to_msg_id
                    )
                    await loading_msg.delete()
                except Exception:
                    await utils.answer(
                        loading_msg,
                        f"{captions[0]}\n\n🔗 <a href='{image_urls[0]}'>Открыть изображение</a>"
                    )

        except Exception as e:
            await utils.answer(
                loading_msg,
                self.strings("error").format(str(e))
            )

    @loader.command(
        ru_doc="рандом rule34",
        en_doc="Random "
    )
    async def r34randomcmd(self, message: Message):
        """Случайное изображение"""
        loading_msg = await utils.answer(message, self.strings("searching_random"))
        
        try:

            source_index = random.randint(0, len(self.api_sources) - 1)

            results, source_name = await self._make_request("", 100, source_index)
            
            if not results:

                for i in range(len(self.api_sources)):
                    if i != source_index:
                        try:
                            results, source_name = await self._make_request("", 100, i)
                            if results:
                                break
                        except:
                            continue
            
            if not results:
                await utils.answer(
                    loading_msg,
                    "😔 <b>Не удалось получить случайные изображения</b>"
                )
                return

 
            random_post = random.choice(results)
            info = await self._get_image_info(random_post, source_name)
            
            image_url = (info.get("file_url") or 
                        info.get("large_file_url") or 
                        info.get("sample_url"))
            
            if not image_url:
                await utils.answer(
                    loading_msg,
                    "😔 <b>Не удалось получить URL изображения</b>"
                )
                return

            caption = self.strings("random_caption").format(
                utils.escape_html(info["tags"][:200] + "..." if len(info["tags"]) > 200 else info["tags"]),
                info["id"],
                info["source"]
            )
            
            try:
                await self._client.send_file(
                    message.peer_id,
                    image_url,
                    caption=caption,
                    parse_mode="HTML",
                    reply_to=message.reply_to_msg_id
                )
                await loading_msg.delete()
            except Exception:

                await utils.answer(
                    loading_msg,
                    f"{caption}\n\n🔗 <a href='{image_url}'>Открыть изображение</a>"
                )

        except Exception as e:
            await utils.answer(
                loading_msg,
                self.strings("error").format(str(e))
            )