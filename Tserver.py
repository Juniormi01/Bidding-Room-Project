import socket
import threading
import time
from datetime import datetime, timedelta

# Define the Item class
class Item:
    def __init__(self, name, initial_price, units):
        self.name = name
        self.current_price = initial_price
        self.units = units
        self.highest_bidder = None
        self.bidding_deadline = None

# Initialize items
items = [
    Item("Laptop", 500, 2),
    Item("Smartphone", 300, 3),
    Item("Headphones", 50, 5)
]

clients = []  # List to keep track of connected clients
clients_lock = threading.Lock()  # Lock for thread-safe access to the clients list
items_lock = threading.Lock()  # Lock for thread-safe access to the items list

def handle_client(client_socket, client_address):
    with clients_lock:
        clients.append(client_socket)
    print(f"Client {client_address} connected.")
    
    while True:
        try:
            bid_data = client_socket.recv(1024).decode()
            if not bid_data:
                break
            item_name, bid_amount = bid_data.split(',')
            bid_amount = float(bid_amount)

            with items_lock:
                for item in items:
                    if item.name == item_name and item.units > 0:
                        if bid_amount > item.current_price and item.highest_bidder != client_socket:
                            item.current_price = bid_amount
                            item.highest_bidder = client_socket
                            item.bidding_deadline = datetime.now() + timedelta(seconds=30)
                            broadcast(f"New highest bid for {item_name}: ${bid_amount}", client_socket)
                            client_socket.send(f"Your bid for {item_name} is now the highest at ${bid_amount}".encode())
                        else:
                            client_socket.send(f"Bid rejected. Either the bid is too low or you already have the highest bid.".encode())
                        break
                else:
                    client_socket.send(f"Item {item_name} not found or sold out.".encode())
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
            break
    
    with clients_lock:
        if client_socket in clients:
            clients.remove(client_socket)
    client_socket.close()
    print(f"Client {client_address} disconnected.")

def broadcast(message, exclude_socket=None):
    with clients_lock:
        for client in clients:
            if client != exclude_socket:
                try:
                    client.send(message.encode())
                except:
                    clients.remove(client)

def manage_bidding():
    while True:
        with items_lock:
            for item in items:
                if item.units > 0 and item.bidding_deadline and datetime.now() > item.bidding_deadline:
                    if item.highest_bidder:
                        item.units -= 1
                        winner_index = clients.index(item.highest_bidder) + 1
                        broadcast(f"Item {item.name} sold to Client {winner_index} for ${item.current_price}")
                        item.highest_bidder.send(f"Congratulations! You won {item.name} for ${item.current_price}".encode())
                    item.highest_bidder = None
                    item.bidding_deadline = None
        time.sleep(1)

def start_server():
    server_ip = input("Enter server IP (leave blank for localhost): ") or 'localhost'
    server_port = int(input("Enter server port (default 12345): ") or 12345)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Server started on {server_ip}:{server_port}, waiting for connections...")
    
    # Start bidding manager thread
    bidding_thread = threading.Thread(target=manage_bidding, daemon=True)
    bidding_thread.start()
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        with clients_lock:
            for client in clients:
                client.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()
