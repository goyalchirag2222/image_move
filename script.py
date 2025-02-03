import os
import shutil

current_directory = os.getcwd()  # This gets the current working directory
target_directory = 'older'  # Name of the target folder where you want to move images

# Check if the target folder exists, if not, create it
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# Loop through all files in the current directory
for file_name in os.listdir(current_directory):
    # Check if the file is a PNG image
    if file_name.lower().endswith('.png'):
        # Build the full path to the file
        file_path = os.path.join(current_directory, file_name)
        
        target_path = os.path.join(current_directory, target_directory, file_name)
        
        # Move the file to the target directory
        shutil.move(file_path, target_path)
        print(f"Moved {file_name} to {target_directory}")
