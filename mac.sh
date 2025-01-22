#!/bin/bash

help() {
    echo "How to use this script:"
    echo "$0 ,network-interface> <new-mac-address>"
    echo "Example: $0 eth0 00:1A:2B:3C:4D:5E"
    echo "Example for random MAC: $0 eth0 random"
    echo "Example to reset MAC address: $0 eth0 reset"
    exit 1
}

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

if [[ "$#" -ne 2 ]]; then
    help
fi

interface=$1
new_mac=$2

if [[ $EUID -ne 0 ]]; then
    echo "Error: Script needs to be run with sudo or as root."
    exit 1
fi

if ! ip link show "$interface" &> /dev/null; then
    echo "Error: Network interface '$interface' not found."
    exit 1
fi

if [[ "$new_mac" != "random" && "$new_mac" != "reset" ]]; then
    check_mac "$new_mac"
fi

mac_down () {
    sudo ip link set dev "$1" down || {echo "Error: Failed to bring the interface down."; exit 1; }
}

mac_up () {
    sudo ip link set dev "$1" up || {echo "Error: Failed to bring the interface up."; exit 1; }
}

install_macchanger() {
    echo "Macchanger is not installed. Installing mcchanger..."
    sudo apt update
    sudo apt install -y macchanger || {echo "Error: failed to install mcchanger."; exit 1; }
}

if ! command -v macchanger &> /dev/null; then
    install_macchanger
fi

random_mac() {
    sudo macchanger -r "$1" || {echo "Error}
}

change_mac() {
    sudo macchanger --mac="$2" "$1"
}

original_mac() {
    sudo macchanger -p "$1"
}

mac_down "$interface"

if [[ "$new_mac" == "random" ]]; then
    random_mac "$interface"
elif [[ "$new_mac" == "reset" ]]; then
    original_mac "$interface"
else
    change_mac "$interface" "$new_mac"
fi

mac_up "$interface"
echo "Current MAC address of '$interface':" ip link show "$interface" | grep ether | awk '{print $2}'