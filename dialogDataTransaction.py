from PyQt6.QtWidgets import *

from datetime import date

from Model.transaction import *
from Model.applicationData import *

class InputDialogTransaction(QDialog):
    def __init__(self, appData: AppData) -> None:
        super().__init__()
        
        self.setWindowTitle("New transaction")
        self.resize(200, 200)

        self.appData = appData

        self.initUI()

    def initUI(self):      
        self.setStyleSheet("""
            background-color: #C9C7C7
        """)


        layout = QVBoxLayout()
        self.setLayout(layout)

        # self.labelNote = QLabel(self, "Note")

        # self.tabWidget = QTabWidget()
        # self.tabWidget.addTab(self, "Graph")
        
        self.labelExpense = QLabel(self)
        self.labelExpense.setText("Expense")
        layout.addWidget(self.labelExpense)

        self.__lineEditExpense = QLineEdit(self)
        layout.addWidget(self.__lineEditExpense)

        self.comboboxCategoria = QComboBox(self)
        self.comboboxCategoria.addItems(Linq.to_list(Linq.select(self.appData.get_categories(), lambda c: c.name)))
        layout.addWidget(self.comboboxCategoria)



        subWidget = QWidget()
        subLayout = QHBoxLayout()
        subWidget.setLayout(subLayout)
        layout.addWidget(subWidget)

        self.btnOk = QPushButton("Ok", self)
        self.btnOk.clicked.connect(self.evt_btn_ok_clicked)
        subLayout.addWidget(self.btnOk)

        self.btnCancel = QPushButton("Cancel", self)
        self.btnCancel.clicked.connect(self.evt_btn_cancel_clicked)
        subLayout.addWidget(self.btnCancel)

        # layout.addWidget(self.tabWidget)


    def evt_btn_ok_clicked(self) -> None:
        if self.__lineEditExpense.text() == "":
            QMessageBox.warning(self, "!", "Type fields")
            return

        try:
            float(self.__lineEditExpense.text())
        except:
            QMessageBox.warning(self, "!", "Wrong input")
            return

        self.registDate = date.today()

        
        categories = {}
        for c in self.appData.get_categories():
            categories[c.name] = c.id

        self.categoria = categories[self.comboboxCategoria.currentText()]

        self.payment = float(self.__lineEditExpense.text())

        QDialog.accept(self)

    def evt_btn_cancel_clicked(self) -> None:
        QDialog.reject(self)
