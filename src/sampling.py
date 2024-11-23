import argparse
from netaddr import IPNetwork, IPAddress, IPSet
import pyshark
import json

def load_json():
    with open('./google_ips.json', 'r') as file:
        data = json.load(file)['prefixes']
        return [i["ipv4Prefix"] for i in data if "ipv4Prefix" in i]

def pktHandler(timestamp, srcIP, dstIP, lenIP, outfile):
    global ssnets
    global scnets
    global npkts
    global last_ks
    global T0
    global outc
    
    if (IPAddress(srcIP) in scnets and IPAddress(dstIP) in ssnets) or (IPAddress(srcIP) in ssnets and IPAddress(dstIP) in scnets):
        if npkts==0:
            T0=float(timestamp)
            last_ks=0
            
        ks=int(float(timestamp)-T0)

        if ks>last_ks:
            outfile.write('{} {} {} {}\n'.format(*outc))
            # print('{} {} {} {}'.format(*outc))
            outc=[0,0,0,0]  
            
        if ks>last_ks+1:
            for _ in range(last_ks+1,ks):
                outfile.write('{} {} {} {}\n'.format(*outc))
                # print('{} {} {} {}'.format(*outc))
                  
        
        if IPAddress(srcIP) in scnets: #Upload
            outc[0]=outc[0]+1
            outc[1]=outc[1]+int(lenIP)

        if IPAddress(dstIP) in scnets: #Download
            outc[2]=outc[2]+1
            outc[3]=outc[3]+int(lenIP)
        
        last_ks=ks
        npkts=npkts+1

    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True)
    parser.add_argument('-o', '--output', nargs='?', required=True)
    args = parser.parse_args()

    input_file = "./captures/" + args.input
    output_file = "./sampled_data/" + args.output
    
    global scnets
    cnets=['192.168.1.0/24']
    scnets = IPSet(cnets)
    
    global ssnets
    snets = load_json()
    ssnets = IPSet(snets)

    global npkts
    global last_ks
    global T0
    global outc

    npkts = 0
    outc = [0, 0, 0, 0]
    
    out = open(output_file, 'w')
    capture = pyshark.FileCapture(input_file, display_filter='ip')
    for pkt in capture:
        timestamp, srcIP, dstIP, lenIP = pkt.sniff_timestamp, pkt.ip.src, pkt.ip.dst, pkt.ip.len
        pktHandler(timestamp, srcIP, dstIP, lenIP, out)
    out.close()

if __name__ == '__main__':
    main()
