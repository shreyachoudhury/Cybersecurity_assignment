import socket

HOST = '127.0.0.1'  # Change to server's IP if not local
PORT = 12345

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'B')  # Identify as Client B
        while True:
            data = s.recv(1024)
            if not data:
                break
            number = float(data.decode('utf-8'))
            result = number ** 2  # Or any operation
            s.sendall(str(result).encode('utf-8'))

if __name__ == "__main__":
    run_client()
