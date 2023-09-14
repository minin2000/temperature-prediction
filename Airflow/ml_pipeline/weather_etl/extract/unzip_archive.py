import gzip
import shutil
import os

def unzip_archive(file_path, file_name = "data.xls"):

    folder_path = os.path.dirname(file_path)
    # Step 1: Extract the .gz file
    full_path = os.path.join(folder_path, file_name)
    with gzip.open(file_path, 'rb') as f_in, open(full_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    # Step 2: Get XLS filepath
    xls_path = os.path.abspath(full_path)

    # Step 3: Delete the .gz file
    os.remove(file_path)
    print('| XLS successfully extracted.')
    return xls_path
