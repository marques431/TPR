# Upload equaly sized parts in a constant interval

# Zip file
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


# Google Upload
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1v1Pse9xihZVzLclq0EYIj5K8csW0jJrB"

from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2 import service_account
import httplib2

def authenticate():
	creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
	
	# If the credentials are expired or near expiry, refresh them
	if creds and creds.expired and creds.refresh_token:
		creds.refresh(Request())
	
	return creds

def upload_file(file_path):
	creds = authenticate()

	# Directly use the credentials in the build() function, no need for manual authorization
	service = build('drive', 'v3', credentials=creds)

	file_metadata = {
		'name': file_path,
		'parents': [PARENT_FOLDER_ID]
	}

	# MediaFileUpload with chunking for large files
	media = MediaFileUpload(file_path, mimetype='application/zip', resumable=True)

	request = service.files().create(
		body=file_metadata,
		media_body=media
	)

	response = None
	while response is None:
		status, response = request.next_chunk()
		if status:
			print(f"Upload {int(status.progress() * 100)}%.")

	print("Upload complete")



def find_output_zip_files(folder_path):
	matching_files = []
	for filename in os.listdir(folder_path):
		if filename.startswith("output") and filename.endswith(".zip"):
			matching_files.append(os.path.join(folder_path, filename))
	return matching_files


import time

if __name__ == "__main__":
	# Zip folder
	file_to_zip = '/home/dev06/Downloads/wordpress'
	output_zip_file = 'outputV3'
	max_part_size = 10 * 1024 * 1024
	print(f"Zipping {file_to_zip}")
	zip_folder_in_parts(file_to_zip, output_zip_file, max_part_size)
	output_zip_file += ".zip"
	print(f"Zip complete: {output_zip_file}...")

	# Upload file
	folder_path = './'
	files = find_output_zip_files(folder_path)
	for file in files:
		file = file.lstrip("./")
		print(f"Processing file: {file}")
		print(f"Uploading {file}...")
		upload_file(file)

		# Delete file
		try:
			os.remove(file)
			print(f"File {file} deleted successfully.")
		except Exception as e:
			print(f"Error deleting file {file}: {e}")
		time.sleep(5)
