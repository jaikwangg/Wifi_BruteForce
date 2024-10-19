# __main__.py
import argparse
import test_scan
import wifi_bruteforce
import network_scanner

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wifi_brute_force", action="store_true", help="Try to brute force all wifi detected by this device")
    parser.add_argument("-s", "--scan_ips", action="store_true", help="Scan all IPs on this network")
    parser.add_argument("-i", "--simple_scan", action="store_true", help="Perform a simple IP scan")
    args = parser.parse_args()

    if args.wifi_brute_force:
        wifi_bruteforce.start()

    if args.scan_ips:
        network_scanner.scan_ips()

    if args.simple_scan:
        test_scan.simple_scan()

if __name__ == '__main__':
    main()
