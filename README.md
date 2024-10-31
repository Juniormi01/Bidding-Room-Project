
# Multiplayer Tic-Tac-Toe Game

This project implements a simple multiplayer Tic-Tac-Toe game using Python sockets. Players can host a game or join an existing game to compete against each other on a 3x3 board. The game follows the classic Tic-Tac-Toe rules, where players take turns marking cells on the board, aiming to align three symbols horizontally, vertically, or diagonally.

## Features

- Multiplayer support through TCP sockets
- Simple text-based board display
- Valid move checking and player turn management
- Game result detection (win, lose, or tie)
- Threaded connection handling to separate game flow from network communication

## Requirements

- Python 3.x
- Basic understanding of sockets and threading in Python

## Getting Started

### Installation

1. Clone this repository or copy the code into a local directory.
2. Ensure Python 3 is installed on your machine.

### Usage

To start a Tic-Tac-Toe game, decide which player will host the game and which will connect.

#### 1. Host the Game

The hosting player runs:
python Main.py


This initializes the server on localhost and binds it to port 9999 by default. Once the client connects, the game will begin.

### 2. Connect to a Game
The joining player should run:

python Main2.py
Update the connect_to_game method to match the host's IP and port if they are not localhost:9999.

Game Controls
Hosting Player starts with the symbol X.
Joining Player uses the symbol 0.
To make a move, enter the desired row and column (e.g., 1,2).
The game alternates turns, checking for a winner or tie after each move.

Example Playthrough
Host runs the script and waits for a client connection.
Client connects to the host.
Players take turns making moves by entering row,column coordinates.
Game results are displayed as soon as there's a winner or tie.
Code Structure
The TicTacToe class handles the game logic and networking. Key methods include:

- host_game(): Hosts a new game and waits for a client.
- connect_to_game(): Connects to an existing hosted game.
- handle_connection(): Manages moves and game flow between the players.
- apply_move(): Validates and applies a move to the board.
- check_valid_move(): Checks if a selected cell is available.
- check_if_won(): Checks if a player has won the game.
- print_board(): Displays the current board state.
