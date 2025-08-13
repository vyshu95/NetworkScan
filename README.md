# NetworkScan
Network Chat communication to scan devices, ports and number of devices online
🔍 How It Works
You run server.py on one machine.

You run client.py on any machine that can connect to it (e.g., same network).

Clients can chat or send special /commands.

Commands:
/devices — Counts active IPs on 192.168.1.0/24.

/ports <ip> — Shows open ports on that IP.

/scan — Lists IPs that responded to ping.

You can update the subnet (192.168.1.0/24) to match your network.

To Test:
Run server.py.

Run multiple instances of client.py on other terminals (or systems).

Type normal messages or use commands like:

/devices

/ports 192.168.1.10

/scan
