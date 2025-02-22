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

from .. import loader, utils
import ast
import operator as op

def safe_eval(expr: str):
    allowed_operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.Pow: op.pow,
        ast.Mod: op.mod,
        ast.FloorDiv: op.floordiv,
    }
    
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in allowed_operators:
                raise TypeError(f"Оператор {node.op} не поддерживается")
            return allowed_operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -_eval(node.operand)
            else:
                raise TypeError("Неподдерживаемый унарный оператор")
        else:
            raise TypeError("Неподдерживаемый тип выражения")
    
    tree = ast.parse(expr, mode='eval')
    return _eval(tree.body)

@loader.tds
class CalculatorMod(loader.Module):
    """Модуль калькулятор."""
    
    strings = {"name": "CalculatorMod"}
    
    async def calccmd(self, message):
        """<выражение>."""
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("Использование: .calc <выражение>")
            return
        try:
            result = safe_eval(args)
        except Exception as e:
            await message.edit(f"🧐Ошибка при вычислении: {e}")
            return
        await message.edit(f"✅Результат: {result}")
