from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QPushButton


# In the pyQT application, where you want to launch Brainbay, you will
# Create an instance of 'QProcess'
# This instance will be used to start the brainbay application

class MyApp(QPushButton):
    def __init__(self):
        super().__init__('Launch BrainBay')
        self.process = QProcess(self)
        self.clicked.connect(self.launchBrainBay)

    def launchBrainBay(self):
        address = "~/home/gigantorz/.wine/drive_c/users/gigantorz/AppData/Local/BrainBay"
        self.process.start(address)

if __name__ == '__main__':
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()