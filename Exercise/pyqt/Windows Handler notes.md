
# Windows "Handle"
an abstract reference value to a resource, often memory or an open file or a pipe.

a handle is an abstraction which hides a real memory address from the API user allowing the system to reorganize physical memory transparently to the program.
Resolving a handle into a pointer locks the memory, and releasing the handle invalidates the pointer.
	In this case think of it as an index into a table of pointer..
		you use the index for the system API calls, and the system change the pointer in the table at will

Alternatively a real pointer may be given as the handle when the API writer intends that the user of the API be insulated from the specifics of what the address returned points to; 
	in this case it must be considered that what handle points to may change at any time
	the handle should therefore be treated as simply an opaque meaningful only to the api.

In any modern operating system, even the so-called "real pointers" are still opaque handles into the virtual memory space of the process, which enables the O/S to manage and rearrange memory without invalidating the pointers within the process.

The value of a handle is not meaningful. It should be treated as an opaque value.

---
A `HANDLE` is a context-specific unique identifier. By context-specific, I mean that a handle obtained from one context cannot necessarily be used in any other aribtrary context that also works on `HANDLE`s.

For example, `GetModuleHandle` returns a unique identifier to a currently loaded module. The returned handle can be used in other functions that accept module handles. It cannot be given to functions that require other types of handles. For example, you couldn't give a handle returned from `GetModuleHandle` to `HeapDestroy` and expect it to do something sensible.

The `HANDLE` itself is just an integral type. Usually, but not necessarily, it is a pointer to some underlying type or memory location. For example, the `HANDLE` returned by `GetModuleHandle` is actually a pointer to the base virtual memory address of the module. But there is no rule stating that handles must be pointers. A handle could also just be a simple integer (which could possibly be used by some Win32 API as an index into an array).

`HANDLE`s are intentionally opaque representations that provide encapsulation and abstraction from internal Win32 resources. This way, the Win32 APIs could potentially change the underlying type behind a HANDLE, without it impacting user code in any way (at least that's the idea).

Consider these three different internal implementations of a Win32 API that I just made up, and assume that `Widget` is a `struct`.

```cpp
Widget * GetWidget (std::string name)
{
    Widget *w;

    w = findWidget(name);

    return w;
}
```

```cpp
void * GetWidget (std::string name)
{
    Widget *w;

    w = findWidget(name);

    return reinterpret_cast<void *>(w);
}
```

```cpp
typedef void * HANDLE;

HANDLE GetWidget (std::string name)
{
    Widget *w;

    w = findWidget(name);

    return reinterpret_cast<HANDLE>(w);
}
```

The first example exposes the internal details about the API: it allows the user code to know that `GetWidget` returns a pointer to a `struct Widget`. This has a couple of consequences:

- the user code must have access to the header file that defines the `Widget` struct
- the user code could potentially modify internal parts of the returned `Widget` struct

Both of these consequences may be undesirable.

The second example hides this internal detail from the user code, by returning just `void *`. The user code doesn't need access to the header that defines the `Widget` struct.

The third example is exactly the same as the second, but we just call the `void *` a `HANDLE` instead. Perhaps this discourages user code from trying to figure out exactly what the `void *` points to.

Why go through this trouble? Consider this fourth example of a newer version of this same API:

```cpp
typedef void * HANDLE;

HANDLE GetWidget (std::string name)
{
    NewImprovedWidget *w;

    w = findImprovedWidget(name);

    return reinterpret_cast<HANDLE>(w);
}
```

Notice that the function's interface is identical to the third example above. This means that user code can continue to use this new version of the API, without any changes, even though the "behind the scenes" implementation has changed to use the `NewImprovedWidget` struct instead.

The handles in these example are really just a new, presumably friendlier, name for `void *`, which is exactly what a `HANDLE` is in the Win32 API (look it up [at MSDN](http://msdn.microsoft.com/en-us/library/aa383751(VS.85).aspx)). It provides an opaque wall between the user code and the Win32 library's internal representations that increases portability, between versions of Windows, of code that uses the Win32 API.

---
https://stackoverflow.com/questions/52282780/what-is-the-proper-way-to-manage-windows-in-pyqt5

Closes Answer: https://stackoverflow.com/questions/63597475/running-a-windows-executable-calc-exe-etc-inside-a-pyqt-application


built off of this question:
https://stackoverflow.com/questions/41474647/run-a-foreign-exe-inside-a-python-gui-pyqt

---
The provided source code is a Python script that utilizes the PyQt6 library to create a graphical user interface (GUI) application. Let's go through the code and examine the PyQt6 calls and functions that are being used.

1. importing the necessary modules
``` python
import sys
import subprocess
import threading
import time
import win32gui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWindow, QPixmap
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QMainWindow, QLabel
```
- `sys` module is imported to access system-specific parameters and functions.
- `subprocess` module is imported to create a new process and run an external executable.
- `threading` module is imported to create and manage threads for concurrent execution.
- `time` module is imported to work with time-related functions.
- `win32gui` module is imported to interact with the Windows GUI.
- `Qt` module from PyQt6.QtCore is imported to access Qt constants.
- `QWindow`, `QPixmap`, `QWidget`, `QApplication`, `QVBoxLayout`, `QGridLayout`, `QMainWindow`, and `QLabel` classes are imported from PyQt6.QtWidgets to create the GUI components.
2 Class declaration:
``` python
class Example(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.widget = QWidget()
        self.widget.setFixedSize(500, 500)
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
```
- The `Example` class is defined, which inherits from the `QMainWindow` class provided by PyQt6.
- In the constructor (`__init__`), the `super()` function is called to initialize the base class (`QMainWindow`).
- The central widget of the main window is set to an instance of `QWidget` called `self.central_widget`.
- Another widget called `self.widget` is created and its size is fixed to 500x500 pixels. It is styled with a yellow background color.
- An image label (`QLabel`) is created and set as a child of the main window (`self`).
- The image for the label is set using a QPixmap, which loads an image file (`'images/splash_.jpg'`) and scales it to half the width of the main window while maintaining the aspect ratio.
- A grid layout (`QGridLayout`) is created on the central widget, and the `self.widget` is added to it at position (0, 0) spanning 2 rows and 1 column.
- A vertical layout (`QVBoxLayout`) is created on `self.widget`.
- The `initUI()` method is called to initialize the UI.
- The image label (`self.label`) is added to the grid layout at position (0, 1).

3. `initUI()` method:
``` python
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
```

- The `initUI()` method is responsible for initializing the user interface.
- A new thread (`threading.Thread`) is created with the `runExe()` method as the target. This allows the application to run an external executable concurrently.
- The `hwnd` variable is initialized to 0.
- A timer is started using `start = time.time()`.
- A while loop is used to find the window with the class name "brainbay" using the `win32gui.FindWindowEx()` function. The loop continues until the window is found or the timeout (5 seconds) is reached.
- Inside the loop, a small delay (`time.sleep(0.01)`) is introduced to avoid excessive CPU usage.
- If the window is not found within the timeout, a message is printed and the method returns.
- If the window is found, a `QWindow` object is created from the window handle (`hwnd`).
- The `QWindow` is wrapped in a widget container using `QWidget.createWindowContainer()`.
- The container widget is added to the vertical layout (`self.v_layout`).

4. `runExe()` method:
``` python
@staticmethod
def runExe():
    # Update this path to the location of brainBay.exe on your system
    exePath = "C:\\Users\\Rayma\\AppData\\Local\\BrainBay\\brainBay.exe"
    subprocess.Popen(exePath)
```

The provided source code is a Python script that utilizes the PyQt6 library to create a graphical user interface (GUI) application. Let's go through the code and examine the PyQt6 calls and functions that are being used.

1. Importing the necessary modules:
   ```python
   import sys
   import subprocess
   import threading
   import time
   import win32gui
   from PyQt6.QtCore import Qt
   from PyQt6.QtGui import QWindow, QPixmap
   from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QGridLayout, QMainWindow, QLabel
   ```
   - `sys` module is imported to access system-specific parameters and functions.
   - `subprocess` module is imported to create a new process and run an external executable.
   - `threading` module is imported to create and manage threads for concurrent execution.
   - `time` module is imported to work with time-related functions.
   - `win32gui` module is imported to interact with the Windows GUI.
   - `Qt` module from PyQt6.QtCore is imported to access Qt constants.
   - `QWindow`, `QPixmap`, `QWidget`, `QApplication`, `QVBoxLayout`, `QGridLayout`, `QMainWindow`, and `QLabel` classes are imported from PyQt6.QtWidgets to create the GUI components.

2. Class declaration:
   ```python
   class Example(QMainWindow):
       def __init__(self):
           super().__init__()

           self.central_widget = QWidget()
           self.setCentralWidget(self.central_widget)
           
           self.widget = QWidget()
           self.widget.setFixedSize(500, 500)
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
   ```
   - The `Example` class is defined, which inherits from the `QMainWindow` class provided by PyQt6.
   - In the constructor (`__init__`), the `super()` function is called to initialize the base class (`QMainWindow`).
   - The central widget of the main window is set to an instance of `QWidget` called `self.central_widget`.
   - Another widget called `self.widget` is created and its size is fixed to 500x500 pixels. It is styled with a yellow background color.
   - An image label (`QLabel`) is created and set as a child of the main window (`self`).
   - The image for the label is set using a QPixmap, which loads an image file (`'images/splash_.jpg'`) and scales it to half the width of the main window while maintaining the aspect ratio.
   - A grid layout (`QGridLayout`) is created on the central widget, and the `self.widget` is added to it at position (0, 0) spanning 2 rows and 1 column.
   - A vertical layout (`QVBoxLayout`) is created on `self.widget`.
   - The `initUI()` method is called to initialize the UI.
   - The image label (`self.label`) is added to the grid layout at position (0, 1).

3. `initUI()` method:
   ```python
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
   ```
   - The `initUI()` method is responsible for initializing the user interface.
   - A new thread (`threading.Thread`) is created with the `runExe()` method as the target. This allows the application to run an external executable concurrently.
   - The `hwnd` variable is initialized to 0.
   - A timer is started using `start = time.time()`.
   - A while loop is used to find the window with the class name "brainbay" using the `win32gui.FindWindowEx()` function. The loop continues until the window is found or the timeout (5 seconds) is reached.
   - Inside the loop, a small delay (`time.sleep(0.01)`) is introduced to avoid excessive CPU usage.
   - If the window is not found within the timeout, a message is printed and the method returns.
   - If the window is found, a `QWindow` object is created from the window handle (`hwnd`).
   - The `QWindow` is wrapped in a widget container using `QWidget.createWindowContainer()`.
   - The container widget is added to the vertical layout (`self.v_layout`).

4. `runExe()` method:
   ```python
   @staticmethod
   def runExe():
       # Update this path to the location of brainBay.exe on your system
       exePath = "C:\\Users\\Rayma\\AppData\\Local\\BrainBay\\brainBay.exe"
       subprocess.Popen(exePath)
   ```
   - The `runExe()` method is a static method that runs an external executable (`brainBay.exe` in this case).
   - The path to the executable is specified in the `exePath` variable. You may need to update this path to match the location of the `brainBay.exe` file on your system.
   - The `subprocess.Popen()` function is used to launch the executable.

Overall, this code sets up a PyQt6 application with a main window, a fixed-size widget, and an image label. It also runs an external executable (`brainBay.exe`) in a separate thread and embeds its window within the application's UI.


The `initUI(self)` method in your exercise2.py file is responsible for initializing the user interface of your PyQt application. Let's break down its functionality:

1. `t = threading.Thread(target=self.runExe)`: This line creates a new thread that will run the `runExe` method. This allows the application to run an external executable concurrently with the rest of the PyQt application.
    
2. `t.start()`: This line starts the execution of the thread.
    
3. `hwnd = 0`: This line initializes a variable `hwnd` which will later hold the handle to the window of the external application.
    
4. The `while hwnd == 0:` loop: This loop is used to continuously check if the window of the external application has been created yet. It does this by calling the `win32gui.FindWindowEx` function.
    
    - `win32gui.FindWindowEx(0, 0, None, "brainbay")`: This function is part of the `win32gui` module, which is a Python wrapper for the Windows API. The `FindWindowEx` function retrieves a handle to a window whose class name and window name match the specified strings. In this case, it's looking for a window with the name "brainbay". If it finds such a window, it returns the handle to this window. If it doesn't, it returns `0`.
5. `window = QWindow.fromWinId(hwnd)`: Once the handle to the window is obtained, this line creates a `QWindow` object from it. `QWindow` is a class provided by PyQt that represents a window in the underlying windowing system. `fromWinId` is a static method of `QWindow` that creates a `QWindow` object from a window system identifier. In this case, it's creating a `QWindow` object from the handle of the "brainbay" window.
    
6. `widget = QWidget.createWindowContainer(window, self.central_widget)`: This line creates a `QWidget` that can contain the `QWindow` object. `QWidget` is a base class for all user interface objects in PyQt, and `createWindowContainer` is a static method that creates a `QWidget` which makes it possible to embed platforms that have native child widgets, such as Windows and macOS, into Qt applications. The `window` parameter is the `QWindow` object to be embedded, and `self.central_widget` is the parent widget.
    
7. `self.v_layout.addWidget(widget)`: Finally, this line adds the newly created `QWidget` to the vertical layout (`self.v_layout`) of the PyQt application. This effectively embeds the "brainbay" window into the PyQt application.