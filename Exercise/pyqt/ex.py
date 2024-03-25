import os
import glob
import concurrent.futures
import time

def search_for_file(start_path, filename):
    pattern = os.path.join(start_path, '**', filename)
    for filepath in glob.iglob(pattern, recursive=True):
        return filepath
    return None

def double_backslashes(input_string):
    return input_string.replace("\\", "\\\\")

if __name__ == "__main__":
    start_time = time.time()
    target_file = 'brainbay.exe'
    # Define start paths as different partitions or directories you want to search in
    start_paths = [drive + ":\\" for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(drive + ":\\")]
    found_files = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map the search function to the executor with multiple start paths
        future_to_path = {executor.submit(search_for_file, start_path, target_file): start_path for start_path in start_paths}
        for future in concurrent.futures.as_completed(future_to_path):
            filepath = future.result()
            if filepath:
                found_files.append(filepath)

    if found_files:
        for file_path in found_files:
            print("Found:", double_backslashes(file_path))
    else:
        print(f"{target_file} not found anywhere on the system.")
    print("Total Time elapsed ", time.time() - start_time)