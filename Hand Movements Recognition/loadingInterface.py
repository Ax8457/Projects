from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QProgressBar, QLabel, QFrame, QVBoxLayout
import time


class LoadingInterface(QWidget):
    def __init__(self, TheDigitalHand):
        super().__init__()
        self.setFixedSize(600,450)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.aTheDigitalHand = TheDigitalHand
        self.aCounter = 0
        self.aIteration = 120

        self.initui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        self.frame.setStyleSheet("QFrame{background-color: #333;"
                                 "color: #fff;}")
        layout.addWidget(self.frame)

        # FONT FAMILY
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(40)

        # TITLE
        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setFont(font)
        self.labelTitle.setStyleSheet("color: #78ca7c;")
        self.labelTitle.resize(self.width(), 150)
        self.labelTitle.move(-20, 40)
        self.labelTitle.setText('The DigitalHand')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        # LOADING LABEL
        self.labelLoading = QLabel(self.frame)
        self.labelLoading.setFont(font)
        self.labelLoading.resize(self.width(), 50)
        self.labelLoading.move(-20, self.labelTitle.height() + 40)
        self.labelLoading.setStyleSheet("color: #fff")
        self.labelLoading.setText("loading")
        self.labelLoading.setAlignment(Qt.AlignCenter)

        # PROGRESS BAR
        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(396, 50)
        self.progressBar.move(90, self.labelLoading.y() + 90)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar{"
                                       "background-color: #fff;"
                                       "color:#333;"
                                       "border-radius: 5px;}"
                                       "QProgressBar::chunk {"
                                       "background-color: #78ca7c;"
                                       "width:20px;"
                                       "margin:0.5px;"
                                       "border-radius: 5px;}")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setRange(0, self.aIteration)
        self.progressBar.setValue(20)

    def loading(self):
        self.progressBar.setValue(self.aCounter)

        if self.aCounter == int(self.aIteration * 0.3):
            self.labelLoading.setText("loading.")
        elif self.aCounter == int(self.aIteration * 0.6):
            self.labelLoading.setText("loading..")
        elif self.aCounter == int(self.aIteration * 0.9):
            self.labelLoading.setText("loading...")
        elif self.aCounter >= self.aIteration:
            self.timer.stop()
            self.close()
            time.sleep(1)

            self.aTheDigitalHand.show()

        self.aCounter += 1