# WireGuard
WireGuard runs on the raspi, and is set to auto start on boot. 
It allows for a tunnel from any device that can pass the key-handshake - in this case, my own devices. This tunnel functions roughly as a VPN would, but instead of being able to access my entire local network, I only gain access to a subnet creates from the raspi (192.168.2.0/24).

Connection from the Clients runs from the corresponding .conf file. The keys have been exchanged for this to work.
