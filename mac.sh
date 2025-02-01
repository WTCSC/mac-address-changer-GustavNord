#!/bin/bash
# Use 'set-e' to ensure the script will stop on an error which would prevent further execution of commands that may lead to weird behavior.
set -e

# Function for how to use the script and examples.
help() {
    echo "How to use this script:"
    echo "$0 <network-interface> <new-mac-address>"
    echo "Example: $0 eth0 00:1A:2B:3C:4D:5E"
    echo "Example for random MAC: $0 eth0 random"
    echo "Example to reset MAC address: $0 eth0 reset"
    exit 1
}

# Function to validate the MAC address format and make sure the provided MAC address matches the 'correct' format.
check_mac() {
    local mac=$1
    if [[ $mac =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]; then
        return 0
    else
        echo "Error: The MAC Address isn't in the correct format."
        echo "Format should be: 00:1A:2B:3C:4D:5E"
        exit 1
    fi
}

# If two arguments are not provided, it shows the usage instructions.
if [[ "$#" -ne 2 ]]; then
    echo "Error: Invalid number of arguments."
    help
fi

# Stores the command line arguments into variables for easier refrence.
interface=$1
new_mac=$2

# Make sure the script is run as root or with sudo inorder to modify the network settings.
if [[ $EUID -ne 0 ]]; then
    echo "Error: Script needs to be run with sudo or as root."
    exit 1
fi

# Make sure the interface exists to avoid invalid operations.
if ! ip link show "$interface" &> /dev/null; then
    echo "Error: Network interface '$interface' not found."
    exit 1
fi

# Validate the new MAC address format unless it's under random or reset.
if [[ "$new_mac" != "random" && "$new_mac" != "reset" ]]; then
    check_mac "$new_mac"
fi

# Function to bring down the network interface to avoid causing conflicts or disruptions in network activity. This is required before making any changes to the MAC address.
mac_down () {
    ip link set dev "$1" down
}

# Function to bring up the network interface, enables the interface again after the changes to the MAC address are done. 
mac_up () {
    ip link set dev "$1" up
}

# Function to install macchanger because this script can't work without it.
install_macchanger() {
    echo "Error: Macchanger is not installed. Installing macchanger..."
    # Make sure the system can use 'apt', otherwise user has to install macchanger manually. 
    if ! command -v apt &> /dev/null; then
        echo "Error: This script is for systems that support 'apt'. Install macchanger manually."
        exit 1
    fi
    # Used to update the package list and install macchanger.
    apt update
    apt install -y macchanger
}

# Checks if macchanger is installed, if not, installs it. 
if ! command -v macchanger &> /dev/null; then
    install_macchanger
fi

# Function to give a random MAC address to the specified interface.
random_mac() {
    sudo macchanger -r "$1"
}

# Function to change the MAC address to the user's desired value.
change_mac() {
    sudo macchanger --mac="$2" "$1"
}

# Function to reset to the original MAC address.
original_mac() {
    sudo macchanger -p "$1"
}

# Bring the interface down before making changes to the MAC address.
mac_down "$interface"

# Assign a random MAC address.
if [[ "$new_mac" == "random" ]]; then
    random_mac "$interface"
# Resets back to the origianl MAC address.
elif [[ "$new_mac" == "reset" ]]; then
    original_mac "$interface"
# Changes MAC address to user input.
else
    change_mac "$interface" "$new_mac"
fi

# Brings the network interface back up after the changes are made. 
mac_up "$interface"

# Echos the current MAC address of the specified interface. 
echo "Current MAC address of '$interface': $(ip link show "$interface" | grep ether | awk '{print $2}')"
