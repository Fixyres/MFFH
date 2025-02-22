# ------------------------------------------------------------
# Module: QuizAI
# Description: Игра-викторина с разными темами и сложностями
# Author: @kmodules
# ------------------------------------------------------------
# Licensed under the GNU AGPLv3
# https:/www.gnu.org/licenses/agpl-3.0.html
# ------------------------------------------------------------
# Author: @MeKsenon
# Commands: .quiz
# scope: hikka_only
# meta banner: https://i.ibb.co/NsMcJVJ/6116dddf-38f7-4bad-9b69-10c1e3c19fa5.jpg
# meta developer: @kmodules
# ------------------------------------------------------------

import asyncio
import json
import random
import requests
from .. import loader, utils
from telethon.tl.types import Message

version = (1, 0, 2)

@loader.tds
class QuizGameMod(loader.Module):
    """Игра-викторина с разными темами и сложностями"""

    strings = {
        "name": "QuizAI",
        "no_api_key": "❌ Установите API-Key!\nВозьмите свой API-Key отсюда: https://aistudio.google.com\nДалее введите: .fcfg QuizAI api_key КЛЮЧ",
        "invalid_args": '❌ Используйте: .quiz -t "тема" -d <сложность> -m <stable/fast>\nПример: .quiz -t "Minecraft" -d easy -m stable',
        "invalid_difficulty": "❌ Сложность может быть: easy, normal, hard, extreme или impossible",
        "invalid_mode": "❌ Режим может быть: stable или fast",
        "generating_stable": """┏ 🔄 Генерирую нейро-викторину...
┃
┗ 🔥 Модель: gemini-1.5-pro-0827, будет немного долго.

🕰️ Вам не хочется ждать? Поменяйте тэг -m на -m fast""",
        "generating_fast": """┏ 🔄 Генерирую нейро-викторину...
┃
┗ 🔥 Модель: gemini-1.5-flash-0827, будет быстро.

🤖 Хотите стабильные ответы? Поменяйте тэг -m на -m stable""",
        "api_error": "😔 Ошибка при получении данных от API. Проверьте API-Key и повторите попытку.",
        "json_error": "😔 Ошибка при обработке данных от API. Проверьте ответ от API.",
        "no_questions": "😔 Закончились вопросы.",
        "quiz_completed": """┏ 🎯 Викторина завершена!
┃
┣ 📊 Ваша статистика:
┣ ✅ Правильных ответов: {}
┣ ❌ Неправильных ответов: {}
┣ 📈 Точность: {:.1f}%
┃
┗ 🔄 Новая игра: .quiz""",
        "correct_answer": """┏ ✅ Правильно!
┗ Ответ: {}

┏ ❓ Вопрос: {}
┣ 📑 Сложность: {}
┣ 📊 Прогресс: {}/10
┗ ⚙️ Ответы:""",
        "incorrect_answer": """┏ ❌ Неправильно!
┗ Правильный ответ: {}

┏ ❓ Вопрос: {}
┣ 📑 Сложность: {}
┣ 📊 Прогресс: {}/10
┗ ⚙️ Ответы:"""
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_key",
                "",
                lambda: "Возьмите свой API-Key отсюда: https://aistudio.google.com",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )
    
    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._quiz_data = None
        self._used_questions = set()
        self.correct_answers = 0
        self.total_questions = 0
        
    @loader.command()
    async def quiz(self, message: Message):
        """Начать викторину
        Аргументы: -t "тема" -d <easy/normal/hard/impossible> -m <stable/fast>
        Пример: .quiz -t "Minecraft" -d easy -m stable"""
        
        if not self.config["api_key"]:
            await utils.answer(message, self.strings["no_api_key"])
            return
        
        args = utils.get_args_raw(message)
        
        try:
            parts = args.split('" -')
            theme_part = parts[0].split('-t "')[1]
            args_parts = parts[1].split()
            difficulty = args_parts[1].lower()
            mode = args_parts[3].lower() if len(args_parts) > 3 else "stable"
        except:
            await utils.answer(message, self.strings["invalid_args"])
            return
            
        if difficulty not in ["easy", "normal", "hard", "extreme", "impossible"]:
            await utils.answer(message, self.strings["invalid_difficulty"])
            return

        if mode not in ["stable", "fast"]:
            await utils.answer(message, self.strings["invalid_mode"])
            return

        model = "gemini-1.5-pro-exp-0827" if mode == "stable" else "gemini-1.5-flash-exp-0827"
        
        await utils.answer(message, self.strings["generating_stable" if mode == "stable" else "generating_fast"])
        
        system_prompt = f'''You are a quiz generator. Generate 10 very accurate and specific questions about {theme_part}.

Rules:
1. Questions must be specifically about {theme_part}
2. All answers must be factually correct
3. Wrong answers must be plausible but clearly incorrect
4. Questions difficulty should match {difficulty} level
5. No duplicates or similar questions
6. Questions should test real knowledge about {theme_part}

Return exactly this JSON format:
{{
  "quiz": {{
    "quiz_1": {{
      "question": "your specific question",
      "quiz_theme": "{theme_part}",
      "difficulty": "{difficulty}",
      "answer": "correct answer",
      "not_correct_answers": [
        "wrong answer 1",
        "wrong answer 2", 
        "wrong answer 3"
      ]
    }},
    "quiz_2": {{...}},
    ...up to quiz_10
  }}
}}

Return ONLY valid JSON, no other text. Default: Russian language. Generate on russian language, if no on this language...'''
        result = self.gemini_request(system_prompt, model)
        if not result:
             await utils.answer(message, self.strings["api_error"])
             return
        try:
            self._quiz_data = json.loads(result)
        except json.JSONDecodeError:
             await utils.answer(message, self.strings["json_error"])
             return
        self._used_questions = set()
        self.correct_answers = 0
        self.total_questions = 0
        
        await self.show_question(message)
        
    async def get_unused_question(self):
        available_questions = [q for q in self._quiz_data["quiz"].values() 
                             if q["question"] not in self._used_questions]
            
        if not available_questions:
            return None
        
        question = random.choice(available_questions)
        self._used_questions.add(question["question"])
        return question
        
    async def show_question(self, message):
        current_quiz = await self.get_unused_question()
        
        if not current_quiz:
            await utils.answer(message, self.strings["no_questions"])
            return
        
        answers = current_quiz["not_correct_answers"] + [current_quiz["answer"]]
        random.shuffle(answers)
        
        buttons = []
        for answer in answers:
            buttons.append([{
                "text": answer,
                "callback": self.quiz_callback,
                "args": (answer == current_quiz["answer"], current_quiz)
            }])
            
        await self.inline.form(
            text=f"""┏ ❓ Вопрос: {current_quiz["question"]}
┣ 📑 Сложность: {current_quiz["difficulty"]}
┣ 📊 Прогресс: {self.total_questions}/10
┗ ⚙️ Ответы:""",
            message=message,
            reply_markup=buttons
        )
    
    async def quiz_callback(self, call, is_correct: bool, current_quiz: dict):
        self.total_questions += 1
        if is_correct:
            self.correct_answers += 1
            
        if self.total_questions >= 10:
            accuracy = (self.correct_answers / 10) * 100
            await call.edit(
                text=self.strings["quiz_completed"].format(
                    self.correct_answers,
                    10 - self.correct_answers,
                    accuracy
                )
            )
            return
            
        next_quiz = await self.get_unused_question()
        if not next_quiz:
            accuracy = (self.correct_answers / self.total_questions) * 100
            await call.edit(
                text=self.strings["quiz_completed"].format(
                    self.correct_answers,
                    self.total_questions - self.correct_answers,
                    accuracy
                )
            )
            return
        answers = next_quiz["not_correct_answers"] + [next_quiz["answer"]]
        random.shuffle(answers)
        
        buttons = []
        for answer in answers:
            buttons.append([{
                "text": answer,
                "callback": self.quiz_callback,
                "args": (answer == next_quiz["answer"], next_quiz)
            }])

        if is_correct:
            text = self.strings["correct_answer"].format(
                current_quiz["answer"],
                next_quiz["question"],
                next_quiz["difficulty"],
                self.total_questions
            )
        else:
            text = self.strings["incorrect_answer"].format(
                current_quiz["answer"],
                next_quiz["question"],
                next_quiz["difficulty"],
                self.total_questions
            )
            
        await call.edit(
            text=text,
            reply_markup=buttons
        )
    
    def gemini_request(self, prompt, model):
        GEMINI_API_KEY = self.config["api_key"]
        BASE_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts":[
                    {"text": prompt}
                ]
            }],
            "generationConfig": {
                "temperature": 0.0,
                "candidateCount": 1
            }
        }

        proxies = {
            'http': 'http://nkzeuopd:od0ij6ste4xi@107.172.163.27:6543',
            'https': 'http://nkzeuopd:od0ij6ste4xi@107.172.163.27:6543'
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                json=data,
                proxies=proxies,
                verify=False,
                timeout=60
            )
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException as e:
            return None
        except (KeyError, json.JSONDecodeError):
            return None
