#  _____                          
# |_   _|____  ____ _ _ __   ___  
#   | |/ _ \ \/ / _` | '_ \ / _ \ 
#   | | (_) >  < (_| | | | | (_) |
#   |_|\___/_/\_\__,_|_| |_|\___/ 
# meta banner: https://i.ibb.co/Z1RrLnfv/image-9708.jpg                               
# meta developer: @Toxano_Modules

from .. import loader, utils
from telethon.tl.types import Message
import random
import asyncio
import logging

logger = logging.getLogger(__name__)

@loader.tds
class CasinoMod(loader.Module):
    """Модуль казино с виртуальными монетами"""

    strings = {
        "name": "Casino",
        "roulette_title": "🎰 Рулетка",
        "roulette_result": "🎲 Результат: {} ({})",
        "dice_title": "🎲 Четное/нечетное",
        "dice_result": "Выпало: {} ({})",
        "russian_roulette_title": "🔫 Русская рулетка",
        "russian_roulette_result": "Результат: {} ({})",
        "win": "🎉 <b>Вы выиграли {} монет!</b>",
        "lose": "😢 <b>Вы проиграли {} монет</b>",
        "current_balance": "💰 Ваш текущий баланс: {} монет",
        "not_enough_coins": "❌ Недостаточно монет для ставки",
        "min_bet": "❌ Минимальная ставка: 10 монет",
        "invalid_bet": "❌ Неверная сумма ставки. Введите число больше 10",
        "profile": (
            "👤 <b>Профиль игрока</b>\n\n"
            "👾 <b>Никнейм:</b> {}\n"
            "💰 <b>Баланс:</b> {} монет\n"
            "✨ <b>Выиграно всего:</b> {} монет\n"
            "💸 <b>Проиграно всего:</b> {} монет\n"
            "🏆 <b>Рекордный выигрыш:</b> {} монет\n\n"
            "📊 <b>Винрейт:</b> {}%"
        ),
        "spinning": "🎰 Крутим рулетку...",
        "playing_dice": "🎲 Бросаем кости...",
        "shooting": "🔫 *щелчок*",
        "rr_shot": "💀 БАХ! Вы проиграли!",
        "rr_survived": "😅 Вы выжили и выиграли!",
        "dice_number": "🎲 Выпало число: {}",
        "even": "четное",
        "odd": "нечетное",
    }
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "initial_coins",
                300,
                "Начальное количество монет",
                validator=loader.validators.Integer(minimum=100),
            ),
            loader.ConfigValue(
                "max_bet",
                1000000,
                "Максимальная ставка",
                validator=loader.validators.Integer(minimum=100),
            ),
        )

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        # Инициализация данных игрока
        self._coins = self.get("coins", self.config["initial_coins"])
        self._wins = self.get("wins", 0)
        self._losses = self.get("losses", 0)
        self._max_win = self.get("max_win", 0)
        self._games_played = self.get("games_played", 0)
        
    def _save_stats(self):
        """Сохранение статистики в базу данных"""
        self.set("coins", self._coins)
        self.set("wins", self._wins)
        self.set("losses", self._losses)
        self.set("max_win", self._max_win)
        self.set("games_played", self._games_played)

    async def _validate_bet(self, bet: int) -> bool:
        """Проверка валидности ставки"""
        try:
            bet = int(bet)
            if bet < 10:
                return False
            if bet > self._coins:
                return False
            if bet > self.config["max_bet"]:
                return False
            return True
        except ValueError:
            return False

    @loader.command(ru_doc="Играть в рулетку")
    async def roulette(self, message: Message):
        """Play roulette"""
        await self.inline.form(
            message=message,
            text="💰 Введите сумму ставки:",
            reply_markup=[
                [{"text": "Сделать ставку", "input": "Введите сумму ставки:", "handler": self._process_roulette_bet}],
                [{"text": "Отмена", "action": "close"}]
            ],
        )

    async def _process_roulette_bet(self, call, bet: str):
        """Обработка ставки в рулетке"""
        if not await self._validate_bet(bet):
            await call.edit(
                self.strings("invalid_bet"),
                reply_markup=[[{"text": "🔙 Назад", "action": "close"}]],
            )
            return

        bet = int(bet)
        
        colors = {
            "red": "🔴",
            "black": "⚫️",
            "green": "💚",
        }

        await call.edit(
            "🎰 Выберите цвет:",
            reply_markup=[
                [
                    {"text": f"{colors['red']} Красное (x2)", "callback": self._process_roulette_game, "args": (bet, "red")},
                    {"text": f"{colors['black']} Черное (x2)", "callback": self._process_roulette_game, "args": (bet, "black")},
                ],
                [{"text": f"{colors['green']} Зеро (x14)", "callback": self._process_roulette_game, "args": (bet, "green")}],
                [{"text": "🔙 Назад", "action": "close"}],
            ],
        )

    async def _process_roulette_game(self, call, bet: int, color: str):
        """Обработка игры в рулетку"""
        await call.edit(self.strings("spinning"))
        await asyncio.sleep(3)

        result = random.choice(["red", "black"] * 18 + ["green"])
        number = random.randint(0, 36)

        multiplier = 14 if color == "green" else 2
        won = result == color

        if won:
            win_amount = bet * multiplier
            self._coins += win_amount
            self._wins += win_amount
            self._max_win = max(self._max_win, win_amount)
            result_text = self.strings("win").format(win_amount)
        else:
            self._coins -= bet
            self._losses += bet
            result_text = self.strings("lose").format(bet)

        self._games_played += 1
        self._save_stats()

        await call.edit(
            f"{result_text}\n"
            f"{self.strings('roulette_result').format(number, result)}\n"
            f"{self.strings('current_balance').format(self._coins)}",
            reply_markup=[
                [{"text": "🔄 Играть снова", "callback": self.roulette}],
                [{"text": "🔙 Выход", "action": "close"}],
            ],
        )

    @loader.command(ru_doc="Посмотреть профиль")
    async def profile(self, message: Message):
        """View casino profile"""
        winrate = round(self._wins / max(1, self._games_played) * 100, 2)
        
        await self.inline.form(
            message=message,
            text=self.strings("profile").format(
                message.sender.first_name,
                self._coins,
                self._wins,
                self._losses,
                self._max_win,
                winrate
            ),
            reply_markup=[
                [
                    {"text": "🎰 Рулетка", "callback": self.roulette},
                    {"text": "🎲 Кости", "callback": self.dice},
                ],
                [{"text": "🔫 Русская рулетка", "callback": self.russian_roulette}],
                [{"text": "🔙 Закрыть", "action": "close"}],
            ],
        )
    @loader.command(ru_doc="Игра в четное/нечетное")
    async def dice(self, message: Message):
        """Play even/odd dice game"""
        await self.inline.form(
            message=message,
            text="💰 Введите сумму ставки:",
            reply_markup=[
                [{"text": "Сделать ставку", "input": "Введите сумму ставки:", "handler": self._process_dice_bet}],
                [{"text": "Отмена", "action": "close"}]
            ],
        )

    async def _process_dice_bet(self, call, bet: str):
        """Обработка ставки в игре четное/нечетное"""
        if not await self._validate_bet(bet):
            await call.edit(
                self.strings("invalid_bet"),
                reply_markup=[[{"text": "🔙 Назад", "action": "close"}]],
            )
            return

        bet = int(bet)
        
        await call.edit(
            "🎲 Выберите ставку:",
            reply_markup=[
                [
                    {"text": "2️⃣ Четное (x2)", "callback": self._process_dice_game, "args": (bet, "even")},
                    {"text": "1️⃣ Нечетное (x2)", "callback": self._process_dice_game, "args": (bet, "odd")},
                ],
                [{"text": "🔙 Назад", "action": "close"}],
            ],
        )

    async def _process_dice_game(self, call, bet: int, choice: str):
        """Обработка игры в четное/нечетное"""
        await call.edit(self.strings("playing_dice"))
        await asyncio.sleep(2)

        result = random.randint(1, 6)
        is_even = result % 2 == 0
        result_type = "even" if is_even else "odd"
        
        won = (choice == "even" and is_even) or (choice == "odd" and not is_even)
        
        if won:
            win_amount = bet * 2
            self._coins += win_amount
            self._wins += win_amount
            self._max_win = max(self._max_win, win_amount)
            result_text = self.strings("win").format(win_amount)
        else:
            self._coins -= bet
            self._losses += bet
            result_text = self.strings("lose").format(bet)

        self._games_played += 1
        self._save_stats()

        await call.edit(
            f"{result_text}\n"
            f"🎲 Выпало число: {result} ({'четное' if is_even else 'нечетное'})\n"
            f"{self.strings('current_balance').format(self._coins)}",
            reply_markup=[
                [{"text": "🔄 Играть снова", "callback": self.dice}],
                [{"text": "🔙 Выход", "action": "close"}],
            ],
        )

    @loader.command(ru_doc="Русская рулетка")
    async def russian_roulette(self, message: Message):
        """Play Russian roulette"""
        await self.inline.form(
            message=message,
            text="💰 Введите сумму ставки:",
            reply_markup=[
                [{"text": "Сделать ставку", "input": "Введите сумму ставки:", "handler": self._process_rr_bet}],
                [{"text": "Отмена", "action": "close"}]
            ],
        )

    async def _process_rr_bet(self, call, bet: str):
        """Обработка ставки в русской рулетке"""
        if not await self._validate_bet(bet):
            await call.edit(
                self.strings("invalid_bet"),
                reply_markup=[[{"text": "🔙 Назад", "action": "close"}]],
            )
            return

        bet = int(bet)
        
        await call.edit(
            "🔫 Выберите количество патронов:",
            reply_markup=[
                [
                    {"text": "1 патрон (x2)", "callback": self._process_rr_game, "args": (bet, 1)},
                    {"text": "2 патрона (x3)", "callback": self._process_rr_game, "args": (bet, 2)},
                ],
                [
                    {"text": "3 патрона (x4)", "callback": self._process_rr_game, "args": (bet, 3)},
                    {"text": "4 патрона (x5)", "callback": self._process_rr_game, "args": (bet, 4)},
                ],
                [
                    {"text": "5 патронов (x6)", "callback": self._process_rr_game, "args": (bet, 5)},
                ],
                [{"text": "🔙 Назад", "action": "close"}],
            ],
        )

    async def _process_rr_game(self, call, bet: int, bullets: int):
        """Обработка игры в русскую рулетку"""
        await call.edit(self.strings("shooting"))
        await asyncio.sleep(2)

        # Шанс выживания уменьшается с количеством патронов
        survived = random.randint(1, 6) > bullets
        multiplier = bullets + 1  # Множитель зависит от количества патронов

        if survived:
            win_amount = bet * multiplier
            self._coins += win_amount
            self._wins += win_amount
            self._max_win = max(self._max_win, win_amount)
            result_text = (
                f"😅 Вы выжили!\n"
                f"{self.strings('win').format(win_amount)}"
            )
        else:
            self._coins -= bet
            self._losses += bet
            result_text = (
                f"💀 Выстрел!\n"
                f"{self.strings('lose').format(bet)}"
            )

        self._games_played += 1
        self._save_stats()

        await call.edit(
            f"{result_text}\n"
            f"{self.strings('current_balance').format(self._coins)}",
            reply_markup=[
                [{"text": "🔄 Играть снова", "callback": self.russian_roulette}],
                [{"text": "🔙 Выход", "action": "close"}],
            ],
        )
