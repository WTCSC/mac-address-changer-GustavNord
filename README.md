# MAC Address changer
This script allows users to change the MAC address of a network interface. It can be used to set a custom MAC address, create a random MAC address, or revert back to the original MAC address. This script handles the installation of macchanger if it's not installed already.

---
## Introduction
This script allows users to change the MAC address of a specified network interface on Linux. It has three different modes:
- Set a custom MAC address.
- Set a random MAC address.
- Reset the MAC address to the original MAC address.

This script will disable and enable the network interface to ensure system stability when changing the MAC address. 


## Installation Instructions
1. Clone or download repository.
2. Ensure the script is executable
```bash
chmod +x mac.sh
```
3. Install macchanger (also included in script):
```bash
sudo apt install mcchanger
```

## Usage
Run this script from the command line to change the MAC address of the specified network interface.

Basic command format:
```bash
./mac.sh <network-interface> <new-mac-address>
```

Example:
```bash
./mac.sh eth0 00:1A:2B:3C:4D:5E
```

To reset (revert to original):
```bash
./mac.sh eth0 reset
```

To generate and use a random MAC address:
```bash
./mac.sh eth0 random
```


## Command-Line Arguments



## Error Handling



## Examples



## License



