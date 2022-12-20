from datetime import date
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from Model.dbContext import *
from Model.categoria import *
from Model.timePeriod import *
from linq import *

class AppData(QWidget):

    signalAccountsUpdate = pyqtSignal()

    signalGoalsUpdate = pyqtSignal()

    signalTransactionsUpdate = pyqtSignal()

    signalCategoriesUpdate = pyqtSignal()

    signalBalanceUpdate = pyqtSignal()

    signalGraphUpdate = pyqtSignal(TimePeriod)

    def __init__(self, dbPath: str):
        super().__init__()

        self.dbContext = DBContext(dbPath)
        
        self.accounts = {}

        self.update_accounts_list()

        self.selectedAccountId = self.get_first_account().id

        self.selectedDate = date.today()

        self.timePeriod = TimePeriod.Month

        self.timePeriods = {
            TimePeriod.Month : lambda t: t.registDate.year == self.selectedDate.year and t.registDate.month == self.selectedDate.month,
            TimePeriod.Day: lambda t: t.registDate.year == self.selectedDate.year and t.registDate.month == self.selectedDate.month and t.registDate.day == self.selectedDate.day,
            TimePeriod.Year: lambda t: t.registDate.year == self.selectedDate.year
            }

        self.goals = []

        self.categories = []

        self.selectedCategoria = 0 # All

        self.transactions = []

        self.slot_update_account_id(self.selectedAccountId)

#---Filters---------------------------------------------------

    def filter_for_date(self):
        self.transactions = Linq.to_list(
            Linq.where(
                self.transactions,
                self.timePeriods[self.timePeriod])
        )

    def filter_for_categoria(self):
        if self.selectedCategoria != 0:
            self.transactions = Linq.to_list(
                Linq.where(
                    self.transactions, 
                    lambda t: t.categoriaId == self.selectedCategoria)
            )


    def slot_filter_for_date(self, newDate: date, newTimePeriod: TimePeriod):
        self.selectedDate = newDate
        self.timePeriod = newTimePeriod

        self.update_transactions_list()

    def slot_filter_for_categoria(self, categoriaId: int):
        self.selectedCategoria = categoriaId

        self.update_transactions_list()

#---Balance---------------------------------------------------

    def get_balance(self):
        return self.get_balance_by_account_id(self.selectedAccountId)

    def get_balance_by_account_id(self, accountId: int):
        for acc in self.accounts.values():
            if acc["account"].id == accountId:
                return acc["balance"]
        return 0

    def update_balance(self, cash: float):
        self.accounts[self.selectedAccountId]["balance"] += cash

        self.signalBalanceUpdate.emit()

#---Categories---------------------------------------------------

    def get_selected_categoria(self):
        return self.selectedCategoria

    def get_categories(self):
        return Linq.to_list(Linq.select(self.categories, lambda c: c["categoria"]))

    def get_categories_with_expense(self):
        return self.categories

    def get_categoria_by_name(self, name: str):
        for cat in self.categories:
            if cat["categoria"].name == name:
                return cat["categoria"]

    def add_categoria(self, name: str):
        self.dbContext.add_categoria(self.selectedAccountId, name)

        self.update_categorias_list()

    def remove_categoria_by_id(self, id: int):
        categoriaExpenses = 0

        for cat in self.categories:
            if cat["categoria"].id == id:
                categoriaExpenses = cat["expenses"]
                break

        self.dbContext.remove_categoria_by_id_with_transactions(id)

        self.update_transactions_list()
        self.update_categorias_list()
        self.update_balance(-categoriaExpenses)

    def update_categorias_list(self):
        self.categories.clear()

        categorias = Linq.where(self.dbContext.get_categories(), lambda c: c.accountId == self.selectedAccountId)

        for cat in categorias:
            self.categories.append(
                {
                    "categoria": cat,
                    "expenses": 
                    Linq.sum(
                        Linq.where(
                            self.transactions,
                            lambda t: t.categoriaId == cat.id
                        ),
                        lambda t: t.payment
                    )
            })

        self.signalCategoriesUpdate.emit()
        self.signalGraphUpdate.emit(self.timePeriod)

#---Transactions---------------------------------------------------

    def get_transactions(self):
        return self.transactions

    def slot_add_transaction(self, categoriaId: int, registDate: date, payment: float):

        strDate = f"{registDate.day}/{registDate.month}/{registDate.year}"

        self.dbContext.add_transaction(self.selectedAccountId, categoriaId, strDate, payment)

        self.update_balance(payment)

        self.update_transactions_list()

        self.update_categorias_list()

    def slot_delete_transaction(self, id: int):
        self.dbContext.remove_transaction(id)

        self.update_accounts_list()

        self.update_transactions_list()

        self.update_categorias_list()

    def update_transactions_list(self):
        self.transactions.clear()

        self.transactions = Linq.to_list(
            Linq.where(self.dbContext.get_transactions(), lambda t: t.accountId == self.selectedAccountId)
        )

        self.filter_for_date()

        self.filter_for_categoria()

        self.update_categorias_list()

        self.signalTransactionsUpdate.emit()
        self.signalGraphUpdate.emit(self.timePeriod)

#---Goal---------------------------------------------------
    
    def get_goals(self):
        return self.goals

    def add_goal(self, name: str, moneyAmount: float, finishMoneyAmount: float):
        self.dbContext.add_goal(self.selectedAccountId, name, moneyAmount, finishMoneyAmount)

        self.update_goals_list()

    def remove_goal_by_id(self, id: int):
        self.dbContext.remove_goal_by_id(id)

        self.update_goals_list()

    def update_goal_by_id(self, goalId: int, cash: float):
        self.dbContext.update_goal_by_id(goalId, cash)

        self.update_goals_list()

    def update_goals_list(self):
        self.goals = Linq.to_list(
            Linq.where(
                self.dbContext.get_goals(), 
                lambda g: g.accountId == self.selectedAccountId
            )
        )

        self.signalGoalsUpdate.emit()

#---Account------------------------------------------------

    def get_account_id(self):
        return self.selectedAccountId

    def get_first_account(self):
        for acc in self.accounts.values():
            return acc["account"]

    def get_accounts(self):
        return Linq.to_list(Linq.select(self.accounts.values(), lambda a: a["account"]))

    def add_account(self, accountName: str):
        self.dbContext.add_account(accountName)

        self.update_accounts_list()

    def remove_account_by_id(self, id: int):
        self.dbContext.remove_account_by_id(id)

        self.update_accounts_list()

        if self.selectedAccountId == id:
            self.slot_update_account_id(self.get_first_account().id)

    def update_accounts_list(self):
        self.accounts.clear()

        accounts = self.dbContext.get_accounts()

        if len(accounts) == 0:
            self.add_account("Cash")
            accounts = self.dbContext.get_accounts()

        for acc in accounts:
            self.accounts[acc.id] = {"account": acc, "balance": Linq.sum(
                Linq.where(
                    self.dbContext.get_transactions(),
                    lambda t: t.accountId == acc.id
                ),
                lambda t: t.payment
            )}

        self.signalAccountsUpdate.emit()
        self.signalBalanceUpdate.emit()

    def slot_update_account_id(self, accountId: int):

        # if accountId not in Linq.to_list(Linq.select(self.accounts, lambda a: a["account"].id)):
        #     return

        self.selectedAccountId = accountId

        self.signalBalanceUpdate.emit()

        self.update_transactions_list()
        self.update_categorias_list()
        self.update_goals_list()
