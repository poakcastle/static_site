import os
import shutil

def copy_dir_content(dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
         os.makedirs(dest_dir_path)
    for item in os.listdir(dir_path):
        source_path = os.path.join(dir_path, item)
        destination_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            copy_dir_content(source_path, destination_path)
        else:
            raise Exception(f"Error: {item} is neither a file nor a directory")