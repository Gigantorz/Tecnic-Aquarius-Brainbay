import sys
import subprocess
import threading
import time
import win32gui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindow, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QMainWindow, QLabel
import os
import glob
import concurrent.futures


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
        # Update this path to the location of brainBay.exe on your system
        exePath = self.app_data_search()
        if not exePath:
            exePath = self.everywhere_data_search()
            if not exePath:
                print("Failed to find .exe file, please reinstall Brainbay.exe and make sure use default settings")
                exit(0)
        # exePath = "C:\\Users\\Rayma\\AppData\\Local\\BrainBay\\brainBay.exe"
        t = threading.Thread(target=self.runExe(exePath))
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

    def find_file(self, start_path, filename):
        # Construct a search pattern
        pattern = os.path.join(start_path, '**', filename)
        # Search for the file using the pattern, in all subdirectories
        for filepath in glob.glob(pattern, recursive=True):
            return filepath  # Return the first file match
        return None  # Return None if the file is not found

    def double_backslashes(self, input_string):
        # Replace each backslash with two backslashes
        return input_string.replace("\\", "\\\\")

    def app_data_search(self):
        start_time = time.time()
        # Explicitly use the LOCALAPPDATA environment variable to target AppData\Local
        local_appdata_path = os.getenv('LOCALAPPDATA')
        target_file = 'brainbay.exe'
        
        # Search for brainbay.exe within AppData\Local
        file_path = self.find_file(local_appdata_path, target_file)
        print("Total Time elapsed ", time.time() - start_time)

        if file_path:
            # If found, adjust the file path to use double backslashes
            modified_string = self.double_backslashes(file_path)
            print("Modified string:", modified_string)
            return file_path
        else:
            # If not found, print a message specifying the search was in AppData\Local
            print(f"{target_file} not found in {local_appdata_path} or its subdirectories.")
            return False

    def everywhere_data_search(self):
        start_time = time.time()
        target_file = 'brainbay.exe'
        # Define start paths as different partitions or directories you want to search in
        start_paths = [drive + ":\\" for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(drive + ":\\")]
        found_files = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map the search function to the executor with multiple start paths
            future_to_path = {executor.submit(self.search_for_file, start_path, target_file): start_path for start_path in start_paths}
            for future in concurrent.futures.as_completed(future_to_path):
                filepath = future.result()
                if filepath:
                    found_files.append(filepath)
        print("Total Time elapsed ", time.time() - start_time)
        if found_files:
            for file_path in found_files:
                print("Found:", self.double_backslashes(file_path))
                return file_path
        else:
            print(f"{target_file} not found anywhere on the system.")
            return False

    @staticmethod
    def runExe(exePath):
        subprocess.Popen(exePath)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.resize(1980, 800)
    ex.show()
    sys.exit(app.exec())