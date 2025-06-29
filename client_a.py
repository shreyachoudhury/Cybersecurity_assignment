import socket
import time

HOST = '127.0.0.1'  # Change to server's IP if not local
PORT = 12345

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'A')  # Identify as Client A

        # Get number from user
        number = input("Enter a number: ")
        start_time = time.time()
        # Send number and timestamp
        s.sendall(f"{number} {start_time}".encode('utf-8'))

        # Receive result from server
        result = s.recv(1024).decode('utf-8')
        end_time = time.time()
        delay = end_time - start_time

        print(f"Result: {result}")
        print(f"Delay (Client A): {delay:.4f} seconds")

if __name__ == "__main__":
    run_client()
