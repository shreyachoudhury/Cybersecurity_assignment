import socket
import threading
import time

HOST = ''  # Listen on all interfaces
PORT = 12345

clients = {'A': None, 'B': None}
start_time = None

def handle_client(conn: socket.socket, addr, identity: str):
    global start_time
    print(f"[{addr}] Connected as Client {identity}")
    clients[identity] = conn

    try:
        while True:
            if identity == 'A':
                # Receive number and timestamp from A
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                # Split into number and timestamp
                parts = data.split()
                if len(parts) >= 2:
                    number = parts[0]
                    start_time = float(parts[1])
                    if clients['B']:
                        clients['B'].sendall(number.encode('utf-8'))
            elif identity == 'B':
                # Receive result from B
                result = conn.recv(1024)
                if not result:
                    break
                if clients['A']:
                    clients['A'].sendall(result)
                    # Server prints result and delay
                    end_time = time.time()
                    delay = end_time - start_time
                    print(f"[Server] Result: {result.decode('utf-8')}")
                    print(f"[Server] Delay (A start to server result): {delay:.4f} seconds")
    except Exception as e:
        print(f"[{addr}] Error: {e}")
    finally:
        if identity in clients and clients[identity] == conn:
            clients[identity] = None
        conn.close()
        print(f"[{addr}] Client {identity} disconnected")

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on port {PORT}")
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
