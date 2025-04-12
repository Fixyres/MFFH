# Copyright 2025, werpyock
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
__version__ = (1, 0, 0)
# meta developer: @wmodules

from hikkatl.types import Message
from .. import loader, utils
import asyncio

@loader.tds
class WordByWordMod(loader.Module):
    """Анимация текста по словам"""
    strings = {
        "name": "WordByWord",
        "stopped": "✅ Анимации остановлены",
        "invalid_args": "❌ Неверные аргументы. Формат: <задержка в ms> \"текст\"",
        "invalid_delay": "❌ Задержка должна быть положительным числом"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "delay_between_edit",
                900,
                validator=loader.validators.Integer(minimum=1)
            )
        )
        self.running_tasks = {}

    async def wordbywordcmd(self, message: Message):
        """<задержка в ms> "текст" - анимировать текст по словам"""
        try:
            args = utils.get_args_raw(message)
            if not args:
                await utils.answer(message, self.strings("invalid_args"))
                return

            delay = self.config["delay_between_edit"]
            text = ""
            if args[0] in ('"', "'"):
                end_quote = args.rfind(args[0], 1)
                if end_quote > 0:
                    text = args[1:end_quote]
                    other_args = args[end_quote+1:].strip()
                    if other_args:
                        try:
                            delay = max(1, int(float(other_args)))
                        except ValueError:
                            await utils.answer(message, self.strings("invalid_delay"))
                            return
                else:
                    text = args
            else:
                parts = args.split(maxsplit=1)
                if len(parts) == 2:
                    try:
                        delay = max(1, int(float(parts[0])))
                        text = parts[1].strip('"\'')
                    except ValueError:
                        text = args.strip('"\'')
                else:
                    text = args.strip('"\'')

            if not text:
                await utils.answer(message, self.strings("invalid_args"))
                return
            chat_id = utils.get_chat_id(message)
            if chat_id in self.running_tasks:
                self.running_tasks[chat_id].cancel()
            task = asyncio.create_task(
                self._animate_text(message, text, delay)
            )
            self.running_tasks[chat_id] = task
            task.add_done_callback(lambda _: self.running_tasks.pop(chat_id, None))

        except Exception as e:
            await utils.answer(message, f"❌ Ошибка: {str(e)}")

    async def wordbywordstopcmd(self, message: Message):
        """Остановить все анимации"""
        stopped = False
        for chat_id, task in list(self.running_tasks.items()):
            task.cancel()
            self.running_tasks.pop(chat_id, None)
            stopped = True
        
        if stopped:
            await utils.answer(message, self.strings("stopped"))
        else:
            await utils.answer(message, "ℹ️ Нет активных анимаций для остановки")

    async def _animate_text(self, message: Message, text: str, delay: int):
        try:
            words = text.split()
            current_text = ""
            
            for word in words:
                current_text += f" {word}" if current_text else word
                await utils.answer(message, current_text)
                await asyncio.sleep(delay / 1000)
                
        except asyncio.CancelledError:
            await utils.answer(message, "✅ Анимации остановлены")
        except Exception as e:
            await utils.answer(message, f"❌ Ошибка анимации: {str(e)}")
