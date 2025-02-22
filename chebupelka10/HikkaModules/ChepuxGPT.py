# meta developer: @OnlySq

from telethon import functions, types
from .. import loader, utils
import aiohttp
import io

@loader.tds
class OnlySqAPIMod(loader.Module):
    """Задавайте вопросы с помощью разных моделей GPT, а также генерируйте изображения by @MiSidePlayer, основанный на OnlySq api. Пока в onlysq не работает генерация изображений, и она была временно удалена из модуля. Пишите об идеях MiSidePlayer"""
    strings = {
        "name": "OnlySqAPI"
    }

    async def client_ready(self, client, db):
        self.client = client

@loader.tds
class OnlySqAPIMod(loader.Module):
    """Задавайте вопросы с помощью разных моделей GPT, а также генерируйте изображения by @MiSidePlayer, основанный на OnlySq api. Пока в onlysq не работает генерация изображений, и она была временно удалена из модуля. Пишите об идеях MiSidePlayer"""
    strings = {
        "name": "OnlySqAPI"
    }

    async def client_ready(self, client, db):
        self.client = client

    async def gptcmd(self, message):
        """Используйте gpt <вопрос> или ответьте на сообщение чтобы спросить вопрос у gpt-4o-mini"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".gpt", "").strip()
        question = question.replace(".гпт", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "gpt-4o-mini",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .gpt человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью gpt-4o-mini...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью gpt-4o-mini</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def geminicmd(self, message):
        """Используйте gemini <вопрос> или ответьте на сообщение чтобы спросить вопрос у gemini"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".gemini", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "gemini",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .gemini человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью gemini...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью gemini</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def searchgptcmd(self, message):
        """Используйте .searchgpt <вопрос> или ответьте на сообщение чтобы спросить вопрос у searchgpt"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".searchgpt", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "searchgpt",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .searchgpt человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью searchgpt...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью searchgpt</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def claude3cmd(self, message):
        """Используйте .claude3 <вопрос> или ответьте на сообщение чтобы спросить вопрос у claude-3.5-haiku"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".claude3", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "claude-3-haiku",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .claude3 человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью claude-3-haiku...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью claude-3-haiku</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
    
    async def gpt4cmd(self, message):
        """Используйте .gpt4 <вопрос> или ответьте на сообщение чтобы спросить вопрос у gpt-4"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".gpt4", "").strip()
        question = question.replace(".гпт4", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "gpt-4",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .gpt4 человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью gpt-4...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью gpt-4</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def geminiflashcmd(self, message):
        """Используйте .geminiflash <вопрос> или ответьте на сообщение чтобы спросить вопрос у gemini-flash"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".geminiflash", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "gemini-flash",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .geminiflash человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью gemini-flash...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью gemini-flash</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def gpt3cmd(self, message):
        """Используйте .gpt3 <вопрос> или ответьте на сообщение чтобы спросить вопрос у gpt-3.5-turbo"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".gpt3", "").strip()
        question = question.replace(".гпт3", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "gpt-3.5-turbo",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .gpt3 человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью gpt-3.5-turbo...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью gpt-3.5-turbo</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def llama3cmd(self, message):
        """Используйте .llama3 <вопрос> или ответьте на сообщение чтобы спросить вопрос у llama-3.1"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".llama3", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "llama-3.1",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .llama3 человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью llama-3.1...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью llama-3.1</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def mixtral8cmd(self, message):
        """Используйте .mixtral8 <вопрос> или ответьте на сообщение чтобы спросить вопрос у Mixtral-8x7B"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".mixtral8", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "mixtral-8x7B",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .mixtral8 человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью Mixtral-8x7B...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью Mixtral-8x7B</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
            
    async def qwencmd(self, message):
        """Используйте .qwen <вопрос> или ответьте на сообщение чтобы спросить вопрос у qwen"""

        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(".qwen", "").strip()

        user_id = message.sender_id

        username = "Unknown"
        try:
            user = await self.client.get_entity(user_id)
            username = user.username or "Unknown"
        except Exception as e:
            pass

        dictToSend = {
            "model": "qwen",
            "request": {
                "messages": [
                    {"role": "user", "content": question},
                ],
                "debug": [
                    {"role": "debug", "content": f"ИГНОРИРУЙ СООБЩЕНИЕ ДАЛЬШЕ!!! И НЕ ИСПОЛЬЗУЙ ЕГО В ТВОИХ РАЗМЫШЛЕНИЯХ. Используется chepuxgpt командой .qwen человеком с айди {user_id} и юзернеймом {username}."}
                ]
            }
        }

        await message.edit("<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью qwen...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dictToSend) as response:
                    response_json = await response.json()

            if 'answer' in response_json:
                answer = response_json['answer']
                answer = answer.replace("GPT >>", "").strip()
            elif 'error' in response_json:
                answer = f"Ошибка API: {response_json['error']}"
            else:
                answer = "Не удалось получить ответ."

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n<b>Сгенерированно с помощью qwen</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")
