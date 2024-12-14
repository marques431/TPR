import argparse
from netaddr import IPNetwork, IPAddress, IPSet
import pyshark
import json
import time

def load_json():
    """Carrega os prefixos IP de um arquivo JSON."""
    with open('./google_ips.json', 'r') as file:
        data = json.load(file)['prefixes']
        # Carrega prefixos IPv4 e IPv6
        return [i["ipv4Prefix"] for i in data if "ipv4Prefix" in i] + \
               [i["ipv6Prefix"] for i in data if "ipv6Prefix" in i]

def pktHandler(timestamp, srcIP, dstIP, lenIP, outfile):
    """Manipula pacotes, conta uploads e downloads."""
    global ssnets
    global scnets
    global npkts
    global last_ks
    global T0
    global outc

    if (IPAddress(srcIP) in scnets and IPAddress(dstIP) in ssnets) or (IPAddress(srcIP) in ssnets and IPAddress(dstIP) in scnets):
        if npkts == 0:
            T0 = float(timestamp)
            last_ks = 0
            
        ks = int(float(timestamp) - T0)

        # Escreve a saída a cada segundo
        if ks > last_ks:
            outfile.write('{} {} {} {}\n'.format(*outc))
            outc = [0, 0, 0, 0]  
            
        # Preenche segundos sem pacotes
        if ks > last_ks + 1:
            for _ in range(last_ks + 1, ks):
                outfile.write('{} {} {} {}\n'.format(*outc))
        
        # Contagem de upload e download
        if IPAddress(srcIP) in scnets:  # Upload
            outc[0] += 1
            outc[1] += int(lenIP)

        if IPAddress(dstIP) in scnets:  # Download
            outc[2] += 1
            outc[3] += int(lenIP)
        
        last_ks = ks
        npkts += 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='?', required=True, help="Arquivo de entrada PCAP")
    parser.add_argument('-o', '--output', nargs='?', required=True, help="Arquivo de saída")
    args = parser.parse_args()

    input_file = "./captures/" + args.input
    output_file = "./sampled_data/" + args.output
    
    global scnets
    cnets = ['172.16.0.0/12', '192.168.0.0/12', '10.0.0.0/8', 'fc00::/7', 'fe80::/10']
    client_ipv6s = [
        "2001:8a0:ed24:2c00::/64",
        "fe80::aa5e:45ff:febe:aef6",
        "fe80::bb26:b37a:ce89:2fcf"
    ]
    cnets.extend(client_ipv6s)
    scnets = IPSet(cnets)
    
    global ssnets
    snets = load_json()
    service_ipv6s = [
        "2a00:1450:4003:811::200e",
        "2a00:1450:4003:803::200a",
        "2a00:1450:4003:80c::200a"
    ]
    snets.extend(service_ipv6s)
    ssnets = IPSet(snets)

    global npkts
    global last_ks
    global T0
    global outc

    npkts = 0
    outc = [0, 0, 0, 0]
    
    out = open(output_file, 'w')
    capture = pyshark.FileCapture(input_file, display_filter='ip || ipv6')
    print("Sampling...") 
    start_time = time.time()
    
    for pkt in capture:
        try:
            if hasattr(pkt, 'ip'): 
                timestamp, srcIP, dstIP, lenIP = pkt.sniff_timestamp, pkt.ip.src, pkt.ip.dst, pkt.ip.len
            elif hasattr(pkt, 'ipv6'):  
                timestamp, srcIP, dstIP = pkt.sniff_timestamp, pkt.ipv6.src, pkt.ipv6.dst
                lenIP = int(pkt.ipv6.plen) + 40
            else:
                continue  # Ignora pacotes que não são IP
            
            pktHandler(timestamp, srcIP, dstIP, lenIP, out)
        
        except AttributeError:
            continue

    out.close()
    end_time = time.time()
    print(f"Sampling done. Time taken: {(end_time - start_time):.2f} seconds")

if __name__ == '__main__':
    main()

