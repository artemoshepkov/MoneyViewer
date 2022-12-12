from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from datetime import date

from Model.applicationData import *
from Model.dbContext import *
from dialogDataTransaction import *
from Model.transaction import *
from Model.timePeriod import *

from linq import *

class MyQListWidgetItem(QListWidgetItem):
    def __init__(self, text: str, id: int):
        super().__init__(text)

        self.id = id

    

class ListWindow(QWidget):
    signalCategoriaChanged = pyqtSignal(int)

    signalAddTransaction = pyqtSignal(int, date, float)

    signalDeleteTransaction = pyqtSignal(Transaction)
    def __init__(self, appData: AppData):
        super().__init__()

        self.appData = appData

        self.signalAddTransaction.connect(self.appData.slot_add_transaction)
        self.signalDeleteTransaction.connect(self.appData.slot_delete_transaction)
        self.signalCategoriaChanged.connect(self.appData.slot_filter_for_categoria)

        self.appData.signalTransactionsUpdate.connect(self.slot_update_listWidget)
        self.appData.signalCategoriesUpdate.connect(self.update_combobox_categories)

        self.itemSize = QSize(50, 50)

        self.setFixedSize(260, 320)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.comboboxCategoriaFilter = QComboBox(self)
        self.update_combobox_categories()
        self.comboboxCategoriaFilter.activated.connect(self.slot_filter)
        layout.addWidget(self.comboboxCategoriaFilter)

        self.listWidgetTransactions = QListWidget(self)
        self.slot_update_listWidget()
        layout.addWidget(self.listWidgetTransactions)

        self.btnAdd = QPushButton("+")
        self.btnAdd.clicked.connect(self.slot_btn_add_clicked)
        layout.addWidget(self.btnAdd)

        self.btnDelete = QPushButton("-")
        self.btnDelete.clicked.connect(self.slot_btn_delete_clicked)
        layout.addWidget(self.btnDelete)

    def update_combobox_categories(self):
        self.comboboxCategoriaFilter.clear()

        categories = Linq.to_list(Linq.select(self.appData.get_categories(), lambda c: c.name))
        categories.insert(0, "All")

        self.comboboxCategoriaFilter.addItems(categories)

    def slot_btn_add_clicked(self) -> None:
        if len(self.appData.get_categories()) == 0:
            QMessageBox.warning(self, "!", "Need to add categoria in tab 'Categoria'")
            return

        dlgTransaction = InputDialogTransaction(self.appData)
        
        if dlgTransaction.exec():
            self.signalAddTransaction.emit(dlgTransaction.categoria, dlgTransaction.registDate, -dlgTransaction.payment)
            
    def slot_btn_delete_clicked(self) -> None:
        deletedItem = self.listWidgetTransactions.takeItem(self.listWidgetTransactions.currentRow())

        self.signalDeleteTransaction.emit(deletedItem.id)

    def slot_filter(self):
        categoriaName = self.comboboxCategoriaFilter.currentText()
        if categoriaName == "All":
            self.signalCategoriaChanged.emit(0)
        else:
            self.signalCategoriaChanged.emit(self.appData.get_categoria_by_name(categoriaName).id)

    def slot_update_listWidget(self):
        self.listWidgetTransactions.clear()

        categories = {}
        for c in self.appData.get_categories():
            categories[c.id] = c.name

        if len(categories) == 0:
            print("Categories list is null")
            return

        transactions = self.appData.get_transactions()

        if len(transactions) == 0:
            print("Transactions list is null")
            return

        for item in transactions:
            newItem = QListWidgetItem(categories[item.categoriaId] + "\t" + str(item))
            newItem.setSizeHint(self.itemSize)
            self.listWidgetTransactions.addItem(newItem)

