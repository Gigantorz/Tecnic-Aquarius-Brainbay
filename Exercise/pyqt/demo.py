import sys
import subprocess
import threading
import time
import win32gui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindow, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QMainWindow, QLabel



class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.widget = QWidget()
        self.widget.setFixedSize(1980, 500)
        self.widget.setStyleSheet("background-color: yellow;")
        
        # Adjust path to the image as necessary
        self.label = QLabel(self)
        self.label.setPixmap(
            QPixmap('images/splash_.jpg').scaled(self.size().width() // 2, self.size().height(), Qt.AspectRatioMode.KeepAspectRatio)
        )
        
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.addWidget(self.widget, 0, 0, 2, 1)
        
        self.v_layout = QVBoxLayout(self.widget)
        self.initUI()
        self.grid_layout.addWidget(self.label, 0, 1, 1, 1)

    def initUI(self):
        t = threading.Thread(target=self.runExe)
        t.start()

        # Adjust these values based on the actual window title and class name of brainBay.exe
        hwnd = 0
        start = time.time()
        while hwnd == 0:
            time.sleep(0.01)
            hwnd = win32gui.FindWindowEx(0, 0, None, "brainbay")  # Window class name might need to be adjusted
            end = time.time()
            if end - start > 5:  # Timeout after 5 seconds
                print("Could not find the brainBay window.")
                return

        window = QWindow.fromWinId(hwnd)
        widget = QWidget.createWindowContainer(window, self.central_widget)
        self.v_layout.addWidget(widget)

    @staticmethod
    def runExe():
        # Update this path to the location of brainBay.exe on your system
        exePath = "C:\\Users\\Rayma\\AppData\\Local\\BrainBay\\brainBay.exe"
        subprocess.Popen(exePath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.resize(1980, 800)
    ex.show()
    sys.exit(app.exec())