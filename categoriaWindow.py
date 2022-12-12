from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QPieSlice

from Model.applicationData import *
from dlgInputWindow import *

class MyQListWidgetItem(QListWidgetItem):
    def __init__(self, id: int,text: str = ""):
        super().__init__(text)

        self.id = id

class CategoriaWindow(QWidget):
    def __init__(self, parent, appData: AppData):
        super().__init__(parent)

        self.appData = appData

        self.appData.signalCategoriesUpdate.connect(self.slot_update_chart)

        self.itemSize = QSize(50, 50)

        self.initUi()

    def initUi(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        self.chartView = QChartView()
        mainLayout.addWidget(self.chartView)

        self.listWidgetCategories = QListWidget()
        mainLayout.addWidget(self.listWidgetCategories)

        self.slot_update_chart()

    def slot_update_chart(self):
        categories =  self.appData.get_categories_with_expense()

        self.list_widget_update(categories)

        self.chart_update(categories)

    def list_widget_update(self, categories):
        self.listWidgetCategories.clear()
            
        for cat in categories:
            itemWidget = QWidget()

            itemLayout = QHBoxLayout()
            itemWidget.setLayout(itemLayout)

            itemLabel = QLabel(str(cat["categoria"]) + "\t" + str(cat["expenses"]))
            itemLayout.addWidget(itemLabel)

            buttonDelete = QPushButton("-")
            buttonDelete.clicked.connect(self.slot_remove_categoria(cat["categoria"].id))
            itemLayout.addWidget(buttonDelete)

            item = MyQListWidgetItem(cat["categoria"].id)
            item.setSizeHint(self.itemSize)

            self.listWidgetCategories.addItem(item)
            self.listWidgetCategories.setItemWidget(item, itemWidget)

        buttonAddAccount = QPushButton("+")
        buttonAddAccount.clicked.connect(self.slot_add_categoria)        
        
        itemLayout = QHBoxLayout()
        itemLayout.addWidget(buttonAddAccount)

        itemWidget  = QWidget()
        itemWidget.setLayout(itemLayout)
        self.itemsSize = itemWidget.sizeHint()

        item = QListWidgetItem()
        item.setSizeHint(self.itemsSize)

        self.listWidgetCategories.addItem(item)
        self.listWidgetCategories.setItemWidget(item, itemWidget)

    def chart_update(self, categories):
        series = QPieSeries()
        series.setHoleSize(0.4)

        sumExpenses = Linq.sum(
            Linq.select(
                categories,
                lambda c: c["expenses"]
            ),
            lambda c: c
        )

        for cat in categories:
            if sumExpenses != 0:
                series.append(str(cat["categoria"]), cat["expenses"] / sumExpenses * 100)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Title")

        self.chartView.setChart(chart)

    def slot_add_categoria(self):
        dlgInputWindow = DlgInputWindow("Type name for categoria")

        if dlgInputWindow.exec():
            self.appData.add_categoria(dlgInputWindow.input)

    def slot_remove_categoria(self, id: int):
        def remove_categoria():
            self.appData.remove_categoria_by_id(id)

        return remove_categoria
