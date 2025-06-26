import socket
import math

HOST = '127.0.0.1'  # Server IP
PORT = 12345           # Server Port

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'B')  # Identify as Client B

        # Receive number from server
        number = float(s.recv(1024).decode('utf-8'))

        # Compute square (numerical operation)
        result = number ** 2

        # Send result back to server
        s.sendall(str(result).encode('utf-8'))

if __name__ == "__main__":
    run_client()
