import os
import zipfile

def unzip_parts(zip_file_name, output_folder):
    # Concatenate all parts into a single zip file
    temp_zip_file = zip_file_name + '.zip'
    with open(temp_zip_file, 'wb') as full_zip:
        part_number = 1
        while True:
            part_file_name = f"{zip_file_name}.part{part_number:03d}.zip"
            if not os.path.isfile(part_file_name):
                break  # Exit if no more parts are found
            
            with open(part_file_name, 'rb') as part_file:
                full_zip.write(part_file.read())
                print(f'Added: {part_file_name}')

            part_number += 1

    # Now extract the combined zip file
    with zipfile.ZipFile(temp_zip_file, 'r') as zipf:
        zipf.extractall(output_folder)
        print(f'Extracted all parts to: {output_folder}')

    # Optionally remove the temporary combined zip file
    os.remove(temp_zip_file)
    print(f'Removed temporary zip file: {temp_zip_file}')

# Example usage
base_zip_file_name = 'output_zip'  # Base name of the zip files (without .partXX.zip)
output_directory = 'unzipped_content'  # Directory to extract files to

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

unzip_parts(base_zip_file_name, output_directory)
