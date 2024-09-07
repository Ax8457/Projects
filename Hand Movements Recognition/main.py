import sys
from PyQt5 import QtWidgets
import mainInterface as uitf
import loadingInterface as litf

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    TheDigitalHand = QtWidgets.QMainWindow()
    ui = uitf.MainInterface()
    ui.setupUi(TheDigitalHand)
    ui.mainLoop()
    loading = litf.LoadingInterface(TheDigitalHand)
    loading.show()
    sys.exit(app.exec_())
