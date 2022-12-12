from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QSize, pyqtSignal

from Model.dbContext import *
from dlgInputWindow import *
from dlgGoalWindow import *
from linq import *

from Model.applicationData import *

class MyQListWidgetItem(QListWidgetItem):
    def __init__(self, id: int,text: str = ""):
        super().__init__(text)

        self.id = id

class AccoountsGoalsWindow(QWidget):
    signalSelectedAccount = pyqtSignal(int)

    def __init__(self, parent, appData: AppData):
        super().__init__(parent)

        self.appData = appData

        self.signalSelectedAccount.connect(self.appData.slot_update_account_id)

        self.appData.signalAccountsUpdate.connect(self.slot_update_accounts_list_widget)

        self.appData.signalBalanceUpdate.connect(self.slot_update_accounts_list_widget)

        self.appData.signalGoalsUpdate.connect(self.slot_update_goals_list_widget)

        self.itemsSize = QSize(50, 50)

        self.defultColorText = Qt.GlobalColor.black
        self.selectedAccountColorText = Qt.GlobalColor.red

        self.initUI()
    

    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        labelAccounts = QLabel("Accounts")
        layout.addWidget(labelAccounts)
        
        self.listWidgetAccounts = QListWidget()
        self.listWidgetAccounts.itemDoubleClicked.connect(self.slot_select_account)
        layout.addWidget(self.listWidgetAccounts)

        self.slot_update_accounts_list_widget()

        labelGoals = QLabel("Goals")
        layout.addWidget(labelGoals)

        self.listWidgetGoals = QListWidget()
        self.listWidgetGoals.itemDoubleClicked.connect(self.slot_add_money_to_goal)
        layout.addWidget(self.listWidgetGoals)

        self.slot_update_goals_list_widget()

    def add_button_to_list_widget(self, listWidget: QListWidget, event):
        buttonAddAccount = QPushButton("+")
        buttonAddAccount.clicked.connect(event)        
        
        itemLayout = QHBoxLayout()
        itemLayout.addWidget(buttonAddAccount)

        itemWidget  = QWidget()
        itemWidget.setLayout(itemLayout)
        self.itemsSize = itemWidget.sizeHint()

        item = QListWidgetItem()
        item.setSizeHint(self.itemsSize)

        listWidget.addItem(item)
        listWidget.setItemWidget(item, itemWidget)

    def slot_update_accounts_list_widget(self):
        self.listWidgetAccounts.clear()

        for account in self.appData.get_accounts():
            itemLayout = QHBoxLayout()

            itemLabel = QLabel(str(account) + "\t" + str(self.appData.get_balance_by_account_id(account.id)))
            itemLayout.addWidget(itemLabel)

            buttonDelete = QPushButton("-")
            buttonDelete.clicked.connect(self.slot_delete_account(account.id))
            itemLayout.addWidget(buttonDelete)

            itemWidget = QWidget()
            itemWidget.setLayout(itemLayout)

            newItem = MyQListWidgetItem(account.id)
            newItem.setSizeHint(self.itemsSize)
            self.listWidgetAccounts.addItem(newItem)
            self.listWidgetAccounts.setItemWidget(newItem, itemWidget)

        for i in range(len(self.listWidgetAccounts)):
            if self.listWidgetAccounts.item(i) == self.appData.get_account_id():
                self.listWidgetAccounts.item(i).setForeground(Qt.GlobalColor.red)

        # self.listWidgetAccounts.item().setForeground(Qt.GlobalColor.red)

        self.add_button_to_list_widget(self.listWidgetAccounts, self.slot_add_account)

    def slot_update_goals_list_widget(self):
        self.listWidgetGoals.clear()

        for goal in self.appData.get_goals():
                itemLayout = QHBoxLayout()

                itemLabel = QLabel(str(goal))
                itemLayout.addWidget(itemLabel)
                
                progressBar = QProgressBar()
                progressBar.setMinimum(0)
                progressBar.setMaximum(goal.finishMoneyAmount)

                if goal.moneyAmount > goal.finishMoneyAmount:
                    progressBar.setValue(goal.finishMoneyAmount)
                else:
                    progressBar.setValue(goal.moneyAmount)
                itemLayout.addWidget(progressBar)

                buttonDelete = QPushButton("-")
                buttonDelete.clicked.connect(self.slot_delete_goal(goal.id))
                itemLayout.addWidget(buttonDelete)

                itemWidget = QWidget()
                itemWidget.setLayout(itemLayout)

                newItem = MyQListWidgetItem(goal.id)
                newItem.setSizeHint(self.itemsSize)
                self.listWidgetGoals.addItem(newItem)
                self.listWidgetGoals.setItemWidget(newItem, itemWidget)

        self.add_button_to_list_widget(self.listWidgetGoals, self.slot_add_goal)

    def add_item_to_list_widget(self, listWidget, name, id):
        newItem = MyQListWidgetItem(id, name)
        newItem.setSizeHint(self.itemsSize)
        listWidget.addItem(newItem)

    def slot_delete_account(self, id: int):
        def delete_account():
            self.appData.remove_account_by_id(id)

            if self.listWidgetAccounts.count() > 1:
                self.slot_select_account(MyQListWidgetItem(self.listWidgetAccounts.item(0)))
                return
            
            self.appData.add_account("Cash")

        return delete_account

    def slot_delete_goal(self, id: int):
        def delete_goal():
            self.appData.remove_goal_by_id(id)

        return delete_goal

    def slot_add_account(self):
        dlgWindow = DlgInputWindow("Type name for new account")

        if dlgWindow.exec():
            self.appData.add_account(dlgWindow.lineEditInput.text())

    def slot_add_goal(self):
        dlgWindow = DlgGoalWindow()

        if dlgWindow.exec():
            self.appData.add_goal(dlgWindow.goalName, 0, dlgWindow.goalFinishMoneyAmount)

    def slot_add_money_to_goal(self, item: MyQListWidgetItem):
        dlgWindow = DlgInputWindow("Type money for goal", int)

        if dlgWindow.exec():
            self.appData.update_goal_by_id(item.id, int(dlgWindow.lineEditInput.text()))

    def slot_select_account(self, item: MyQListWidgetItem):
        
        for i in range(self.listWidgetAccounts.count()):
            self.listWidgetAccounts.item(i).setForeground(self.defultColorText)

        item.setForeground(self.selectedAccountColorText)

        self.signalSelectedAccount.emit(item.id)


