import socket
import threading

HOST = ''  # Listen on all interfaces
PORT = 12345

clients = {'A': None, 'B': None}

def handle_client(conn: socket.socket, addr, identity: str):
    print(f"[{addr}] Connected as Client {identity}")
    clients[identity] = conn

    try:
        if identity == 'A':
            # Receive number from A and forward to B
            number = conn.recv(1024)
            if clients['B']:
                clients['B'].sendall(number)
        elif identity == 'B':
            # Receive result from B and forward to A
            result = conn.recv(1024)
            if clients['A']:
                clients['A'].sendall(result)
    except Exception as e:
        print(f"[{addr}] Error: {e}")
    finally:
        if identity in clients and clients[identity] == conn:
            clients[identity] = None
        conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on port {PORT}")
        while True:
            conn, addr = s.accept()
            # Wait for client to identify themselves
            identity = conn.recv(1024).decode('utf-8').strip()
            if identity in ('A', 'B'):
                threading.Thread(
                    target=handle_client,
                    args=(conn, addr, identity),
                    daemon=True
                ).start()
            else:
                conn.close()

if __name__ == "__main__":
    run_server()
