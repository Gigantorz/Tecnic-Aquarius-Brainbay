import os
import glob
import time

def find_file(start_path, filename):
    # Construct a search pattern
    pattern = os.path.join(start_path, '**', filename)
    # Search for the file using the pattern, in all subdirectories
    for filepath in glob.glob(pattern, recursive=True):
        return filepath  # Return the first file match
    return None  # Return None if the file is not found

def double_backslashes(input_string):
    # Replace each backslash with two backslashes
    return input_string.replace("\\", "\\\\")

if __name__ == "__main__":
    start_time = time.time()
    # Explicitly use the LOCALAPPDATA environment variable to target AppData\Local
    local_appdata_path = os.getenv('LOCALAPPDATA')
    target_file = 'brainbay.exe'
    
    # Search for brainbay.exe within AppData\Local
    file_path = find_file(local_appdata_path, target_file)
    
    if file_path:
        # If found, adjust the file path to use double backslashes
        modified_string = double_backslashes(file_path)
        print("Modified string:", modified_string)
    else:
        # If not found, print a message specifying the search was in AppData\Local
        print(f"{target_file} not found in {local_appdata_path} or its subdirectories.")
    print("Total Time elapsed ", time.time() - start_time)