# meta developer:@DieModules

from .. import loader, utils
from telethon.tl.custom import Message
import time

@loader.tds
class FinanceModule(loader.Module):
    """Модуль для учета финансов"""
    strings = {
        "name": "FinanceModule",
        "balance": "<b>Текущий баланс:</b> {}",
        "income_added": "<emoji document_id=5393360308133699762>✅</emoji> <b>Доход добавлен:</b> {}",
        "expense_added": "<emoji document_id=5393360308133699762>✅</emoji> <b>Расход добавлен:</b> {}",
        "invalid_amount": "<emoji document_id=5393110903677790336>❎</emoji> <b>Неверная сумма.</b>",
        "insufficient_funds": "<b>Недостаточно средств для этой операции.</b>",
        "actions": "<b>История счета:</b>\n{}"
    }

    async def client_ready(self, client, db):
        self.db = db
        self.db.set(self.strings["name"], "history", [])

    async def balancecmd(self, message: Message):
        """Показать текущий баланс"""
        balance = self.db.get(self.strings["name"], "balance", 0)
        await utils.answer(message, self.strings["balance"].format(balance))

    async def incomecmd(self, message: Message):
        """Добавить доход: .income сумма"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["invalid_amount"])
            return
        try:
            amount = float(args)
        except ValueError:
            await utils.answer(message, self.strings["invalid_amount"])
            return
        balance = self.db.get(self.strings["name"], "balance", 0)
        balance += amount
        self.db.set(self.strings["name"], "balance", balance)
        history = self.db.get(self.strings["name"], "history", [])
        history.append(f"<emoji document_id=5373001317042101552>📈</emoji> <b>Доходы</b>:\n{time.strftime('%Y-%m-%d %H:%M:%S')} +{amount}")
        self.db.set(self.strings["name"], "history", history)
        await utils.answer(message, self.strings["income_added"].format(amount))

    async def expensecmd(self, message: Message):
        """Добавить расход: .expense сумма"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["invalid_amount"])
            return
        try:
            amount = float(args)
        except ValueError:
            await utils.answer(message, self.strings["invalid_amount"])
            return
        balance = self.db.get(self.strings["name"], "balance", 0)
        if balance - amount < 0:
            await utils.answer(message, self.strings["insufficient_funds"])
            return
        balance -= amount
        self.db.set(self.strings["name"], "balance", balance)
        history = self.db.get(self.strings["name"], "history", [])
        history.append(f"<emoji document_id=5361748661640372834>📉</emoji> <b>Расходы:</b>\n{time.strftime('%Y-%m-%d %H:%M:%S')} -{amount}")
        self.db.set(self.strings["name"], "history", history)
        await utils.answer(message, self.strings["expense_added"].format(amount))

    async def actionscmd(self, message: Message):
        """Показать историю транзакций"""
        history = self.db.get(self.strings["name"], "history", [])
        actions_str = "\n".join(history) if history else "История счета пуста."
        await utils.answer(message, self.strings["actions"].format(actions_str))
        