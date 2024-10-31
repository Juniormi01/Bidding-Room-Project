import socket
import threading
import random
import time

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Server: {message}")
        except:
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))  # Replace 'server_ip_address' with the server's IP
    print("Connected to the server.")
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()
    while True:
        # Simulate bidding with a 70% chance
        if random.random() < 0.7:
            item_name = random.choice(["Laptop", "Smartphone", "Headphones"])
            bid_amount = random.uniform(1, 1000)  # Replace with your bidding logic
            bid_message = f"{item_name},{bid_amount}"
            client_socket.send(bid_message.encode())
        time.sleep(random.uniform(1, 5))  # Wait before next bid attempt

if __name__ == "__main__":
    start_client()
