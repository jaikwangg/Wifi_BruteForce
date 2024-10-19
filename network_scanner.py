# network_scanner.py
from scapy.all import ARP, Ether, srp

def scan_ips(interface='eth0', ips='192.168.1.0/24'):
    """Perform a simple ARP scan with Scapy."""
    try:
        print('[*] Start to scan')
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp = ARP(pdst=ips)
        packet = ether/arp
        print(f"Scanning {ips} on interface {interface}")
        result = srp(packet, timeout=2, iface=interface, verbose=False)[0]

        if not result:
            print("No responses received.")
        else:
            for sent, received in result:
                print(f"IP: {received.psrc}, MAC: {received.hwsrc}")

    except Exception as e:
        print(f"Error: {e}")
