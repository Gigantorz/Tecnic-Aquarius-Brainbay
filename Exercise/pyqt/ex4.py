import os

exe = 'brainbay.exe'  # Name of the executable file we're looking for

# Iterate over the directory tree starting from 'C:\AppData'
for root, dirs, files in os.walk(r'C:\Users'):
    for name in files:
        if name == exe:  # Check if the current file matches the desired executable
            print(os.path.abspath(os.path.join(root, name)))  # Print the absolute path of the executable


print("Not found?")