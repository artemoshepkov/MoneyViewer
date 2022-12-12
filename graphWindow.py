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

        self.appData.signalTransactionsUpdate.connect(self.update_graph_to_year)

        self.appData.signalCategoriesUpdate.connect(self.update_graph_to_year)

        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.chartView = QChartView()
        layout.addWidget(self.chartView)

        self.update_graph_to_year()

    def update_graph_to_year(self):

        months = ("J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D")

        barSets = []

        tmpBarSets = {}

        categories = self.appData.get_categories()

        if len(categories) == 0:
            # print("Categories is null")
            return

        for categoria in categories:
            barSets.append(QBarSet(categoria.name))
            tmpBarSets[categoria.id] = [0,0,0,0,0,0,0,0,0,0,0,0]


        # for tran in self.appData.get_transactions():
        #     tmpBarSets[tran.categoriaId][tran.registDate.month - 1] = tran.payment

        # for i in range(len(barSets)):
        #     barSets[i].append(tmpBarSets[i])

        barSeries = QBarSeries()

        for barSet in barSets:
            barSeries.append(barSet)

        newChart = QChart()
        newChart.addSeries(barSeries)
        newChart.setTitle("Expenses")

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()

        max = Linq.max(self.appData.get_transactions(), lambda t: t.payment)
        if max is None:
            max = 1000

        axisY.setRange(0, max)

        newChart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        newChart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)        
        
        newChart.legend().setVisible(True)
        newChart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.chartView.setChart(newChart)

