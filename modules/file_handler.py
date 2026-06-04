import os
import shutil

def move_to_processed(file_path):
    
    filename = os.path.basename(file_path)
    
    destination = os.path.join("processed", filename)
    
    shutil.move(file_path, destination)

    print(f"{filename} moved to processed folder successfully!")