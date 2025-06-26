import socket
import threading

HOST = ''  # Listen on all interfaces
PORT = 12345

clients = {'A': None, 'B': None}

def handle_client(conn: socket.socket, addr, identity: str):
    clients[identity] = conn
    try:
        while True:
            if identity == 'A':
                data = conn.recv(1024)
                if not data:
                    break
                # Forward number to B
                if clients['B']:
                    clients['B'].sendall(data)
            elif identity == 'B':
                result = conn.recv(1024)
                if not result:
                    break
                # Forward result to A
                if clients['A']:
                    clients['A'].sendall(result)
    except Exception as e:
        pass
    finally:
        if identity in clients and clients[identity] == conn:
            clients[identity] = None
        conn.close()

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
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
