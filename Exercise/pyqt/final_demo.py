"""
Written by: Raymart Datuin
Tecniq Aquarius
Winter 2024
University of Alberta
 
Description:

Notes:
"""
import logging
import os
import glob
import time
import concurrent.futures
from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication, QPushButton
import concurrent.futures

logging.basicConfig(level=logging.INFO)

class MyApp(QPushButton):
    """
    This class makes a clickable button that launches brainbay.exe
    
    Quality of life feature:
    - finds brainbay.exe wherever stored in the os.
    - launches separate window, for brainbay.exe
    """
    def __init__(self):
        super().__init__('Launch BrainBay')
        self.exePath = False
        self.exePath = self.app_data_search()
        if not self.exePath:
            self.exePath = self.everywhere_data_search()
            if not self.exePath:
                logging.error("Failed to find .exe file, please reinstall Brainbay.exe and make sure use default settings")
                exit(0)
        self.setGeometry(500, 500, 450, 400)
        self.setWindowTitle('Exercise 3')
        self.show()
        self.process = QProcess(self)
        self.clicked.connect(self.launchBrainBay)

    def find_file(self, start_path, filename):
        """
        Finds the file in the operating system
        """
        pattern = os.path.join(start_path, '**', filename)
        for filepath in glob.glob(pattern, recursive=True):
            return filepath
        return None

    def app_data_search(self):
        """
        Searches through the AppData hidden folder within user for brainbay.exe, because that is the 
        brainbay.exe default folder. 
        """
        start_time = time.time()
        local_appdata_path = os.getenv('LOCALAPPDATA')
        target_file = 'brainbay.exe'
        file_path = self.find_file(local_appdata_path, target_file)
        logging.info("Total Time elapsed %s", time.time() - start_time)

        if file_path:
            return file_path
        else:
            logging.warning("%s not found in %s or its subdirectories.", target_file, local_appdata_path)
            return False

    def everywhere_data_search(self):
        """
        Searches through whole computer to find brainbay.exe. Last ditch effor if can't be found in 
        AppData directory, because this twice slower than app_data_search(), even though we are using concurrency.
        """
        start_time = time.time()
        target_file = 'brainbay.exe'
        start_paths = [drive + ":\\" for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(drive + ":\\")]
        found_files = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_path = {executor.submit(self.search_for_file, start_path, target_file): start_path for start_path in start_paths}
            for future in concurrent.futures.as_completed(future_to_path):
                filepath = future.result()
                if filepath:
                    found_files.append(filepath)
        logging.info("Total Time elapsed %s", time.time() - start_time)
        if found_files:
            for file_path in found_files:
                logging.info("Found: %s", self.double_backslashes(file_path))
                return file_path
        else:
            logging.warning("%s not found anywhere on the system.", target_file)
            return False

    def launchBrainBay(self):
        """
        After clicking the button, this will launch brainbay.
        """
        self.process.start(self.exePath)

if __name__ == '__main__':
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec()
