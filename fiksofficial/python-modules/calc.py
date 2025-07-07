#         ______     ___  ___          _       _      
#    ____ | ___ \    |  \/  |         | |     | |     
#   / __ \| |_/ /   _| .  . | ___   __| |_   _| | ___ 
#  / / _` |  __/ | | | |\/| |/ _ \ / _` | | | | |/ _ \
# | | (_| | |  | |_| | |  | | (_) | (_| | |_| | |  __/
#  \ \__,_\_|   \__, \_|  |_/\___/ \__,_|\__,_|_|\___|
#   \____/       __/ |                                
#               |___/                                 

# На модуль распространяется лицензия "GNU General Public License v3.0"
# https://github.com/all-licenses/GNU-General-Public-License-v3.0

# meta developer: @pymodule

from .. import loader, utils
import math
import ast

from ..inline.types import InlineQuery


@loader.tds
class CalcMod(loader.Module):
    """Калькулятор."""
    strings = {
        "name": "Calc",
        "no_expr": "🚫 Please provide a math expression to evaluate.",
        "calc_result": "🧮 Expression: <code>{expr}</code>\n📥 Result: <code>{result}</code>",
        "inline_title": "🧮 Result for: {expr}",
        "inline_desc": "Click to paste the result: {result}",
    }

    strings_ru = {
        "no_expr": "🚫 Укажи математическое выражение для вычисления.",
        "calc_result": "🧮 Выражение: <code>{expr}</code>\n📥 Ответ: <code>{result}</code>",
        "inline_title": "🧮 Результат для: {expr}",
        "inline_desc": "Нажми, чтобы вставить: {result}",
    }

    def __init__(self):
        self._math_context = {
            k: getattr(math, k)
            for k in dir(math)
            if not k.startswith("__")
        }
        self._math_context.update({
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
        })

    def safe_eval(self, expr: str):
        try:
            tree = ast.parse(expr, mode="eval")
            for node in ast.walk(tree):
                if not isinstance(node, (
                    ast.Expression, ast.Call, ast.Name, ast.Load,
                    ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
                    ast.Pow, ast.USub, ast.UAdd, ast.FloorDiv
                )):
                    return "🚫 Invalid expression"
            return eval(compile(tree, "<calc>", "eval"), {"__builtins__": {}}, self._math_context)
        except Exception as e:
            return f"🚫 Error: {e}"

    @loader.command(doc="[Math Expression] - Calculate a math expression", ru_doc="[Выражение] - Вычислить выражение")
    async def calc(self, message):
        expr = utils.get_args_raw(message)
        if not expr:
            return await utils.answer(message, self.strings("no_expr"))

        result = self.safe_eval(expr)
        await utils.answer(message, self.strings("calc_result").format(expr=expr, result=result))

    @loader.inline_everyone
    async def calc_inline_handler(self, query: InlineQuery):
        """[Math Expression] - Calculate a math expression"""
        expr = query.args
        if not expr:
            return [
                {
                    "title": "🧮 Calc",
                    "description": "Введите выражение, например: 2+2 или sin(pi/2)",
                    "message": "🔢 Просто введи математическое выражение после @бота",
                }
            ]

        result = self.safe_eval(expr)
        return [
            {
                "title": self.strings("inline_title").format(expr=expr),
                "description": self.strings("inline_desc").format(result=result),
                "message": self.strings("calc_result").format(expr=expr, result=result),
            }
        ]