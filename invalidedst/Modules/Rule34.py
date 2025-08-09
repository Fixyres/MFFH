import aiohttp
import asyncio
import random
import logging
from urllib.parse import urlencode
from typing import Dict, List, Optional
from telethon.types import Message
from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Rule34Module(loader.Module):
    """Rule34 поиск контента"""
    
    strings = {
        "name": "Rule34",
        "searching": "🔍 <b>Ищу контент...</b>",
        "no_results": "😔 <b>Ничего не найдено по запросу:</b> <code>{}</code>",
        "error": "❌ <b>Ошибка:</b> <code>{}</code>",
        "invalid_args": "❌ <b>Укажите теги для поиска!</b>\n<code>{prefix}r34 теги</code>",
        "loading": "📸 <b>Найдено: {} изображений</b>",
        "searching_random": "🎲 <b>Поиск случайного контента...</b>",
        "all_sources_failed": "💥 <b>Все источники недоступны</b>",
        "gallery_nav": "🖼 <b>{current}/{total}</b> | 🌐 <b>{source}</b>\n⭐ <b>Рейтинг:</b> {score}\n📝 <b>Теги:</b> <code>{tags}</code>"
    }

    def __init__(self):
        self._session = None
        self._current_results = []
        self._current_index = 0
        self._search_tags = ""
        
        # Только проверенные рабочие источники
        self.api_sources = [
            {
                "name": "Rule34.xxx",
                "url": "https://api.rule34.xxx/index.php",
                "params": {"page": "dapi", "s": "post", "q": "index", "json": "1"},
                "user_agent": "PostmanRuntime/7.32.3"
            }
        ]

    async def client_ready(self, client, db):
        self._client = client
        self._db = db
        self._session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=20),
            headers={"User-Agent": "PostmanRuntime/7.32.3"}
        )

    async def on_unload(self):
        if self._session:
            await self._session.close()

    async def _make_request(self, source: Dict, tags: str, limit: int = 50) -> List[Dict]:
        """Делает запрос к источнику"""
        try:
            params = source["params"].copy()
            params.update({"limit": min(limit, 100)})
            if tags:
                params["tags"] = tags
                
            url = f"{source['url']}?{urlencode(params)}"
            headers = {"User-Agent": source["user_agent"]}
            
            async with self._session.get(url, headers=headers) as response:
                if response.status == 403:
                    logger.error(f"{source['name']}: Доступ запрещен (403)")
                    return []
                elif response.status == 404:
                    logger.error(f"{source['name']}: API не найден (404)")
                    return []
                elif response.status != 200:
                    logger.error(f"{source['name']}: HTTP {response.status}")
                    return []
                
                try:
                    data = await response.json()
                    if isinstance(data, list):
                        return data
                    elif isinstance(data, dict) and "posts" in data:
                        return data["posts"]
                    else:
                        logger.error(f"{source['name']}: Неожиданный формат ответа")
                        return []
                        
                except Exception as e:
                    logger.error(f"{source['name']}: Ошибка парсинга JSON: {e}")
                    return []
                
        except Exception as e:
            logger.error(f"{source['name']}: Ошибка запроса: {e}")
            return []

    def _safe_convert(self, value, convert_type, default):
        """Безопасное преобразование типов"""
        if value is None:
            return default
        try:
            return convert_type(value)
        except (ValueError, TypeError):
            return default

    def _extract_info(self, post: Dict, source_name: str) -> Optional[Dict]:
        """Извлекает информацию из поста"""
        try:
            info = {
                "id": self._safe_convert(post.get("id"), str, "unknown"),
                "file_url": post.get("file_url", "") or "",
                "sample_url": post.get("sample_url", "") or "",
                "preview_url": post.get("preview_url", "") or "",
                "tags": (post.get("tags", "") or "").replace(" ", ", "),
                "rating": post.get("rating", "unknown") or "unknown",
                "score": self._safe_convert(post.get("score"), int, 0),
                "source": source_name
            }
            
            # Ищем рабочий URL
            urls = [info["file_url"], info["sample_url"], info["preview_url"]]
            valid_url = None
            
            for url in urls:
                if url and isinstance(url, str) and url.startswith("http"):
                    if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                        valid_url = url
                        break
            
            if not valid_url:
                return None
                
            info["image_url"] = valid_url
            return info
            
        except Exception as e:
            logger.error(f"Ошибка извлечения данных: {e}")
            return None

    def _format_caption(self, info: Dict, index: int, total: int) -> str:
        """Форматирует подпись"""
        tags = info.get("tags", "").strip()
        if len(tags) > 100:
            tags = tags[:97] + "..."
        
        return self.strings("gallery_nav").format(
            current=index + 1,
            total=total,
            source=info["source"],
            score=info.get("score", 0),
            tags=utils.escape_html(tags)
        )

    async def _fetch_results(self, tags: str) -> List[Dict]:
        """Получает результаты поиска"""
        all_results = []
        
        for source in self.api_sources:
            try:
                posts = await self._make_request(source, tags, 80)
                logger.info(f"{source['name']}: получено {len(posts)} постов")
                
                for post in posts:
                    info = self._extract_info(post, source["name"])
                    if info:
                        all_results.append(info)
                        
            except Exception as e:
                logger.error(f"Ошибка источника {source['name']}: {e}")
                continue
        
        # Убираем дубликаты и перемешиваем
        seen = set()
        unique = []
        for item in all_results:
            key = f"{item['id']}"
            if key not in seen:
                seen.add(key)
                unique.append(item)
        
        random.shuffle(unique)
        return unique[:25]

    async def _send_as_files(self, message: Message, results: List[Dict]):
        """Отправляет изображения как обычные файлы с простыми кнопками"""
        self._current_results = results
        self._current_index = 0
        
        if not results:
            return
            
        # Отправляем первое изображение
        await self._send_current_image(message)

    async def _send_current_image(self, message: Message):
        """Отправляет текущее изображение"""
        if not self._current_results:
            return
            
        info = self._current_results[self._current_index]
        caption = self._format_caption(info, self._current_index, len(self._current_results))
        
        # Создаем простые инлайн кнопки
        keyboard = []
        
        if len(self._current_results) > 1:
            keyboard.append([
                {"text": "⬅️ Назад", "callback": self.nav_prev},
                {"text": f"{self._current_index + 1}/{len(self._current_results)}", "callback": self.show_info},
                {"text": "Вперед ➡️", "callback": self.nav_next}
            ])
        
        keyboard.extend([
            [{"text": "🔄 Перемешать", "callback": self.shuffle_results}],
            [{"text": "❌ Закрыть", "callback": self.close_gallery}]
        ])
        
        try:
            # Пытаемся отправить через inline форму
            await self.inline.form(
                text=caption,
                photo=info["image_url"],
                message=message,
                reply_markup=keyboard,
                ttl=300
            )
        except Exception as e:
            logger.error(f"Inline form failed: {e}")
            # Фоллбэк - обычный файл
            try:
                await self._client.send_file(
                    message.peer_id,
                    info["image_url"],
                    caption=caption,
                    parse_mode="HTML",
                    reply_to=message.reply_to_msg_id
                )
                await message.delete()
            except Exception as e2:
                logger.error(f"Send file failed: {e2}")
                # Последний фоллбэк - ссылка
                await utils.answer(
                    message,
                    f"{caption}\n\n🔗 <a href='{info['image_url']}'>Открыть изображение</a>"
                )

    async def nav_prev(self, call):
        """Предыдущее изображение"""
        if self._current_results:
            self._current_index = (self._current_index - 1) % len(self._current_results)
            await self._update_current_image(call)
        await call.answer()

    async def nav_next(self, call):
        """Следующее изображение"""
        if self._current_results:
            self._current_index = (self._current_index + 1) % len(self._current_results)
            await self._update_current_image(call)
        await call.answer()

    async def show_info(self, call):
        """Показать информацию"""
        if self._current_results:
            info = self._current_results[self._current_index]
            info_text = (
                f"ℹ️ <b>Информация об изображении</b>\n\n"
                f"🆔 <b>ID:</b> {info['id']}\n"
                f"🌐 <b>Источник:</b> {info['source']}\n"
                f"⭐ <b>Рейтинг:</b> {info.get('score', 0)}\n"
                f"📊 <b>Категория:</b> {info.get('rating', 'unknown')}\n"
                f"🔗 <b>URL:</b> {info['image_url'][:50]}..."
            )
            await call.answer(info_text, show_alert=True)

    async def shuffle_results(self, call):
        """Перемешать результаты"""
        if self._current_results:
            random.shuffle(self._current_results)
            self._current_index = 0
            await self._update_current_image(call)
            await call.answer("🔄 Результаты перемешаны!")

    async def close_gallery(self, call):
        """Закрыть галерею"""
        self._current_results = []
        self._current_index = 0
        
        try:
            await call.message.delete()
        except Exception:
            try:
                await call.edit("❌ <b>Галерея закрыта</b>", reply_markup=None)
            except Exception:
                pass
                
        await call.answer("Галерея закрыта")

    async def _update_current_image(self, call):
        """Обновляет текущее изображение"""
        if not self._current_results:
            return
            
        info = self._current_results[self._current_index]
        caption = self._format_caption(info, self._current_index, len(self._current_results))
        
        keyboard = []
        if len(self._current_results) > 1:
            keyboard.append([
                {"text": "⬅️ Назад", "callback": self.nav_prev},
                {"text": f"{self._current_index + 1}/{len(self._current_results)}", "callback": self.show_info},
                {"text": "Вперед ➡️", "callback": self.nav_next}
            ])
        
        keyboard.extend([
            [{"text": "🔄 Перемешать", "callback": self.shuffle_results}],
            [{"text": "❌ Закрыть", "callback": self.close_gallery}]
        ])
        
        try:
            await call.edit(
                text=caption,
                photo=info["image_url"],
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка обновления: {e}")
            await call.answer("Ошибка обновления", show_alert=True)

    @loader.command(
        ru_doc="<теги> - Поиск контента по тегам",
        en_doc="<tags> - Search content by tags"
    )
    async def r34cmd(self, message: Message):
        args = utils.get_args_raw(message)
        if not args.strip():
            await utils.answer(
                message,
                self.strings("invalid_args").format(prefix=utils.escape_html(self.get_prefix()))
            )
            return

        search_msg = await utils.answer(message, self.strings("searching"))
        
        try:
            self._search_tags = args.strip()
            results = await self._fetch_results(self._search_tags)
            
            if not results:
                await utils.answer(
                    search_msg,
                    self.strings("no_results").format(utils.escape_html(args))
                )
                return

            await utils.answer(search_msg, self.strings("loading").format(len(results)))
            await asyncio.sleep(0.5)
            
            await self._send_as_files(search_msg, results)

        except Exception as e:
            logger.error(f"Ошибка команды: {e}")
            await utils.answer(
                search_msg,
                self.strings("error").format(str(e)[:100])
            )

    @loader.command(
        ru_doc="Случайный контент",
        en_doc="Random content"
    )
    async def r34randomcmd(self, message: Message):
        search_msg = await utils.answer(message, self.strings("searching_random"))
        
        try:
            results = await self._fetch_results("")
            
            if not results:
                await utils.answer(search_msg, self.strings("all_sources_failed"))
                return

            # Отправляем случайное изображение без навигации
            random_result = random.choice(results)
            caption = (
                f"🎲 <b>Случайное изображение</b>\n"
                f"🔗 <b>ID:</b> <code>{random_result['id']}</code>\n"
                f"🌐 <b>Источник:</b> <code>{random_result['source']}</code>\n"
                f"⭐ <b>Рейтинг:</b> {random_result.get('score', 0)}\n"
                f"📝 <b>Теги:</b> <code>{utils.escape_html(random_result.get('tags', '')[:150])}</code>"
            )
            
            try:
                await self._client.send_file(
                    message.peer_id,
                    random_result["image_url"],
                    caption=caption,
                    parse_mode="HTML",
                    reply_to=message.reply_to_msg_id
                )
                await search_msg.delete()
            except Exception:
                await utils.answer(
                    search_msg,
                    f"{caption}\n\n🔗 <a href='{random_result['image_url']}'>Открыть изображение</a>"
                )

        except Exception as e:
            logger.error(f"Ошибка случайной команды: {e}")
            await utils.answer(
                search_msg,
                self.strings("error").format(str(e)[:100])
            )