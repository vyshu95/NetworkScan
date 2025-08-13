import socket
import threading
import ipaddress
import subprocess

clients = []

# Broadcast messages to all clients
def broadcast(msg, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(msg.encode())
            except:
                clients.remove(client)

# Handle commands and chat
def handle_client(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(f"[CLIENT] {msg}")
            if msg.startswith('/'):
                response = handle_command(msg)
                client_socket.send(response.encode())
            else:
                broadcast(msg, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

# Handle commands
def handle_command(command):
    if command == "/devices":
        return str(count_devices())
    elif command.startswith("/ports"):
        parts = command.split()
        if len(parts) != 2:
            return "Usage: /ports <ip>"
        return scan_ports(parts[1])
    elif command == "/scan":
        return scan_network()
    else:
        return "Unknown command."

# Count online devices in local subnet
def count_devices():
    subnet = ipaddress.IPv4Network('192.168.1.0/24', strict=False)
    online = 0
    for ip in subnet.hosts():
        if ping(str(ip)):
            online += 1
    return f"Devices online: {online}"

# Ping an IP
def ping(ip):
    try:
        output = subprocess.check_output(['ping', '-n', '1', '-w', '500', ip], stderr=subprocess.DEVNULL)
        return "TTL=" in output.decode()
    except:
        return False

# Scan ports of a given IP
def scan_ports(ip):
    open_ports = []
    for port in range(20, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return f"Open ports on {ip}: {open_ports}"

# Scan and list devices online
def scan_network():
    subnet = ipaddress.IPv4Network('192.168.1.0/24', strict=False)
    online_ips = []
    for ip in subnet.hosts():
        if ping(str(ip)):
            online_ips.append(str(ip))
    return f"Online devices: {online_ips}"

# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("[SERVER] Listening on port 5555...")
    
    while True:
        client_socket, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
