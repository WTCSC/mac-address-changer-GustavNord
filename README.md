# MAC Address changer
This script allows users to change the MAC address of a network interface. It can be used to set a custom MAC address, create a random MAC address, or revert back to the original MAC address. This script handles the installation of macchanger if it's not installed already.

---
## Introduction
This script allows users to change the MAC address of a specified network interface on Linux. It has three different modes:
- Set a custom MAC address.
- Set a random MAC address.
- Reset the MAC address to the original MAC address.

This script will disable and enable the network interface to ensure system stability when changing the MAC address. 

This script assumes that the system used uses `apt`. If your system does not use `apt`, you have to manually install `macchanger`.

The MAC address format for this script is `00:1A:2B:3C:4D:5E` or `XX:XX:XX:XX:XX:XX` where `X` is a hexadecimal number (0-9, a-f).

This script only works if `macchanger` is installed. The script will automatically attempt to install it if it's missing. 

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
This script accepts two command line arguments

- **Network Interface:**
   The name of the network interface (eth0, wlan0 for example).

- **New MAC Address:**
   The new MAC address to set to. Using "random" will create a random MAC address and using "reset" will revert the MAC address to the original one. 


## Error Handling
This script includes error handling for some situations.
- **Running as root:** The script must be run with `sudo` or as root to be able to modify the network settings.
   * Error: `"Error: Script needs to be run with sudo or as root."`

- **Invalid arguments:** The script will show an error if the wrong number of arguments are given.
   * Error: `"Error: Invalid number of arguments."`

- **Network interface not found:** Will return an error if the specified network interface does not exist.
   * Error: `"Error: Network interface '<interface>' not found."`

- **Invalid MAC address format:** If the MAC address provided is not in the correct format.
   * Error: `"Error: The MAC address isn't in the correct format."`

## Troubleshooting


## Examples



## License



