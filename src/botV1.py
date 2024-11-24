# Mass upload

# Zip file
import shutil

def zipFolder(file_to_zip, output_zip):
	shutil.make_archive(output_zip, 'zip', file_to_zip)


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

if __name__ == "__main__":
	# Zip folder
	file_to_zip = '/home/dev06/Downloads/wordpress'
	output_zip_file = 'outputV1'
	print(f"Zipping {file_to_zip}")
	zipFolder(file_to_zip, output_zip_file)
	output_zip_file += ".zip"
	print(f"Zip complete: {output_zip_file}...")

	# Upload file
	print(f"Uploading {output_zip_file}...")
	upload_file(output_zip_file)
