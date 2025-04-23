# meta developer: @OnlySq

from telethon import functions, types
from .. import loader, utils
import aiohttp
import io

@loader.tds
class OnlySqAPIMod(loader.Module):
    """Задавайте вопросы и генерируйте изображения с помощью моделей AI через OnlySq API by @chepuxcat."""
    strings = {"name": "OnlySqAPI"}

    async def client_ready(self, client, db):
        self.client = client

    async def _process_ai_request(self, message, model, command):
        """Общая функция для обработки текстовых запросов к AI моделям."""
        question = utils.get_args_raw(message)
        if not question:
            reply = await message.get_reply_message()
            if reply:
                question = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не задали вопрос.</b>")
                return

        question = question.replace(f".{command}", "").strip()

        dict_to_send = {
            "model": model,
            "request": {"messages": [{"role": "user", "content": question}]}
        }

        await message.edit(f"<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую ответ с помощью {model}...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dict_to_send) as response:
                    response_json = await response.json()

            answer = response_json.get("choices", [{}])[0].get("message", {}).get("content", f"Ошибка API: {response_json.get('error', 'Не удалось получить ответ.')}")
            answer = answer.replace("GPT >>", "").strip()

            await utils.answer(message, f"<b><emoji document_id=6323343426343404864>❓</emoji> Вопрос:</b> {question}\n"
                                      f"<b><emoji document_id=6323463440614557670>☺️</emoji> Ответ:</b> {answer}\n\n"
                                      f"<b>Сгенерировано с помощью {model}</b>")
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")

    async def _process_image_request(self, message, model, command):
        """Общая функция для генерации изображений."""
        prompt = utils.get_args_raw(message)
        if not prompt:
            reply = await message.get_reply_message()
            if reply:
                prompt = reply.raw_text
            else:
                await utils.answer(message, "<b><emoji document_id=5321288244350951776>👎</emoji> Вы не указали описание для изображения.</b>")
                return

        prompt = prompt.replace(f".{command}", "").strip()

        dict_to_send = {
            "model": model,
            "request": {"messages": [{"role": "user", "content": prompt}]}
        }

        await message.edit(f"<b><emoji document_id=5409143295039252230>🔄</emoji> Генерирую изображение с помощью {model}...</b>")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post('https://api.onlysq.ru/ai/v2', json=dict_to_send) as response:
                    if response.status != 200:
                        await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Ошибка API: {response.status}</b>")
                        return
                    image_data = await response.read()

            image = io.BytesIO(image_data)
            image.name = f"{model}_image.png"

            await message.delete()
            await self.client.send_file(
                message.to_id,
                image,
                caption=f"<b><emoji document_id=6323343426343404864>🖼️</emoji> Изображение:</b> {prompt}\n"
                        f"<b>Сгенерировано с помощью {model}</b>"
            )
        except Exception as e:
            await utils.answer(message, f"<b><emoji document_id=5314591660192046611>❌</emoji> Произошла ошибка:</b> {e}")

    async def gptcmd(self, message):
        """Используйте .gpt <вопрос> для gpt-4o-mini."""
        await self._process_ai_request(message, "gpt-4o-mini", "gpt")

    async def searchgptcmd(self, message):
        """Используйте .searchgpt <вопрос> для searchgpt."""
        await self._process_ai_request(message, "searchgpt", "searchgpt")

    async def claude3cmd(self, message):
        """Используйте .claude3 <вопрос> для claude-3-haiku."""
        await self._process_ai_request(message, "claude-3-haiku", "claude3")

    async def gpt4cmd(self, message):
        """Используйте .gpt4 <вопрос> для gpt-4."""
        await self._process_ai_request(message, "gpt-4", "gpt4")

    async def gpt3cmd(self, message):
        """Используйте .gpt3 <вопрос> для gpt-3.5-turbo."""
        await self._process_ai_request(message, "gpt-3.5-turbo", "gpt3")

    async def llama3cmd(self, message):
        """Используйте .llama3 <вопрос> для llama-3.1."""
        await self._process_ai_request(message, "llama-3.1", "llama3")

    async def qwencmd(self, message):
        """Используйте .qwen <вопрос> для qwen."""
        await self._process_ai_request(message, "qwen", "qwen")

    async def kandinskycmd(self, message):
        """Используйте .kandinsky <описание> для генерации изображения с kandinsky."""
        await self._process_image_request(message, "kandinsky", "kandinsky")

    async def fluxcmd(self, message):
        """Используйте .flux <описание> для генерации изображения с flux."""
        await self._process_image_request(message, "flux", "flux")

    async def claude35cmd(self, message):
        """Используйте .claude35 <вопрос> для claude-3.5-sonnet."""
        await self._process_ai_request(message, "claude-3.5-sonnet", "claude35")

    async def gpt4ocmd(self, message):
        """Используйте .gpt4o <вопрос> для gpt-4o."""
        await self._process_ai_request(message, "gpt-4o", "gpt4o")

    async def gpt4turbocmd(self, message):
        """Используйте .gpt4turbo <вопрос> для gpt-4-turbo."""
        await self._process_ai_request(message, "gpt-4-turbo", "gpt4turbo")

    async def llama33cmd(self, message):
        """Используйте .llama33 <вопрос> для llama-3.3."""
        await self._process_ai_request(message, "llama-3.3", "llama33")

    async def deepseekv3cmd(self, message):
        """Используйте .deepseekv3 <вопрос> для deepseek-v3."""
        await self._process_ai_request(message, "deepseek-v3", "deepseekv3")

    async def qwen25cmd(self, message):
        """Используйте .qwen25 <вопрос> для qwen-2.5-32b."""
        await self._process_ai_request(message, "qwen-2.5-32b", "qwen25")

    async def mistralsmallcmd(self, message):
        """Используйте .mistralsmall <вопрос> для mistral-small-3.1."""
        await self._process_ai_request(message, "mistral-small-3.1", "mistralsmall")

    async def commandcmd(self, message):
        """Используйте .command <вопрос> для command."""
        await self._process_ai_request(message, "command", "command")

    async def commandlightcmd(self, message):
        """Используйте .commandlight <вопрос> для command-light."""
        await self._process_ai_request(message, "command-light", "commandlight")

    async def commandnightlycmd(self, message):
        """Используйте .commandnightly <вопрос> для command-nightly."""
        await self._process_ai_request(message, "command-nightly", "commandnightly")

    async def commandlightnightlycmd(self, message):
        """Используйте .commandlightnightly <вопрос> для command-light-nightly."""
        await self._process_ai_request(message, "command-light-nightly", "commandlightnightly")

    async def commandr03cmd(self, message):
        """Используйте .commandr03 <вопрос> для command-r-03-2024."""
        await self._process_ai_request(message, "command-r-03-2024", "commandr03")

    async def commandr08cmd(self, message):
        """Используйте .commandr08 <вопрос> для command-r-08-2024."""
        await self._process_ai_request(message, "command-r-08-2024", "commandr08")

    async def commandrcmd(self, message):
        """Используйте .commandr <вопрос> для command-r."""
        await self._process_ai_request(message, "command-r", "commandr")

    async def commandrpluscmd(self, message):
        """Используйте .commandrplus <вопрос> для command-r-plus."""
        await self._process_ai_request(message, "command-r-plus", "commandrplus")

    async def commandrplus04cmd(self, message):
        """Используйте .commandrplus04 <вопрос> для command-r-plus-04-2024."""
        await self._process_ai_request(message, "command-r-plus-04-2024", "commandrplus04")

    async def commandr7bcmd(self, message):
        """Используйте .commandr7b <вопрос> для command-r7b-12-2024."""
        await self._process_ai_request(message, "command-r7b-12-2024", "commandr7b")

    async def commandacmd(self, message):
        """Используйте .commanda <вопрос> для command-a-03-2025."""
        await self._process_ai_request(message, "command-a-03-2025", "commanda")

    async def c4aiayacmd(self, message):
        """Используйте .c4aiaya <вопрос> для c4ai-aya-expanse-32b."""
        await self._process_ai_request(message, "c4ai-aya-expanse-32b", "c4aiaya")

    async def gemma34bcmd(self, message):
        """Используйте .gemma34b <вопрос> для gemma-3-4b-it."""
        await self._process_ai_request(message, "gemma-3-4b-it", "gemma34b")

    async def gemini15flashcmd(self, message):
        """Используйте .gemini15flash <вопрос> для gemini-1.5-flash."""
        await self._process_ai_request(message, "gemini-1.5-flash", "gemini15flash")

    async def gemini15procmd(self, message):
        """Используйте .gemini15pro <вопрос> для gemini-1.5-pro."""
        await self._process_ai_request(message, "gemini-1.5-pro", "gemini15pro")

    async def deepseekr1cmd(self, message):
        """Используйте .deepseekr1 <вопрос> для deepseek-r1."""
        await self._process_ai_request(message, "deepseek-r1", "deepseekr1")

    async def o3minicmd(self, message):
        """Используйте .o3mini <вопрос> для o3-mini."""
        await self._process_ai_request(message, "o3-mini", "o3mini")

    async def evilcmd(self, message):
        """Используйте .evil <вопрос> для evil."""
        await self._process_ai_request(message, "evil", "evil")

    async def mistralcmd(self, message):
        """Используйте .mistral <вопрос> для mistral."""
        await self._process_ai_request(message, "mistral", "mistral")
