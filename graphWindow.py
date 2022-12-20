from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtCharts import *

import random

from Model.applicationData import *
from Model.dbContext import *
from dlgInputWindow import *
from dlgGoalWindow import *
from linq import *

class GraphWindow(QWidget):
    def __init__(self, parent, appData: AppData):
        super().__init__(parent)

        self.appData = appData

        self.appData.signalGraphUpdate.connect(self.update_graph)

        self.appData.signalGraphUpdate.connect(self.update_graph)

        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.chartView = QChartView()
        layout.addWidget(self.chartView)

        self.update_graph_to_month()

    def update_graph(self, d: TimePeriod):
        if d == TimePeriod.Month or d == TimePeriod.Day:
            self.update_graph_to_month()
        elif d == TimePeriod.Year:
            self.update_graph_to_year()

    def update_graph_to_month(self):
        barSets = []

        tmpBarSets = {}

        categories = self.appData.get_categories()

        index = 0
        indexes = {}
        for categoria in categories:
            barSets.append(QBarSet(categoria.name))
            tmpBarSets[categoria.id] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            indexes[index] = categoria.id
            index += 1

        if len(categories) > 0:
            for tran in self.appData.get_transactions():
                tmpBarSets[tran.categoriaId][tran.registDate.day - 1] = -tran.payment

        self.set_graph(tmpBarSets, barSets, indexes)

    def update_graph_to_year(self):
        barSets = []

        tmpBarSets = {}

        categories = self.appData.get_categories()

        index = 0
        indexes = {}
        for categoria in categories:
            barSets.append(QBarSet(categoria.name))
            tmpBarSets[categoria.id] = [0,0,0,0,0,0,0,0,0,0,0,0]
            indexes[index] = categoria.id
            index += 1

        if len(categories) > 0:
            for tran in self.appData.get_transactions():
                tmpBarSets[tran.categoriaId][tran.registDate.month - 1] = -tran.payment

        self.set_graph(tmpBarSets, barSets, indexes)



    def set_graph(self, tmpBarSets, barSets, indexes):
        for i in range(len(barSets)):
            barSets[i].append(tmpBarSets[indexes[i]])

        barSeries = QBarSeries()

        for barSet in barSets:
            barSeries.append(barSet)

        newChart = QChart()
        newChart.addSeries(barSeries)
        newChart.setTitle("Expenses")

        newChart.createDefaultAxes()     
        
        newChart.legend().setVisible(True)
        newChart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chartView.setChart(newChart)
