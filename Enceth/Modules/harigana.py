# meta developer: @Enceth
import random
from .. import loader, utils

@loader.tds
class HiraganaQuiz(loader.Module):
    """Тесты для изучения хираганы."""

    strings = {
        "name": "HiraganaQuiz",
        "start_quiz": "Начинаем тест. Введите 'стоп', чтобы закончить.",
        "correct": "Правильно",
        "wrong": "Неправильно. Правильный ответ: {}",
        "stop_quiz": "Тест завершён. Правильных ответов: {}, неправильных: {}.",
    }

    HIRAGANA = {
        "あ": "а", "い": "и", "う": "у", "え": "э", "お": "о",
        "か": "ка", "き": "ки", "く": "ку", "け": "кэ", "こ": "ко",
        "さ": "са", "し": "си", "す": "су", "せ": "сэ", "そ": "со",
        "た": "та", "ち": "ти", "つ": "цу", "て": "тэ", "と": "то",
        "な": "на", "に": "ни", "ぬ": "ну", "ね": "нэ", "の": "но",
        "は": "ха", "ひ": "хи", "ふ": "фу", "へ": "хэ", "ほ": "хо",
        "ま": "ма", "み": "ми", "む": "му", "め": "мэ", "も": "мо",
        "や": "я", "ゆ": "ю", "よ": "ё",
        "ら": "ра", "り": "ри", "る": "ру", "れ": "рэ", "ро": "ро",
        "わ": "ва", "を": "о", "ん": "н",
    }

    def __init__(self):
        self.is_quizzing = False
        self.correct_answers = 0
        self.wrong_answers = 0
        self.current_question = None
        self.quiz_chat_id = None
        self.quiz_user_id = None  

    async def quizcmd(self, message):
        """Начать тест по хирагане"""
        if self.is_quizzing:
            await utils.answer(message, "Тест уже запущен. Чтобы закончить, напишите 'стоп'")
            return

        self.is_quizzing = True
        self.quiz_chat_id = message.chat_id
        self.quiz_user_id = message.from_id  
        self.correct_answers = 0
        self.wrong_answers = 0

        await utils.answer(message, self.strings["start_quiz"])
        await self.ask_question(message)
        
    async def ask_question(self, message):
        """Начать тест"""
        self.current_question = random.choice(list(self.HIRAGANA.items()))
        question = self.current_question[0]
        await utils.answer(message, f"Как читается этот символ? {question}")

    async def watcher(self, message):
        """Обрабатывает ответы пользователя"""
        if not self.is_quizzing or not message.text:
            return

        if message.from_id != self.quiz_user_id:
            return

        if message.chat_id != self.quiz_chat_id:
            return

        answer = message.text.strip().lower()

        if answer == "стоп":
            self.is_quizzing = False
            self.quiz_chat_id = None  
            self.quiz_user_id = None  
            await utils.answer(
                message,
                self.strings["stop_quiz"].format(self.correct_answers, self.wrong_answers),
            )
            return

        if answer == self.current_question[1]:
            self.correct_answers += 1
            await utils.answer(message, self.strings["correct"])
        else:
            self.wrong_answers += 1
            await utils.answer(message, self.strings["wrong"].format(self.current_question[1]))

        await self.ask_question(message)
