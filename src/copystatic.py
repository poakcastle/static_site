import os
import shutil

def copy_dir_content(dir_path):
    source = dir_path
    destination = source.replace("static", "public", 1)
    os.mkdir(destination)
    for item in os.listdir(dir_path):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        elif os.path.isdir(source_path):
            copy_dir_content(source_path)
        else:
            raise Exception(f"Error: {item} is neither a file nor a directory")