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
                print("upload detected")
                # You could further analyze packet size, duration, or patterns here

# Function to start sniffing network traffic
def start_sniffing():
    print("Starting network traffic capture for Google Drive uploads...")
    #sniff(prn=packet_callback, store=0)
    sniff(iface="eno2", prn=packet_callback, store=0)  # Replace "wlan0" with your network interface


if __name__ == "__main__":
    # Get Google's IP ranges
    google_ips = get_google_ip_ranges()

    if google_ips:
        start_sniffing()
    else:
        print("Google IP ranges could not be fetched. Exiting.")
