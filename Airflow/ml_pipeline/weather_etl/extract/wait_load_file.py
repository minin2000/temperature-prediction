import os
import time

def wait_load_file(folder_path, timeout = 15, file_extension = ".xls.gz"):

    start_time = time.time()

    while time.time() - start_time < timeout:
        gz_files = [file for file in os.listdir(folder_path) if file.endswith(file_extension)]
        if len(gz_files) == 1:
            file_name = gz_files[0]
            file_path = os.path.join(folder_path, file_name)
            print('| File successfully downloaded.')
            return(file_path) 
        time.sleep(1)  # Wait for 1 second before checking again

    if len(gz_files) == 0:
        raise Exception("| No file found within the timeout.")
    elif len(gz_files) > 1:
        raise Exception("| Multiple files found within the timeout.")
    