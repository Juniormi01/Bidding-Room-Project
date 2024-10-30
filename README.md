
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
```bash
python tic_tac_toe.py
