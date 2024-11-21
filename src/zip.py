import os
import zipfile
import shutil

def zip_folder_in_parts(folder_path, zip_file_name, part_size):
    # Create a temporary zip file
    temp_zip_file = zip_file_name + '.zip'
    
    # Create a zip file
    with zipfile.ZipFile(temp_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder and add files to the zip
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Split the zip file into parts
    part_number = 1
    with open(temp_zip_file, 'rb') as f:
        while True:
            part_file_name = f"{zip_file_name}.part{part_number:03d}.zip"
            with open(part_file_name, 'wb') as part_file:
                part_data = f.read(part_size)
                if not part_data:
                    break
                part_file.write(part_data)
                print(f'Created: {part_file_name}')
            part_number += 1

    # Remove the temporary zip file
    os.remove(temp_zip_file)
    print(f'Removed temporary zip file: {temp_zip_file}')

# Example usage
folder_to_zip = '/home/dev06/Downloads/wordpress'  # Replace with your folder path
output_zip_file = 'output_zip'          # Replace with your desired output zip file name
max_part_size = 10 * 1024 * 1024        # Size limit in bytes (10 MB in this case)

zip_folder_in_parts(folder_to_zip, output_zip_file, max_part_size)
