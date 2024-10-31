
# Multiplayer Tic-Tac-Toe Game with GUI

This project is a multiplayer Tic-Tac-Toe game built with Python. It uses sockets for network communication and Tkinter for a graphical user interface (GUI), making it easy and fun to play in real-time with a friend.

## Features

- **Multiplayer Support**: Play against a friend over a local network using TCP sockets.
- **Graphical Interface**: Uses Tkinter to provide a user-friendly interface with styled buttons and visual cues.
- **Styled Design**: Light and active colors make the game visually engaging and improve gameplay experience.
- **Game Status Notifications**: Alerts players when there’s a win, loss, or tie.


## Requirements

- Python 3.x
- Basic understanding of sockets and threading in Python
- Tkinter (comes pre-installed with most Python distributions)

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

## Game Controls
Hosting Player starts with the symbol X.
Joining Player uses the symbol 0.
Click on a cell to make a move, and the board will automatically update.
The game alternates turns, and alerts appear when there’s a win, loss, or tie.

## Example Playthrough
Host runs the script and waits for a client connection.
Client connects to the host.
Players take turns making moves by selecting the cell they wish to take.
Game results are displayed as soon as there's a winner or tie.

## GUI Styling 
The GUI has been styled for a more enjoyable experience:

- Button Colors: Each cell has a light beige color (#FFDDC1) that darkens slightly when clicked.
- Turn Indicator Colors: Player X moves are highlighted with a red shade (#FF6347), and player 0 moves use a blue shade (#4682B4).
- Font and Layout: The buttons use a bold Helvetica font (size 24) for readability, and are spaced apart for a clean look.

## Code Structure:

The TicTacToeGUI class handles the game logic, networking, and GUI. Key methods include:
- host_game(): Hosts a new game and waits for a client.
- connect_to_game(): Connects to an existing hosted game.
- make_move(): Handles the player's move and sends it to the opponent.
- receive_move(): Receives the opponent's move and updates the GUI.
- check_winner(): Checks if a player has won or if the game is a tie.
- display_winner(): Displays the game result (win, lose, or tie).
- create_board(): Initializes the styled GUI with Tkinter.
