import sys

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi

from mainWindow import *
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainWindow = MainWindow()

    mainWindow.show()

    app.exec()

#     from PyQt6.QtWidgets import *
# from PyQt6.QtCore import *
# from PyQt6.QtGui import QAction, QIcon

# import os
# import csv

# from Model.dbContext import *
# from dialogDataTransaction import *
# from calendarEdit import *
# from linq import *
# from listWindow import *
# from AccountsGoalsWindow import *
# from graphWindow import *
# from categoriaWindow import *

# from Model.applicationData import *

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.appData = AppData("money_viewer.db")
        
#         self.appData.signalBalanceUpdate.connect(self.update_balance)

#         self.setWindowTitle("MoneyViewer")

#         self.appHeight = 600
#         self.appWidth = 900

#         self.resize(self.appWidth, self.appHeight)
#         # self.setFixedSize(self.appWidth, self.appHeight)

#         self.initUI()
    
#     def initUI(self):        
#         self.mainLayout = QHBoxLayout()
#         self.setLayout(self.mainLayout)

#         groupBox = QGroupBox(self)
#         groupBox.setGeometry(0, 0, 300, self.appHeight)

#         groupBoxLayout = QVBoxLayout()
#         groupBox.setLayout(groupBoxLayout)
        
#         self.mainLayout.addWidget(groupBox)

#         menuBar = QMenuBar(self)
#         self.setMenuBar(menuBar)

#         fileMenu = QMenu("&File", self)
#         menuBar.addMenu(fileMenu)

#         exportAction = QAction("&Export to CVS", self)
#         exportAction.triggered.connect(self.slot_export_CVS)
#         fileMenu.addAction(exportAction)


#         self.balanceLabel = QLabel()
#         groupBoxLayout.addWidget(self.balanceLabel)
#         self.update_balance()

#         self.listWidgetTransactions = ListWindow(self.appData)
#         groupBoxLayout.addWidget(self.listWidgetTransactions)

#         self.calendar = CalendarEdit(self)
#         self.calendar.signalDateUpdate.connect(self.appData.slot_filter_for_date)
#         self.calendar.date_update(0)
#         groupBoxLayout.addWidget(self.calendar)


#         groupBoxRight = QGroupBox(self)
#         groupBoxRight.setGeometry(299, 0, self.appHeight, self.appHeight)

#         groupBoxLayoutRight = QVBoxLayout()
#         groupBoxRight.setLayout(groupBoxLayoutRight)
        
#         self.mainLayout.addWidget(groupBoxRight)

#         self.tabs = QTabWidget()
#         groupBoxLayoutRight.addWidget(self.tabs)

#         self.tabs.resize(600, 400)

#         self.tabAccountGoals = AccoountsGoalsWindow(self, self.appData)
#         self.tabGraph = GraphWindow(self, self.appData)
#         self.tabCatogories = CategoriaWindow(self, self.appData)

#         self.tabs.addTab(self.tabAccountGoals, "Goals")
#         self.tabs.addTab(self.tabGraph, "Graph")
#         self.tabs.addTab(self.tabCatogories, "Categories")

#     def update_balance(self):
#         self.balanceLabel.setText(str(self.appData.get_balance()))

#     def slot_export_CVS(self):
#         fileName = QFileDialog.getSaveFileName(self, "Save to CVS", os.getenv("HOME"))
        
#         categories = {}
#         for c in self.appData.get_categories():
#             categories[c.id] = c.name

#         if len(categories) == 0:
#             print("Categories list is null")
#             return

#         transactions = self.appData.get_transactions()
        
#         with open(fileName[0], "w") as file:
#             writer = csv.writer(file)

#             for tran in transactions:
#                 writer.writerow([categories[tran.categoriaId], str(tran.registDate), str(tran.payment)])
