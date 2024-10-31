import socket
import threading
import time
import random

# Define the Item class
class Item:
    def __init__(self, name, initial_price, units):
        self.name = name
        self.current_price = initial_price
        self.units = units

# Initialize items
items = [
    Item("Laptop", 500, 2),
    Item("Smartphone", 300, 3),
    Item("Headphones", 50, 5)
]

# List to keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive bid from client
            bid_data = client_socket.recv(1024).decode()
            if not bid_data:
                break
            item_name, bid_amount = bid_data.split(',')
            bid_amount = float(bid_amount)
            # Process the bid
            for item in items:
                if item.name == item_name and item.units > 0:
                    if bid_amount > item.current_price:
                        item.current_price = bid_amount
                        # Notify all clients about the new highest bid
                        broadcast(f"New highest bid for {item_name}: ${bid_amount}", client_socket)
                    break
        except:
            break
    client_socket.close()

def broadcast(message, exclude_socket=None):
    for client in clients:
        if client != exclude_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started and listening for connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Client {client_address} connected.")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
