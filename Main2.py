import socket
import threading

class TicTacToe:
    """A simple multiplayer Tic-Tac-Toe game using sockets for communication."""

    def __init__(self):
        """Initialize the game board, player symbols, and game state variables."""
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"  # Track whose turn it is to play
        self.you = "X"   # The symbol for the local player
        self.opponent = "0"  # The symbol for the opponent
        self.winner = None
        self.game_over = False
        self.counter = 0  # Counts the total moves made to detect a tie

    def host_game(self, host, port):
        """Set up the server to host the game and wait for a client to connect.

        Args:
            host (str): The hostname or IP address to bind the server to.
            port (int): The port number to bind the server to.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()  # Wait for a connection from a client

        self.you = "X"
        self.opponent = "0"
        threading.Thread(target=self.handle_connection, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        """Connect to an existing game hosted by another player.

        Args:
            host (str): The hostname or IP address of the server to connect to.
            port (int): The port number of the server to connect to.
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = '0'
        self.opponent = 'X'
        threading.Thread(target=self.handle_connection, args=(client,)).start()

    def handle_connection(self, client):
        """Handle the game connection and manage moves between players.

        Args:
            client (socket): The socket connection to the other player.
        """
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter a move (row, column): ")
                if self.check_valid_move(move.split(',')):
                    client.send(move.encode('utf-8'))
                    self.apply_move(move.split(','), self.you)
                    self.turn = self.opponent
                else:
                    print("Invalid Move!")
            else:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
        client.close()

    def apply_move(self, move, player):
        """Apply a player's move to the board, check for game results, and display the board.

        Args:
            move (list): A list with two elements, representing row and column.
            player (str): The symbol of the player making the move ('X' or '0').
        """
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("You win!")
                exit()
            elif self.winner == self.opponent:
                print("You lose!")
                exit()
        else:
            if self.counter == 9:
                print("It is a tie :/")
                exit()

    def check_valid_move(self, move):
        """Check if a move is valid (i.e., the cell is empty).

        Args:
            move (list): A list with two elements, representing row and column.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):
        """Check if either player has won the game by forming a row, column, or diagonal.

        Returns:
            bool: True if a player has won, False otherwise.
        """
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True
        return False

    def print_board(self):
        """Print the current state of the game board to the console."""
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("-----------")

# Example usage to start a new game as the host
game = TicTacToe()
game.connect_to_game('localhost', 9999)