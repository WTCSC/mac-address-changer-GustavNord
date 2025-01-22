#!/bin/bash

help() {
    echo "How to use this script:"

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

interface=$2
new_mac=$3

if [[ $EUID -ne 0 ]]; then
    echo "Error: Script needs to be run with sudo or as root."
    exit 1
fi

if [[ "$#" -ne 0 ]]; then
    echo "Usage: $0 <network-interface> <new-mac-address>"
    exit 1
fi

if ! ip link show "$INTERFACE" &> /dev/null; then
    echo "Error: Network interface '$INTERFACE' not found."
    exit 1
fi

install_macchanger() {
    echo "Macchanger is not installed. Installing mcchanger..."
    sudo apt update
    sudo apt install -y macchanger
}

random_mac() {
    sudo macchanger -r $2
}

change_mac() {
    sudo macchanger --mac= $3 interface
}

original_mac() {
    sudo macchanger -p interface
}
