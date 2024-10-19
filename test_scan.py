# Open Your Text Editor of Choice and Let's Get Started!
# First, we'll import some needed modules

import sys
from datetime import datetime
from scapy.all import srp, Ether, ARP, conf

# These aren't all the modules we need, but we'll import the rest later on.

def simple_scan():
    
    interface = 'eth0'
    ip_range = '192.168.1.0/24'
    """
    Scan IPs in the given range using the specified network interface.
    """
    try:
        # Inform the user that the scan has started
        print("Starting the scan...")

        # Record the start time
        start_time = datetime.now()

        # Set Scapy verbosity to 0 (silent mode)
        conf.verb = 0

        # Define ARP request and Ethernet frame
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        # Perform the scan
        ans, unans = srp(packet, timeout=2, iface=interface, inter=0.1)

        # Print the results
        print("MAC - IP")
        for sent, received in ans:
            print(f"{received.hwsrc} - {received.psrc}")

        # Record the end time and calculate duration
        end_time = datetime.now()
        duration = end_time - start_time

        # Print the total time taken
        print(f"Scan completed in {duration}")

    except KeyboardInterrupt:
        # Handle user interruption
        print("\nScan interrupted by user.")
        sys.exit(1)

