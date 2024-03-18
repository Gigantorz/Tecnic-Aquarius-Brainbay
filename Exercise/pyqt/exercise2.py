import subprocess
import time
import win32gui


def initUI(self):
    # create a process
    address_windows2 = "C:\\Users\\Rayma\\AppData\\Local\\BrainBay\\brainBay.exe"
    subprocess.Popen(address_windows2)
    hwnd = win32gui.FindWindowEx(0, 0, "brainbayFrame", "brainbay")
    time.sleep(0.05)
    window = QWindow.fromWinId(hwnd)
    self.createWindowContainer(window, self)
    self.setGeometry(500, 500, 450, 400)
    self.setWindowTitle('File dialog')
    self.show()

## Get this to work...