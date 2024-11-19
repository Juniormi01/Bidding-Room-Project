
# Multysocket connection bidding room in python

This project implements a distributed auto-bidding system consisting of a server and multiple clients. The server manages the auction process for various items, while clients participate by placing bids. The system ensures fair bidding, manages item availability, and tracks purchases.

## Features

**Server:**

- Manages auction items with starting prices and unit availability.
- Tracks the highest bid for each item and broadcasts updates to clients.
- Implements bidding deadlines to close auctions after a specified time.
- Excludes the current highest bidder from rebidding until outbid.
- Declares winners and records successful purchases.

**Clients:**

- Connect to the server to participate in bidding.
- Randomly decide whether to bid (70% chance).
- Place bids within a predefined maximum acceptable price for each item.
- Stop bidding once the maximum acceptable price is reached.
- Receive updates about ongoing auctions and winning results.


## Requirements

- Programming Language: Python 3.x
- Libraries: No external libraries required (uses standard Python libraries: socket, threading, time, random).

## Getting Started

### Installation

1. Clone this repository or copy the code into a local directory.
2. Ensure Python 3 is installed on your machine.

### Usage

To start the bidding system, decide which machine will host the server and which will run the clients.

#### 1. Start the Server

Run the server script on the hosting machine:

```
python Tserver.py
```
This initializes the server and starts listening for client connections on localhost and port 12345 by default.

### 2. Start the client

Run the client script on each participating machine:
```
python Tclient.py
```
When prompted, enter the server's IP address. Each client will connect to the server and start participating in the bidding process.

## System Controls

#### Server:

Tracks the bidding process, item availability, and announces winners.
Automatically ends auctions for items with no remaining units.

#### Clients:

Simulate bidding with randomized logic and predefined maximum prices.
Receive updates and notifications from the server in real-time.

### Example Playthrough

Start the server by running Tserver.py on a machine.
Start the clients by running Tclient.py on multiple machines.
Clients connect to the server and begin receiving auction updates.
Clients place bids based on their logic until all items are sold out or the system is externally terminated.


### Code Structure:
#### Server (Tserver.py):

#### Core Classes:
- Item: Represents an auction item with attributes for name, starting price, units, and highest bid tracking.
- Key Functions:
- handle_client(): Handles bid reception and broadcasts updates.
- broadcast(): Sends messages to all connected clients.
- manage_bidding(): Tracks deadlines and finalizes winning bids.
- start_server(): Initializes and runs the server.

#### Client (Tclient.py):

#### Core Classes:
- Client: Manages bidding logic and connection to the server.
- Key Functions:
- receive_messages(): Listens for updates from the server.
- start_bidding(): Automates client-side bidding behavior.
- start_client(): Connects the client to the server and starts bidding.
