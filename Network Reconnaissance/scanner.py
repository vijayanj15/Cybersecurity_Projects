# scanner.py

import socket
import threading
from queue import Queue
import argparse
import ipaddress
import re
import time
import nvdlib  # New import for CVE lookup
from scapy.all import ARP, Ether, srp

# --- PHASE 1: HOST DISCOVERY AND PORT SCANNING (Your existing code) ---

# A list to store the open ports we find for a single host
open_ports_list = []
# A lock to prevent race conditions when multiple threads write to the list
print_lock = threading.Lock()

def discover_hosts(ip_range):
    print(f"[*] Discovering hosts in {ip_range}...")
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
    except ValueError:
        print("[!] Invalid IP range format. Use CIDR notation (e.g., 192.168.1.1/24).")
        return []

    arp_request = ARP(pdst=str(network))
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether_frame / arp_request
    result, _ = srp(packet, timeout=2, verbose=False)

    active_hosts = []
    for sent, received in result:
        active_hosts.append(received.psrc)
    
    if active_hosts:
        print(f"[*] Found {len(active_hosts)} live hosts.")
    else:
        print("[*] No hosts found.")
        
    return active_hosts

def scan_port(target_ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            with print_lock:
                open_ports_list.append(port)
        s.close()
    except socket.error:
        pass

def threader(target_ip, q):
    while not q.empty():
        port = q.get()
        scan_port(target_ip, port)
        q.task_done()

def port_scanner(target_ip, ports_to_scan, num_threads=100):
    global open_ports_list
    open_ports_list = []
    
    q = Queue()
    for port in range(1, ports_to_scan + 1):
        q.put(port)

    for _ in range(num_threads):
        t = threading.Thread(target=threader, args=(target_ip, q))
        t.daemon = True
        t.start()
    
    q.join()
    return sorted(open_ports_list)

# --- PHASE 2: SERVICE & VERSION DETECTION (NEW CODE) ---

def get_banner(target_ip, port):
    """
    Connects to an open port and grabs the service banner.
    """
    try:
        s = socket.socket()
        s.settimeout(2) # Set a timeout for the connection
        s.connect((target_ip, port))
        banner = s.recv(1024).decode('utf-8', errors='ignore').strip()
        s.close()
        return banner
    except Exception as e:
        return None # Return None if banner can't be grabbed

# --- PHASE 3: VULNERABILITY ANALYSIS (NEW CODE) ---

def parse_banner(banner):
    """
    Parses common banner formats to extract product and version.
    This is a simple parser and can be expanded.
    """
    if not banner:
        return None, None
    
    # Common patterns: Product/Version, Product Version, etc.
    # Example: "vsFTPd 2.3.4", "Apache/2.2.8", "OpenSSH_4.7p1"
    match = re.search(r'([a-zA-Z0-9\._-]+)[ /_]([0-9]+\.[0-9]+(?:\.[0-9]+)?)', banner)
    if match:
        product = match.group(1).lower().replace('-', '') # Normalize product name
        version = match.group(2)
        # Handle cases like 'openssh'
        if 'ssh' in product:
            product = 'openssh'
        return product, version

    return None, None

# The new, corrected find_cves function

# The final, most reliable version of find_cves in scanner.py

def find_cves(product, version):
    """
    Searches the NVD for CVEs related to a specific product and version.
    """
    if not product or not version:
        return []
    
    # --- PASTE YOUR NVD API KEY HERE ---
    NVD_API_KEY = "PASTE_YOUR_NVD_API_KEY_HERE"  # <-- PASTE YOUR KEY INSIDE THE QUOTES
    
    try:
        # We don't need time.sleep() when using an API key because our limit is much higher
        results = nvdlib.searchCVE(keywordSearch=f"{product} {version}", limit=5, key=NVD_API_KEY)
        
        cve_list = []
        if not results:
            return [] # No CVEs found for this keyword

        for cve in results:
            description = cve.descriptions[0].value.splitlines()[0]
            cve_list.append(f"  - {cve.id}: {description[:100]}...")
            
        return cve_list
    
    except Exception as e:
        # This will now print any error message we get from the API
        print(f"        [!] Error during CVE lookup: {e}")
        return []


# --- MAIN LOGIC (UPDATED) ---

def main():
    parser = argparse.ArgumentParser(description="Python Network Vulnerability Scanner")
    parser.add_argument("target", help="Target IP address or CIDR range (e.g., 192.168.1.1/24)")
    parser.add_argument("-p", "--ports", type=int, default=1024, help="Number of ports to scan (default: 1024)")
    args = parser.parse_args()

    hosts_to_scan = discover_hosts(args.target)
    if not hosts_to_scan:
        return
    
    print("-" * 50)

    for host in hosts_to_scan:
        print(f"[*] Scanning host: {host}")
        open_ports = port_scanner(host, args.ports)
        
        if not open_ports:
            print("    [-] No open ports found.")
        else:
            for port in open_ports:
                banner = get_banner(host, port)
                if banner:
                    print(f"    [+] Port {port}: {banner}")
                    
                    # --- CVE Lookup Integration ---
                    product, version = parse_banner(banner)
                    if product:
                        print(f"        -> Parsed as Product: {product}, Version: {version}")
                        cves = find_cves(product, version)
                        if cves:
                            print("        [!] VULNERABLE: Found potential CVEs:")
                            for cve in cves:
                                print(f"          {cve}")
                else:
                    print(f"    [+] Port {port}: Open (No banner received)")

        print("-" * 50)

if __name__ == "__main__":
    main()



