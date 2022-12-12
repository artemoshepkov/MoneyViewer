from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from datetime import date
from datetime import timedelta

from Model.timePeriod import *

class CalendarEdit(QWidget):

    signalDateUpdate = pyqtSignal(date, TimePeriod)

    def __init__(self, parent):
        super().__init__(parent)

        self.__currentDate = date.today()
        self.__timePeriods = {"Month": TimePeriod.Month, "Day": TimePeriod.Day, "Year": TimePeriod.Year}
        self.__timePeriod = TimePeriod.Month

        self.initUI()

    
    def initUI(self):
        gridLayout = QGridLayout()        
        self.setLayout(gridLayout)

        self.__comboboxTimePeriod = QComboBox(self)
        self.__comboboxTimePeriod.addItems(self.__timePeriods.keys())
        self.__comboboxTimePeriod.activated.connect(self.__evt_combobox_time_period)
        gridLayout.addWidget(self.__comboboxTimePeriod, 0, 1)

        self.__labelDate = QLabel(self)
        self.__labelDate.setText(str(self.__currentDate))
        gridLayout.addWidget(self.__labelDate, 1, 1)

        self.__btnPrevDate = QPushButton("<", self)
        self.__btnPrevDate.clicked.connect(self.__evt_btn_prev_date_clicked)
        gridLayout.addWidget(self.__btnPrevDate, 1, 0)

        self.__btnNextDate = QPushButton(">", self) 
        self.__btnNextDate.clicked.connect(self.__evt_btn_next_date_clicked)
        gridLayout.addWidget(self.__btnNextDate, 1, 2)

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

