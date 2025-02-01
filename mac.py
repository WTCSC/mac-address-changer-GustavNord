import subprocess
import sys
import re
import os

# Function to display help message and exit the script
def help():
    print("How to use this script:")
    print(f"{sys.argv[0]} <network_interface> <new_mac_address>")
    print("Example: {} eth0 00:1A:2B:3C:4D:5E".format(sys.argv[0]))
    print("Example for random MAC: {} eth0 random".format(sys.argv[0]))
    print("Example to reset MAC address: {} eth0 reset".format(sys.argv[0]))
    sys.exit(1)

# Function to validate the format of the MAC address received
def check_mac(mac):
    # Check if the MAC address is in the correct format
    if re.match(r'^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$', mac):
        return True
    else:
        # Print error if MAC address format is not in the correct format
        print("Error: The MAC Address isn't in the correct format.")
        print("Format should be: 00:1A:2B:3C:4D:5E")
        sys.exit(1)

# Makes sure that only two arguments are passed
if len(sys.argv) != 3:
    print("Error: Invalid number of arguments.")
    help()

# Assign arguments to variables
interface = sys.argv[1]
new_mac = sys.argv[2]

# Check if the script is run with sudo or as root
if os.geteuid() != 0:
    print("Error: Script needs to be run with sudo or as root.")
    sys.exit(1)

# Function to check if a network interface exists
def interface_exists(interface, timeout=5):
    try:
        # Checks the interface using 'ip link show' command
        subprocess.run(['ip', 'link', 'show', interface], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        return True
    except subprocess.CalledProcessError:
        # If interface isn't found, return False
        return False
    except subprocess.TimeoutExpired:
        # Handles weather or not command takes too long
        print(F"Error: Checking interface '{interface}' timed out.")
        return False
    except Exception as e:
        # Catch any other errors that may happen
        print(f"An unexpected error occurred: {e}")
        return False

# Checks if the network interface exists
if not interface_exists(interface):
    print(f"Error: Network interface '{interface}' not found.")
    sys.exit(1)

# Function to bring the interface up
def mac_up(interface):
    subprocess.run(['ip', 'link', 'set', 'dev', interface, 'up'], check=True)

# Function to bring the interface down
def mac_down(interface): 
    subprocess.run(['ip', 'link', 'set', 'dev', interface, 'down'], check=True)

# Function to install macchanger if not already installed
def install_macchanger():
    print("Error: Macchanger is not installed. Installing macchanger...")
    # Check if system supports 'apt'
    if subprocess.run(['command', '-v', 'apt'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
        print("Error: This script is for systems that support 'apt'. Install macchanger manually.")
        sys.exit(1)
    subprocess.run(['apt', 'update'], check=True)
    subprocess.run(['apt', 'install', '-y', 'macchanger'], check=True)

# Function to set a random MAC address
def random_mac(interface):
    subprocess.run(['macchanger', '-r', interface], check=True)

# Function to change the MAC address to a specific one
def change_mac(interface, new_mac):
    subprocess.run(['macchanger', '--mac', new_mac, interface], check=True)

# Function to change the MAC address back to the original one
def original_mac(interface):
    subprocess.run(['macchanger', '-p', interface], check=True)

# Check if user has requested a random MAC address or reset the MAC address instead of a custom valued one
if new_mac != "random" and new_mac != "reset":
    # Checks custom MAC address
    check_mac(new_mac)

# Install macchanger if it is not already installed
if subprocess.run(['command', '-v', 'macchanger'], stdout=subprocess.PIPE, text=True).returncode != 0:
    install_macchanger()

# Bring network interface down before changing MAC address
mac_down(interface)

# Change MAC address based on the user's input
if new_mac == "random":
    random_mac(interface)
elif new_mac == "reset":
    original_mac(interface)
else:
    change_mac(interface, new_mac)

# Bring network interface back up
mac_up(interface)

# Get and then display the current MAC address of the interface
result = subprocess.run(['ip', 'link', 'show', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = result.stdout
# Regular expression to extract MAC address from the output
match = re.search(r'ether (\S+)', output)
if match:
    # Extracted MAC address
    mac_address = match.group(1)
    print(f"Current MAC address of '{interface}': {mac_address}")
else:
    print("Error: Failed to retrieve the current MAC address.")