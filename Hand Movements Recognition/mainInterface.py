from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
import numpy as np
import cv2
import time
import pyautogui
import functions as fn


class MainInterface:
    def __init__(self):
        self.aLabel = ""

    def setupUi(self, TheDigitalHand):
        TheDigitalHand.resize(1200, 650)
        TheDigitalHand.setMinimumSize(QtCore.QSize(1200, 650))
        TheDigitalHand.setMaximumSize(QtCore.QSize(1200, 650))
        TheDigitalHand.setStyleSheet("background-color: #333")

        self.centralwidget = QtWidgets.QWidget(TheDigitalHand)

        # FONT FAMILY
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(12)

        # CAMERA
        self.groupBox_1 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_1.setGeometry(QtCore.QRect(70, 30, 480, 380))
        self.groupBox_1.setFont(font)
        self.groupBox_1.setStyleSheet("color: #78ca7c")

        # WHITEBOARD
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(640, 30, 480, 380))
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("color: #78ca7c")

        # AFFICHE CAMERA ET WHITEBOARD
        self.videoLabel_1 = QtWidgets.QLabel(self.groupBox_1)
        self.videoLabel_1.setGeometry(QtCore.QRect(0, 20, 480, 360))
        self.videoLabel_2 = QtWidgets.QLabel(self.groupBox_2)
        self.videoLabel_2.setGeometry(QtCore.QRect(0, 20, 480, 360))

        # ZONE DE TEXTE
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(70, 430, 1051, 80))
        self.groupBox_3.setFont(font)
        self.groupBox_3.setStyleSheet("color: #78ca7c")

        # ECRITURE DANS LA ZONE DE TEXTE
        self.labelDescription = QLabel(self.groupBox_3)
        self.labelDescription.setFont(font)
        self.labelDescription.setStyleSheet("color: #fff")
        self.labelDescription.move(10, 25)
        self.labelDescription.resize(600, 50)

        # BTN1
        self.checkBox_1 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_1.setGeometry(QtCore.QRect(100, 530, 231, 21))
        self.checkBox_1.setFont(font)
        self.checkBox_1.setStyleSheet("color: #78ca7c")

        # BTN2
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setGeometry(QtCore.QRect(500, 530, 301, 21))
        self.checkBox_2.setFont(font)
        self.checkBox_2.setStyleSheet("color: #78ca7c")

        # BTN3
        self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setGeometry(QtCore.QRect(890, 530, 181, 21))
        self.checkBox_3.setFont(font)
        self.checkBox_3.setStyleSheet("color: #78ca7c")

        # BTN4
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(540, 580, 111, 41))
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton{"
                                      "padding:1px;"
                                      "border-radius:5px;"
                                      "border:None;"
                                      "font-size:14px;"
                                      "background-color:#FF5733;"
                                      "color:#fff;}")
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.clicked.connect(TheDigitalHand.close)

        # LOGO
        self.image = QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(1090, 540, 100, 100))
        self.image.setMinimumSize(QtCore.QSize(100, 100))
        self.image.setMaximumSize(QtCore.QSize(100, 100))
        self.image.setPixmap(QPixmap("ressources/logo_ui.png"))

        TheDigitalHand.setCentralWidget(self.centralwidget)
        self.labeling(TheDigitalHand)
        QtCore.QMetaObject.connectSlotsByName(TheDigitalHand)

    def labeling(self, TheDigitalHand):
        _translate = QtCore.QCoreApplication.translate
        TheDigitalHand.setWindowTitle(_translate("TheDigitalHand", "The DigitalHand"))
        self.groupBox_1.setTitle(_translate("TheDigitalHand", "Camera"))
        self.groupBox_2.setTitle(_translate("TheDigitalHand", "White board"))
        self.groupBox_3.setTitle(_translate("TheDigitalHand", "Results display"))
        self.checkBox_1.setText(_translate("TheDigitalHand", "Display rectangle"))
        self.checkBox_2.setText(_translate("TheDigitalHand", "Enable mouse connection"))
        self.checkBox_3.setText(_translate("TheDigitalHand", "Display label"))
        self.pushButton.setText(_translate("TheDigitalHand", "Quit"))

    def btnState(self, checkBox):
        if checkBox is not None:
            return checkBox.isChecked()

        return False

    def mainLoop(self):
        pyautogui.FAILSAFE = False

        self.width, self.height = 480, 360
        self.wScreen, self.hScreen = pyautogui.size()
        self.frameR = 70
        self.epsilon = 17
        self.prev_frame_time = 0
        self.new_frame_time = 0

        self.smooth = 2
        self.plocX, self.plocY = 0, 0
        self.clocX, self.clocY = 0, 0

        self.cap = cv2.VideoCapture(1200)
        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

        self.HandTracer = fn.HandDetector()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateVideoFrame)
        self.timer.start(30)  # Délai en millisecondes (ici, 30fps)

    def updateVideoFrame(self):
        success, image1 = self.cap.read()
        width1, height1 = 640, 480
        rw1 = width1 / self.width
        rh1 = height1 / self.height
        state1 = self.btnState(self.checkBox_1)
        state2 = self.btnState(self.checkBox_2)
        state3 = self.btnState(self.checkBox_3)

        self.HandTracer.drawRectangleAndLabel(image1, rw1 * self.width, rh1 * self.height, self.epsilon, state1, state3,self.aLabel)

        whiteboard = np.full((self.height, self.width, 3), (255, 255, 255), dtype=np.uint8)
        self.HandTracer.drawHandOnWhiteBoard(whiteboard)
        whichHand = self.HandTracer.whichHand(whiteboard)
        fingerPositionList = self.HandTracer.mouseTracer(whiteboard, self.wScreen, state2)

        if state2:
            self.labelDescription.setText(">> Connection established")
        else:
            self.labelDescription.setText(">> Waiting for connection...")

        if len(fingerPositionList) != 0:
            x1, y1 = fingerPositionList[8][1:]
            fingers = self.HandTracer.countUpFingers(whichHand)

            if state3:
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    self.aLabel = "Track"

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    self.aLabel = "Click mode"

                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                    self.aLabel = "Right click"

                elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    self.aLabel = "Copy"

                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    self.aLabel = "Past"

                elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    self.aLabel = "Drag"
                else:
                    self.aLabel = ""

            cv2.rectangle(image1, (self.frameR, self.frameR), (int(rw1 * (self.width - self.frameR)), int(rh1 * (self.height - self.frameR))), (255, 0, 255), 2)

            if state2:
                # TRACK  MODE
                if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    x3 = np.interp(x1, (self.frameR, self.width - self.frameR), (0, self.wScreen))
                    y3 = np.interp(y1, (self.frameR, self.height - self.frameR), (0, self.hScreen))
                    clocX = self.plocX + (x3 - self.plocX) / self.smooth
                    clocY = self.plocY + (y3 - self.plocY) / self.smooth
                    pyautogui.moveTo(self.wScreen - clocX, clocY)
                    cv2.circle(image1, (int(rw1 * x1), int(rh1 * y1)), 10, (0, 0, 255), cv2.FILLED)
                    self.labelDescription.setText(">> Track")
                    self.plocX, self.plocY = clocX, clocY

                # CLICK MODE : SIMPLE AND DOUBLE CLICK
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    length = self.HandTracer.distanceBetweenTwoFingers(8, 12)
                    self.labelDescription.setText(">> Click mode")
                    if length < 25:
                        cv2.circle(image1, (int(rw1 * x1), int(rh1 * y1)), 10, (0, 255, 255), cv2.FILLED)
                        pyautogui.click()
                        self.labelDescription.setText(">> Click detected")

                # RIGHT CLICK
                elif fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 0:
                    x3 = np.interp(x1, (self.frameR, self.width - self.frameR), (0, self.wScreen))
                    y3 = np.interp(y1, (self.frameR, self.height - self.frameR), (0, self.hScreen))
                    clocX = self.plocX + (x3 - self.plocX) / self.smooth
                    clocY = self.plocY + (y3 - self.plocY) / self.smooth
                    pyautogui.rightClick(self.wScreen - clocX, clocY)
                    self.labelDescription.setText(">> Right click")
                    self.plocX, self.plocY = clocX, clocY

                # COPY
                elif fingers[0] == 1 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('c')
                    self.labelDescription.setText(">> Copy")

                # PAST
                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('v')
                    self.labelDescription.setText(">> Past")

                # DRAG
                elif fingers[0] == 0 and fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    pyautogui.mouseDown()
                    x3 = np.interp(x1, (self.frameR, self.width - self.frameR), (0, self.wScreen))
                    y3 = np.interp(y1, (self.frameR, self.height - self.frameR), (0, self.hScreen))
                    clocX = self.plocX + (x3 - self.plocX) / self.smooth
                    clocY = self.plocY + (y3 - self.plocY) / self.smooth
                    self.plocX, self.plocY = clocX, clocY
                    pyautogui.moveTo(self.wScreen - clocX, clocY)

                # DROP
                elif fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
                    pyautogui.mouseUp()
                
                else:
                    self.labelDescription.setText(">> ")

        # CALCUL FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - self.prev_frame_time)
        self.prev_frame_time = new_frame_time
        fps = int(fps)

        # TRAITEMENT POUR AFFICHAGE
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        image1 = QImage(image1.data, image1.shape[1], image1.shape[0], QImage.Format_RGB888)
        whiteboard = cv2.cvtColor(whiteboard, cv2.COLOR_BGR2RGB)
        whiteboard = QImage(whiteboard.data, whiteboard.shape[1], whiteboard.shape[0], QImage.Format_RGB888)

        # AFFICHE FPS
        painter = QPainter(image1)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont()
        font.setFamily("Courier")
        font.setPointSize(20)
        painter.setFont(font)
        fill_color = QColor(255, 255, 0)
        painter.setPen(fill_color)
        painter.drawText(520, 35, "FPS : " + str(fps))
        painter.end()

        # AFFICHE CAMERA ET WHITEBOARD
        scaled_image_1 = image1.scaled(self.videoLabel_1.size(), Qt.AspectRatioMode.KeepAspectRatio)
        scaled_image_2 = whiteboard.scaled(self.videoLabel_2.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.videoLabel_1.setPixmap(QPixmap.fromImage(scaled_image_1))
        self.videoLabel_2.setPixmap(QPixmap.fromImage(scaled_image_2))