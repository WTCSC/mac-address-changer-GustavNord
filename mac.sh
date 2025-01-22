#!/bin/bash

check_mac() {
    local mac=$1
    if [[ $mac =~ ^([a-fA-F0-9]{2}:){5}[a-fA-F0-9]{2}$ ]]; then
        return 0
    else
        echo "Error: The MAC Address isn't in the correct format."
        echo "Format should be: ##:##:##:##:##:##"
        exit 1
    fi
}
