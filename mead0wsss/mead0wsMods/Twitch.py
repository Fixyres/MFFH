__version__ = (1, 0, 0)

# ███╗░░░███╗███████╗░█████╗░██████╗░░█████╗░░██╗░░░░░░░██╗░██████╗░██████╗
# ████╗░████║██╔════╝██╔══██╗██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔════╝
# ██╔████╔██║█████╗░░███████║██║░░██║██║░░██║░╚██╗████╗██╔╝╚█████╗░╚█████╗░
# ██║╚██╔╝██║██╔══╝░░██╔══██║██║░░██║██║░░██║░░████╔═████║░░╚═══██╗░╚═══██╗
# ██║░╚═╝░██║███████╗██║░░██║██████╔╝╚█████╔╝░░╚██╔╝░╚██╔╝░██████╔╝██████╔╝
# ╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═════╝░░╚════╝░░░░╚═╝░░░╚═╝░░╚═════╝░╚═════╝░
#                © Copyright 2025
#            ✈ https://t.me/mead0wssMods

# scope: hikka_only
# scope: hikka_min 1.3.3
# meta developer: @mead0wssMods

import aiohttp
from .. import loader, utils

@loader.tds
class TwitchMod(loader.Module):
    """Модуль для работы с Twitch"""
    strings = {"name": "Twitch"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "CLIENT_ID",
                "",
                lambda: "Client ID из Twitch Dev Console [https://dev.twitch.tv/console/]",
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                "ACCESS_TOKEN",
                "",
                lambda: "Access Token с scope user:read:follows [https://twitchtokengenerator.com/]",
                validator=loader.validators.Hidden()
            ),
            loader.ConfigValue(
                "TARGET_USERNAME",
                "",
                lambda: "Ваш никнейм пользователя Twitch [https://www.twitch.tv/",
                validator=loader.validators.Hidden()
            ),
        )
        self.session = aiohttp.ClientSession()

    async def client_ready(self, client, db):
        self._client = client

    async def get_user_id(self, username=None):
        """Получаем ID пользователя"""
        url = "https://api.twitch.tv/helix/users"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"login": username or self.config["TARGET_USERNAME"]}
        
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data["data"][0]["id"] if data.get("data") else None

    async def get_all_followed(self, user_id):
        """Получаем всех подписанных стримеров"""
        url = "https://api.twitch.tv/helix/channels/followed"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"user_id": user_id}
        
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("data", [])

    async def get_live_streams(self, logins=None, game_id=None, limit=100):
        """Получаем онлайн стримы"""
        url = "https://api.twitch.tv/helix/streams"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"first": limit}
        
        if logins:
            params["user_login"] = logins[:100]
        if game_id:
            params["game_id"] = game_id
            
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("data", [])

    async def get_top_games(self, limit=10):
        """Получаем топ игр"""
        url = "https://api.twitch.tv/helix/games/top"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"first": limit}
        
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("data", [])

    async def search_games(self, query):
        """Поиск игр по названию"""
        url = "https://api.twitch.tv/helix/search/categories"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"query": query}
        
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("data", [])

    async def get_channel_info(self, broadcaster_id):
        """Получаем информацию о канале"""
        url = "https://api.twitch.tv/helix/channels"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"broadcaster_id": broadcaster_id}
        
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("data", [{}])[0]

    async def get_channel_followers(self, broadcaster_id):
        """Получаем количество фолловеров канала"""
        url = "https://api.twitch.tv/helix/channels/followers"
        headers = {
            "Client-ID": self.config["CLIENT_ID"],
            "Authorization": f"Bearer {self.config['ACCESS_TOKEN']}"
        }
        params = {"broadcaster_id": broadcaster_id, "first": 1}
        
        async with self.session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data.get("total", 0)

    @loader.command()
    async def followed(self, message):
        """Показать всех подписанных стримеров"""
        user_id = await self.get_user_id()
        if not user_id:
            await utils.answer(message, "<emoji document_id=5019523782004441717>❌</emoji> Пользователь не найден!")
            return
            
        followed = await self.get_all_followed(user_id)
        if not followed:
            await utils.answer(message, "<emoji document_id=5190748314026385859>🤷‍♂️</emoji> Нет подписок")
            return
            
        text = "<emoji document_id=4999434394599948988>🎮</emoji> Каналы на которые зафолловлен:\n\n"
        for channel in followed[:25]:
            followers_count = await self.get_channel_followers(channel["broadcaster_id"])
            text += (f"<emoji document_id=5944753741512052670>📷</emoji> <b><a href='https://twitch.tv/{channel['broadcaster_login']}'>"
                    f"{channel['broadcaster_name']}</a></b>  [<emoji document_id=6032609071373226027>👥</emoji> <code>{followers_count}</code> Фолловеров]\n")
        
        if len(followed) > 25:
            text += f"\n...и еще {len(followed) - 25} стримеров"
            
        await utils.answer(message, text)

    @loader.command()
    async def streams(self, message):
        """Показать онлайн стримы"""
        user_id = await self.get_user_id()
        if not user_id:
            await utils.answer(message, "<emoji document_id=5019523782004441717>❌</emoji> Пользователь не найден!")
            return  
            
        followed = await self.get_all_followed(user_id)
        if not followed:
            await utils.answer(message, "<emoji document_id=5190748314026385859>🤷‍♂️</emoji> Нет подписок")
            return
            
        logins = [channel["broadcaster_login"] for channel in followed]
        live_streams = await self.get_live_streams(logins[:100])
        
        if not live_streams:
            await utils.answer(message, "<emoji document_id=4926956800005112527>🔴</emoji> Сейчас никто не стримит")
            return
            
        text = "<emoji document_id=4999434394599948988>🎮</emoji> Стримеры ведущие трансляцию:\n"
        for stream in live_streams:
            channel_info = await self.get_channel_info(stream["user_id"])
            followers_count = await self.get_channel_followers(stream["user_id"])
            text += (f'\n<b><emoji document_id=5879770735999717115>👤</emoji> <a href="https://twitch.tv/{stream["user_login"]}">{stream["user_name"]}</a></b>'
                    f'<b><blockquote><emoji document_id=5348214678524805365>🎮</emoji> {stream["game_name"]}\n'
                    f'<emoji document_id=6037397706505195857>👁</emoji> <code>{stream["viewer_count"]}</code> зрителей\n'
                    f'<emoji document_id=6032609071373226027>👥</emoji> <code>{followers_count}</code> фолловеров\n'
                    f'<emoji document_id=5879785854284599288>ℹ️</emoji> {stream["title"]}\n</blockquote></b>')
        
        await utils.answer(message, text)

    @loader.command()
    async def streamer(self, message):
        """Информация о стримере"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5019523782004441717>❌</emoji> Укажите ник стримера")
            return
            
        user_id = await self.get_user_id(args)
        if not user_id:
            await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> Стример {args} не найден")
            return
            
        channel_info = await self.get_channel_info(user_id)
        followers_count = await self.get_channel_followers(user_id)
        
        text = (f"<emoji document_id=4999434394599948988>🎮</emoji> <b>Информация о:</b>\n\n <b><emoji document_id=5879770735999717115>👤</emoji> <a href='https://twitch.tv/{args}'>{args}</a></b>:\n"
               f"<b><blockquote><emoji document_id=6032609071373226027>👥</emoji> Фолловеров: <code>{followers_count}</code>\n"
               f"<emoji document_id=5879785854284599288>ℹ️</emoji> Описание стрима (пусто = офф): <code>{channel_info.get('title', 'Нет описания')}</code>\n"
               f"<blockquote><emoji document_id=5348214678524805365>🎮</emoji> Игра на стриме: <code>{channel_info.get('game_name', 'Не указана')}</code>   \n"
               f"<emoji document_id=6028171274939797252>🔗</emoji> Ссылка: https://twitch.tv/{args}</b></blockquote>")
        
        await utils.answer(message, text)

    @loader.command()
    async def topgames(self, message):
        """Топ игр на Twitch"""
        games = await self.get_top_games(10)
        if not games:
            await utils.answer(message, "<emoji document_id=5019523782004441717>❌</emoji> Не удалось получить список игр")
            return
            
        text = "<emoji document_id=4999434394599948988>🎮</emoji> Топ игр на Twitch:\n\n"
        text += "\n".join(
            f"<b><blockquote>{i+1}. {game['name']} (ID: <code>{game['id']}</code>)</blockquote></b>"
            for i, game in enumerate(games))
            
        await utils.answer(message, text)

    @loader.command()
    async def game(self, message):
        """Поиск игры и стримы по ней"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "<emoji document_id=5019523782004441717>❌</emoji> Укажите название игры")
            return
            
        games = await self.search_games(args)
        if not games:
            await utils.answer(message, f"<emoji document_id=5019523782004441717>❌</emoji> Игра '{args}' не найдена")
            return
            
        game = games[0]
        streams = await self.get_live_streams(game_id=game["id"])
        
        text = (f"<emoji document_id=5348214678524805365>🎮</emoji> Игра: {game['name']}\n"
               f"<emoji document_id=6028171274939797252>🔗</emoji> Изображение: {game['box_art_url'].replace('{width}x{height}', '300x400')}\n\n")
               
        if streams:
            text += f"<emoji document_id=4999434394599948988>🎮</emoji> Топ стримов ({len(streams)} онлайн):\n\n"
            for stream in streams[:5]:
                followers_count = await self.get_channel_followers(stream["user_id"])
                text += (f'<b><emoji document_id=5879770735999717115>👤</emoji> <a href="https://twitch.tv/{stream["user_login"]}">{stream["user_name"]}</a>\n'
                         f'<blockquote><emoji document_id=6037397706505195857>👁</emoji> <code>{stream["viewer_count"]}</code> зрителей\n'
                         f'<emoji document_id=6032609071373226027>👥</emoji> <code>{followers_count}</code> фолловеров\n'
                         f'<emoji document_id=5879785854284599288>ℹ️</emoji>{stream["title"]}\n</blockquote></b>')
        else:
            text += "Сейчас никто не стримит эту игру"
            
        await utils.answer(message, text)
