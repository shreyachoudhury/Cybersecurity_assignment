import socket
import threading

HOST = ''  # Server IP
PORT = 12345           # Server Port

# Shared storage for client connections
clients = {'A': None, 'B': None}

def handle_client(conn: socket.socket, addr):
    """Handle client connections and route messages"""
    with conn:
        # Receive client identity (A or B)
        identity = conn.recv(1024).decode('utf-8').strip()
        print(f"[{addr}] Connected as Client {identity}")

        # Store connection
        clients[identity] = conn

        if identity == 'A':
            # Forward number from A to B
            number = conn.recv(1024)
            if clients['B']:
                clients['B'].sendall(number)
        elif identity == 'B':
            # Forward result from B to A
            result = conn.recv(1024)
            if clients['A']:
                clients['A'].sendall(result)

def run_server():
    """Main server function"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    run_server()
