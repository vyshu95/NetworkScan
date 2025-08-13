import socket
import threading

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode()
            print(msg)
        except:
            print("[ERROR] Lost connection to server.")
            sock.close()
            break

def send_messages(sock):
    while True:
        msg = input()
        sock.send(msg.encode())

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

if __name__ == "__main__":
    main()
