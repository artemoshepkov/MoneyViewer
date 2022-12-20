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

    signalDeleteTransaction = pyqtSignal(int)

    def __init__(self, appData: AppData, objectsColor: str):
        super().__init__()

        self.appData = appData

        self.signalAddTransaction.connect(self.appData.slot_add_transaction)
        self.signalDeleteTransaction.connect(self.appData.slot_delete_transaction)
        self.signalCategoriaChanged.connect(self.appData.slot_filter_for_categoria)

        self.appData.signalTransactionsUpdate.connect(self.slot_update_listWidget)
        self.appData.signalCategoriesUpdate.connect(self.update_combobox_categories)

        self.itemSize = QSize(50, 50)

        self.objectsColor = objectsColor

        self.setFixedSize(260, 320)

        self.categoriaName = "All"

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.comboboxCategoriaFilter = QComboBox(self)
        self.comboboxCategoriaFilter.setMinimumSize(150, 30)
        self.comboboxCategoriaFilter.setMaximumSize(150, 30)
        self.comboboxCategoriaFilter.setStyleSheet("""
        QComboBox {
            background-color: #%s;
            font-size: 14px;
            }""" % self.objectsColor)
        self.update_combobox_categories()
        self.comboboxCategoriaFilter.activated.connect(self.slot_filter)
        layout.addWidget(self.comboboxCategoriaFilter, 1, Qt.AlignmentFlag.AlignHCenter)

        self.listWidgetTransactions = QListWidget(self)
        self.listWidgetTransactions.setStyleSheet("background-color: #%s" % self.objectsColor)
        self.slot_update_listWidget()
        layout.addWidget(self.listWidgetTransactions)

        self.btnAdd = QPushButton("+")
        self.btnAdd.setMaximumSize(50, 50)
        self.btnAdd.setMinimumSize(50, 50)
        self.btnAdd.setStyleSheet(
            """
                QPushButton {
                    border-style: solid;
                    border-width: 2px;
                    border-radius: 25px;
                    background-color: #%s;
                    font-size: 20px;
                    text-align: center;
                    }
                }
            """ % self.objectsColor
        )
        self.btnAdd.clicked.connect(self.slot_btn_add_clicked)
        layout.addWidget(self.btnAdd, 1, alignment = Qt.AlignmentFlag.AlignRight)

    def update_combobox_categories(self):
        self.comboboxCategoriaFilter.clear()

        categories = Linq.to_list(Linq.select(self.appData.get_categories(), lambda c: c.name))
        categories.insert(0, "All")

        self.comboboxCategoriaFilter.addItems(categories)

        self.comboboxCategoriaFilter.setCurrentText(self.categoriaName)

    def slot_btn_add_clicked(self) -> None:
        if len(self.appData.get_categories()) == 0:
            QMessageBox.warning(self, "!", "Need to add categoria in tab 'Categoria'")
            return

        dlgTransaction = InputDialogTransaction(self.appData)
        
        if dlgTransaction.exec():
            self.signalAddTransaction.emit(dlgTransaction.categoria, dlgTransaction.registDate, -dlgTransaction.payment)
            
    def slot_btn_delete_clicked(self, id: int) -> None:
        def delete_transaction():
            reply = QMessageBox.question(self, 'Attention',"Are you sure to delete it?", QMessageBox.StandardButton.Ok, QMessageBox.StandardButton.Cancel)

            if reply == QMessageBox.StandardButton.Cancel:
                return
                
            self.signalDeleteTransaction.emit(id)

        return delete_transaction

    def slot_filter(self):
        self.categoriaName = self.comboboxCategoriaFilter.currentText()
        if self.categoriaName == "All":
            self.signalCategoriaChanged.emit(0)
        else:
            self.signalCategoriaChanged.emit(self.appData.get_categoria_by_name(self.categoriaName).id)

    def slot_update_listWidget(self):
        self.listWidgetTransactions.clear()

        categories = {}
        for c in self.appData.get_categories():
            categories[c.id] = c.name

        if len(categories) == 0:
            return

        transactions = self.appData.get_transactions()

        if len(transactions) == 0:
            return

        for item in transactions:
            itemWidget = QWidget()

            itemLayout = QHBoxLayout()
            itemWidget.setLayout(itemLayout)

            itemLabelCateg = QLabel(categories[item.categoriaId])
            itemLabelCateg.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                }
                """
            )
            itemLayout.addWidget(itemLabelCateg)

            itemLabelDate = QLabel(str(item.registDate.year) + "-" + str(item.registDate.month) + "-" + str(item.registDate.day)) 
            itemLabelDate.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                }
                """
            )
            itemLayout.addWidget(itemLabelDate, 1, Qt.AlignmentFlag.AlignHCenter)

            itemLabelPayment = QLabel(str(item)) 
            itemLabelPayment.setStyleSheet(
                """
                QLabel {
                    font-size: 14px;
                }
                """
            )
            itemLayout.addWidget(itemLabelPayment, 1, Qt.AlignmentFlag.AlignRight)

            btnDelete = QPushButton("-")
            btnDelete.setStyleSheet("""
            QPushButton {
                background: #%s;
                font-size: 18px;
                width: 25px;
                height: 15px;
                border-style: solid;
                border-width: 1px;
                border-color: black;
                border-radius: 7px; }
                    """ % self.objectsColor)
            btnDelete.clicked.connect(self.slot_btn_delete_clicked(item.id))
            itemLayout.addWidget(btnDelete)

            newItem = QListWidgetItem()
            newItem.setSizeHint(self.itemSize)

            self.listWidgetTransactions.addItem(newItem)
            self.listWidgetTransactions.setItemWidget(newItem, itemWidget)






