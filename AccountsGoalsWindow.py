from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QMessageBox
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

class MyQWidget(QWidget):
    def __init__(self, account: Account, balance: str, slot_delete):
        super().__init__()

        itemLayout = QHBoxLayout()

        self.itemLabelName = QLabel(str(account))
        self.itemLabelName.setStyleSheet("""
                QLabel {
                    color: #000000;
                    font-size: 15px;  }
                        """)
        itemLayout.addWidget(self.itemLabelName)

        self.itemLabelBalance = QLabel(balance)        
        self.itemLabelBalance.setStyleSheet("""
                QLabel {
                    font-size: 15px;  }
                        """)
        self.itemLabelBalance.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        itemLayout.addWidget(self.itemLabelBalance)

        buttonDelete = QPushButton("-")
        buttonDelete.setMinimumWidth(25)
        buttonDelete.setMaximumWidth(25)
        buttonDelete.setStyleSheet("""
                QPushButton {
                    background: #D9D9D9;  
                    border-style: solid;
                    border-width: 2px;
                    border-radius: 8px;
                    border-color: #D9D9D9;
                    font-size: 15px;}
                        """)
        buttonDelete.clicked.connect(slot_delete(account.id))
        itemLayout.addWidget(buttonDelete)

        self.setLayout(itemLayout)

    def set_color(self, color: str):
        self.itemLabelName.setStyleSheet("QLabel { color: %s; font-size: 15px; }" % (color))


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
        headersColor = "A8A8A8"

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        labelAccounts = QLabel("Accounts")
        labelAccounts.setStyleSheet(
                """
                QLabel {
                    font-size: 16px;
                    color: #%s;
                }
                """ % headersColor)
        layout.addWidget(labelAccounts)
        
        self.listWidgetAccounts = QListWidget()
        self.listWidgetAccounts.itemDoubleClicked.connect(self.slot_select_account)
        layout.addWidget(self.listWidgetAccounts)

        self.slot_update_accounts_list_widget()

        labelGoals = QLabel("Goals")
        labelGoals.setStyleSheet(
                """
                QLabel {
                    font-size: 16px;
                    color: #%s;
                }
                """ % headersColor)
        layout.addWidget(labelGoals)

        self.listWidgetGoals = QListWidget()
        self.listWidgetGoals.itemDoubleClicked.connect(self.slot_add_money_to_goal)
        layout.addWidget(self.listWidgetGoals)

        self.slot_update_goals_list_widget()

    def add_button_to_list_widget(self, listWidget: QListWidget, event):
        buttonAdd = QPushButton("+")
        buttonAdd.setMaximumWidth(33)
        buttonAdd.setStyleSheet("""
            QPushButton {
                border-style: solid;
                font-size: 18px;  }
                    """)
        buttonAdd.clicked.connect(event)        
        
        itemLayout = QHBoxLayout()
        itemLayout.addWidget(buttonAdd, 1, alignment = Qt.AlignmentFlag.AlignLeft)

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
            itemWidget = MyQWidget(account,  str(self.appData.get_balance_by_account_id(account.id)), self.slot_delete_account)

            newItem = MyQListWidgetItem(account.id)
            newItem.setSizeHint(self.itemsSize)
            self.listWidgetAccounts.addItem(newItem)
            self.listWidgetAccounts.setItemWidget(newItem, itemWidget)

        for i in range(len(self.listWidgetAccounts)):
            if self.listWidgetAccounts.item(i).id == self.appData.get_account_id():
                self.listWidgetAccounts.itemWidget(self.listWidgetAccounts.item(i)).set_color("red")

        self.add_button_to_list_widget(self.listWidgetAccounts, self.slot_add_account)

    def slot_update_goals_list_widget(self):
        self.listWidgetGoals.clear()

        for goal in self.appData.get_goals():
                itemLayout = QHBoxLayout()

                itemLabel = QLabel(str(goal))
                itemLabel.setStyleSheet("""
                QLabel {
                    font-size: 15px;  }
                        """)
                itemLayout.addWidget(itemLabel)
                
                progressBar = QProgressBar(textVisible=False)
                progressBar.setMinimum(0)
                progressBar.setMaximum(goal.finishMoneyAmount)
                progressBar.setStyleSheet(
                    """
                    QProgressBar {
                        border-radius: 6px;
                        min-height: 5px;
                        max-height: 8px;
                        background-color: #D9D9D9;
                    }
                    """
                )

                if goal.moneyAmount > goal.finishMoneyAmount:
                    progressBar.setValue(goal.finishMoneyAmount)
                else:
                    progressBar.setValue(goal.moneyAmount)
                itemLayout.addWidget(progressBar)

                buttonDelete = QPushButton("-")
                buttonDelete.setMinimumWidth(25)
                buttonDelete.setMaximumWidth(25)
                buttonDelete.setStyleSheet("""
                QPushButton {
                    background: #D9D9D9;  
                    border-style: solid;
                    border-width: 2px;
                    border-radius: 8px;
                    border-color: #D9D9D9;
                    font-size: 15px; }
                        """)

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
            reply = QMessageBox.question(self, 'Attention',"Are you sure to delete it?", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Cancel:
                return

            self.appData.remove_account_by_id(id)

            self.slot_select_account(self.listWidgetAccounts.item(0))

        return delete_account

    def slot_delete_goal(self, id: int):
        def delete_goal():
            reply = QMessageBox.question(self, 'Attention',"Are you sure to delete it?", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Cancel:
                return
            
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
        try:
            tmp = item.id
        except:
            return

        dlgWindow = DlgInputWindow("Type money for goal", int)

        if dlgWindow.exec():
            self.appData.update_goal_by_id(item.id, int(dlgWindow.lineEditInput.text()))

    def slot_select_account(self, item: MyQListWidgetItem):
        try:
            self.signalSelectedAccount.emit(item.id)
        except:
            print("It wasn`t elem of list")


