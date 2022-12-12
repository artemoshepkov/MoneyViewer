from Model.db import *
import typing as t
from Model.transaction import *
from Model.goal import *
from Model.account import *
from Model.categoria import *
from linq import *

from datetime import date, datetime

class DBContext:
    def __init__(self, database_name: str) -> None:
        self.db = DB(database_name=database_name)

#----------------------------------------------------------

    def get_categories(self):
        command = "SELECT * FROM categoria"

        cursor = self.db.execute(command)

        categories = []

        for tuple in cursor:
            categories.append(Categoria(tuple[0], tuple[1], tuple[2]))

        return categories

    def add_categoria(self, accountId: int, name: str):
        command = "INSERT INTO categoria (account_id, name) VALUES (?, ?)"

        self.db.execute(command, (accountId, name,))

    def remove_categoria_by_id_with_transactions(self, id: int):
        command = f"DELETE FROM categoria WHERE id = {id}"

        self.db.execute(command)

        self.remove_transactions_by_categoria_id(id)

    def remove_categories_by_account_id(self, accountId: int):
        command = f"DELETE FROM categoria WHERE account_id = {accountId}"

        self.db.execute(command)

#----------------------------------------------------------

    def get_transactions(self):
        command = "SELECT * FROM transact"

        cursor = self.db.execute(command)

        transactions = []

        for tuple in cursor:
            transactions.append(Transaction(tuple[0], tuple[1], tuple[2], datetime.strptime(tuple[3], "%d/%m/%Y"), tuple[4]))

        return transactions

    def add_transaction(self, accountId: int, categoriaId: int, registDate: str, payment: float) -> None:
        command = "INSERT INTO transact (account_id, categoria_id, date, payment) VALUES (?, ?, ?, ?)"

        self.db.execute(command, (accountId, categoriaId, registDate, payment,))

    def remove_transaction(self, id: int) -> None:
        command = f"DELETE FROM transact WHERE id = {id}"

        self.db.execute(command)

    def remove_transactions_by_account_id(self, accountId: int):
        command = f"DELETE FROM transact WHERE account_id = {accountId}"

        self.db.execute(command)

    def remove_transactions_by_categoria_id(self, categoriaId: int):
        command = f"DELETE FROM transact WHERE categoria_id = {categoriaId}"

        self.db.execute(command)
#----------------------------------------------------------

    def get_goals(self):
        command = "SELECT * FROM goal"

        cursor = self.db.execute(command)

        goals = []

        for tuple in cursor:
            goals.append(Goal(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4]))

        return goals

    def add_goal(self, accountId: int, name: str, moneyAmount: float, finishMoneyAmount: float):
        command = "INSERT INTO goal (account_id, name, money_amount, finish_money_amount) VALUES (?, ?, ?, ?)"

        self.db.execute(command, (accountId, name, moneyAmount, finishMoneyAmount,))

    def remove_goal_by_id(self, id: int):
        command = f"DELETE FROM goal WHERE id = {id}"

        self.db.execute(command)

    def remove_goals_by_account_id(self, accountId: int):
        command = f"DELETE FROM goal WHERE account_id = {accountId}"

        self.db.execute(command)

    def update_goal_by_id(self, id: int, newCash: float):
        command = f"UPDATE goal SET money_amount = money_amount + {newCash} WHERE id = {id}"

        self.db.execute(command)

#----------------------------------------------------------

    def get_accounts(self):
        command = "SELECT * FROM account;"

        cursor = self.db.execute(command)

        accounts = []

        for tuple in cursor:
            accounts.append(Account(tuple[0], tuple[1]))

        return accounts

    def add_account(self, name: str):
        command = "INSERT INTO account (name) VALUES (?)"

        self.db.execute(command, (name,))

    def remove_account_by_id(self, id: int):
        command = f"DELETE FROM account WHERE id = {id}"

        self.db.execute(command)

        self.remove_goals_by_account_id(id)

        self.remove_transactions_by_account_id(id)

        self.remove_categories_by_account_id(id)

        


        


    