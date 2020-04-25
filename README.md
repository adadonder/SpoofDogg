# SpoofDogg
SpoofDogg is a tool that initially starts an ARP spoofing attack.
It can also be started to initiate an automatic DNS spoofing attack afterwards as well
````
$ python3 setup.py install
````
or
````
$ pip install .
````

Be sure to run with ``python3``.
```
usage: spoofdogg.py [-h] [-dns] target host

SpoofDogg is a tool that initially starts an ARP spoofing attack. It can also
be started to initiate an automatic DNS spoofing attack afterwards as well

positional arguments:
  target             Victim IP address to poison
  host               The host to intercept packets from. Usually this is the
                     gateway

optional arguments:
  -h, --help         show this help message and exit
  -dns, --dns_spoof  Start DNS spoofing after ARP poisoning. Only works on
                     Linux machines due to iptables usage.

```
<ANY ADDITIONAL INFO>

<NAME> is released under the Apache 2.0 license. See [LICENSE](https://github.com/adadonder/SpoofDogg/blob/master/LICENSE) for details.

Feel free to contact me via e-mail: adadonderr@gmail.com
