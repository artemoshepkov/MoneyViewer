from PyQt6.QtWidgets import *

class DlgInputWindow(QDialog):
    def __init__(self, textForInput: str, typeInput: type = str):
        super().__init__()

        self.typeInput = typeInput

        self.input = None

        self.initUI(textForInput)

    def initUI(self, textForInput: str):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        label = QLabel(textForInput)
        layout.addWidget(label)

        self.lineEditInput = QLineEdit(self)
        layout.addWidget(self.lineEditInput)

        buttonOk = QPushButton("Ok")
        buttonOk.clicked.connect(self.evt_buttonOk_clicked)
        layout.addWidget(buttonOk)

        buttonCancel = QPushButton("Cancel")
        buttonCancel.clicked.connect(self.evt_buttonCancel_clicked)
        layout.addWidget(buttonOk)

    def evt_buttonOk_clicked(self):
        if  self.lineEditInput.text() == "":
            QMessageBox.warning(self, "!", "Type field")
            return

        try:
            self.input = self.typeInput(self.lineEditInput.text())
        except:
            QMessageBox.warning(self, "!", "Wrong input")
            return

        QDialog.accept(self)

    def evt_buttonCancel_clicked(self):
        QDialog.reject(self)