#!/bin/bash

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
