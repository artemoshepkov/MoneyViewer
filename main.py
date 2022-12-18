import sys
import time

from PyQt6.QtWidgets import *
from PyQt6.uic import loadUi
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from mainWindow import *

class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()

        self.initUI()


    def initUI(self):
        self.setStyleSheet(
            """
            background-color: #C9C7C7 
            """
        )

        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        label = QLabel("Welcome")
        label.setStyleSheet("""
            QLabel {
                font-size: 15px;
            }
        """)
        mainLayout.addWidget(label, 1, Qt.AlignmentFlag.AlignCenter)

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(101) 
        mainLayout.addWidget(self.progressBar, 1, Qt.AlignmentFlag.AlignCenter)

    def progress(self):
        for i in range(1, 101):
            time.sleep(0.01)
            self.progressBar.setValue(i)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    splashScreen = SplashScreen()
    splashScreen.show()
    splashScreen.progress()

    mainWindow = MainWindow()

    splashScreen.finish(mainWindow)

    mainWindow.show()

    app.exec()