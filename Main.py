import socket
import threading
import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master):
        """Initialize the game with Tkinter and basic network variables."""
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.configure(bg="#333333")
        
        # Styling attributes
        self.button_color = "#FFDDC1"
        self.button_active_color = "#F7C6C7"
        self.font = ('Helvetica', 24, 'bold')
        
        # Networking attributes
        self.you = "X"
        self.opponent = "0"
        self.turn = self.you
        self.winner = None
        self.game_over = False
        self.socket = None
        self.is_host = False  # Track if the player is the host

        # Board setup
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        """Create a 3x3 board of styled buttons for the Tic-Tac-Toe game."""
        for row in range(3):
            for col in range(3):
                btn = tk.Button(self.master, text=" ", font=self.font,
                                width=5, height=2, bg=self.button_color,
                                activebackground=self.button_active_color,
                                relief="groove",
                                command=lambda r=row, c=col: self.make_move(r, c))
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = btn

    def make_move(self, row, col):
        """Handle a player's move, update the board, and check for a win."""
        if self.game_over or self.board[row][col] != " " or self.turn != self.you:
            return
        
        # Update the board with player's move
        self.board[row][col] = self.you
        self.buttons[row][col].config(text=self.you, disabledforeground="#FF6347")
        self.buttons[row][col].config(state="disabled")  # Disable button after click
        self.turn = self.opponent
        
        # Send move to opponent
        self.socket.send(f"{row},{col}".encode('utf-8'))
        
        if self.check_winner():
            self.display_winner()
        else:
            self.turn = self.opponent  # Switch turn to opponent

    def receive_move(self):
        """Receive the opponent's move from the socket."""
        while not self.game_over:
            data = self.socket.recv(1024).decode('utf-8')
            if data:
                row, col = map(int, data.split(","))
                self.board[row][col] = self.opponent
                self.buttons[row][col].config(text=self.opponent, disabledforeground="#4682B4")
                self.buttons[row][col].config(state="disabled")  # Disable button after opponent's move
                
                if self.check_winner():
                    self.display_winner()
                else:
                    self.turn = self.you  # Switch turn back to the player

    def check_winner(self):
        """Check if there's a winner or if the game is a tie."""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != " ":
                self.winner = self.board[i][0]
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != " ":
                self.winner = self.board[0][i]
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            return True
        if all(self.board[row][col] != " " for row in range(3) for col in range(3)):
            self.winner = "Tie"
            return True
        return False

    def display_winner(self):
        """Display the game result."""
        self.game_over = True
        if self.winner == self.you:
            messagebox.showinfo("Tic Tac Toe", "You win!")
        elif self.winner == self.opponent:
            messagebox.showinfo("Tic Tac Toe", "You lose!")
        else:
            messagebox.showinfo("Tic Tac Toe", "It's a tie!")
    
    def reset_game(self):
        """Reset the game for a new round."""
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = self.you
        self.winner = None
        self.game_over = False
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ", state="normal")

    def host_game(self, host, port):
        """Set up the server to host the game and wait for a client connection."""
        self.is_host = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(1)
        client, _ = self.socket.accept()
        self.socket = client
        threading.Thread(target=self.receive_move).start()

    def connect_to_game(self, host, port):
        """Connect to an existing game hosted by another player."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.you = "0"  # Change symbol for client
        self.opponent = "X"
        self.turn = self.opponent  # Let host start the game
        threading.Thread(target=self.receive_move).start()


# Start GUI and setup network game
def main():
    root = tk.Tk()
    game = TicTacToeGUI(root)

    # Choose to host or join the game
    choice = input("Do you want to (h)ost or (j)oin a game? ")
    if choice.lower() == 'h':
        game.host_game("localhost", 9999)
    elif choice.lower() == 'j':
        game.connect_to_game("localhost", 9999)
    
    root.mainloop()

main()
