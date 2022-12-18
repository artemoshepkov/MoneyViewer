from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from datetime import date
from datetime import timedelta

from Model.timePeriod import *

class CalendarEdit(QWidget):

    signalDateUpdate = pyqtSignal(date, TimePeriod)

    def __init__(self, parent, objectsColor: str):
        super().__init__(parent)

        self.objectsColor = objectsColor

        self.__currentDate = date.today()
        self.__timePeriods = {"Month": TimePeriod.Month, "Day": TimePeriod.Day, "Year": TimePeriod.Year}
        self.__timePeriod = TimePeriod.Month

        self.initUI()

    
    def initUI(self):
        mainLayout = QVBoxLayout()        
        self.setLayout(mainLayout)

        subLayout = QHBoxLayout()
        subWidget = QWidget()
        subWidget.setStyleSheet("""
        QWidget {
            background-color: #%s;
            border: none;
            margin: 0px;
            }
        """ % self.objectsColor)
        subWidget.setLayout(subLayout)
        mainLayout.addWidget(subWidget, 1, Qt.AlignmentFlag.AlignTop)

        self.__btnPrevDate = QPushButton("<", self)
        self.__btnPrevDate.setStyleSheet("""
        QPushButton {
            font-size: 30px;
            }""")
        self.__btnPrevDate.clicked.connect(self.__evt_btn_prev_date_clicked)
        subLayout.addWidget(self.__btnPrevDate)

        self.__labelDate = QLabel(self)
        self.__labelDate.setMinimumWidth(200)
        self.__labelDate.setStyleSheet("""
        QLabel {
            font-size: 16px;
            }""")
        self.__labelDate.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.__labelDate.setText(str(self.__currentDate))
        subLayout.addWidget(self.__labelDate)

        self.__btnNextDate = QPushButton(">", self)
        self.__btnNextDate.setStyleSheet("""
        QPushButton {
            font-size: 30px;
            }""")
        self.__btnNextDate.clicked.connect(self.__evt_btn_next_date_clicked)
        subLayout.addWidget(self.__btnNextDate)

        self.__comboboxTimePeriod = QComboBox(self)
        self.__comboboxTimePeriod.setMinimumSize(100, 30)
        self.__comboboxTimePeriod.setMaximumSize(100, 30)
        self.__comboboxTimePeriod.setStyleSheet("""
        QComboBox {
            background-color: #%s;
            font-size: 12px;
            margin: 0px;
            }""" % self.objectsColor)
        self.__comboboxTimePeriod.addItems(self.__timePeriods.keys())
        self.__comboboxTimePeriod.activated.connect(self.__evt_combobox_time_period)
        mainLayout.addWidget(self.__comboboxTimePeriod, 1, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

    def __evt_combobox_time_period(self):
        self.__timePeriod = self.__timePeriods[self.__comboboxTimePeriod.currentText()]

        self.signalDateUpdate.emit(self.__currentDate, self.__timePeriod)

    def __evt_btn_prev_date_clicked(self):
        self.date_update(-1)

    def __evt_btn_next_date_clicked(self):
        self.date_update(1)

    def date_update(self, sign = 1):
        self.__currentDate = self.__currentDate + sign * timedelta(days=self.__timePeriod.value)
        self.__labelDate.setText(str(self.__currentDate))

        self.signalDateUpdate.emit(self.__currentDate, self.__timePeriod)

