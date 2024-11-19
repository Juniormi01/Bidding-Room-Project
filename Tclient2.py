import socket
import threading
import random
import time

class Client:
    def __init__(self, max_prices):
        self.max_prices = max_prices
        self.purchased_items = []
        self.running = True

    def receive_messages(self, client_socket):
        while self.running:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Server: {message}")

                # Update client state based on server messages
                if "Congratulations!" in message:
                    item_name = message.split(" ")[2]  # Extract item name
                    self.purchased_items.append(item_name)
            except:
                print("Disconnected from server.")
                break

    def start_bidding(self, client_socket):
        while self.running:
            try:
                item_name = random.choice(list(self.max_prices.keys()))
                max_price = self.max_prices[item_name]
                bid_amount = random.uniform(1, max_price)

                if bid_amount <= max_price:
                    bid_message = f"{item_name},{bid_amount:.2f}"
                    client_socket.send(bid_message.encode())
                    print(f"Placed bid: {bid_message}")
            except:
                print("Failed to send bid.")
                break

            time.sleep(random.uniform(1, 5))  # Wait before next bid attempt

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_ip = input("Enter server IP: ")
        server_port = int(input("Enter server port: "))
        client_socket.connect((server_ip, server_port))
        print("Connected to the server.")
    except Exception as e:
        print(f"Failed to connect to server: {e}")
        return

    # Define max acceptable prices for items
    max_prices = {
        "Laptop": 700,
        "Smartphone": 500,
        "Headphones": 100
    }
    client = Client(max_prices)

    try:
        # Start threads for receiving messages and bidding
        receive_thread = threading.Thread(target=client.receive_messages, args=(client_socket,))
        receive_thread.start()

        bidding_thread = threading.Thread(target=client.start_bidding, args=(client_socket,))
        bidding_thread.start()

        while True:
            command = input("Type 'exit' to quit: ").strip().lower()
            if command == "exit":
                print("Exiting client...")
                client.running = False
                break
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
