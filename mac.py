import subprocess
import sys
import re
import os

def help():
    print("How to use this script:")
    print(f"{sys.argv[0]} <network_interface> <new_mac_address>")
    print("Example: {} eth0 00:1A:2B:3C:4D:5E".format(sys.argv[0]))
    print("Example for random MAC: {} eth0 random".format(sys.argv[0]))
    print("Example to reset MAC address: {} eth0 reset".format(sys.argv[0]))
    sys.exit(1)

def check_mac(mac):
    if re.match(r'^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$', mac):
        return True
    else:
        print("Error: The MAC Address isn't in the correct format.")
        print("Format should be: 00:1A:2B:3C:4D:5E")
        sys.exit(1)

if len(sys.argv) != 3:
    print("Error: Invalid number of arguments.")
    help()

interface = sys.argv[1]
new_mac = sys.argv[2]

if os.geteuid() != 0:
    print("Error: Script needs to be run with sudo or as root.")
    sys.exit(1)

def interface_exists(interface, timeout=5):
    try:
        subprocess.run(['ip', 'link', 'show', interface], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        print(F"Error: Checking interface '{interface}' timed out.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

if not interface_exists(interface):
    print(f"Error: Network interface '{interface}' not found.")
    sys.exit(1)

def mac_up(interface):
    subprocess.run(['ip', 'link', 'set', 'dev', interface, 'up'], check=True)

def mac_down(interface): 
    subprocess.run(['ip', 'link', 'set', 'dev', interface, 'down'], check=True)

def install_macchanger():
    print("Error: Macchanger is not installed. Installing macchanger...")
    if subprocess.run(['command', '-v', 'apt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("Error: This script is for systems that support 'apt'. Install macchanger manually.")
        sys.exit(1)
    subprocess.run(['apt', 'update'], check=True)
    subprocess.run(['apt', 'install', '-y', 'macchanger'], check=True)

def random_mac(interface):
    subprocess.run(['macchanger', '-r', interface], check=True)

def change_mac(interface, new_mac):
    subprocess.run(['macchanger', '--mac', new_mac, interface], check=True)

def original_mac(interface):
    subprocess.run(['macchanger', '-p', interface], check=True)

if new_mac != "random" and new_mac != "reset":
    check_mac(new_mac)

if subprocess.run(['command', '-v', 'macchanger'], stdout=subprocess.PIPE, text=True).returncode != 0:
    install_macchanger()

mac_down(interface)

if new_mac == "random":
    random_mac(interface)
elif new_mac == "reset":
    original_mac(interface)
else:
    change_mac(interface, new_mac)

mac_up(interface)

result = subprocess.run(['ip', 'link', 'show', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = result.stdout
match = re.search(r'ether (\S+)', output)
if match:
    mac_address = match.group(1)
    print(f"Current MAC address of '{interface}': {mac_address}")
else:
    print("Error: Failed to retrieve the current MAC address.")