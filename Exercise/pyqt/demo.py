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
        """
        There is something wrong about how the windows handler is being retrieved or even how it is working that it is not grabbing the 
        entirity of the brainbay software, because there are still some stuff that are floating around from it. 

        This doesn't mean it won't work well with other software, so this could still work with MNE scan and analyze.
        """

        while hwnd == 0:
            time.sleep(0.01) # to give the other thread execute the runExe() function and launch brainbay
            # Part of the win32 gui module, which is a python wrapper for the windows API
            # FindWindowEx retrieves a handle toa window whose class name and window name matched the specified string.
            hwnd = win32gui.FindWindowEx(0, 0, None, "brainbay")  # Get the windows handler.
            end = time.time()
            if end - start > 5:  # Timeout after 5 seconds
                print("Could not find the brainBay window.")
                return

        # Qwindow is a class that represents a window in the underlying windowing system.
        window = QWindow.fromWinId(hwnd) # if window is found return the windowID
        widget = QWidget.createWindowContainer(window, self.central_widget) # The found windowID is wrapped in a widget container using createWindowContainer
        self.v_layout.addWidget(widget) # container widget is added to the vertical_layout.

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