import subprocess
import sys
import re
import os

def help():
    print("How to use this script:")
    print(f"{sys.argv[0]} <network_interface> <new_mac_address>")
    print("Example: {} eth0 00:1A:2B:3C:4D:5E".format(sys.argv[0]))
    print("Example for random MAC: {} eth0 random">format(sys.argv[0]))
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
user_input0 = sys.argv[3]


if os.geteuid() != 0:
    print("Error: Script needs to be run with sudo or as root.")
    sys.exit(1)
