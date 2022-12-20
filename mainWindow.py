from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QAction, QIcon
from PyQt6 import QtWebEngineWidgets

import os
import csv

from Model.dbContext import *
from dialogDataTransaction import *
from calendarEdit import *
from linq import *
from listWindow import *
from AccountsGoalsWindow import *
from graphWindow import *
from categoriaWindow import *

from Model.applicationData import *

class HtmlWindow(QMainWindow):
    def __init__(self):
        super(HtmlWindow, self).__init__()
        self.setWindowTitle('Reference')
        self.setGeometry(5,30,900,730)
        self.browser = QtWebEngineWidgets.QWebEngineView()
        self.browser.load(QUrl('file:///' + os.path.abspath("HTML/index.html").replace("\\","/")))
        self.setCentralWidget(self.browser)
        self.button = QPushButton('Exit', self)
        self.button.setFixedSize(100,50)
        self.button.move(800, 680) 
        self.button.clicked.connect(self.close)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("icon.png"))

        self.appData = AppData("money_viewer.db")
        
        self.appData.signalBalanceUpdate.connect(self.update_balance)

        self.setWindowTitle("MoneyViewer")

        self.appHeight = 600
        self.appWidth = 900

        self.htmlwindow = HtmlWindow()

        # self.resize(self.appWidth, self.appHeight + 22)
        self.setFixedSize(self.appWidth, self.appHeight + 22)

        self.initUI()
    
    def initUI(self):        
        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.setStyleSheet("background-color: #C9C7C7")

        self.init_menu()
        self.init_left_part()
        self.init_right_part()

    def init_menu(self):
        menuBar = QMenuBar(self)
        menuBar.setStyleSheet("background-color: white")
        self.setMenuBar(menuBar)


        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        
        exportAction = QAction("&Export to CVS", self)
        exportAction.triggered.connect(self.slot_export_CVS)
        fileMenu.addAction(exportAction)

        referenceMenu = QMenu("&Reference", self)
        menuBar.addMenu(referenceMenu)
        
        referenceAction = QAction("&Help", self)
        referenceAction.triggered.connect(self.slot_open_reference)
        referenceMenu.addAction(referenceAction)

    def init_left_part(self):

        backGroundColor = "ADAAAA"

        objectsColor = "D9D9D9"

        groupBox = QGroupBox(self)
        groupBox.setStyleSheet("background-color: #%s" % backGroundColor)
        groupBox.setGeometry(0, 22, 300, self.appHeight)

        groupBoxLayout = QVBoxLayout(self)
        groupBox.setLayout(groupBoxLayout)
        self.mainLayout.addWidget(groupBox)

        self.balanceLabel = QLabel(self)
        self.balanceLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balanceLabel.setMinimumSize(125, 35)
        self.balanceLabel.setMaximumSize(125, 35)
        self.balanceLabel.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                background-color: #B8B7B7;
                color: #FFFFFF;
                border-radius: 2px;
                margin: 0px;
            }
            """)
        groupBoxLayout.addWidget(self.balanceLabel, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.update_balance()

        self.calendar = CalendarEdit(self, objectsColor)
        self.calendar.signalDateUpdate.connect(self.appData.slot_filter_for_date)
        self.calendar.date_update(0)
        groupBoxLayout.addWidget(self.calendar, 1, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.listWidgetTransactions = ListWindow(self.appData, objectsColor)
        self.listWidgetTransactions.setMinimumHeight(425)
        groupBoxLayout.addWidget(self.listWidgetTransactions, 1, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    def init_right_part(self):
        tabsBackgroundColor = "EFEFEF"

        groupBoxRight = QGroupBox(self)
        groupBoxRight.setGeometry(299, 22, self.appHeight, self.appHeight)

        groupBoxLayoutRight = QVBoxLayout()
        groupBoxRight.setLayout(groupBoxLayoutRight)
        
        self.mainLayout.addWidget(groupBoxRight)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("background-color: #%s" % tabsBackgroundColor)
        groupBoxLayoutRight.addWidget(self.tabs)

        self.tabs.resize(600, 400)

        self.tabAccountGoals = AccoountsGoalsWindow(self, self.appData)
        self.tabGraph = GraphWindow(self, self.appData)
        self.tabCatogories = CategoriaWindow(self, self.appData, tabsBackgroundColor)

        self.tabs.addTab(self.tabAccountGoals, "Goals")
        self.tabs.addTab(self.tabGraph, "Graph")
        self.tabs.addTab(self.tabCatogories, "Categories")

    def update_balance(self):
        self.balanceLabel.setText(str(self.appData.get_balance()))

    def slot_export_CVS(self):
        fileName = QFileDialog.getSaveFileName(self, "Save to CVS", os.getenv("HOME"))
        
        categories = {}
        for c in self.appData.get_categories():
            categories[c.id] = c.name

        if len(categories) == 0:
            print("Categories list is null")
            return

        transactions = self.appData.get_transactions()
        
        with open(fileName[0], "w") as file:
            writer = csv.writer(file)

            for tran in transactions:
                writer.writerow([categories[tran.categoriaId], str(tran.registDate), str(tran.payment)])

        reply = QMessageBox.question(self, 'Open file',"Do you wanna open it?", QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No:
            return

        os.system(fileName[0])
        

    def slot_open_reference(self):
        self.htmlwindow.show()