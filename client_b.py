import socket

HOST = '127.0.0.1'  # Change to server's IP if not local
PORT = 12345

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'B')  # Identify as Client B
        print("Client B ready. Waiting for number...")
        while True:
            # Receive number from server
            data = s.recv(1024)
            if not data:
                break
            number = float(data.decode('utf-8'))
            print(f"Received number: {number}")
            # Compute square
            result = number ** 2
            print(f"Computed result: {result}")
            # Send result to server
            s.sendall(str(result).encode('utf-8'))

if __name__ == "__main__":
    run_client()
