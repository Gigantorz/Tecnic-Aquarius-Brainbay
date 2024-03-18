import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton
import subprocess
import time
from win32gui import FindWindow, GetWindowRect

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PyQt Wrapper')
        self.initUI()

    def initUI(self):
        # Example: Launch notepad.exe
        subprocess.Popen(["notepad.exe"])
        time.sleep(1)  # Wait for the window to open. Adjust as necessary.

        # Find the window handle for Notepad
        hwnd = FindWindow(None, "Untitled - Notepad")

        if hwnd:
            rect = GetWindowRect(hwnd)  # Get window dimensions
            x, y, width, height = rect
            self.setGeometry(x, y, width - x, height - y)  # Resize PyQt window

        # Create a button
        button = QPushButton("Click me", self)
        button.setGeometry(10, 10, 100, 30)  # Set button position and size

app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())