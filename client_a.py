import socket
import time

HOST = '127.0.0.1'  # Server IP
PORT = 12345           # Server Port

def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'A')  # Identify as Client A

        # Get number from user
        number = input("Enter a number: ")
        start_time = time.time()  # Start timing

        # Send number to server
        s.sendall(number.encode('utf-8'))

        # Receive result from server
        result = s.recv(1024).decode('utf-8')
        end_time = time.time()  # End timing

        # Calculate and display delay
        delay = end_time - start_time
        print(f"Result: {result}")
        print(f"Delay: {delay:.4f} seconds")

if __name__ == "__main__":
    run_client()
