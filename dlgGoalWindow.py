from PyQt6.QtWidgets import *

class DlgGoalWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.goalName = ""
        self.goalFinishMoneyAmount = -1

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        labelName = QLabel("Type name for goal")
        layout.addWidget(labelName)

        self.lineEditGoalName = QLineEdit(self)
        layout.addWidget(self.lineEditGoalName)

        labelFinishMoneyAmount = QLabel("Type money what you want")
        layout.addWidget(labelFinishMoneyAmount)

        self.lineEditGoalFinishMoney = QLineEdit(self)
        layout.addWidget(self.lineEditGoalFinishMoney)

        buttonOk = QPushButton("Ok")
        buttonOk.clicked.connect(self.evt_buttonOk_clicked)
        layout.addWidget(buttonOk)

        buttonCancel = QPushButton("Cancel")
        buttonCancel.clicked.connect(self.evt_buttonCancel_clicked)
        layout.addWidget(buttonOk)

    def evt_buttonOk_clicked(self):
        self.goalName = self.lineEditGoalName.text()
        try:
            self.goalFinishMoneyAmount = float(self.lineEditGoalFinishMoney.text())
        except:
            QMessageBox.warning(self, "!", "Wrong input")
            return

        if  self.goalName == "" or self.goalFinishMoneyAmount < 0:
            QMessageBox.warning(self, "!", "Type field")
            return

        QDialog.accept(self)

    def evt_buttonCancel_clicked(self):
        QDialog.reject(self)